
import sys

def findIndex(l, v, lowerBound):
    upper = len(l)-1
    lower = lowerBound

    if upper == -1:
        return lowerBound

    if l[-1] < v:
        return upper

    if l[lowerBound] > v:
        return lowerBound

    count = 0
    while count < len(l):
        count += 1
        if upper == lower:
            return upper
        pos = (upper + lower) // 2
        # print(lower,upper,pos,l[pos],v)
        assert pos > 0
        if l[pos] == v:
            return pos
        elif l[pos] > v:
            if l[pos-1] < v:
                ## best value
                return pos
            upper = pos

        elif l[pos] < v:
            ## we are too low, so increment
            lower = pos+1

    print("len",len(l),"count", count,"lower", lower,"pos=", pos,"upper=", upper,"l[lower]=", l[lower],
            "v=", v, "l[pos]=",l[pos], "l[upper]=", l[upper])
    assert False

def main(argv):
    s = int(argv[1])
    v = float(argv[2])
    if len(argv) > 3:
        lowerBound = int(argv[3])
    else:
        lowerBound = 0
    l = list(range(s))
    print(findIndex(l, v, lowerBound))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
