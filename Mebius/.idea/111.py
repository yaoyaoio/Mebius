#!/usr/bin/env python3
#coding:utf8
age = 22
counter = 0
#一共循环十次
for i in range(10):#range会把每次的值赋值给i
    print('循环第%s次'%i)
    print(counter)
    if counter<3:
        guess_num = int(input("input your guess num:"))
        if guess_num == age :
            print("Congratulations! you got it.")
            break  #不会执行后面的代码，直接跳出整个循环。
        elif guess_num>age:
            print(counter)
            print("Think smaller!")
        else:
            print(counter)
            print("Think bigger")
    else:
        print(counter)
        continue_confirm = input("do you want to continue because you are stupid:")
        if continue_confirm == 'y':
            counter = 0
        else:
            print("bye")
            break
    counter +=  1