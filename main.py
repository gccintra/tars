import flet as ft

from app.services.ai_service import AIService
from app.services.audio_service import AudioService
from app.services.database_service import DatabaseService
from app.core.project_manager import ProjectManager
from app.core.workflow_manager import WorkflowManager
from app.services.vector_db_service import VectorDBService
from app.ui.main_app import MainApp


DB_PATH = "data/tars_main.db"


if __name__ == "__main__":
    db_service = DatabaseService(DB_PATH)

    audio_service = AudioService()
    ai_service = AIService()
    vector_service = VectorDBService()

    project_manager = ProjectManager(db_service)
    workflow_manager = WorkflowManager(db_service=db_service, vector_service=vector_service, audio_service=audio_service, ai_service=ai_service)
        
  
    app_instance = MainApp(project_manager=project_manager, workflow_manager=workflow_manager)

    ft.app(target=app_instance.main)