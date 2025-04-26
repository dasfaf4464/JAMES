import random
import string

def randomName():
    first = ''
    last = ''
    return first + ' ' + last

def randomUserKey():
    charset = list(string.ascii_lowercase)
    return ''.join(random.sample(charset,10))

def randomServerCode():
    charset = list(string.ascii_uppercase + string.digits)
    first = ''.join(random.sample(charset, 4))
    second = ''.join(random.sample(charset, 4))
    third = ''.join(random.sample(charset, 4))
    return first + '-' + second + '-' + third

def checkServerCodeFormat(code):
    codelist = list(code)
    if (len(code) != 14) or any(codelist[i] != '-' for i in [4, 9]):
        return False
    else:
        for alphabet in codelist[0:4] + codelist[5:9] + codelist[10:14]:
            if alphabet not in string.ascii_uppercase:
                return False
    return True