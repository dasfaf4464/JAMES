import random
import string
import re
from config import NAME_ADJ, NAME_NOUN

def create_user_key():
    charset = list(string.ascii_lowercase)
    return ''.join(random.sample(charset,12))

def create_server_code():
    charset = list(string.ascii_uppercase + string.digits)
    first = ''.join(random.sample(charset, 4))
    second = ''.join(random.sample(charset, 4))
    third = ''.join(random.sample(charset, 4))
    return first + '-' + second + '-' + third

def check_server_code_format(code:str):
    pattern = r'^[A-Z]{4}-[A-Z]{4}-[A-Z]{4}$'
    return bool(re.match(pattern, code))

def create_user_name():
    adj = NAME_ADJ[random.randint(0, len(NAME_ADJ)-1)]
    noun = NAME_NOUN[random.randint(0, len(NAME_NOUN)-1)]
    return adj+' '+noun