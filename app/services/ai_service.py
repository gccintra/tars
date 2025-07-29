import os
from openai import OpenAI
from google import genai
from google.genai import types



class AIService:
    def __init__(self, openai_api_key: str | None = None, google_api_key: str | None = None):
        # --- Cliente OpenAI ---
        if not openai_api_key:
            print("AVISO: Chave da API da OpenAI não fornecida. Funções de transcrição e GPT não funcionarão.")
            self.openai_client = None
        else:
            self.openai_client = OpenAI(api_key=openai_api_key)
            print("Cliente da OpenAI inicializado.")

        # --- Cliente Google (Gemini) ---
        if not google_api_key:
            print("AVISO: Chave da API do Google não fornecida. Funções do Gemini não funcionarão.")
            self.google_client = None
        else:
            self.google_client = genai.Client(api_key=google_api_key)
            print("Cliente do Google (Gemini) inicializado.")
            

    def audio_transcription(self, audio_path: str) -> str:
        if not self.openai_client:
            raise ConnectionError("Cliente da OpenAI não inicializado. Verifique a chave da API.")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado em: {audio_path}")

        print(f"Enviando áudio '{os.path.basename(audio_path)}' para transcrição via Whisper...")
        
        try:
            with open(audio_path, 'rb') as audio_file:
                transcription = self.openai_client.audio.transcriptions.create(
                  model="whisper-1", 
                  file=audio_file
                )
            print("Transcrição concluída com sucesso.")
            return transcription.text
        except Exception as e:
            print(f"Ocorreu um erro durante a transcrição: {e}")
            return f"Erro na transcrição: {e}"

    def generate_with_gemini(self, prompt: str) -> str:
        if not self.google_client:
            raise ConnectionError("Cliente do Google (Gemini) não inicializado. Verifique a chave da API.")
        
        print("Gerando texto com o modelo de linguagem (gemini-2.5-flash)...")
        try:
            response = self.google_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=1.2
                )
            )
            print("Análise gerada com sucesso.")
            return response.text
        except Exception as e:
            print(f"Ocorreu um erro na geração com Gemini: {e}")
            return f"Erro na geração com Gemini: {e}"

    def generate_with_openai(self, prompt: str, model: str = "gpt-4o") -> str:
        if not self.openai_client:
            raise ConnectionError("Cliente da OpenAI não inicializado. Verifique a chave da API.")
        
        print(f"Gerando texto com OpenAI ({model})...")
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=1.2
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Ocorreu um erro na geração com OpenAI: {e}")
            return f"Erro na geração com OpenAI: {e}"