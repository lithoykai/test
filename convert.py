import subprocess

def converter_mkv_para_mp4(entrada_mkv, saida_mp4, novo_titulo):
    try:
        subprocess.run(
            [
                'ffmpeg',
                '-i', entrada_mkv,
                '-c:v', 'copy',  
                '-c:a', 'copy',  
                '-metadata', f'title={novo_titulo}',
                saida_mp4
            ],
            check=True
        )
        print(f"Conversão de {entrada_mkv} para {saida_mp4} concluída com sucesso.")
    except subprocess.CalledProcessError as e:
        print("Erro durante a conversão:", e)

# Solicitar informações do usuário
entrada_mkv = input("Digite o caminho completo do arquivo MKV de entrada: ")
saida_mp4 = input("Digite o caminho completo do arquivo MP4 de saída: ")
novo_titulo = input("Digite o novo título para o vídeo: ")

# Chamar a função com as entradas fornecidas pelo usuário
converter_mkv_para_mp4(entrada_mkv, saida_mp4, novo_titulo)
