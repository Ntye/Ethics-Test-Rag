# test_install.py
try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.vectorstores import FAISS
    from langchain_mistralai import ChatMistralAI
    from langchain_community.embeddings import HuggingFaceEmbeddings

    print("✅ Toutes les importations réussies !")

    # Test Mistral
    llm = ChatMistralAI(
        mistral_api_key="test",
        model="mistral-small"
    )
    print("✅ ChatMistralAI initialisé")

    # Test embeddings
    embeddings = HuggingFaceEmbeddings()
    print("✅ HuggingFaceEmbeddings initialisé")

    print("\n🎉 Installation réussie !")

except Exception as e:
    print(f"❌ Erreur : {e}")