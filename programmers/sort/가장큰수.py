def solution(numbers):
    ls = list(map(str,numbers))
    ls.sort(key=lambda x: x*3, reverse = True)
    answer = str(int(''.join(ls))) # 인수값이 [0,0,0,0] 일 때 "0000" 이 아닌 "0"이 나오게 해줘야 하기 때문
    return answer