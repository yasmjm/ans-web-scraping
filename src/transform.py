import pandas as pd
import pdfplumber
import zipfile
import os
from pathlib import Path

# confg
PASTA_ANEXOS = "anexos"
ANEXO_I = Path("data/raw/Anexo_I.pdf")
CSV_SAIDA = Path("data/processed/Rol_de_Procedimentos.csv")
ZIP_SAIDA = Path("data/processed/Teste_Yasmim.zip") 
LEGENDA = {
    "OD": "Odontológico",
    "AMB": "Ambulatorial"
}

def extrair_tabela_pdf():
    """Extrai a tabela do PDF usando pdfplumber"""
    print("🔍 Extraindo tabela do PDF...")
    todas_tabelas = []
    
    with pdfplumber.open(ANEXO_I) as pdf:
        for pagina in pdf.pages:
            tabela = pagina.extract_table()
            if tabela:
                # vai pegar o cabeçalho so na primeira página
                if not todas_tabelas:
                    cabecalho = tabela[0]
                    todas_tabelas.append(cabecalho)
                # add linhas de dados (ignora cabeçalho repetido)
                todas_tabelas.extend(tabela[1:])
    
    if not todas_tabelas:
        raise ValueError("Nenhuma tabela encontrada no PDF!")
    
    return todas_tabelas

def tratar_dados(tabela):
    """Limpa e estrutura os dados"""
    print("🧹 Limpando dados...")
    df = pd.DataFrame(tabela[1:], columns=tabela[0])
    
    # remove linhas vazias/duplicadas
    df = df.dropna(how='all').drop_duplicates()
    
    # substitui abreviações conforme legenda
    for col in df.columns:
        if col in LEGENDA:
            df[col] = df[col].replace(LEGENDA)
    
    return df

def salvar_compactar(df):
    """Salva CSV e compacta"""
    print("💾 Salvando CSV...")
    df.to_csv(CSV_SAIDA, index=False, encoding='utf-8-sig')
    
    print("🗜 Compactando...")
    with zipfile.ZipFile(ZIP_SAIDA, 'w') as zipf:
        zipf.write(CSV_SAIDA)
    
    print(f"✅ Arquivo {ZIP_SAIDA} criado com sucesso!")

def main():
    print("\n" + "="*50)
    print("ETAPA 2: TRANSFORMAÇÃO DE DADOS")
    print("="*50)
    
    # extrair dados do PDF
    tabela = extrair_tabela_pdf()
    
    # estruturar e limpar dados
    df = tratar_dados(tabela)
    
    # salvar e compactar
    salvar_compactar(df)

if __name__ == "__main__":
    main()