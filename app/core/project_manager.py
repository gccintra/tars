
import os
from app.services.database_service import DatabaseService
from app.database.models import Project, Epic

class ProjectManager:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        self.active_project: Project | None = None
        self.active_epic: Epic | None = None

    def create_project(self, name: str, context: str) -> Project:

        db_folder_name = name.replace(" ", "_")


        db_path = f"data/{db_folder_name}/chroma_db"
        output_path = f"data/{db_folder_name}/output"
        context_path = f"data/{db_folder_name}/context"

        new_project = self.db_service.create_project(
            name=name,
            context=context,
            context_path=context_path,
            output_path=output_path,
            db_path=db_path
        )

        if new_project:
            print(f"Projeto '{new_project.name}' criado com sucesso.")
        
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            os.makedirs(os.path.dirname(context_path), exist_ok=True)

        self.load_project(new_project.id)
        return new_project
    
    def create_epic(self, name: str, context: str):
        if not self.active_project:
            raise ValueError("Nenhum projeto ativo. Carregue um projeto antes de criar um épico.")
        new_epic = self.db_service.create_epic(
            name=name,
            context=context,
            project_id=self.active_project.id
        )
        self.load_epic(new_epic.id)
        return new_epic
        
    def load_project(self, project_id: int):
        print("tentnado loadar o projeto")
        self.active_project = self.db_service.get_project_by_id(project_id)
        self.active_epic = None
        if self.active_project:
            print(f"Projeto '{self.active_project.name}' carregado.")
        else:
            raise ValueError(f"Projeto com ID {project_id} não encontrado.")
    
    def load_epic(self, epic_id: int):
        epic = self.db_service.get_epic_by_id(epic_id)
        if epic and self.active_project and epic.project_id == self.active_project.id:
            self.active_epic = epic
            print(f"Épico '{self.active_epic.name}' carregado.")
        else:
            self.active_epic = None
            raise ValueError(f"Épico com ID {epic_id} não encontrado ou não pertence ao projeto ativo.")
        
    
    def get_all_projects(self) -> list[Project]:
        return self.db_service.get_all_projects()
    
    def get_setting(self, key: str):
        return self.db_service.get_setting(key)

    def set_setting(self, key: str, value: str):
        # TODO: colocar um try catch aqui pra pegar os erros
        self.db_service.set_setting(key=key, value=value)