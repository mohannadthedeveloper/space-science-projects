import pygame as py
import math
import numpy as np
import random

py.init()
WIDTH, HEIGHT = 1000, 800
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Galactic Spin")
clock = py.time.Clock()
font = py.font.SysFont(None, 22)

# --- Parameters ---
num_particles = 1500
max_radius = 320
num_arms = 4
rotation_speed = 0.004  # controls galactic spin

# --- Particle generation ---
# Strong bias toward center, and ensure actual 0-radius stars exist
radii = np.random.power(5.0, size=num_particles) * max_radius
radii *= np.random.uniform(0.0, 1.0, size=num_particles)  # adds some true near-0 values

# sprinkle a few exact core stars
for i in range(20):
    radii[i] = random.uniform(0, 2)

base_angles = np.random.uniform(0, 2 * math.pi, num_particles)
arm_indices = np.random.randint(0, num_arms, num_particles)
arm_offsets = (2 * math.pi / num_arms) * arm_indices
spiral_twist = (radii / max_radius) * 3.5
angles = base_angles + arm_offsets + spiral_twist

colors = [  # randomizes colors for the stars
    (random.randint(180, 255), random.randint(180, 255), random.randint(200, 255))
    for _ in range(num_particles)
]

# --- Halo settings ---
halo_on = False
cx, cy = WIDTH // 2, HEIGHT // 2

# --- Main loop ---
t = 0
run = True
while run:
    dt = clock.tick(60) / 1000
    t += dt

    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        elif event.type == py.KEYDOWN:
            if event.key == py.K_h:
                halo_on = not halo_on

    # --- Update galaxy rotation ---
    angular_velocity = rotation_speed * (1.5 - radii / max_radius)
    angles += angular_velocity

    # --- Background ---
    screen.fill((6, 6, 20))

    if halo_on:
        halo_surface = py.Surface((WIDTH, HEIGHT), py.SRCALPHA)

        # multiple layers for smooth fade
        for i in range(8):
            alpha = 175 - i * 10
            radius = 175 + i * 25
            color = (80, 40, 100, alpha)
            py.draw.circle(halo_surface, color, (cx, cy), radius)

        screen.blit(halo_surface, (0, 0))

    # --- Draw spinning galaxy ---
    x = cx + radii * np.cos(angles)
    y = cy + radii * np.sin(angles)
    for i in range(num_particles):
        brightness = max(40, 255 - int(radii[i] * 0.5))
        col = tuple(min(255, int(c * (brightness / 255))) for c in colors[i])
        py.draw.circle(screen, col, (int(x[i]), int(y[i])), 2)

    # --- Central bulge (reduced size to match clumping) ---
    py.draw.circle(screen, (255, 255, 200), (cx, cy), 8)

    # --- Text info ---
    label1 = font.render(
        f"Dark Matter Halo: {'ON' if halo_on else 'OFF'}   (press H to toggle)",
        True,
        (220, 220, 255)
    )
    screen.blit(label1, (20, 20))

    py.display.flip()

py.quit()
