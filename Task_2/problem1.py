number = float (input("please enter a number"))
numbers = []


while number != -1 :
    numbers.append(number)
    number = float(input("please enter a number"))

if len(numbers) == 0 :
    print ("the array is empty")

elif len(numbers) == 1 :
    print ("the array has only one element which is ",numbers[0])

else:
    max1_value = numbers[0]
    min1_value = numbers[0]
    max2_value=numbers[0]
    min2_value = numbers[0]

    for i in range (1,len(numbers)) :
     if numbers[i] > max1_value :
       max1_value=numbers[i]
     elif numbers[i]<min1_value :
         min1_value=numbers[i]


max2_value=max(numbers)
min2_value=min(numbers)

print("the max is",max1_value,"and the min is",min1_value)
print("the max is",max2_value,"and the min is",min2_value)

