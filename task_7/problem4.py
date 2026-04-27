class Player:
    def __init__(self,name,score):
        self.name=name
        self.score=score

class Team:
    def __init__(self):
        self.members=[]

    def add_player(self,player_obj):
        self.members.append(player_obj)

p1 = Player("Ali", 10)
p2 = Player("Sara", 15)
p3 = Player("Omar", 20)

team = Team()

team.add_player(p1)
team.add_player(p2)
team.add_player(p3)


for player in team.members:
    print(player.name, player.score)