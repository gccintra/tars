import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from app.database.models import Project
from app.services.database_service import DatabaseService

class VectorDBService:
    def __init__(self, openai_api_key: str):
        if not openai_api_key:
            raise ValueError("A chave da API da OpenAI é necessária para o serviço de embeddings.")
        self.embedding_function = OpenAIEmbeddings(openai_api_key=openai_api_key)

    def _get_project_chromadb_path(self, project: Project) -> str:
        if not os.path.isdir(project.db_folder_path):
            os.makedirs(project.db_folder_path, exist_ok=True)
             
        return os.path.join(project.db_folder_path, "chroma_db")
    

    def index_project_context(self, project: Project, db_service: DatabaseService):
        print(f"Iniciando indexação inteligente para o projeto: '{project.name}'")
        context_path = project.context_folder_path
        
        all_current_files = {}
        for root, _, files in os.walk(context_path):
            for file in files:
                file_path = os.path.join(root, file)
                all_current_files[file_path] = os.path.getmtime(file_path)

        indexed_files_map = {f.file_path: f.last_modified for f in db_service.get_indexed_files_for_project(project.id)}

        files_to_index_paths = []
        for path, mod_time in all_current_files.items():
            if path not in indexed_files_map or indexed_files_map[path] < mod_time:
                files_to_index_paths.append(path)

        if not files_to_index_paths:
            print("Nenhum arquivo novo ou modificado para indexar. Base de conhecimento está atualizada.")
            return

        print(f"Encontrados {len(files_to_index_paths)} arquivo(s) novo(s) ou modificado(s) para indexar.")

        docs_to_index = []
        for path in files_to_index_paths:
            try:
                if path.endswith(".txt"):
                    loader = TextLoader(path, encoding='utf-8')
                    docs_to_index.extend(loader.load())
                elif path.endswith(".pdf"):
                    loader = PyPDFLoader(path)
                    docs_to_index.extend(loader.load())
                elif path.endswith(".docx"):
                    loader = Docx2txtLoader(path)
                    docs_to_index.extend(loader.load())
            except Exception as e:
                print(f"Erro ao carregar o arquivo {path}: {e}")

        if not docs_to_index:
            print("Nenhum documento compatível encontrado.")
            return
        
        print(f"{len(docs_to_index)} documento(s) carregado(s). Dividindo em chunks...")

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs_to_index)
        
        print(f"Documentos divididos em {len(chunks)} chunks. Adicionando ao banco de dados vetorial...")

        db_path = self._get_project_chromadb_path(project)
        vector_store = Chroma(
            persist_directory=db_path,
            embedding_function=self.embedding_function
        )
        vector_store.add_documents(chunks) 

        for path in files_to_index_paths:
            mod_time = all_current_files[path]
            db_service.update_or_create_indexed_file(project.id, path, mod_time)

        print(f"Indexação incremental concluída com sucesso!")


    def get_retriever(self, project: Project, search_k: int = 5):
        """
        Carrega o banco de dados vetorial de um projeto e retorna um objeto "retriever".
        O retriever é um componente do LangChain pronto para ser usado em cadeias (chains) de IA.

        :param project: O objeto do projeto ativo.
        :param search_k: O número de documentos relevantes a serem retornados na busca.
        """
        db_path = self._get_project_chromadb_path(project)

        if not os.path.exists(db_path):
            print(f"AVISO: Nenhum banco de dados vetorial encontrado para o projeto '{project.name}'. Execute a indexação primeiro.")
            return None

        vector_store = Chroma(
            persist_directory=db_path,
            embedding_function=self.embedding_function
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": search_k})
        print(f"Retriever para o projeto '{project.name}' carregado com sucesso.")
        return retriever
