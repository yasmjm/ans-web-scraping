from src.scraping import download_anexos
from src.transform import processar_anexo_i
from pathlib import Path

def configurar_diretorios():
    """Garante que todas as pastas existam"""
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    Path("data/processed").mkdir(parents=True, exist_ok=True)

def executar_fluxo():
    print("🔍 ETAPA 1: Baixando Anexos...")
    download_anexos()  # Agora salva em data/raw/
    
    print("\n🔄 ETAPA 2: Processando Anexo I...")
    processar_anexo_i()  # Lê de data/raw/, salva em data/processed/
    
    print("\n✅ Concluído! Verifique:")
    print("- PDFs em: data/raw/")
    print("- Resultados em: data/processed/")

if __name__ == "__main__":
    configurar_diretorios()
    executar_fluxo()