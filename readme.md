# Aplicativo de Detecção de Mãos com Chat Integrado
- **Feito por Marcelo**
## Descrição da Aplicação

Este é um aplicativo de demonstração que combina detecção de mãos em tempo real com um llm, utilizando o Custom vision (object detection) e o Gemini da google.  O aplicativo foi desenvolvido para mostrar como é possivel desenvolver diversas soluçÕes com essa ferramenta, desde um chat de libras ao que sua imaginação permitir

### Finalidade

A aplicação visa demonstrar:

- **Detecção de Mãos**: Utiliza visão computacional para detectar mãos .
- **Detecção de Sinais de Libras**: Utiliza visão computacional para detectar sinais de Libra .
- **Interação via Chat**: Apresenta um chat simulado onde o usuário pode interagir através de mensagens digitadas.


### Funcionamento

Quando uma mão é detectada com alta probabilidade pela câmera do computador, o aplicativo abre automaticamente uma janela de chat simulado. O usuário pode então enviar um sinal de Oi em libra, que são respondidas por respostas Dinamicas geradas pelo próprio Gemini.
observação a unica mensagem que o Custom vision é o Oi

## Instruções de Uso

### Requisitos

1. **Python**: Certifique-se de ter o Python instalado. Recomenda-se a versão 3.x.
2. **Bibliotecas Python**: Instale as seguintes bibliotecas Python:
```bash
pip install opencv-python-headless pillow requests google-generativeai
```

### Executando o Aplicativo

1. **Baixar o Código**: Clone ou baixe o código-fonte do repositório.
2. **Executar o Aplicativo**:
- Navegue até o diretório onde o arquivo Python `app.py` está localizado.
- Execute o aplicativo Python:
  ```bash
  python app.py
  ```
3. **Utilizando o Aplicativo**:
- A janela do aplicativo será aberta, mostrando a detecção em tempo real da câmera.
- Clique no botão "Detectar Mãos" para iniciar a detecção de mãos.
- Se uma mão for detectada com alta probabilidade, a janela de chat será aberta automaticamente.
-Ao lado tem uma camera com a opção de enviar libras ao fazer o sinal de Oi e pressionar em enviar a mensagem sera enviada no chat.


4. **Encerrando o Aplicativo**:
- Feche a janela principal do aplicativo para encerrar a execução. Certifique-se de que todas as câmeras estão liberadas ao finalizar.

## Descrição das Ferramentas Utilizadas

- **Python**: Linguagem de programação utilizada para o desenvolvimento.
- **OpenCV**: Biblioteca de visão computacional utilizada para captura e processamento de vídeo.
- **Tkinter**: Biblioteca padrão do Python para criação de interfaces gráficas.
- **Azure Custom Vision**: Serviço de IA da Microsoft utilizado para detecção de objetos em imagens.
- **Google Gemini**: Serviço de IA da Google para geração avançada de textos e diálogos e pesquisa.
- **PIL (Pillow)**: Biblioteca para processamento de imagens.
- **Requests**: Biblioteca para realizar requisições HTTP.

