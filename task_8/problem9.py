n= int(input("please enter the number of rooms :  "))
counter=0
if (1 <= n <= 100):
    for i in range(n):
      arr=input().split()
      arr=[int(x) for x in arr]
      p=arr[0]
      q=arr[1]
      if 0 <= p <= q <= 100:
         if q-p >= 2:
            counter+=1
    print(counter)   