"""
Mistral Agent와 연결되어 내용을 주고받는 클래스입니다.
agent는 총 네 개 입니다.
"""

from mistralai import Mistral
from config import API_KEY, AGENT_ID
from concurrent.futures import ThreadPoolExecutor
import queue
import threading
import time

class LLMManager:
    llm_thread = ThreadPoolExecutor(max_workers=4)

    api_key = API_KEY
    
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.client = Mistral(api_key=self.api_key)

    def request_llm(self, prompt:str):
        try:
            agent_response = self.client.agents.complete(
                agent_id=self.agent_id,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            print(agent_response.choices[0].message.content)
        except Exception as e:
            print(f"오류 발생: {e}")

    def create_prompt(self, user_input:str):
        prompt = "다음 질문을 한국어로 정제해줘, 정제는 맞춤법, 오타, 맥락에 맞는 단어 수정이고 고등학생이 알이들을 수 있도록 해줘 :"
        return prompt + user_input

user_question = "문장 형식에서 변항이 자유롭게 나타나도 실제 값이나 대상이 주입되면 더이상 자유롭지 못한것 아니야? 그렴 변항의 자유로움과 속박됨은 문장형식에서 양화사나 값이 대응되서 나타나는것에 의존하는거야?"
l1 = LLMManager(agent_id=AGENT_ID[0])
l2 = LLMManager(agent_id=AGENT_ID[1])
l3 = LLMManager(agent_id=AGENT_ID[2])

"""
def test1():
    start = time.time()
    l1.request_llm(user_question)
    end = time.time()
    print(f'l1 - {end-start}')

def test2():
    start = time.time()
    l2.request_llm(user_question)
    end = time.time()
    print(f'l2 - {end-start}')

def test3():
    start = time.time()
    l2.request_llm(user_question)
    end = time.time()
    print(f'l3 - {end-start}')

t1 = threading.Thread(target=test1, daemon=True)
t2 = threading.Thread(target=test2, daemon=True)
t3 = threading.Thread(target=test3, daemon=True)
"""