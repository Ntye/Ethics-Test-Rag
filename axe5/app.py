from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_juridique_mistral import RAGJuridiqueMistral
import logging
import os

# Configure basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Global variable to hold the RAG system instance
rag_system = None
rag_initialized = False

def initialize_rag_system():
    """
    Initializes the RAG system by loading the vector store and setting up the QA chain.
    """
    global rag_system, rag_initialized
    if rag_system is None:
        logging.info("Initializing RAG system...")
        try:
            # Check if the FAISS index files exist before proceeding
            index_path = "./faiss_index_mistral"
            if not os.path.exists(os.path.join(index_path, "index.faiss")) or \
               not os.path.exists(os.path.join(index_path, "index.pkl")):
                logging.warning("FAISS index files not found. RAG system will not be initialized.")
                rag_initialized = False
                return

            rag_system = RAGJuridiqueMistral()
            rag_system.load_vectorstore()
            rag_system.setup_qa_chain()
            rag_initialized = True
            logging.info("RAG system successfully initialized.")
        except Exception as e:
            logging.error(f"Error during RAG system initialization: {e}")
            rag_initialized = False

@app.route("/query", methods=["POST"])
def query_endpoint():
    """
    Handles POST requests to the /query endpoint.
    Expects a JSON payload with a "question" key.
    """
    if not rag_initialized or rag_system is None:
        logging.warning("Query received but RAG system is not initialized.")
        return jsonify({
            "error": "RAG system is not initialized. Please ensure the FAISS index is generated."
        }), 503

    # Ensure the request has a JSON body
    data = request.json
    if not data or "question" not in data:
        return jsonify({"error": "Invalid request. 'question' key is required in the JSON body."}), 400

    question = data["question"]
    logging.info(f"Received question: {question}")

    try:
        # Perform the query
        result = rag_system.query(question)

        # Format sources for a clean JSON response
        formatted_sources = [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in result.get('sources', [])
        ]

        response = {
            "answer": result.get("answer"),
            "sources": formatted_sources
        }

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"An error occurred while processing the query: {e}")
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == "__main__":
    # Initialize the RAG system before starting the Flask app
    initialize_rag_system()
    # Run the Flask app, making it accessible on the network
    app.run(host="0.0.0.0", port=5000)
