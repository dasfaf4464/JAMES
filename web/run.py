import subprocess
import threading
import re
from app import create_app
from waitress import serve
from config import CLOUDFLARE_TUNNEL_COMMAND, MARIADB_COMMAND, REDIS_COMMAND

app = create_app()

cloudflare_process = None
cloudflare_URL = None
mariadb_process = None
redis_process = None

def start_cloudflare():
    global cloudflare_process
    cloudflare_process = subprocess.Popen(
        CLOUDFLARE_TUNNEL_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    global cloudflare_URL
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

def start_mariadb():
    global mariadb_process
    mariadb_process = subprocess.Popen(
        MARIADB_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    mariadb_process.wait()

def start_redis():
    global redis_process
    redis_process = subprocess.Popen(
        REDIS_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    redis_process.wait()
      
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
    print('Starting Waitress Server...')
    serve(app, host='0.0.0.0', port=5000, threads=4)

if __name__ == "__main__":
    cloudflare_thread = threading.Thread(target=run_cloudflare, daemon=True)
    mariadb_thread = threading.Thread(target=run_mariadb, daemon=True)
    #redis_thread = threading.Thread(target=run_redis, daemon=True)
    flask_thread = threading.Thread(target=run_flask, daemon=True)

    flask_thread.start()
    cloudflare_thread.start()
    mariadb_thread.start()
    #redis_thread.start()

    flask_thread.join()
