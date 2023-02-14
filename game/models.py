from django.db import models



 
class Player(models.Model):
    #unique id for each player
    player_id = models.CharField(max_length=100,unique=True)

class Game(models.Model):
    #player1
    player1 = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='player1',null=True)
    #player2
    player2 = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='player2', null=True)
    #current shooter
    current_shooter = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='current_shooter', null=True)
    #winner
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, related_name='winner', null=True)