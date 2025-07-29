import os
import shutil
from dotenv import load_dotenv
from pathlib import Path

# Importa todas as suas classes de serviço e core
from app.services.database_service import DatabaseService
from app.services.vector_db_service import VectorDBService
from app.services.ai_service import AIService
from app.services.audio_service import AudioService
from app.core.project_manager import ProjectManager
from app.core.workflow_manager import WorkflowManager

# --- CONFIGURAÇÕES DO TESTE ---
TEST_PROJECT_NAME = "WebApp de Vendas (Teste de Integração)"
TEST_PROJECT_PATH = "data/vendas_webapp"

CONTEXT_PATH = f"{TEST_PROJECT_PATH}/context_files"
OUTPUT_PATH = f"{TEST_PROJECT_PATH}/output_files"
DB_PATH = f"{TEST_PROJECT_PATH}/chroma_db"
MAIN_DB_PATH = "data/tars_main.db"

def setup_services_and_managers():
    """Inicializa todos os componentes necessários para o teste."""
    print("--- Inicializando Serviços e Managers ---")
    load_dotenv()
    
    # Garante que o diretório para o DB de teste exista
    os.makedirs(os.path.dirname(MAIN_DB_PATH), exist_ok=True)
    
    db_service = DatabaseService(db_path=MAIN_DB_PATH)
    vector_service = VectorDBService(openai_api_key=os.getenv("OPENAI_API_KEY"))
    ai_service = AIService(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    audio_service = AudioService()
    
    project_manager = ProjectManager(db_service=db_service)
    workflow_manager = WorkflowManager(db_service, vector_service, audio_service, ai_service)
    
    return db_service, vector_service, project_manager, workflow_manager

def run_full_test():
    db_service, vector_service, project_manager, workflow_manager = setup_services_and_managers()
    
    print("\n--- PASSO 1: Criando Projeto e Épico ---")
    project_manager.create_project(
        name=TEST_PROJECT_NAME,
        context="Projeto de um web app de vendas.",
        context_path=str(CONTEXT_PATH),
        output_path=str(OUTPUT_PATH),
        db_path=str(DB_PATH) 
    )
    
    project = project_manager.active_project
    print(f"Projeto '{project.name}' criado e carregado com sucesso.")

    project_manager.create_epic(
        name="001 - Gerenciamento de Usuários",
        context="Funcionalidades de cadastro e login.",
    )

    epic = project_manager.active_epic
    print(f"Épico '{epic.name}' criado e carregado com sucesso.")


    os.makedirs(CONTEXT_PATH, exist_ok=True)
    with open(f"{CONTEXT_PATH}/regras_de_senha.txt", "w", encoding="utf-8") as f:
        f.write("A senha deve ter no mínimo 8 caracteres e conter um número.")
    
    vector_service.index_project_context(project_manager.active_project, db_service)
    print("Contexto indexado com sucesso.")

    print("\n--- PASSO 3: Executando o fluxo de criação de documento ---")
    
    user_request_text = "Eu quero que o usuário possa se cadastrar no sistema usando um e-mail e uma senha. O sistema precisa validar a força da senha."
    print(f"Solicitação do usuário (simulada): '{user_request_text}'")
    
    workflow_manager.new_feature_doc(
        prompt_request=user_request_text,
        epic=project_manager.active_epic,
        project=project_manager.active_project
    )

    print("\n--- PASSO 4: Verificando se as HUs foram salvas no Banco de Dados ---")
    
    hustories_in_db = db_service.get_user_stories_for_epic(project_manager.active_epic.id)
    if hustories_in_db and len(hustories_in_db) > 0:
        print(f"SUCESSO! {len(hustories_in_db)} HU(s) foram salvas no banco de dados para o épico '{epic.name}'.")
        first_hu = hustories_in_db[0]
        print(f"  - Exemplo de HU salva: '{first_hu.name}' (ID: {first_hu.id})")
    else:
        print("FALHA! Nenhuma HU foi encontrada no banco de dados após a execução.")

def cleanup():
    print("\n--- EXECUTANDO LIMPEZA ---")
    if os.path.exists(TEST_PROJECT_PATH):
        shutil.rmtree(TEST_PROJECT_PATH)
        print(f"Pasta de teste '{TEST_PROJECT_PATH}' removida.")

if __name__ == "__main__":
    try:
        #cleanup() 
        run_full_test()
    except Exception as e:
        print(f"\n!!!!!! OCORREU UM ERRO DURANTE O TESTE !!!!!!\n{e}")
        import traceback
        traceback.print_exc()
    # finally:
    #     cleanup()