import requests
import os
import sys
import signal
from threading import Event
from urllib.parse import urlparse, unquote

# Variável global para controlar a interrupção
stop_event = Event()

def get_filename_from_url(url):
    # Extrai o nome do arquivo da URL e preserva a extensão
    path = urlparse(url).path
    return unquote(os.path.basename(path))

def download_file(url, dest_dir, custom_name=None):
    global stop_event

    # Obtém o nome original do arquivo a partir da URL
    file_name = get_filename_from_url(url)
    file_ext = os.path.splitext(file_name)[1]  # Obtém a extensão do arquivo

    if custom_name:
        # Aplica a extensão original ao nome customizado, se presente
        file_name = custom_name + file_ext

    dest = os.path.join(dest_dir, file_name)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 1048576  # Aumentando para 1 MB

        with open(dest, 'wb') as file:
            downloaded_size = 0
            for chunk in response.iter_content(chunk_size=chunk_size):
                if stop_event.is_set():
                    print("\nDownload interrompido.")
                    return
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Calcula e exibe o progresso em tempo real
                    progress = (downloaded_size / total_size) * 100
                    sys.stdout.write(f"\r[*] {downloaded_size / 1024:.2f} KB / {total_size / 1024:.2f} KB @ {len(chunk) / 1024:.2f} KB/s [{progress:.2f}%]")
                    sys.stdout.flush()

        print(f"\nArquivo salvo em: {dest}")
    except Exception as e:
        print(f"Erro: {e}")

def download_multiple_files(file_urls, dest_dir):
    global stop_event
    for url in file_urls:
        original_name = get_filename_from_url(url)
        custom_name = input(f"Digite o nome para o arquivo '{original_name}' (ou pressione Enter para usar o nome original): ").strip()
        if not custom_name:
            custom_name = None
        print(f"\nBaixando {url} para {os.path.join(dest_dir, original_name)}...")
        download_file(url, dest_dir, custom_name)

def signal_handler(sig, frame):
    global stop_event
    print("\nInterrompido pelo usuário.")
    stop_event.set()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    # Solicita o diretório de saída do usuário
    dest_dir = input("Digite o caminho do diretório de saída para os arquivos: ").strip()
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)  # Cria o diretório caso não exista
    
    file_urls = []
    
    while True:
        try:
            url = input("Digite o URL do arquivo (ou 'sair' para encerrar): ")
            if url.lower() == 'sair':
                break
            file_urls.append(url)
        except KeyboardInterrupt:
            print("\nEntrada interrompida. Encerrando o programa.")
            break
    
    download_multiple_files(file_urls, dest_dir)
