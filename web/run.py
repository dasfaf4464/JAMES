import subprocess
import threading
import re
import signal
import sys
from app import create_app
from waitress import serve
from config import CLOUDFLARE_TUNNEL_COMMAND

app = create_app()

cloudflared_process = None

def start_cloudflare():
    global cloudflared_process
    cloudflared_process = subprocess.Popen(
        CLOUDFLARE_TUNNEL_COMMAND,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # stdout+stderr 합치기
        text=True
    )

    tunnel_url = None

    # 주소를 찾을 때까지 읽기
    for line in cloudflared_process.stdout:
        #print("[cloudflared]", line.strip())  # 디버그용 출력
        match = re.search(r'https://[a-z0-9-]+\.trycloudflare\.com', line)
        if match:
            tunnel_url = match.group()
            print(f"Cloudflare Tunnel URL: {tunnel_url}")
            break

    if tunnel_url is None:
        print("Failed to retrieve Cloudflare Tunnel URL.")
        cloudflared_process.terminate()
        return None

    # cloudflared가 살아있는 동안 대기
    try:
        cloudflared_process.wait()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Terminating cloudflared...")
        cloudflared_process.terminate()

    return tunnel_url

def run_cloudflare():
    print("Starting Cloudflare Tunnel...")
    tunnel_url = start_cloudflare()
    if tunnel_url:
        print(f"Tunnel running at {tunnel_url}")
    else:
        print("Cloudflare tunnel failed.")

def signal_handler(sig, frame):
    print("\n[!] Caught termination signal. Shutting down...")
    if cloudflared_process:
        cloudflared_process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 클라우드플레어는 별도 스레드로
    cloudflare_thread = threading.Thread(target=run_cloudflare, daemon=True)
    cloudflare_thread.start()

    # 메인 스레드는 서버 실행
    serve(app, host='0.0.0.0', port=5000, threads=8)
