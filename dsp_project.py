import random

def lotto_all_sum(lotto):
    sum = 0
    for i in lotto:
        sum=sum+i
    return sum

def lotto_find_odd(lotto):
    count=0
    for i in lotto:
        if(i%2!=0):
            count+=1
    return count

col_count=0

while(col_count<10):
    lotto=[]
    row_count=0
    while(row_count<6):
        ball=random.randint(1,45)
        if(ball not in lotto):
            lotto.append(ball)
            row_count+=1

    lotto_sum=lotto_all_sum(lotto)
    odd_num=lotto_find_odd(lotto)

    if(lotto_sum>=81 and lotto_sum<=200 and odd_num>=2 and odd_num<=4):
        for i in range(0, 6, 1):
            print('{0:<3d}'.format(lotto[i]), end='')
        print('{0:s} {1:<3d} {2:s} {3:d} {4:s} {5:d} {6:s}'.format(':', lotto_sum, '[', odd_num, ':', 6-odd_num, ']'))
        col_count += 1
