import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

# Create a figure and axis with black background (space theme)
fig, ax = plt.subplots(facecolor="black")
fig.canvas.manager.set_window_title("PyTellurion")
ax.set_facecolor("black")

# Define angular positions for circular motion (0 to 2π radians)
theta = np.linspace(0, 2*np.pi, 1000)         # For Earth's orbit around the Sun
theta_moon = 12 * theta                       # Moon goes around faster (scaled ×12)

# Parametric equations for Earth's circular orbit (centered at Sun at (80,80))
x_orbit = (2 * np.cos(theta)*50) + 80
y_orbit = (np.sin(theta)*50) + 80

# Plot Sun, Earth, Moon, and their orbits
scat_sun_fake = ax.scatter(80, 80, s=100, color="orange", label="The Sun")  
# ^ Fake Sun only for legend (real Sun drawn with concentric glowing circles)

scat_earth = ax.scatter(x_orbit[0], y_orbit[0], label="The Earth", s=100, color="#3266a8")  
# ^ Earth at initial position

scat_moon = ax.scatter(x_orbit[0]+5, y_orbit[0], label="The Moon", s=25, color='gray')     
# ^ Moon starts next to Earth

orbit_earth = ax.plot(x_orbit, y_orbit, color="#3266a8", linewidth=1, linestyle="--", label="Earth's Orbit")  
# ^ Dashed line showing Earth's orbit path

orbit_moon = ax.plot(x_orbit[0]+5, y_orbit[0], label="Moon's Orbit", color="gray")[0]      
# ^ Dynamic line for Moon's orbit (updated per frame)

# Sun's position
x_sun, y_sun = 80, 80

# Draw concentric circles around Sun to simulate a glowing effect
colors = ['#ff8000', '#f78c22ff', '#f89838ff']  # Shades of orange/yellow
radii = [10, 20, 30]                            # Increasing radii for glow

for radius, color in zip(radii[::-1], colors[::-1]):  
    circle = plt.Circle((x_sun, y_sun), radius, color=color, zorder=10)
    ax.add_patch(circle)

# Store orbital path data of Earth & Moon (for eclipse calculations later)
x_orbit_moon_values = []
y_orbit_moon_values = []

# Function that updates Earth & Moon positions for each animation frame
def animate(frame):
    # Earth position along its orbit
    x_earth = x_orbit[frame]
    y_earth = y_orbit[frame]
    data_earth = np.array([x_earth, y_earth]).T
    scat_earth.set_offsets(data_earth)

    # Moon position orbiting around Earth
    x_moon = np.cos(theta_moon[frame]) * 15 + x_earth
    y_moon = np.sin(theta_moon[frame]) * 15 + y_earth
    data_moon = np.array([x_moon, y_moon]).T
    scat_moon.set_offsets(data_moon)
    
    # Update Moon's orbital path (growing line)
    x_orbit_moon_values.append(x_moon)
    y_orbit_moon_values.append(y_moon)
    orbit_moon.set_xdata(x_orbit_moon_values)
    orbit_moon.set_ydata(y_orbit_moon_values)    
    return orbit_moon


# Run the animation (1000 frames, fast interval)
ani = animation.FuncAnimation(fig=fig, func=animate, frames=1000, interval=1)

# Set viewing window (zoom level of space)
ax.set_xlim(-40, 200)
ax.set_ylim(10, 220)
ax.set_aspect('equal')          # Equal scaling on x & y axes
ax.set_title("PyTellurion")        # Title of visualization
fig.set_label("PyTellurion")
plt.legend(loc="upper right")   # Legend in top-right
plt.show()
