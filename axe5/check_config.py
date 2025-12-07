import os
from dotenv import load_dotenv

load_dotenv()

def check_setup():
    print("\n?? VERIFICATION DE LA CONFIGURATION\n")
    print("="*60)

    checks = {}

    # Documents
    docs_path = './documents_juridiques'
    if os.path.exists(docs_path):
        pdf_count = sum(1 for root, dirs, files in os.walk(docs_path) for f in files if f.endswith('.pdf'))
        checks['Documents PDF'] = pdf_count > 0
        if pdf_count > 0:
            print(f"? Documents PDF: {pdf_count} fichiers trouves")
        else:
            print("? Documents PDF: Aucun fichier trouve")
    else:
        checks['Documents PDF'] = False
        print("? Dossier documents_juridiques inexistant")

    # Cle Mistral
    api_key = os.getenv('MISTRAL_API_KEY', '')
    checks['Cle Mistral'] = api_key is not None and api_key != ""
    if checks['Cle Mistral']:
        print(f"? Cle Mistral: Configuree")
    else:
        print("? Cle Mistral: Non configuree ou invalide")

    # Index FAISS
    checks['Index FAISS'] = os.path.exists('./faiss_index_mistral')
    if checks['Index FAISS']:
        print("? Index FAISS: Existe")
    else:
        print("??  Index FAISS: Pas encore cree ^(normal si premiere fois^)")

    print("\n" + "="*60)

    if all([checks['Documents PDF'], checks['Cle Mistral']]):
        print("?? Configuration OK ! Pret a initialiser.\n")
        print("Prochaine etape:")
        print("  python init_rag.py")
    else:
        print("??  Configuration incomplete.\n")
        print("TODO:")
        if not checks['Documents PDF']:
            print("    Ajoutez des PDFs dans documents_juridiques/")
        if not checks['Cle Mistral']:
            print("    Editez .env et ajoutez votre cle Mistral")
            print("    Format: MISTRAL_API_KEY=your_api_key")
    print("="*60 + "\n")

if __name__ == "__main__":
    check_setup()
