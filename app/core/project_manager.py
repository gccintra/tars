

from app.services.audio_service import AudioService
from app.services.database_service import DatabaseService
from app.services.vector_db_service import VectorDBService

class ProjectManager():

    def __init__(self,
                db_service: DatabaseService,
                vector_service: VectorDBService,
                audio_service: AudioService,
                transcription_service: TranscriptionService,
                ai_service: AIService
    ):
        self.db_service = db_service
        self.vector_service = vector_service
        self.audio_service = audio_service
        self.transcription_service = transcription_service
        self.ai_service = ai_service