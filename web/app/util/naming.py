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