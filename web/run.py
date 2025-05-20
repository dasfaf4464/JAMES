"""
프로세스 진입점입니다.
플라스크 실행 이후 redis, mariadb, cloudflare를 개별 쓰레드에서 실행합니다.
플라스크는 웹소켓 지원과 병렬적으로 페이지를 제공하기 위해 eventlet으로 실행됩니다.
각 페이지는 route 모듈로 관리되며 chat:websocket 기능은 chat_manager에 등록되어있습니다.
"""

import subprocess
import threading
import re
from app import create_app
from flask_socketio import SocketIO
from app.api.room import init_socketio
from config import CLOUDFLARE_TUNNEL_COMMAND, MARIADB_COMMAND, REDIS_COMMAND

app = create_app()

socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")
init_socketio(socketio=socketio)

cloudflare_process = None
cloudflare_URL = None
mariadb_process = None
redis_process = None

def start_cloudflare():
    global cloudflare_process
    global cloudflare_URL
    try:
        cloudflare_process = subprocess.Popen(
            CLOUDFLARE_TUNNEL_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    
        tunnel_url = None

        print("read URL... [up to 10s]")
        for line in cloudflare_process.stdout:
            match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
            if match:
                tunnel_url = match.group()
                break

        if tunnel_url is None:
            print("Failed to retrieve Cloudflare Tunnel URL.")
            cloudflare_process.terminate()
            return None
        else:
            cloudflare_URL = tunnel_url
            print(f"Tunnel running at {cloudflare_URL}")

        cloudflare_process.wait()    
    finally:
        if cloudflare_process and cloudflare_process.poll() is None:
            print("Cloudflare thread expired, Terminating Cloudflare process")
            cloudflare_process.terminate()

def start_mariadb():
    global mariadb_process
    try:
        mariadb_process = subprocess.Popen(
        MARIADB_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
        mariadb_process.wait()

    finally:
        if mariadb_process and mariadb_process.poll() is None:
            print("MariaDB thread expired, Terminating MariaDB process")
            mariadb_process.terminate()

def start_redis():
    global redis_process
    try:
        redis_process = subprocess.Popen(
            REDIS_COMMAND,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        redis_process.wait()
    finally:
        if redis_process and redis_process.poll() is None:
            print("Redis thread expired, Terminating Redis process")
            redis_process.terminate()

def run_cloudflare():
    print("Starting Cloudflare Tunnel...")
    start_cloudflare()

def run_mariadb():
    print("Starting MariaDB...")
    start_mariadb()

def run_redis():
    print("Starting Redis...")
    start_redis()

def run_flask():
    print('Starting Server...')
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    #cloudflare_thread = threading.Thread(target=run_cloudflare, daemon=True)
    mariadb_thread = threading.Thread(target=run_mariadb, daemon=True)
    redis_thread = threading.Thread(target=run_redis, daemon=True)
    flask_thread = threading.Thread(target=run_flask, daemon=True)

    mariadb_thread.start()
    redis_thread.start()
    flask_thread.start()
    #cloudflare_thread.start()

    flask_thread.join()
    mariadb_thread.join()
    redis_thread.join()
    #cloudflare_thread.join()
