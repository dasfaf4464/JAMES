import subprocess
import threading
import re
import signal
from app import create_app
from waitress import serve
from config import CLOUDFLARE_TUNNEL_COMMAND, MARIADB_COMMAND, REDIS_COMMAND

app = create_app()

cloudflared_process = None
cloudflare_URL = None
mariadb_process = None
redis_process = None

def start_cloudflare():
    global cloudflared_process
    cloudflared_process = subprocess.Popen(
        CLOUDFLARE_TUNNEL_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    global cloudflare_URL
    tunnel_url = None

    print("read URL...")
    for line in cloudflared_process.stdout:
        match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
        if match:
            tunnel_url = match.group()
            break

    if tunnel_url is None:
        print("Failed to retrieve Cloudflare Tunnel URL.")
        cloudflared_process.terminate()
        return None
    else:
        cloudflare_URL = tunnel_url
        print(f"Tunnel running at {cloudflare_URL}")

    try:
        cloudflared_process.wait()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Terminating cloudflared...")
        cloudflared_process.terminate()

def start_mariadb():
    global mariadb_process
    mariadb_process = subprocess.Popen(
        MARIADB_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    try:
        mariadb_process.wait()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Terminating maraidb...")
        mariadb_process.terminate()

def start_redis():
    global redis_process
    redis_process = subprocess.Popen(
        REDIS_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    try:
        redis_process.wait()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Terminating redis...")
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

def signal_handler(sig, frame):
    print("\n[!] Caught termination signal. Shutting down...")
    if cloudflared_process != None:
        cloudflared_process.terminate()
        print("cloudflare is shuted down")
        cloudflared_process = None
    if mariadb_process != None:
        mariadb_process.terminate()
        print("mariadb is shuted down")
        mariadb_process = None
    if redis_process != None:
        redis_process.terminate()
        print('redis is shuted down')
        redis_process = None

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    cloudflare_thread = threading.Thread(target=run_cloudflare, daemon=True)
    mariadb_thread = threading.Thread(target=run_mariadb, daemon=True)
    #redis_thread = threading.Thread(target=run_redis, daemon=True)

    cloudflare_thread.start()
    mariadb_thread.start()
    #redis_thread.start()

    serve(app, host='0.0.0.0', port=5000, threads=4)
