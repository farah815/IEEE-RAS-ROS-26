t= int(input("please enter the number of test cases : "))

if (1 <= t <= 10**4) :
    for i in range(t):
      
      rating=int(input("please enter the rating : "))
      

      if (-5000 <= rating <= 5000 ):
         if 1900 <= rating:
            print("Division 1")

         elif 1600 <= rating <= 1899:
            print("Division 2")
       
         elif 1400 <= rating <= 1599:
            print("Division 3")

     
         else:
           print("Division 4")
         