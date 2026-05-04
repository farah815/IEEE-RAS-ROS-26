n = int(input("please enter the number of trams's stops : "))

if (2 <= n <= 1000):

    current = 0
    maximum = 0

    for i in range(n):
        arr = input().split()

        a = int(arr[0])   
        b = int(arr[1])   

        current -= a
        current += b

        if current > maximum:
            maximum = current

    print(maximum)
       
       
