def analyze_grades(numbers):
    highest=max(numbers)
    lowest=min(numbers)
    average=sum(numbers)/len(numbers)
    return {
        "average": average,
        "highest": highest,
        "lowest": lowest
    }
result=analyze_grades([10,20,50,30,20,10])
print(result)