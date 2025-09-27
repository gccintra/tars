import os
from openai import OpenAI
from google import genai
from google.genai import types



class AIService:
    def __init__(self, openai_api_key: str | None = None, google_api_key: str | None = None):
        print("[DEBUG] AIService inicializado (chaves armazenadas).")
        self.openai_api_key = openai_api_key
        self.google_api_key = google_api_key

        self._openai_client = None
        self._google_client = None


    def _get_openai_client(self) -> OpenAI:
        if self._openai_client:
            return self._openai_client

        if not self.openai_api_key:
            raise ValueError("Chave da API da OpenAI não configurada. Por favor, adicione-a nas Configurações.")
        
        print("[DEBUG] Criando instância do cliente da OpenAI...")
        self._openai_client = OpenAI(api_key=self.openai_api_key)
        return self._openai_client

    def _get_google_client(self):
        if self._google_client:
            return self._google_client

        if not self.google_api_key:
            raise ValueError("Chave da API do Google não configurada. Por favor, adicione-a nas Configurações.")
            
        print("[DEBUG] Criando instância do cliente do Google Gemini...")
        genai.configure(api_key=self.google_api_key)
        self._google_client = genai.GenerativeModel("gemini-1.5-pro-latest")
        return self._google_client
            

    def audio_transcription(self, audio_path: str) -> str:
        client = self._get_openai_client()

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Arquivo de áudio não encontrado em: {audio_path}")

        print(f"Enviando áudio '{os.path.basename(audio_path)}' para transcrição via Whisper...")
        
        try:
            with open(audio_path, 'rb') as audio_file:
                transcription = client.audio.transcriptions.create(
                  model="whisper-1", 
                  file=audio_file
                )
            print("Transcrição concluída com sucesso.")
            return transcription.text
        except Exception as e:
            print(f"Ocorreu um erro durante a transcrição: {e}")
            return f"Erro na transcrição: {e}"

    def generate_with_gemini(self, prompt: str) -> str:
        client = self._get_google_client()
        
        print("Gerando texto com o modelo de linguagem (gemini-2.5-flash)...")
        try:
            response = client.models.generate_content(
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
        client = self._get_openai_client()
        
        print(f"Gerando texto com OpenAI ({model})...")
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=1.2
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Ocorreu um erro na geração com OpenAI: {e}")
            return f"Erro na geração com OpenAI: {e}"