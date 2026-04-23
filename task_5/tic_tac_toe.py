import os 
import time
from colorama import Fore , Style , init

init(autoreset=True)



score = {
    "X" : 0 ,
    "O" : 0
}

def clear() :
    os.system('cls' if os.name=='nt' 
              else 'clear'
              )
    

def color(value):
    if value == "X":
        return Fore.RED + "X" + Style.RESET_ALL

    elif value == "O":
        return Fore.BLUE + "O" + Style.RESET_ALL

    return value

def display() : 
    clear()
    print(Fore.YELLOW +"\n TIC_TAC_TOE \n")
    print(" " + color(board[0]) + " | " + color(board[1]) + " | " + color(board[2]))
    print("---+---+---")
    print(" " + color(board[3]) + " | " + color(board[4]) + " | " + color(board[5]))
    print("---+---+---")
    print(" " + color(board[6]) + " | " + color(board[7]) + " | " + color(board[8]))

    
    time.sleep(0.2)
 
def display_score():
     print("\n🏆 Score:")
     print(Fore.RED + f"X = {score['X']}  " + Fore.BLUE + f"O = {score['O']}")
 

def check_winner():
    wins = [
   [0,1,2],
   [3,4,5],
   [6,7,8],
   [0,3,6],
   [1,4,7],
   [2,5,8],
   [0,4,8],
   [2,4,6]
        ] 
     
    for a,b,c in wins : 
          if board[a]==board[b]==board[c]:
              return board[a]
         
    return None 





while True :
   board =['1','2','3','4','5','6','7','8','9']
   while True:
       player1=input("player 1 please choose x or o :").upper()
       
   
       if player1 in ["X","O"]:
           break
    
       print("invalid choice!")


   if player1=="X":
       player2="O"
   else :
       player2="X" 
       

     
   current=player1   
   winner = None
   for turn in range(9):
    display()
    

    while True:
          move = input(f"Player {current}, choose position (1-9): ")

          if not move.isdigit():
                print("Enter a number!")
                continue
          
          move=int(move)-1

          if move<0 or move >8:
              print("INVALID POSITION!")
          elif board[move] in ["X","O"]:
              print("TAKEN!")
          else:
              break       
          
    board[move]=current
    winner = check_winner()
    if winner:
        display()
    
        print(Fore.GREEN + f"\n Player {winner} wins!")
        score[winner]+=1
        display_score()
        break
              
          
    if current == player1:
        current = player2
    
              
    elif current == player2:
        current = player1
       

   if not winner:
    display()        
    print(Fore.CYAN + "\n Draw!") 
    display_score()    
   again = input("\nPlay again? (y/n): ").lower()
   if again != "y":
    print("Thanks for playing!")    
    break
       

                
