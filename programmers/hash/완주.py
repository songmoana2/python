def solution(participant, completion):
    	check = {}
	for x in participant:
		check[x] = check.get(x,0) + 1
	for x in completion:
		check[x] = check.get(x,0) - 1

	for x in check:
	    if check[x] > 0 :
	        return x