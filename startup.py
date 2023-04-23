import os
from moviepy.editor import VideoFileClip
#from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

def main():
    os.system('cls') # Limpa o console
    print("Escolha o arquivo de vídeo:")
    file_path = select_file()
    name_file = os.path.basename(file_path)
    print(f"Arquivo escolhido: {name_file}")

    # Obtem o tempo inicial e final do usuário
    start_time = input("\nDigite o tempo inicial no formato HH:MM:SS. Se você deseja selecionar desde o início do vídeo, pressione a tecla Enter. \nTempo inicial: ")
    if start_time == "": 
        start_time = "00:00:00"
    end_time = input("Digite o tempo final no formato HH:MM:SS: ")

    resolution = resolutions(file_path)
    process_video(file_path, start_time, end_time, resolution, name_file)

# Obtem o caminho do arquivo de vídeo
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

# Obtem as resoluções
def resolutions(file_path):
    types_resolutions = {
        '1080p': '1920x1080',
        '900p': '1600x900',
        '720p': '1280x720',
        '540p': '960x540',
        '480p': '854x480',
        '360p': '640x360'
    }
    video_clip = VideoFileClip(file_path)
    current_resolution = f"{video_clip.w}x{video_clip.h}"
    resolutions = [current_resolution]
    resolutions.extend(types_resolutions.keys())
    print(f"\nA resolução atual do vídeo é {current_resolution}.")
    print("Selecione uma opção de resolução:")
    for i, res in enumerate(resolutions):
        print(f"{i + 1} - {res}")
    resolution_option = input("Opção: ")
    try:
        resolution_index = int(resolution_option) - 1
        return resolutions[resolution_index]
    except:
        print("Opção inválida.")
        exit(1)

# Recebe uma string time_str no formato HH:MM:SS e retorna o tempo equivalente em segundos
def time_to_sec(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s


# Recorta o vídeo no intervalo de tempo especificado, redimensiona-o para a resolução especificada e salva o arquivo com o nome fornecido.
def process_video(file_path, start_time, end_time, resolution, name_file):
    clip = VideoFileClip(file_path).subclip(start_time, end_time)

    # Separando a altura e largura
    resolution = resolution.split('x')
    width, height = int(resolution[0]), int(resolution[1])

    clip_resized = clip.resize((width, height))

    # criando a pasta videos se ela não existir
    if not os.path.exists("videos_recortados"):
        os.mkdir("videos_recortados")

    
    clip_resized.write_videofile(os.path.join("videos_recortados", f"{name_file}.mp4"), audio=True)
    print("\nO vídeo foi recortado com sucesso!")


# Start
main()
