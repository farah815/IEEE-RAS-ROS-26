n= int(input("please enter the number of lines : "))

if (1 <= n <= 100) :
    for i in range(n):
       arr=input("please enter the word : ")
       arr1= list(arr)
       if len(arr1)>10:
           print(arr1[0]+str(len(arr1)-2) +arr1[len(arr1) - 1])
       else:
           print(arr)
             

       
        
    
    
    


          