def write_log(message) :
    with open ("log1.txt","a") as file :
       
       file.write(message + "\n")

def  read_logs() :
    try:
        with open("log1.txt","r") as file :
            for line in file :
                print(line.strip())

    except FileNotFoundError as e:
        print("cannot find file :",e)  

read_logs()
write_log("Hello")
write_log("world")
read_logs()