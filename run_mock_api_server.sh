API_PORT=8080
API_HOST="127.0.0.1"

cd assets/mock_api
pip install -r requirements.txt
uvicorn main:app --host $API_HOST --port $API_PORT