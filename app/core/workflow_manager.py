import json
import re
from app.database.models import Epic, Project
from app.services.ai_service import AIService
from app.services.audio_service import AudioService
from app.services.database_service import DatabaseService
from app.services.vector_db_service import VectorDBService
import os


class WorkflowManager():
    def __init__(self,
                db_service: DatabaseService,
                vector_service: VectorDBService,
                audio_service: AudioService,
                ai_service: AIService
    ):
        self.db_service = db_service
        self.vector_service = vector_service
        self.audio_service = audio_service
        self.ai_service = ai_service


    def start_audio_recording(self):
        self.audio_service.start_recording()
        ...

    def stop_audio_recording(self):
        audio_filename = self.audio_service.stop_recording()
        return self.audio_transcription(audio_filename)
        ...

    def pause_audio_recording(self):
        self.audio_service.pause_recording()
        ...

    def resume_audio_recording(self):
        self.audio_service.resume_recording()
        ...

    def audio_transcription(self, audio_filename):
        audio_path = os.path.join(self.audio_service.output_folder, audio_filename)
        audio_transcription = self.ai_service.audio_transcription(audio_path)
        os.remove(audio_path)
        return audio_transcription

    def new_feature_doc(self, prompt_request: str, epic: Epic, project: Project):
        retrieved_context = self.get_context_for_request(prompt_request, project)
        project_context = self.db_service.get_project_context(project.id)
        epic_context = self.db_service.get_epic_context(epic.id)
        
        ai_preference = self.db_service.get_setting("AI_PROVIDER_PREFERENCE")
        prompt_model = self.db_service.get_setting("CREATION_PROMPT_TEMPLATE")

        if not prompt_model:
            raise ValueError("Template de prompt de criação não encontrado nas configurações.")

        final_prompt = prompt_model.format(
            user_request=prompt_request, 
            project_context=project_context, 
            epic_name=epic.name,
            epic_context=epic_context,
            retrieved_context=retrieved_context 
        )

        if ai_preference == "OPENAI":
            response_str = self.ai_service.generate_with_openai(final_prompt)
        else:
            response_str = self.ai_service.generate_with_gemini(final_prompt)

        hus_data = self.extract_json_from_response(response_str)

        if not hus_data:
            print("A IA não retornou nenhuma História de Usuário válida.")
            return None

        print(f"IA gerou {len(hus_data)} HUs. Salvando no banco de dados...")

        for hu_data in hus_data:
            new_hu = self.db_service.create_user_story(
                epic_id=epic.id,
                name=hu_data.get('nome_hu', 'Nome não gerado'),
                status='draft' # Começa como rascunho
            )

            self.db_service.add_chat_message(
                user_story_id=new_hu.id,
                role='user',
                content=final_prompt
            )

            self.db_service.add_chat_message(
                user_story_id=new_hu.id,
                role='ai',
                content=response_str
            )

            print(f"HU '{new_hu.name}' e seu histórico de chat foram criados.")
        
        print("Processo de criação de HUs concluído.")


    def get_context_for_request(self, prompt: str, project: Project) -> str:
        retriever = self.vector_service.get_retriever(project)
        ai_preference = self.db_service.get_setting("AI_PROVIDER_PREFERENCE")
        better_context_search_prompt = self.db_service.get_setting("BETTER_CONTEXT_SEARCH_PROMPT")

        if not better_context_search_prompt:
            print("Buscando contexto diretamente com o prompt do usuário.")
            docs = retriever.invoke(prompt)
            return "\n---\n".join([doc.page_content for doc in docs])

        final_prompt_for_search = better_context_search_prompt.format(user_request=prompt)

        print("Refinando termos de busca com a IA...")
        if ai_preference == "OPENAI":
            refined_search_terms = self.ai_service.generate_with_openai(final_prompt_for_search)
        else:
            refined_search_terms = self.ai_service.generate_with_gemini(final_prompt_for_search)
        
        print(f"Termos de busca refinados: '{refined_search_terms}'")

        docs = retriever.invoke(refined_search_terms)
        
        context_text = "\n---\n".join([doc.page_content for doc in docs])
        return context_text


    def extract_json_from_response(self, response_text: str) -> list:
        if not isinstance(response_text, str) or not response_text.strip():
            print("Aviso: A resposta da IA está vazia ou não é uma string.")
            return []

        # Regex para encontrar um bloco de código JSON: ```json ... ```
        match = re.search(r'```(json)?\s*([\s\S]*?)\s*```', response_text)
        
        if match:
            json_str = match.group(2)
        else:
            json_str = response_text

        try:
            data = json.loads(json_str)
            return data if isinstance(data, list) else [data]
        except json.JSONDecodeError as e:
            print(f"Erro CRÍTICO ao decodificar JSON após a extração: {e}")
            print(f"--- String que causou o erro ---\n{json_str}\n-------------------------------")
            raise ValueError("A resposta da IA não pôde ser convertida para JSON.") from e
