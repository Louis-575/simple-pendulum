import matplotlib; matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint


#Constants
g = 9.81       # gravity (m/s^2)
l = 1.0        # length (m)
theta_0 = [0.0, 1.0] # initial conditions (rad, rad s^-1)

#Constants for the animation
simTime = 20
timeSteps = 2000

#Equation of motion function, x contains both the angle and angular velocity.
# This returns the derivates of both parameters to the function
def equationOfMotion(x, t):
    theta, omega = x
    dtheta_dt = omega
    domega_dt = -g/l * np.sin(theta)
    return [dtheta_dt, domega_dt]

#Solving the equation using odeint
#----------------------------------
t = np.linspace(0, simTime, timeSteps) #Array of time-steps

#odeint expects the function to be f(x, t) for dx/dt
# and expects the outputs to be the derivatives of the inputs
solvedEquation = odeint(equationOfMotion, theta_0, t)

theta=solvedEquation[:,0] #Use the solved equation to find the values of theta

#Finding the cartesian coordinates of the end of the pendulum for the animation
x = l*np.sin(theta)
y= -l*np.cos(theta)

#Visualising the pendulum by both a graph and an animation
#---------------------------------------------------------
fig, (ax_anim, ax_plot) = plt.subplots(1, 2, figsize=(12, 5))

#Animation graph first

#Setting up axes and plot
ax_anim.set_xlim(-1.2*l, 1.2*l) #Uses the length of the pendulum so that it is always scaled correctly
ax_anim.set_ylim(-1.2*l, 0.2*l)
ax_anim.set_aspect('equal')
ax_anim.set_title("Pendulum Animation")

#Plotting a line with empty values of theta and t (we will animate later)
line, = ax_anim.plot([], [], 'o-', lw=3)

#Angle-time graph

#Setting up axes and plot
ax_plot.plot(t, theta, label="theta,(t)")
ax_plot.set_title("Pendulum Angle vs Time")
ax_plot.set_xlabel("Time (s)")
ax_plot.set_ylabel("$\\theta$, (rad)")
ax_plot.grid(True)

#Adding an animated time marker because why not (using empty values again)
time_marker, = ax_plot.plot([], [], 'ro')  # moving marker on plot

#Animating the plots
#--------------------

#Function to draw the animations of each frame
def update(frame):
    line.set_data([0, x[frame]], [0, y[frame]]) #Draws a line between (0,0) and the x and y positions of that frame

    time_marker.set_data([t[frame]], [theta[frame]])  # Draws a marker on the (t, theta) positon of that frame

    return line, time_marker

ani = FuncAnimation(fig, update, frames=len(t), interval= int(simTime * 1000 / timeSteps), blit=True) #Animates using the update function
# and runs the simulation in real time

plt.tight_layout()
plt.show()