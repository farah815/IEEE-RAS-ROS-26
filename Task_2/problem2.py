number = int(input("please enter a number"))
total =0
if number < 0 :
   print("sorry cannot perform on negative data")
elif number == 0 :
  print ("the sum of numbers is" , total)
elif number%2==0:
   while number > 0 :
      total=total+number
      number=number-2
   print ("the sum of numbers is" , total)
else :
     number=number-1
     while number > 0 :
      total=total+number
      number=number-2
     print ("the sum of numbers is" , total)
