from mistralai import Mistral
from config import API_KEY, AGENT_ID

class LLMManager():
    api_key = API_KEY
    agent_id = AGENT_ID
    client = Mistral(api_key=api_key)

    user_question = "다음 질문을 한국어로 정제해줘, 정제는 맞춤법, 오타, 맥락에 맞는 단어 수정이고 고등학생이 알아들을 수 있도록 해줘 : 문장 형식에서 변항이 자유롭게 나타나도 실제 값이나 대상이 주입되면 더이상 자유롭지 못한것 아니야? 그렴 변항의 자유로움과 속박됨은 문장형식에서 양화사나 값이 대응되서 나타나는것에 의존하는거야?"

    try:
        agent_response = client.agents.complete(
            agent_id=agent_id,
            messages=[
                {"role": "user", "content": user_question}
            ]
        )
        print(agent_response.choices[0].message.content)
    except Exception as e:
        print(f"오류 발생: {e}")