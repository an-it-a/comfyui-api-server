cd /app/http-server
nohup functions-framework --target=main_handle &

cd /app/ComfyUI
python main.py