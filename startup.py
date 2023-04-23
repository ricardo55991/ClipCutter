import cv2
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

# Recebe uma string time_str no formato HH:MM:SS e retorna o tempo equivalente em segundos
def time_to_sec(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

root = tk.Tk()
root.withdraw()

# Selecionar o arquivo de vídeo
file_path = filedialog.askopenfilename()

# Obter o tempo inicial e final do usuário
# start_time = input("Digite o tempo inicial no formato HH:MM:SS: ")
# end_time = input("Digite o tempo final no formato HH:MM:SS: ")

start_time = "00:00:00"
end_time = "00:00:05"

# Obter a resolução desejada
cap = cv2.VideoCapture(file_path)
current_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
current_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
current_resolution = f"{current_width}x{current_height}"
resolutions = [current_resolution, "1280x720", "854x480", "640x360"]

print(f"A resolução atual do vídeo é {current_resolution}.")
print("Selecione uma opção de resolução:")
for i, res in enumerate(resolutions):
    print(f"{i + 1} - {res}")

resolution_option = input("Opção: ")
try:
    resolution_index = int(resolution_option) - 1
    resolution = resolutions[resolution_index]
except:
    print("Opção inválida.")
    exit(1)

# Definir os parâmetros de recorte e redimensionamento
fps = cap.get(cv2.CAP_PROP_FPS)

# Calcular o número do quadro inicial e final
start_frame = int(time_to_sec(start_time) * fps)
end_frame = int(time_to_sec(end_time) * fps)
resize_width, resize_height = map(int, resolution.split("x"))

# Criar um vídeo com a nova resolução e recorte
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('video_recortado.mp4', fourcc, cap.get(cv2.CAP_PROP_FPS), (resize_width, resize_height))
for i in tqdm(range(start_frame, end_frame), desc="Recortando vídeo", unit="%", leave=False):
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (resize_width, resize_height))
    out.write(frame)

cap.release()
out.release()

print("O vídeo foi recortado com sucesso!")
