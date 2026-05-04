n= int(input("please enter the number of test cases : "))
counter=0
if (1 <= n <= 1000) :
    
     for i in range(n):
          arr=input().split()
          total=0

          for j in range(3):    
           number=int(arr[j])
           if number==1:
               total += 1
          if total>1:
               counter+=1
                 
print(counter)               

          
          

          
         
