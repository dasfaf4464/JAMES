import random
import string
from config import NAME_ADJ, NAME_NOUN

def create_user_key():
    charset = list(string.ascii_lowercase)
    return ''.join(random.sample(charset,10))

def create_server_code():
    charset = list(string.ascii_uppercase + string.digits)
    first = ''.join(random.sample(charset, 4))
    second = ''.join(random.sample(charset, 4))
    third = ''.join(random.sample(charset, 4))
    return first + '-' + second + '-' + third

def check_server_code_format(code):
    codelist = list(code)
    if (len(code) != 14) or any(codelist[i] != '-' for i in [4, 9]):
        return False
    else:
        for alphabet in codelist[0:4] + codelist[5:9] + codelist[10:14]:
            if alphabet not in string.ascii_uppercase:
                return False
    return True

def create_user_name():
    adj = NAME_ADJ[random.randint(0, len(NAME_ADJ)-1)]
    noun = NAME_NOUN[random.randint(0, len(NAME_NOUN)-1)]
    return adj+noun
