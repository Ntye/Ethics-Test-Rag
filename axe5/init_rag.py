from rag_juridique_mistral import RAGJuridiqueMistral
import sys

def main():
    try:
        rag = RAGJuridiqueMistral()
        success = rag.initialize()

        if success:
            print("\n?? TEST RAPIDE")
            print("="*60)
            test_q = "Qu'est-ce que le code OHADA ?"
            print(f"\n? {test_q}\n")
            result = rag.query(test_q)
            print(f"?? {result['answer'][:300]}...\n")
            print("="*60)
            print("\n? Systeme operationnel !")
            print("\nProchaines etapes:")
            print("    python app.py       : Lancer le backend API")

    except Exception as e:
        print(f"\n? Erreur: {e}")
        print("\nVerifiez:")
        print("    Cle MISTRAL_API_KEY dans .env")
        print("    Documents PDF presents")
        print("    Connexion internet")
        sys.exit(1)

if __name__ == "__main__":
    main()
