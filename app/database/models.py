from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    context = Column(Text, nullable=True)
    context_folder_path = Column(String(255), nullable=True)
    output_folder_path = Column(String(255), nullable=True)
    db_folder_path = Column(String(255), nullable=True) # ChromaDB

    indexed_files = relationship("IndexedFile")
    epics = relationship("Epic", back_populates="project", cascade="all, delete-orphan")

class IndexedFile(Base):
    __tablename__ = 'indexed_files'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(255), nullable=False)
    last_modified = Column(Float, nullable=False) # Armazenamos como timestamp
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)


class Epic(Base):
    __tablename__ = 'epics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    context = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)

    project = relationship("Project", back_populates="epics")
    user_stories = relationship("UserStory", back_populates="epic", cascade="all, delete-orphan")

class UserStory(Base):
    __tablename__ = 'user_stories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default='draft')
    gdocs_id = Column(String(100), nullable=True)
    local_file_path = Column(String(255), nullable=True)
    
    epic_id = Column(Integer, ForeignKey('epics.id'), nullable=False)
    epic = relationship("Epic", back_populates="user_stories")
    chat_history = relationship("ChatHistory", back_populates="user_story", uselist=False, cascade="all, delete-orphan")

class ChatHistory(Base):
    __tablename__ = 'chat_histories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    log = Column(Text, nullable=False)
    user_story_id = Column(Integer, ForeignKey('user_stories.id'), nullable=False)
    user_story = relationship("UserStory", back_populates="chat_history")

class Setting(Base):
    __tablename__ = 'settings'
    key = Column(String(50), primary_key=True)
    value = Column(Text, nullable=True)