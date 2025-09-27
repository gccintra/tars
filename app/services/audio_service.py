import pyaudio
import wave
import threading
import time
import os

class AudioService:
    # A gravação roda em uma thread separada para não bloquear a UI
   
    def __init__(self, output_folder: str = "temp_audio"):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44000

        self.state = 'stopped'
        self.frames = []
        self.pyaudio_instance = None
        self.stream = None
        self.recording_thread = None
        self.output_folder = output_folder
        
        os.makedirs(self.output_folder, exist_ok=True)

    def _recording_loop(self):
        while self.state != 'stopped':
            if self.state == 'recording' and self.stream:
                try:
                    data = self.stream.read(self.chunk)
                    self.frames.append(data)
                except IOError:
                    # O stream foi fechado pelo método pause, o que é esperado.
                    # A thread continuará em loop, dormindo, até ser retomada ou parada.
                    pass 
            else:
                time.sleep(0.1)

    def start_recording(self):
        if self.state != 'stopped':
            print("Por favor, pare a gravação atual antes de iniciar uma nova.")
            return

        self.frames = []
        self.pyaudio_instance = pyaudio.PyAudio()
        self._open_stream()
        
        self.state = 'recording'
        
        self.recording_thread = threading.Thread(target=self._recording_loop)
        self.recording_thread.start()
        print("Gravação iniciada.")

    def _open_stream(self):
        self.stream = self.pyaudio_instance.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

    def _close_stream(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def pause_recording(self):
        if self.state != 'recording':
            print("Não há gravação em andamento para pausar.")
            return
            
        self.state = 'paused'
        self._close_stream()
        print("Gravação pausada.")

    def resume_recording(self):
        if self.state != 'paused':
            print("A gravação não está pausada.")
            return
            
        self._open_stream() 
        self.state = 'recording'
        print("Gravação retomada.")

    def stop_recording(self) -> str | None:
        if self.state == 'stopped':
            print("Não há gravação em andamento para parar.")
            return None

        original_state = self.state
        self.state = 'stopped'
        print("Sinal de parada enviado. Aguardando a thread de gravação finalizar...")
        
        self.recording_thread.join()
        
        print("Thread finalizada. Limpando recursos do PyAudio...")
        
        if original_state == 'recording':
            self._close_stream()
        
        if self.pyaudio_instance:
            self.pyaudio_instance.terminate()
        
        output_filename = os.path.join(self.output_folder, f"gravacao_{int(time.time())}.wav")
        
        if not self.frames:
            print("Nenhum áudio foi gravado.")
            return None

        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.pyaudio_instance.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

        print(f"Gravação finalizada e salva em: {output_filename}")
        return output_filename

if __name__ == "__main__":
    service = AudioService()
    service.start_recording()
    time.sleep(3) # Grava por 3 segundos
    service.pause_recording()
    print("Programa fazendo outras coisas enquanto pausado...")
    time.sleep(2) # Pausado por 2 segundos
    service.resume_recording()
    time.sleep(3) # Grava por mais 3 segundos
    service.stop_recording()