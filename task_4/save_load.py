import json
def save_inventory(data):
   with  open ("inventoryy.json","w") as file :
      json.dump(data,file)
      print("Inventory saved successfully!")

def load_inventory():
   try:
      with open ("inventoryy.json","r") as file :
         data = json.load(file)
         return data
      
   except FileNotFoundError :
      return {}
        
inventory = {"apple": 10, "banana": 5}

print(load_inventory())  

save_inventory(inventory)

print(load_inventory())             
