# neocis take home project --- artillery game



### choice of frame work

#### Installments 

#### choice of front end

"what are good choices for django front end for showing ball trajectories"

HTML5 Canvas: 

Three.js:

etc





Draw balls moving

```
  var radius = 10;
            var time = 0;
            const fps = 30;
       

         for (var timestamp in data) {   
            var canvas = document.getElementById('trajectory-canvas');
            var ctx = canvas.getContext('2d');
            var position = data[timestamp];
            //draw background
            ctx.filldStyle = "yellow";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            // Draw a line segment from the previous position to the current position
            ctx.filldStyle = "red";
            ctx.fillRect(position.x, position.y, radius, 2 * Math.PI, 2 * Math.PI);
            console.log(position.x, position.y);   
```



#### choice of backend

django





Html canvas

key concepts

```
fps frame per second
bx,by: position per frame
velovity per frame

```



## Code model designs

#### calculation of movement

**seperate all force, speed, acclerate vector into x axis and y axis.**

**get initial speed**

the total force on the ball = G + F_drag

**To calculate the air resistance on a ball, you can use the drag equation:**

F_drag = 0.5 * C_d * A * ρ * v^2

where:

- F_drag is the drag force.
- C_d is the drag coefficient, which is around 0.47 for a spherical object.
- A is the cross-sectional area of the ball.. Cross-sectional area refers to the area of a cross-section of the object that is perpendicular to its motion. 
- ρ is the air density.
- v is the velocity of the ball.

C_d= 4.07

A = A = π * r^2

ρ = 1kg/m^3

m = 1kg

Ac_drag = f_drag / m 

**get overall acceleration = A_drag + A_gravity**

using discrete dt to calculate dt+1



#### session management for dif users

https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Sessions#using_sessions

https://docs.djangoproject.com/en/4.1/topics/http/sessions/

```

```



#### web socket for real time update

```

```



