t= int(input("please enter the number of test cases "))

if (1 <= t <= 10000):
    for i in range(t):

     n=int(input())
     if 1 <= n <= 50:
        arr=input().split()
        arr=[int(x) for x in arr]
        operations=max(arr)-min(arr)  
        print(operations)  



    
       
       
