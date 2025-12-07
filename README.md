# Legal RAG API and Frontend

This project contains a backend API for a legal Retrieval-Augmented Generation (RAG) system and a simple chat-based frontend to interact with it.

## Backend (axe5)

The backend is a Flask application that exposes the RAG system via a JSON API. For more details on the backend, please see the `axe5/README.md` file.

### Running the Backend

1.  Navigate to the `axe5` directory:
    ```bash
    cd axe5
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  (If necessary) Generate the FAISS index:
    ```bash
    python init_rag.py
    ```
4.  Run the backend server:
    ```bash
    python app.py
    ```
The backend server will be running at `http://127.0.0.1:5000`.

## Frontend

The frontend is a simple chat application built with HTML, CSS, and JavaScript.

### Running the Frontend

1.  Make sure the backend server is running.
2.  Open the `frontend/index.html` file in your web browser.

You can now interact with the legal RAG system through a user-friendly chat interface.
