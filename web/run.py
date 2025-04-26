from app import create_app

# 애플리케이션 초기화
app = create_app()

# 서버 실행
if __name__ == "__main__":
    app.run(debug=True)  # 디버깅 모드로 실행
