import random
def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)
    return f[i][:-1]

print(repr(randomWord()))
