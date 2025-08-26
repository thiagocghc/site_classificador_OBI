Configurações iniciais do projeto

Deve acrescentar o .ENV para conectar na API OpenAI

pip install python-dotenv
pip install Flask pandas flask-cors

npx create-react-app site-questoes
#npm install react-icons


pip install fastapi "uvicorn[standard]" openai

1. Start na API 
uvicorn .\backend_openai\classficador_api.py

2. Start no Flask
python .\backend_dataset\app.py

3. Start no app React
cd .\site-questoes npm run