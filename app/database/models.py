from __future__ import annotations
from datetime import datetime
from time import timezone
from typing import List

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text, ForeignKey, Float
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

    output_folder_path: Mapped[str | None] = mapped_column(String(255))

    project: Mapped["Project"] = relationship(back_populates="epics")
    user_stories: Mapped[List["UserStory"]] = relationship(back_populates="epic", cascade="all, delete-orphan")


class UserStory(Base):
    __tablename__ = 'user_stories'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='draft')
    gdocs_id: Mapped[str | None] = mapped_column(String(100))

    local_file_path: Mapped[str | None] = mapped_column(String(255))

    hu_data_current: Mapped[dict | None] = mapped_column(JSON)
    
    epic_id: Mapped[int] = mapped_column(ForeignKey('epics.id'), nullable=False)
    epic: Mapped["Epic"] = relationship(back_populates="user_stories")

    chat_messages: Mapped[List["ChatMessage"]] = relationship(         # type: ignore
        back_populates="user_story", 
        cascade="all, delete-orphan",
        order_by="ChatMessage.timestamp"  
    )

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    role: Mapped[str] = mapped_column(String(20), nullable=False)  # 'user' or 'ai'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    user_story_id: Mapped[int] = mapped_column(ForeignKey('user_stories.id'), nullable=False)
    user_story: Mapped["UserStory"] = relationship(back_populates="chat_history")

class Setting(Base):
    __tablename__ = 'settings'
    
    key: Mapped[str] = mapped_column(String(50), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text)