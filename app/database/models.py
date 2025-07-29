from __future__ import annotations
from typing import List

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Nova forma de declarar a Base no SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = 'projects'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    context: Mapped[str | None] = mapped_column(Text)
    context_folder_path: Mapped[str | None] = mapped_column(String(255))
    output_folder_path: Mapped[str | None] = mapped_column(String(255))
    db_folder_path: Mapped[str | None] = mapped_column(String(255))

    indexed_files: Mapped[List["IndexedFile"]] = relationship()
    epics: Mapped[List["Epic"]] = relationship(back_populates="project", cascade="all, delete-orphan")

class IndexedFile(Base):
    __tablename__ = 'indexed_files'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    last_modified: Mapped[float] = mapped_column(nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)

class Epic(Base):
    __tablename__ = 'epics'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    context: Mapped[str | None] = mapped_column(Text)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), nullable=False)

    project: Mapped["Project"] = relationship(back_populates="epics")
    user_stories: Mapped[List["UserStory"]] = relationship(back_populates="epic", cascade="all, delete-orphan")


# Salvar os dados (json) da hu atual, e o usuario vai escolher quando atualizar essas informações e escolher com quais informações ele vai querer atualizar, é necessário salvar isso em tabela para a hora da criação do google docs formatado.
# Adicionar a informação em chat history, de que o agente só pode responder naquele formato json, mesmo que o prompt do usuario nao faça sentido, se o prompt do usuaqrio nao for uma requisição de mudanças, ele não deve responder nada, ou responder uma resposta padrão para eu tratar aqui
class UserStory(Base):
    __tablename__ = 'user_stories'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='draft')
    gdocs_id: Mapped[str | None] = mapped_column(String(100))
    local_file_path: Mapped[str | None] = mapped_column(String(255))
    
    epic_id: Mapped[int] = mapped_column(ForeignKey('epics.id'), nullable=False)
    epic: Mapped["Epic"] = relationship(back_populates="user_stories")
    chat_history: Mapped["ChatHistory"] = relationship(back_populates="user_story", uselist=False, cascade="all, delete-orphan")

class ChatHistory(Base):
    __tablename__ = 'chat_histories'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    log: Mapped[str] = mapped_column(Text, nullable=False)
    
    user_story_id: Mapped[int] = mapped_column(ForeignKey('user_stories.id'), nullable=False)
    user_story: Mapped["UserStory"] = relationship(back_populates="chat_history")

class Setting(Base):
    __tablename__ = 'settings'
    
    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text)