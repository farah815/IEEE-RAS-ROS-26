t= int(input("please enter the number of test cases : "))

if (1 <= t <= 100) :
    for i in range(t):
     n=int(input())
     arr = [int(x) for x in input().split()]
     dominant=0
     index=0

     if len(arr) >= 3:
        if arr[0]==arr[1]:
           dominant = arr[0]
        else:
           dominant =arr[2]
     
      
  
    
     for i in range(len(arr)):
        if arr[i] != dominant:
           index=i+1
           print(index)
           break



          

