import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.database.models import Base, Project, Epic, UserStory, ChatHistory, Setting, IndexedFile

class DatabaseService:
    def __init__(self, db_path: str):
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()


    def get_indexed_files_for_project(self, project_id: int) -> list[IndexedFile]:
        session = self.get_session()
        try:
            files = session.query(IndexedFile).filter_by(project_id=project_id).all()
            return files
        finally:
            session.close()

    def update_or_create_indexed_file(self, project_id: int, file_path: str, mod_time: float):

        session = self.get_session()
        try:
            existing_file = session.query(IndexedFile).filter_by(
                project_id=project_id, 
                file_path=file_path
            ).first()

            if existing_file:
                existing_file.last_modified = mod_time
                print(f"Registro de arquivo atualizado: {os.path.basename(file_path)}")
            else:
                new_file = IndexedFile(
                    project_id=project_id,
                    file_path=file_path,
                    last_modified=mod_time
                )
                session.add(new_file)
                print(f"Novo arquivo registrado: {os.path.basename(file_path)}")
            
            session.commit()
        finally:
            session.close()


    def get_project_by_name(self, name: str) -> Project | None:
        session = self.get_session()
        try:
            project = session.query(Project).filter_by(name=name).first()
            return project
        finally:
            session.close()

    def create_project(self, name: str, context_path: str, output_path: str, db_path: str) -> Project:
        existing = self.get_project_by_name(name)
        if existing:
            print(f"Projeto '{name}' já existe.")
            return existing
            
        session = self.get_session()
        try:
            for path in [context_path, output_path, db_path]:
                os.makedirs(path, exist_ok=True)

            new_project = Project(
                name=name,
                context_folder_path=context_path,
                output_folder_path=output_path,
                db_folder_path=db_path
            )
            session.add(new_project)
            session.commit()
            print(f"Projeto '{name}' criado com sucesso.")
            # A sessão precisa ser atualizada para pegar o ID gerado
            session.refresh(new_project)
            return new_project
        finally:
            session.close()