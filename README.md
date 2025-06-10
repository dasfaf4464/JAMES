# 2025-1 경기대학교 기초캡스톤디자인
## <b>JAMES(Junchul and Miracle Extreme Students)

## 팀원
|조해천|문준서|이상훈|이지연|
|:---:|:---:|:---:|:---:|
|팀장, Back, DB|LLM 설정|논문|Web Front|
|컴퓨터공학부 4학년|컴퓨터공학전공 3학년|수학과 4학년|컴퓨터공학전공 3학년|
|[@github](https://www.github.com/dasfaf4464)|[@github](https://www.github.com/odpd09091)|[@github](https://www.github.com/KGU-LSH)|[@github](https://www.github.com/leejiyeoniya)|

|지도 교수|자문|
|:---:|:---:|
|전준철|김현빈|

## 프로젝트 - Unmute
### 개요
수업이나 강연의 마무리에 질의응답시간을 가지면 장소가 호랑이 앞에서 쥐죽은 듯 조용하다. 우리는 이 현상에 대한 의문을 가지고 질의응답을 활발히하기 위해 ASKGU 서비스를 개발한다.
> <b>질문하는 자는 5분간 바보지만, 질문하지 않는 자는 평생 바보다.

### 개발 환경
- Frontend : HTML, CSS, JS
- Backend : Python Flask, Cloudflare Tunnel
- Database : MariaDB, Redis

### 주요 기능

#### 질의응답 세션 생성 및 참가
- 누구나 질의응답 세션을 생성할 수 있다. 세션은 반영구적이거나 임시적이다.
- 질의응답 세션에 입장할 때 QRcode, URL_Link, 공개된 목록에서 찾아서 입장할 수 있다.
- 세션 입장시 무작위로 생성된 이름을 제공받는다.
#### LLM을 이용한 질문 생성
- 사용자는 질문을 보내면 LLM을 거쳐 질문을 정제한다.
- LLM에서 정제된 질문을 최대 세 개 까지 보내준다.
- 사용자는 받은 질문 중 원하는 질문을 선택하여 세션에 업로드한다.
- 업로드된 질문은 범주로 묶여 어떤 질문 종류가 가장 많은지 알 수 있도록 시각화 효과가 적용 된다. 
#### 악의적 이용 예방
- 익명으로 업로드 될 때 욕설이나 비방이 포함된 글 작성을 예방하고 제지한다.
- 질문 남발을 예방하기 위해 딜레이를 준다.
- 중복 게시를 피하기 위해 이미 업로드 된 질문에 자신의 의견을 포함할 수있는 기능을 포함한다.
#### 사용자 기록 저장
- 사용자는 입장시 무작위로 생성된 임시 키를 부여받는다.
- 해당 임시키를 기간 내 활성화 하지 않으면 기록이 사라진다.
- 사용자는 자신이 한 질문과 대답, 저장한 질문과 대답, 입장한 세션을 볼 수 있다.

### 주요 화면
||||||
|:---:|:---:|:---:|:---:|:---:|
||→ 회원 가입 →|<img src="https://github.com/user-attachments/assets/0c8177d2-e7d4-4971-aa14-541bcda3c5ec" width="auto" height="120">|||
|<img src="https://github.com/user-attachments/assets/076cc23a-f52a-4a93-b92b-87ac4229a904" width="auto" height="120">|→ 로그인 →|<img src="https://github.com/user-attachments/assets/f7ddfc5e-6e18-4f66-bb74-8573fd7fadd6" width="auto" height="120">|→ 기록 보기 →|<img src="https://github.com/user-attachments/assets/b10c17b8-006f-4bd7-8a35-983df62b27bb" width="auto" height="120">|
||→ 세션 생성→|<img src="https://github.com/user-attachments/assets/6a92046e-8823-4f81-88dd-f1af91b1c24d" width="auto" height="120">|→홈에서 생성→|<img src="https://github.com/user-attachments/assets/a4d26eb7-6a5e-40c4-88ba-ea54109d68b6" width="auto" height="120">|
||→ 세션 입장 →|<img src="https://github.com/user-attachments/assets/c64ab907-c2b0-4737-8bac-81d127e79627" width="auto" height="120">|→ 질문하기 →|<img src="https://github.com/user-attachments/assets/4ea0ebb2-4cac-4362-8f0e-6f5192e26bd4" width="auto" height="120">|

## 팀원 공간
### 참고 자료
[참고 페이지 : notion](https://cerulean-transport-2a9.notion.site/AI-1ad265623d0780fab864febae640a97a?pvs=74)

### 주요 일정
#### 교내 캡스톤 디자인
1. 수행 계획서 제출(완)
2. 최종 보고서 제출(완)
3. 캡스톤 디자인 발표(2025-06-13)
#### 한국정보기술학회 대학생논문경진대회
1. 논문 모집(완)
2. 경진 대회(2025-06-13)
