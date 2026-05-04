q= int(input("please enter the number of test cases : "))

if (1 <= q <= 1000) :
    for z in range(q):
     n= int(input("please enter the number of cues n : ")) 

     if 1<= n <=20:
         
      t= input("please enter the string you want to check : ")
      s= input("please enter the name : ")

      if len(s) != len(t):
       print("NO")
       continue

      final=[]
      ss=list(s)
      tt=list(t)

      for i in ss:
         for j in tt:
             if i==j :
                 final.append(i)
                 tt.remove(j)
                 break

      if len(final) == len(ss):
         print("YES")

      else :
         print("NO")  
         continue  

else:
    print("Invalid input")
     
