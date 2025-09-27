# app/services/vector_db_service.py

import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from app.database.models import Project
from app.services.database_service import DatabaseService

class VectorDBService:
    def __init__(self, openai_api_key: str | None = None):
        print("[DEBUG] VectorDBService inicializado.")
        self.openai_api_key = openai_api_key
        self.embedding_function = None

    def _get_embedding_function(self) -> OpenAIEmbeddings:
        if self.embedding_function:
            return self.embedding_function

        if not self.openai_api_key:
            raise ValueError("A chave da API da OpenAI não foi configurada. Por favor, adicione-a nas Configurações.")

        print("[DEBUG] Criando instância da função de embedding da OpenAI...")
        self.embedding_function = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        return self.embedding_function

    def _get_project_chromadb_path(self, project: Project) -> str:
        if not os.path.isdir(project.db_folder_path):
             os.makedirs(project.db_folder_path, exist_ok=True)
        return os.path.join(project.db_folder_path, "chroma_db")
    
    def _load_vector_store(self, project: Project) -> Chroma | None:
        embedding_func = self._get_embedding_function()

        db_path = self._get_project_chromadb_path(project)
        if not os.path.exists(db_path):
            print(f"AVISO: Banco de dados vetorial não encontrado para '{project.name}'.")
            return None
        return Chroma(
            persist_directory=db_path,
            embedding_function=embedding_func
        )

    def index_project_context(self, project: Project, db_service: DatabaseService):
        embedding_func = self._get_embedding_function()

        print(f"Iniciando sincronização para o projeto: '{project.name}'")
        context_path = project.context_folder_path
        
        vector_store = self._load_vector_store(project)

        all_current_files = {}
        if os.path.isdir(context_path):
            for root, _, files in os.walk(context_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_current_files[file_path] = os.path.getmtime(file_path)


        indexed_files = db_service.get_indexed_files_for_project(project.id)
        indexed_files_map = {f.file_path: f for f in indexed_files}
        

        files_to_remove = [f for f in indexed_files if f.file_path not in all_current_files]
        if files_to_remove:
            print(f"Encontrados {len(files_to_remove)} arquivo(s) para remover da indexação.")
            if vector_store:
                ids_to_delete = []
                for file_to_remove in files_to_remove:
                    results = vector_store.get(where={"source": file_to_remove.file_path})
                    ids_to_delete.extend(results['ids'])
                
                if ids_to_delete:
                    print(f"Removendo {len(ids_to_delete)} chunks do ChromaDB...")
                    vector_store.delete(ids=ids_to_delete)
            
            db_service.delete_indexed_files([f.id for f in files_to_remove])
        
        files_to_index_paths = []
        for path, mod_time in all_current_files.items():
            if path not in indexed_files_map or indexed_files_map[path].last_modified < mod_time:
                files_to_index_paths.append(path)

        if not files_to_index_paths:
            print("Nenhum arquivo novo ou modificado para indexar.")
            print("Sincronização concluída.")
            return

        print(f"Encontrados {len(files_to_index_paths)} arquivo(s) novo(s) ou modificado(s) para processar.")
        
        if vector_store:
            ids_to_delete_for_update = []
            for path in files_to_index_paths:
                if path in indexed_files_map: 
                    results = vector_store.get(where={"source": path})
                    ids_to_delete_for_update.extend(results['ids'])
            
            if ids_to_delete_for_update:
                print(f"Removendo {len(ids_to_delete_for_update)} chunks desatualizados antes de atualizar...")
                vector_store.delete(ids=ids_to_delete_for_update)
        
        docs_to_index = []
        for path in files_to_index_paths:
            try:
                if path.endswith(".txt"): loader = TextLoader(path, encoding='utf-8')
                elif path.endswith(".pdf"): loader = PyPDFLoader(path)
                elif path.endswith(".docx"): loader = Docx2txtLoader(path)
                else: continue
                docs_to_index.extend(loader.load())
            except Exception as e:
                print(f"Erro ao carregar o arquivo {path}: {e}")

        if not docs_to_index:
            print("Nenhum documento compatível foi carregado.")
            return
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs_to_index)
        
        print(f"Adicionando {len(chunks)} novos chunks ao ChromaDB...")
        if vector_store is None:
             db_path = self._get_project_chromadb_path(project)
             vector_store = Chroma.from_documents(chunks, embedding_func, persist_directory=db_path)
        else:
             vector_store.add_documents(chunks)
        
        for path in files_to_index_paths:
            mod_time = all_current_files[path]
            db_service.update_or_create_indexed_file(project.id, path, mod_time)

        print("Sincronização incremental concluída com sucesso!")
 
    def get_retriever(self, project: Project, search_k: int = 5):
        vector_store = self._load_vector_store(project)
        if vector_store is None:
            return None
            
        return vector_store.as_retriever(search_kwargs={"k": search_k})