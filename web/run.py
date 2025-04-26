from app import create_app
from waitress import serve

# 애플리케이션 초기화
app = create_app()

# 서버 실행
if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000, threads=8)