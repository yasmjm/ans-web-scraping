import requests
import os
from zipfile import ZipFile
from pathlib import Path

ANEXOS_DIR = Path("data/raw")


def baixar_pdf(url, nome_arquivo):
    """Baixa um arquivo PDF e salva localmente"""
    try:
        resposta = requests.get(url, stream=True, timeout=30)
        resposta.raise_for_status()
        
        # Cria a pasta se não existir
        os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
        
        with open(nome_arquivo, 'wb') as f:
            for chunk in resposta.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"✅ {os.path.basename(nome_arquivo)} baixado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao baixar {os.path.basename(nome_arquivo)}: {str(e)}")
        return False

def compactar_arquivos(arquivos, nome_zip):
    """Compacta vários arquivos em um ZIP"""
    try:
        with ZipFile(nome_zip, 'w') as zipf:
            for arquivo in arquivos:
                if os.path.exists(arquivo):
                    zipf.write(arquivo, os.path.basename(arquivo))
                    print(f"📦 {os.path.basename(arquivo)} adicionado ao ZIP")
                else:
                    print(f"⚠️ Arquivo {os.path.basename(arquivo)} não encontrado")
        print(f"✅ Compactação concluída: {nome_zip}")
        return True
    except Exception as e:
        print(f"❌ Erro ao compactar arquivos: {str(e)}")
        return False

# URLs oficiais dos anexos (atualizadas para 2024)
URLS_ANEXOS = {
    "Anexo_I": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",
    "Anexo_II": "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
}

# Nomes dos arquivos locais
PASTA_DOWNLOAD = "anexos"
ARQUIVOS = {
    "Anexo_I": os.path.join(PASTA_DOWNLOAD, "Anexo_I.pdf"),
    "Anexo_II": os.path.join(PASTA_DOWNLOAD, "Anexo_II.pdf")
}
NOME_ZIP = "anexos_ans.zip"

# Execução principal
if __name__ == "__main__":
    print("🚀 Iniciando download dos anexos...")
    
    # Baixar todos os anexos
    resultados = []
    for nome, url in URLS_ANEXOS.items():
        resultados.append(baixar_pdf(url, ARQUIVOS[nome]))
    
    # Compactar apenas se todos os downloads foram bem-sucedidos
    if all(resultados):
        print("\n📦 Preparando para compactar os arquivos...")
        arquivos_para_zipar = list(ARQUIVOS.values())
        compactar_arquivos(arquivos_para_zipar, NOME_ZIP)
    else:
        print("\n⚠️ Alguns arquivos não foram baixados. A compactação foi cancelada.")
    
    print("\n✅ Processo concluído!")