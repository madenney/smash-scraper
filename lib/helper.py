

def removeCommas(s):
    while "," in s:
        s = s[:s.index(",")] + s[s.index(",")+1:]
    return s