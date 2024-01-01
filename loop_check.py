import sys
from snake import Position

def loop_check(elems:list[Position], index):
    start = elems[index]
    loop = [start]
    found = False

    for i in range(index-1, 0, -1):
        if elems[i] == start:
            found = True
            break
        loop.append(elems[i])

    if not found:
        return False

    for i in range(index, index - len(loop), -1):
        if elems[i] != elems[i-len(loop)]:
            return False
    return True

if __name__ == '__main__':
    elems = [Position(1,2), Position(1,3), Position(1,4), Position(1,3), Position(1,4)]
    index = int(sys.argv[1])
    print(loop_check(elems, index))