n= int(input("please enter the number of test cases : "))

if (1 <= n <= 9261) :
    for i in range(n):
      maximum=0
      a=int(input("please enter first number : "))
      b=int(input("please enter second number : "))
      c=int(input("please enter third number : "))

      if (0 <= a <= 20 and 0 <= b <= 20 and 0 <= c <= 20):
       
         maximum=max(a,b,c)

         if (a + b == c) or (a + c == b) or (b + c == a):
            print("YES")

         else:
           print("NO")
     
        
                   
              
              
  
             