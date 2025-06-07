from mistralai import Mistral
from config import API_KEY, AGENT_ID

import re
import json

RE_KOREAN = re.compile(r"^[ㄱ-ㅎㅏ-ㅣ]+$")
RE_HTML = re.compile(r"<[^>]+>")

MEANINGLESS_PATTERNS = {
    "ㄱㄱ",
    "ㄴㄴ",
    "ㅇㅇ",
    "ㅈㅈ",
    "ㅇㄹ",
    "ㄹㅇ",
    "ㅁㅊ",
    "ㅋㅋ",
    "ㅎㅎ",
    "ㅠㅠ",
    "ㅜㅜ",
    "ㄷㄷ",
    "ㅌㅌ",
    "ㅇㄷ",
    "ㅇㅈ",
}

BANNED_WORDS = {"fuck", "shit", "씨발", "병신", "좆", "개새", "nigger", "bitch"}


def _is_repeated_chars_only(token: str) -> bool:
    return len(set(token)) == 1 and len(token) > 1


def _is_meaningless(token: str) -> bool:
    return (
        RE_KOREAN.fullmatch(token)
        or _is_repeated_chars_only(token)
        or token in MEANINGLESS_PATTERNS
    )


def _contains_banned_word(text: str) -> bool:
    lowered = text.lower()
    return any(bad_word in lowered for bad_word in BANNED_WORDS)


def _contains_html(text: str) -> bool:
    return bool(RE_HTML.search(text))


def preprocess(text: str):
    ERRORCODE_NORMAL = 0
    ERRORCODE_INJECTION = 1
    ERRORCODE_ABNORMAL = 2

    text = text.strip()

    if len(text) < 2 or len(text) > 500:
        return False

    if _contains_banned_word(text) or _contains_html(text):
        return json.dumps(
            {"content": text, "predict_errorcode": ERRORCODE_INJECTION},
            ensure_ascii=False,  # 악의적 입력
        )

    tokens = text.split()
    if tokens and all(_is_meaningless(token) for token in tokens):
        return json.dumps(
            {"content": text, "predict_errorcode": ERRORCODE_ABNORMAL},
            ensure_ascii=False,  # 의미 없음
        )

    return json.dumps(
        {"content": text, "predict_errorcode": ERRORCODE_NORMAL},  # 정상 입력
        ensure_ascii=False,
    )


class LLMClient:
    def __init__(self, api_key, agent_id):
        self.client = Mistral(api_key=api_key)
        self.agent_id = agent_id

    def request(self, prompt: str) -> str:
        try:
            response = self.client.agents.complete(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "text"},
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[LLMClient] 오류 발생: {e}")
            return None


mistral_client = LLMClient(API_KEY, AGENT_ID[0])


def _extract_json_blocks(text):
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


def _parse_valid_json_blocks(blocks):
    valid_jsons = []
    for block in blocks:
        try:
            parsed = json.loads(block)
            valid_jsons.append(parsed)
        except json.JSONDecodeError:
            continue
    return valid_jsons


def postprocess(llm_string: str):
    """
    전체 후처리 파이프라인
    1. 문자열에서 JSON 블록 추출
    2. JSON 파싱 및 dict화
    3. error 코드에 따라 분류
    """
    blocks = _extract_json_blocks(llm_string)
    valid_json = _parse_valid_json_blocks(blocks)

    normal_items = [item for item in valid_json if item.get("error") == 0]
    injection_items = [item for item in valid_json if item.get("error") == 1]
    abnormal_items = [item for item in valid_json if item.get("error") == 2]

    return normal_items, injection_items, abnormal_items
