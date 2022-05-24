def solution(array, commands):
    ls = []
    for i in commands:
        a = sorted(array[i[0]-1:i[1]])
        ls.append(a[i[2]-1])
    return ls