def safe_divide() :
      
     try:
         a= int (input("please enter the first number : "))  
         b= int (input("please enter the second number : "))
         result = a / b
         print("Result =", result)
     
     except ValueError as msg:
          print("valueerror: ",msg) 

     except ZeroDivisionError as msg:
          print("ZeroDivisionError: ",msg)      
safe_divide()          