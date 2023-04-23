import os
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip
from termcolor import colored
import datetime
import time
#from tqdm import tqdm

def main():
    os.system('cls') # Limpa o console
    input(colored("Pressione qualquer tecla para começar, logo após escolha o arquivo de vídeo desejado.", 'cyan', attrs=['bold'])) # Precisa ser comentado em testes
    file_path = select_file()
    name_file = os.path.basename(file_path)
    print(f"Arquivo escolhido: {colored(name_file, 'cyan')}")

    # Obtem a duração do vídeo
    clip = VideoFileClip(file_path)
    duration = clip.duration
    clip.close()

    # Obtem o tempo inicial e final do usuário
    while True:
        start_time = input(f"\nDigite o tempo inicial no formato HH:MM:SS. \n{colored('Obs: Se você deseja selecionar desde o início do vídeo pressione a tecla Enter.', 'grey')} \nTempo inicial: ")
        if start_time == "": 
            start_time = "00:00:00"
        end_time = input("Digite o tempo final no formato HH:MM:SS: ")
        if valid_time(start_time, end_time, duration):
            break

    resolution = resolutions(file_path)
    process_video(file_path, start_time, end_time, resolution, name_file)

    while True:
        print(colored("\nDeseja repetir o procedimento com outro vídeo?", 'cyan', attrs=['bold']))
        print(colored("1 - Sim\n2 - Não", 'yellow', attrs=['bold']))
        repeat = input("Opção: ")
        if repeat == "1":
            main()
        elif repeat == "2":
            break
        else:
            print(colored("Opção inválida!", 'red'))
            time.sleep(2)

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
    
    print(f"\nA resolução atual do vídeo é {colored(current_resolution, 'yellow', attrs=['bold'])}.")
    print("Selecione uma opção de resolução:")
    for i, res in enumerate(resolutions):
        if i == 0:
            print(colored(f"{i + 1} - Resolução Atual({res})", 'cyan'))
        else:
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

    print(colored("\nProcessando...", 'green', attrs=['bold']))
    
    clip_resized.write_videofile(os.path.join("videos_recortados", f"{name_file}"), audio=True)
    print(colored("\nO vídeo foi recortado com sucesso!", 'green', attrs=['bold']))


# Valida os tempos inicias e finais
def valid_time(start_time, end_time, total_time):
    # Converte tempo para segundos
    start_sec = datetime.datetime.strptime(start_time, '%H:%M:%S').time().second + datetime.datetime.strptime(start_time, '%H:%M:%S').time().minute*60 + datetime.datetime.strptime(start_time, '%H:%M:%S').time().hour*3600
    end_sec = datetime.datetime.strptime(end_time, '%H:%M:%S').time().second + datetime.datetime.strptime(end_time, '%H:%M:%S').time().minute*60 + datetime.datetime.strptime(end_time, '%H:%M:%S').time().hour*3600

    if end_sec > total_time:
        print(colored("Erro: O tempo final é maior que a duração do vídeo", "red", attrs=['bold']))
        return False
    elif start_sec > total_time:
        print(colored("Erro: O tempo inicial é maior que a duração do vídeo", "red", attrs=['bold']))
        return False
    elif start_sec > end_sec:
        print(colored("Erro: O tempo inicial é maior que o tempo final", "red", attrs=['bold']))
        return False
    elif end_sec < start_sec:
        print(colored("Erro: O tempo final é menor que o tempo inicial", "red", attrs=['bold']))
        return False
    else:
        return True


# Start
main()
