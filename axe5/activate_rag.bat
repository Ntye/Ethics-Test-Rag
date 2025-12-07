@echo off
echo Activation de l'environnement RAG Juridique...
call conda activate rag-juridique
echo.
echo ========================================
echo   Environnement RAG Juridique active
echo ========================================
echo.
echo Commandes disponibles :
echo   - python check_config.py    : Verifier la config
echo   - python init_rag.py        : Initialiser le RAG
echo   - python app.py             : Lancer le backend API
echo.
cmd /k
