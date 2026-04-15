import platform
import datetime

def log_system_info() :
    os_type=platform.system()

    currentdate=datetime.datetime.now()

    with open ("sys_log.txt","a") as file :
        file.write(f"os_type : {os_type} \n")
        file.write(f"current date : {currentdate} \n")

def main():
    log_system_info()
    print("System information logged successfully.")

if __name__ == "__main__" : 
    main()



