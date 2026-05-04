s = input("please enter the string ")

if (1 <= len(s) <= 200):

    i = 0

    while i+1 < len(s):

        if s[i] == ".":
            print(0, end="")
            i += 1

        else:  
            if s[i + 1] == ".":
                print(1, end="")
            else:
                print(2, end="")
            i += 2