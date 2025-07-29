import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

# Importe seus modelos como antes
from app.database.models import Base, Project, Epic, UserStory, ChatHistory, Setting, IndexedFile

class DatabaseService:
    def __init__(self, db_path: str):
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        # O SessionLocal é a "fábrica" de sessões
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    # --- Métodos para Projetos ---

    def create_project(self, name: str, context: str, context_path: str, output_path: str, db_path: str) -> Project:
        session = self._SessionLocal()
        try:
            stmt = select(Project).where(Project.name == name)
            existing = session.execute(stmt).scalar_one_or_none()
            if existing:
                print(f"Projeto '{name}' já existe.")
                return existing

            new_project = Project(
                name=name,
                context=context,
                context_folder_path=context_path,
                output_folder_path=output_path,
                db_folder_path=db_path
            )
            session.add(new_project)
            session.commit()
            session.refresh(new_project)
            print(f"Projeto '{name}' criado com sucesso.")
            return new_project
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_project_by_id(self, project_id: int) -> Project | None:
        session = self._SessionLocal()
        try:
            stmt = select(Project).where(Project.id == project_id)
            project = session.execute(stmt).scalar_one_or_none()
            return project
        finally:
            session.close()

    def get_project_context(self, project_id: int) -> str:
        project = self.get_project_by_id(project_id)
        return project.context if project else ""
    
    # --- Métodos para Épicos ---

    def create_epic(self, name: str, context: str, project_id: int) -> Epic:
        session = self._SessionLocal()
        try:
            new_epic = Epic(name=name, context=context, project_id=project_id)
            session.add(new_epic)
            session.commit()
            session.refresh(new_epic)
            print(f"Épico '{name}' criado para o projeto ID {project_id}.")
            return new_epic
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_epic_by_id(self, epic_id: int) -> Epic | None:
        session = self._SessionLocal()
        try:
            stmt = select(Epic).where(Epic.id == epic_id)
            epic = session.execute(stmt).scalar_one_or_none()
            return epic
        finally:
            session.close()
            
    def get_epic_context(self, epic_id: int) -> str:
        epic = self.get_epic_by_id(epic_id)
        return epic.context if epic else ""
    
    def get_user_stories_for_epic(self, epic_id: int) -> list[UserStory]:
        session = self._SessionLocal()
        try:
            stmt = select(UserStory).where(UserStory.epic_id == epic_id)
            result = session.execute(stmt)
            return list(result.scalars().all())
        finally:
            session.close()

    # --- Métodos para Histórias de Usuário (HUs) ---

    def create_user_story(self, epic_id: int, name: str, status: str = 'draft') -> UserStory:
        session = self._SessionLocal()
        try:
            new_hu = UserStory(epic_id=epic_id, name=name, status=status)
            session.add(new_hu)
            session.commit()
            session.refresh(new_hu)
            return new_hu
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # --- Métodos para Histórico de Chat ---

    def create_chat_history(self, user_story_id: int, log: str) -> ChatHistory:
        session = self._SessionLocal()
        try:
            new_chat = ChatHistory(user_story_id=user_story_id, log=log)
            session.add(new_chat)
            session.commit()
            session.refresh(new_chat)
            return new_chat
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # --- Métodos para Configurações (Settings) ---

    def get_setting(self, key: str) -> str | None:
        session = self._SessionLocal()
        try:
            stmt = select(Setting).where(Setting.key == key)
            setting = session.execute(stmt).scalar_one_or_none()
            return setting.value if setting else None
        finally:
            session.close()

    def save_setting(self, key: str, value: str):
        session = self._SessionLocal()
        try:
            stmt = select(Setting).where(Setting.key == key)
            setting = session.execute(stmt).scalar_one_or_none()

            if setting:
                setting.value = value
            else:
                setting = Setting(key=key, value=value)
                session.add(setting)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # --- Métodos para Arquivos Indexados ---

    def get_indexed_files_for_project(self, project_id: int) -> list[IndexedFile]:
        session = self._SessionLocal()
        try:
            stmt = select(IndexedFile).where(IndexedFile.project_id == project_id)
            result = session.execute(stmt)
            return list(result.scalars().all())
        finally:
            session.close()

    def update_or_create_indexed_file(self, project_id: int, file_path: str, mod_time: float):
        session = self._SessionLocal()
        try:
            stmt = select(IndexedFile).where(
                IndexedFile.project_id == project_id,
                IndexedFile.file_path == file_path
            )
            existing_file = session.execute(stmt).scalar_one_or_none()
            
            if existing_file:
                existing_file.last_modified = mod_time
            else:
                new_file = IndexedFile(project_id=project_id, file_path=file_path, last_modified=mod_time)
                session.add(new_file)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()