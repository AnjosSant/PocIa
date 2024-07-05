import cv2
import tkinter as tk
from PIL import Image, ImageTk
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Substitua com suas informações do Custom Vision
PREDICTION_KEY = os.getenv('PREDICTION_KEY')
ENDPOINT = os.getenv('ENDPOINT')
PROJECT_ID = os.getenv('PROJECT_ID')
PUBLISHED_NAME = os.getenv('PUBLISHED_NAME')

# Informações do segundo projeto/iteração
SECOND_PROJECT_ID = os.getenv('SECOND_PROJECT_ID')
SECOND_PUBLISHED_NAME = os.getenv('SECOND_PUBLISHED_NAME')

# Configurar a chave da API do Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class HandDetectionApp:
    def __init__(self, root):
        """
        Inicializa a aplicação de detecção de mãos com uma janela principal.

        Args:
            root (tk.Tk): Instância principal do tkinter para construir a GUI.
        """
        self.root = root
        self.root.title("Detecção de Mãos")
        self.configure_generative_model()

        self.video_source = 0  # ID da câmera (0 para câmera padrão)
        self.vid = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW)

        if not self.vid.isOpened():
            print("Erro ao abrir a câmera")
            return

        # Configuração da interface gráfica
        self.canvas = tk.Canvas(root, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.message_label = tk.Label(root, text="")
        self.message_label.pack()

        self.btn_detect_hands = tk.Button(root, text="Detectar Mãos", command=self.detect_hands)
        self.btn_detect_hands.pack(anchor=tk.CENTER, expand=True)
        
        self.delay = 15
        self.update()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update(self):
        """
        Atualiza o frame da câmera exibido na interface gráfica.
        """
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.photo = self.process_frame(frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.photo))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        else:
            print("Erro ao capturar o frame")

        self.root.after(self.delay, self.update)

    def process_frame(self, frame):
        """
        Processa o frame capturado antes de exibi-lo na interface.

        Args:
            frame (numpy.ndarray): Frame capturado pela câmera.

        Returns:
            numpy.ndarray: Frame processado.
        """
        return frame

    def detect_hands(self):
        """
        Inicia a detecção de mãos ao pressionar o botão "Detectar Mãos".
        """
        success, frame = self.detect(self.vid, PROJECT_ID, PUBLISHED_NAME, "Mão")
        if success:
            self.open_chat_window()

    def detect(self, vid, project_id, published_name, type_name, specific_tag=None):
        """
        Realiza a detecção de objetos usando o serviço Custom Vision.

        Args:
            vid (cv2.VideoCapture): Instância da câmera para captura de vídeo.
            project_id (str): ID do projeto no Custom Vision.
            published_name (str): Nome da iteração publicada no Custom Vision.
            type_name (str): Nome do tipo de objeto a ser detectado.
            specific_tag (str, optional): Tag específica para detecção. Defaults to None.

        Returns:
            tuple: Tupla indicando se a detecção foi bem-sucedida e o frame processado.
        """
        ret, frame = vid.read()
        if ret:
            # Converter frame para RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            _, img_encoded = cv2.imencode('.jpg', frame_rgb)
            img_bytes = img_encoded.tobytes()

            # Enviar imagem para o Custom Vision
            headers = {
                'Prediction-Key': PREDICTION_KEY,
                'Content-Type': 'application/octet-stream'
            }
            url = f"{ENDPOINT}/customvision/v3.0/Prediction/{project_id}/detect/iterations/{published_name}/image"
            response = requests.post(url, headers=headers, data=img_bytes)
            
            if response.status_code == 200:
                predictions = response.json().get('predictions', [])
                max_probability = 0.0
                max_tag = None

                for item in predictions:
                    if specific_tag and item['tagName'] == specific_tag:
                        max_probability = item['probability']
                        max_tag = item['tagName']
                        break
                    elif not specific_tag and item['probability'] > max_probability:
                        max_probability = item['probability']
                        max_tag = item['tagName']

                # Verificação de detecção e probabilidade mínima
                if max_probability >= 0.9:
                    print(f"Tag com maior probabilidade: {max_tag}, probabilidade: {max_probability:.2f}")
                    self.message_label.config(text=f'{type_name} detectado')  # Atualize o texto no rótulo
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                    return True, frame
                else:
                    print(f"Probabilidade insuficiente: {max_probability:.2f}")
                    self.message_label.config(text=f'Não é um {type_name}')  # Atualize o texto no rótulo
                    self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                    return False, frame

    def open_chat_window(self):
        """
        Abre uma nova janela para o chat após a detecção de mãos.
        """
        self.root.destroy()  # Fechar a janela inicial de detecção de mãos

        chat_window = tk.Tk()
        chat_window.title("Chat")

        self.chat_log = tk.Text(chat_window, state='disabled', width=50, height=20)
        self.chat_log.grid(row=0, column=0, padx=10, pady=10)

        self.chat_canvas = tk.Canvas(chat_window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH),
                                     height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.chat_canvas.grid(row=0, column=1, padx=10, pady=10)

        self.btn_send_signal = tk.Button(chat_window, text="Enviar Sinal de Libras", command=self.detect_libras)
        self.btn_send_signal.grid(row=1, column=1, pady=10)

        self.chat_vid = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW)

        self.chat_window = chat_window
        self.update_chat_camera()

    def update_chat_camera(self):
        """
        Atualiza o frame da câmera exibido na janela de chat.
        """
        ret, frame = self.chat_vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.chat_canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        else:
            print("Erro ao capturar o frame")

        self.chat_window.after(self.delay, self.update_chat_camera)

    def detect_libras(self):
        """
        Detecta sinais de Libras usando o serviço Custom Vision.
        """
        ret, frame = self.chat_vid.read()
        if ret:
            self.check_libras_in_chat(frame)

    def check_libras_in_chat(self, frame):
        """
        Verifica a detecção de sinais de Libras e atualiza o log de chat.

        Args:
            frame (numpy.ndarray): Frame capturado pela câmera.
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        _, img_encoded = cv2.imencode('.jpg', frame_rgb)
        img_bytes = img_encoded.tobytes()

        headers = {
            'Prediction-Key': PREDICTION_KEY,
            'Content-Type': 'application/octet-stream'
        }
        url = f"{ENDPOINT}/customvision/v3.0/Prediction/{SECOND_PROJECT_ID}/detect/iterations/{SECOND_PUBLISHED_NAME}/image"
        response = requests.post(url, headers=headers, data=img_bytes)

        if response.status_code == 200:
            predictions = response.json().get('predictions', [])
            max_probability = 0.0
            max_tag = None

            for item in predictions:
                if item['probability'] > max_probability and item['tagName'] != 'Not':
                    max_probability = item['probability']
                    max_tag = item['tagName']
                    print(f"Tag com maior probabilidade: {max_tag}")

            if max_probability >= 0.1:
                self.generate_response(max_tag)
                print(f"Tag selecionada: {max_tag}")

    def configure_generative_model(self):
        """
        Configura o modelo generativo para a geração de respostas.
        """
        self.generative_model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, max_tag):
        """
        Gera uma resposta com base na tag máxima detectada.

        Args:
            max_tag (str): Tag com maior probabilidade detectada.
        """
        context = f"Você está participando de uma conversa. e alguem vai falar com voce"
        msg = f" {context} {max_tag}."
        print(f"Prompt: {msg}")
        try:
            # Geração de resposta usando a API do Google Generative AI
            chat_session = self.generative_model.start_chat(history=[]) 
            response = chat_session.send_message(msg)
            self.update_chat_log(response.text)
        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")

    def update_chat_log(self, message):
        """
        Adiciona uma mensagem ao log de chat na interface gráfica.

        Args:
            message (str): Mensagem a ser adicionada ao log de chat.
        """
        self.chat_log.configure(state='normal')
        self.chat_log.insert(tk.END, f"{message}\n")
        self.chat_log.configure(state='disabled')
        self.chat_log.see(tk.END)

    def on_closing(self):
        """
        Ação executada ao fechar a janela principal.
        """
        if self.vid.isOpened():
            self.vid.release()
        if self.chat_vid.isOpened():
            self.chat_vid.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HandDetectionApp(root)
    root.mainloop()
