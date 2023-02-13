
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404,JsonResponse
from django.urls import reverse
#math module for calculating trajectory
import math 

from django.core.exceptions import ObjectDoesNotExist

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone



# Create your views here.
def home(request):
    context = {}
    return render(request,'home.html',context)

def register(request):
    context = {}
    return render(request,'register.html',context)

def login(request):
    context = {}
    return render(request,'login.html',context)

def logout(request):
    context = {}
    return render(request,'logout.html',context)

#helper function for calculating trajectory points 
#from the given angle and velocity
#angle is between 0 and 90 degrees
#velocity is between 0 and 100

#dt is the time interval between each point 
def get_trajectory_data(request):
    cannon,angle_to_cannon,velocity_to_cannon,wind_speed,dt = \
        1,45,500,0,0.1
    x = calculate_trajectory(cannon,angle_to_cannon,velocity_to_cannon,wind_speed,dt)
    
    return x 
def calculate_trajectory(cannon,angle_to_cannon,velocity_to_cannon,wind_speed,dt):
    #constants
    field = [2000,1000]
    cannon1_initial_positon = [500,0]
    cannon2_initial_positon = [1500,1000]
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