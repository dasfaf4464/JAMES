"""
Mistral Agent와 연결되어 내용을 주고받는 클래스입니다.
agent는 총 네 개 입니다.
LLMManager의 인트턴스는 agent와 1:1로 대응됩니다.
"""

from mistralai import Mistral
from config import API_KEY, AGENT_ID
from app.manager.db_manager import mariadb_admin_manager
import re
import json

"""
부정 사용및 입력 전처리 함수
"""
RE_KOREAN = re.compile(r"^[ㄱ-하-ㅣ]+$")

MEANINGLESS_KOR_PATTERNS = {
    "ㄱㄱ",
    "ㄴㄴ",
    "ㅇㅇ",
    "ㅈㅈ",
    "ㅇㄹ",
    "ㄹㅇ",
    "ㅁㅊ",
    "ㅅㅂ",
    "ㅈㅂ",
    "ㅋㅋ",
    "ㅎㅎ",
    "ㅠㅠ",
    "ㅜㅜ",
    "ㄷㄷ",
    "ㅌㅌ",
    "ㅇㄷ",
    "ㅇㅈ",
    "ㅇㅉ",
    "ㄹㅈㄷ",
}


def is_token_meaningless(token):
    token = token.strip()
    if len(set(token)) == 1 and len(token) > 1:
        return True
    if RE_KOREAN.fullmatch(token):
        return True
    return False


def is_fully_meaningless_string(text):
    tokens = text.strip().split()
    if not tokens:
        return False
    for token in tokens:
        if not is_token_meaningless(token):
            return False
    if token in MEANINGLESS_KOR_PATTERNS:
        return True
    return False


"""
형식 검증 및 파이썬 데이터화 함수
"""


def extract_json_blocks(text):
    stack = []
    blocks = []
    start_idx = None

    for i, ch in enumerate(text):
        if ch == "{":
            if not stack:  # 새 JSON 블록의 시작
                start_idx = i
            stack.append("{")
        elif ch == "}":
            if stack:
                stack.pop()
                if not stack and start_idx is not None:
                    block = text[start_idx : i + 1]
                    blocks.append(block)
                    start_idx = None

    return blocks


def parse_valid_json_blocks(blocks):
    valid_jsons = []
    for block in blocks:
        try:
            parsed = json.loads(block)
            valid_jsons.append(parsed)
        except json.JSONDecodeError:
            continue
    return valid_jsons


ERRORCODE_NORMAL = 0
ERRORCODE_INJECTION = 1
ERRORCODE_ABNORMAL = 2


class LLMManager:
    api_key = API_KEY

    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.client = Mistral(api_key=self.api_key)

    def _preprocess(self, user_input: str):
        """
        사용자 입력 전처리기 입니다.
        1. 사용자의 입력이 너무 짧거나 너무 긴 경우 -> False
        2. 의미없는 문자가 나열될 때 -> errorcode = 2
        3. 정상 입력인 경우 error_code = 0
        """
        if len(user_input) < 2 or len(user_input) > 500:
            print(len(user_input))
            return False
        if is_fully_meaningless_string(user_input):
            return ERRORCODE_ABNORMAL
        return ERRORCODE_NORMAL

    def _postprocess(self, llm_string):
        """
        llm에서 반환받은 문자열 후처리기입니다.
        1. 문자열에서 JSON을 찾아냅니다.
        2. JSON의 형식이 일치하지 않는 경우 오류
        3. JSON의 내용이 비정상인 경우 오류
        4. 정상 결과인 경우 사용자에게 전달합니다.
        """
        blocks = extract_json_blocks(llm_string)
        valid_json = parse_valid_json_blocks(blocks)

        noraml_items = [item for item in valid_json if item["error"] == 0]
        injection_items = [item for item in valid_json if item["error"] == 1]
        abnormal_items = [item for item in valid_json if item["error"] == 2]
        return noraml_items, injection_items, abnormal_items

    def _request_llm(self, user_key: str, session_code: str, prompt: str):
        predict_error = self._preprocess(prompt)
        if predict_error is not False:
            request_prompt = (
                f'{{"content": "{prompt}", "predict_errorcode": {predict_error}}}'
            )
        else:
            return False

        try:
            agent_response = self.client.agents.complete(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": request_prompt}],
                response_format={"type": "text"},
            )
            response_prompt = agent_response.choices[0].message.content
            llm_json = self._postprocess(response_prompt)
            llm_keys = []
            for llm_list in llm_json:
                for llm_result in llm_list:
                    mariadb_admin_manager.insert(
                        "fromllm",
                        {
                            "user_key": user_key,
                            "llm": llm_result.get("content"),
                            "original": prompt,
                            "main": llm_result.get("category").get("main"),
                            "sub": llm_result.get("category").get("sub"),
                            "minor": llm_result.get("category").get("minor"),
                            "error": llm_result.get("error"),
                            "session": session_code,
                        },
                    )

            latest_llm = mariadb_admin_manager.put_sql_result(
                "SELECT * FROM fromllm WHERE session = %s AND user_key = %s ORDER BY `key` DESC LIMIT %s",
                (session_code, user_key, 3),
            )

            client_data = [
                {
                    "key": row["key"],
                    "llm": row["llm"],
                    "category": {
                        "main": row["main"],
                        "sub": row["sub"],
                        "minor": row["minor"],
                    },
                }
                for row in latest_llm
            ]

            print(client_data)

            return llm_json
        except Exception as e:
            print(f"오류 발생: {e}")


llmManager = [
    LLMManager(AGENT_ID[0]),
    LLMManager(AGENT_ID[1]),
    LLMManager(AGENT_ID[2]),
    LLMManager(AGENT_ID[3]),
]
