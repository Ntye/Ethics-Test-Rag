"""
RAG Juridique - Version compatible avec vos dépendances
"""

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_mistralai import ChatMistralAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class RAGJuridiqueMistral:
    """RAG optimisé avec Mistral AI"""

    def __init__(self, docs_directory="./documents_juridiques"):
        # Vérifier clé Mistral
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        if not self.mistral_key:
            raise ValueError("❌ MISTRAL_API_KEY non trouvé dans .env")

        self.docs_directory = docs_directory
        self.vectorstore = None
        self.qa_chain = None
        self.index_path = "./faiss_index_mistral"

        # Embeddings locaux gratuits
        print("📦 Chargement des embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        print("✅ Embeddings prêts")

    def load_documents(self):
        """Charger tous les PDFs"""
        print("📚 Chargement des documents...")
        loader = DirectoryLoader(
            self.docs_directory,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        documents = loader.load()
        print(f"✅ {len(documents)} pages chargées")
        return documents

    def split_documents(self, documents):
        """Découper en chunks"""
        print("✂️  Découpage des documents...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=250,
            separators=["\n\nArticle ", "\n\n", "\n", ". ", " "]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✅ {len(chunks)} chunks créés")
        return chunks

    def create_vectorstore(self, chunks):
        """Créer base vectorielle FAISS"""
        print("🔢 Création de la base vectorielle...")
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.vectorstore.save_local(self.index_path)
        print(f"✅ Base sauvegardée dans {self.index_path}")

    def load_vectorstore(self):
        """Charger base existante"""
        print("📂 Chargement de la base vectorielle...")
        self.vectorstore = FAISS.load_local(
            self.index_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print("✅ Base chargée")

    def setup_qa_chain(self):
        """Configurer chaîne Q/A"""
        print("⚙️  Configuration de Mistral AI...")

        template = """Tu es un expert en droit camerounais et OHADA.

Contexte juridique:
{context}

Question: {question}

Instructions:
1. Réponds précisément en français
2. Cite les articles de loi
3. Base-toi sur le contexte fourni
4. Structure ta réponse clairement

Réponse:"""

        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        model = os.getenv("MISTRAL_MODEL", "mistral-medium")

        llm = ChatMistralAI(
            mistral_api_key=self.mistral_key,
            model=model,
            temperature=0.1,
            max_tokens=2000
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        print("✅ Système Q/A configuré")

    def initialize(self):
        """Initialisation complète"""
        print("\n" + "="*60)
        print("🚀 INITIALISATION RAG MISTRAL")
        print("="*60 + "\n")

        documents = self.load_documents()
        if not documents:
            print("⚠️  Aucun document trouvé!")
            return False

        chunks = self.split_documents(documents)
        self.create_vectorstore(chunks)
        self.setup_qa_chain()

        print("\n" + "="*60)
        print("🎉 SYSTÈME PRÊT !")
        print("="*60 + "\n")
        return True

    def query(self, question):
        """Interroger le système"""
        if not self.qa_chain:
            if os.path.exists(self.index_path):
                self.load_vectorstore()
                self.setup_qa_chain()
            else:
                raise Exception("Système non initialisé")

        result = self.qa_chain({"query": question})

        return {
            "answer": result["result"],
            "sources": result["source_documents"]
        }
