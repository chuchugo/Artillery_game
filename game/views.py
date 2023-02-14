
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404,JsonResponse
from django.urls import reverse
#math module for calculating trajectory
import math, uuid
from django.core.exceptions import ObjectDoesNotExist

import json
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from game.forms import ShootForm
from game.models import Player, Game


def home(request):
    context = {}
    return render(request,'home.html',context)

def start_game(request):
    #use session to record the game state, which is the user to whom the game belongs
    context = {}
    # Retrieve the user's ID from the session id, or generate a new one if it doesn't exist
    #get a player player_id=session_key, which may does not exist
    player_id = request.session.session_key
    player, created = Player.objects.get_or_create(player_id=player_id)
    
    #assign new game to the player
    #condition 1: if the player is already in a game which is not end, then return the game
    #condition 2: if there's game waiting for a player, find a game that is waiting for a player
    #condition 3: if there is no game waiting for a player, then create a new game and assign it to the player
    game = None
    try:
        #condition 1 
        player1_games = player.player1.filter(winner=None)
        player2_games = player.player2.filter(winner=None)
        if player1_games.exists() and player1_games.count()>0:
            game = player1_games[0]
        elif player2_games.exists() and player2_games.count()>0:
            game = player2_games[0]
        else:
            #create a new game, assign shooter
            game = Game(player1=player,current_shooter = player)
            game.save()
    except ObjectDoesNotExist:
        print("object does not exist for player ",player_id)

    #the game is decided. then check if we need to wait for another player
    if game.player2 is None or game.player1 is None:
        #wait for another player
        context['wait'] = True
        context['game_id'] = game.id
    else:
        #start the game
        context['wait'] = False
        context['game_id'] = game.id
        #assign the current shooter
        if game.current_shooter is None:
            game.current_shooter = game.player1
            game.save()
    #add info to context
    if game.player1 is not None:
        context['player1'] = game.player1.player_id
    if game.player2 is not None:
        context['player2'] = game.player2.player_id
        #assign the cannon
        # if game.player1 == player:
        #     context['cannon'] = 1
        # else:
        #     context['cannon'] = 2
    return JsonResponse(data=context)

#when this user is the shooter, then return the form
def get_form(request):
    context = {}
    wind_speed = get_wind_speed_to_ground()
    context['wind_speed'] = wind_speed
    #shooter
    player_id = request.session.session_key
    player = Player.objects.get(player_id=player_id)
    game = get_game_by_player(player)
    if game.current_shooter.player_id == player_id:
        context['shooter'] = 'Me'
        context['form'] = ShootForm()
    else:
        context['shooter'] = 'Opponent'
    return render(request,'shoot-form.html',context)

#helper function for getting the current game by player, not history games
#didnt check if the player must have current game
def get_game_by_player(player):
    try:
        game = Game.objects.get(player1=player, winner=None)
    except Game.DoesNotExist:
        try:
            game = Game.objects.get(player2=player, winner=None)
        except Game.DoesNotExist:
            game = None
    return game

#dt is the time interval between each point 
def get_trajectory_data(request):
    cannon,angle_to_cannon,velocity_to_cannon,wind_speed,dt = \
        2,45,500,0,0.1
    x = calculate_trajectory(cannon,angle_to_cannon,velocity_to_cannon,wind_speed,dt)
    return x 

#helper function for calculating trajectory points 
#from the given angle and velocity
#angle is between 0 and 90 degrees
#velocity is between 0 and 100

def calculate_trajectory(cannon,angle_to_cannon,velocity_to_cannon,wind_speed,dt):
    #constants
    field = [2000,1000]
    cannon1_initial_positon = [500,0]
    cannon2_initial_positon = [1500,0]
    ball_diameter = 0.1 #meters
    ball_radius = ball_diameter/2
    ball_mass = 1 #kg
    air_density = 1 #kg/m^3

 
    field = [2000,1000]
    trajectory = []
    #get angle to ground
    angle_to_ground = 0
    if cannon == 2:
        angle_to_ground = 180 - angle_to_cannon
    else:
        angle_to_ground = angle_to_cannon
    #timestamp
    t  = 0
    #calculate the trajectory points
    #1. prepare all the variables
    # velocity to ground at time t
    Vt = [0,0]
    #velocity compared to wind
    Va_t_minus_1 = [0,0]
    #[Vx,Vy] = [V*cos(angle),V*sin(angle)]
    Vt_minus_1 = [velocity_to_cannon * math.cos(angle_to_ground/180 * math.pi),\
        velocity_to_cannon * math.sin(angle_to_ground/180 * math.pi)]
    #wind speed vector
    Vw =[wind_speed,0]
    
    #gravity
    G = [0 , -10 * ball_mass]
    #drag force
    Fd_t_minus_1 = [0,0]
    #total force = drag force + gravity
    F_t_minus_1 = [0,0]

    #position at time t
    Pt = []
    print(Pt)
    if cannon == 1:
        print("cannon1", cannon1_initial_positon)
        Pt = cannon1_initial_positon
    elif cannon == 2:
        print("cannon2")
        Pt = cannon2_initial_positon
    #velocity at time t-1
    Pt_minus_1 = Pt
    print(Pt)
    print({'t':t,'x':Pt[0],'y':Pt[1]})

    print("debug2")
    #2. calculate the trajectory points until the ball hits the ground
    while Pt[1] >= 0:
        #For x axis, y axis
        for axis in [0,1]:
            #velocity compared to wind
            Va_t_minus_1[axis] = Vt_minus_1[axis] - Vw[axis]
            #drag force F_drag = 0.5 * C_d * A * air_density * v^2
            # where:
            # F_drag is the drag force.
            # C_d is the drag coefficient, which is around 0.47 for a spherical object.
            # A is the cross-sectional area of the ball.
            # ρ is the air density.
            # v is the velocity of the ball.
            C_d = 0.47
            A = math.pi * ball_radius * ball_radius 
            k = 0.5  * C_d * A * air_density 
            
            #calculate f drag 
            if Va_t_minus_1[axis] == 0:
                Fd_t_minus_1[axis] = 0
            else:
                Fd_t_minus_1[axis] = - Va_t_minus_1[axis] *Va_t_minus_1[axis] * k * \
                    (Va_t_minus_1[axis] / abs(Va_t_minus_1[axis])) # is for direction of drag force
            
            #calculate total force on the ball
            F_t_minus_1[axis] = G[axis] + Fd_t_minus_1[axis]
            #calculate the velocity at time t
            Vt[axis] = Vt_minus_1[axis] + F_t_minus_1[axis]/ball_mass * dt
            #calculate the position at time t
            Pt[axis] = Pt_minus_1[axis] + Vt_minus_1[axis] * dt + 0.5 * F_t_minus_1[axis]/ball_mass * dt * dt
            #update the velocity and position for next iteration
            Vt_minus_1[axis] = Vt[axis]
            Pt_minus_1[axis] = Pt[axis]
        #update the trajectory
        trajectory.append({'t':t,'x':Pt[0],'y':Pt[1]})
        t += dt
        
    return JsonResponse(trajectory,safe=False)
    

#get wind speed with direction, positive is to the right, negative is to the left
def get_wind_speed_to_ground():
    #get random wind speed and direction using random module
    speed = random.random()*15 + 5
    direction = random.choice([-1, 1]) #0 or 1
    return speed

    return wind_speed,wind_direction
# def get_trajectory_data(request):
#     # Calculate the trajectory data
#     data = {
#         0: {'x':10,'y':10},
#         1: {'x':100,'y':100},
#         2: {'x':20,'y':20},
#         # ...
#     }
#     return JsonResponse(data)