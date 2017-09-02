import sys, crypt, string
# from itertools import chain, combinations_with_replacement

def main():
    if len(sys.argv) != 2:
        print("Usage: ./crack hash")
        exit(1)

    hashStr = sys.argv[1]
    salt = hashStr[:2]

    # pool = string.ascii_letters
    # for generatedPwd in chain.from_iterable(combination_repeatable(pool, size) for size in range(1, 5)):
    for generatedPwd in generateNewPass():
        print(generatedPwd)
        if hashStr == crypt.crypt(generatedPwd, salt):
            print(generatedPwd)
            exit(0)
    exit(1)

def generateNewPass():
   pool = string.ascii_letters
   poolLen = len(pool)
   size = 4
   indices = [-1] * size
   for i in range(size**poolLen):

       for j in reversed(range(size)):
           if all(x == poolLen-1 for x in indices[j:]):
               if j-1 >= 0 and indices[j-1] < poolLen-1:
                   indices[j:] = [0] * (size - j)
                   indices[size-1] = -1
                   indices[j-1] += 1
                   break

       indices[size-1] += 1
       password = ""
       for i in indices:
           if i >= 0:
               password += pool[i]
       yield password


#  def generateNewPass():
#      pool = string.ascii_letters
#      for size in range(1,5):
#          for password in combination_repeatable(pool, size):
#              yield password

def combination_repeatable(pool, size):
    indices = list(range(size))
    poolLen = len(pool)
    yield pool[:size]
    while True:
        for i in reversed(range(size)):
            if indices[i] < poolLen-1:
                break
        else:
            break

        indices[i] += 1
        indices[i+1:] = [0] * (size - 1 - i)

        yield ''.join(pool[i] for i in indices)

if __name__ == '__main__':
    main()


