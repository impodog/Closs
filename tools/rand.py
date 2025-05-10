import random
def randgen(minlen=10,maxlen=20):
    result=str()
    is_first=True
    for i in range(random.randint(minlen,maxlen)):
        result+=chr(random.randint(48+is_first,57))
        is_first=False
    print(result)