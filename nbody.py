from typing import List
from dataclasses import dataclass
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

G = 6.67430 * (10**-11)
dt = 60 * 60 * 24  # Time step: 1 day


@dataclass
class Body:
    x: float
    y: float
    mass: float
    vx: float
    vy: float
    ax: float = 0
    ay: float = 0

    def update_acceleration(self, bodies: List["Body"]):
        self.ax, self.ay = 0, 0
        for other in bodies:
            if other is not self:
                dx = other.x - self.x
                dy = other.y - self.y
                dist_sq = dx**2 + dy**2
                force = G * other.mass / dist_sq
                distance = dist_sq**0.5
                self.ax += force * dx / distance
                self.ay += force * dy / distance

    def update_velocity(self):
        self.vx += self.ax * dt
        self.vy += self.ay * dt

    def update_position(self):
        self.x += self.vx * dt + 0.5 * self.ax * dt**2
        self.y += self.vy * dt + 0.5 * self.ay * dt**2


def simulate(bodies):
    for body in bodies:
        body.update_acceleration(bodies)
    for body in bodies:
        body.update_position()
        body.update_velocity()

def draw_body(body):
    glBegin(GL_POINTS)
    glVertex2f(body.x / 1e11, body.y / 1e11)  # Scale down for visibility
    glEnd()

def render(bodies):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluOrtho2D(-3, 3, -3, 3)  # Set the coordinate system, scaling for visibility
    for body in bodies:
        draw_body(body)
    pygame.display.flip()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glPointSize(5)  # Set the size of the points

    bodies = [
        Body(0, 0, 1.989 * 10**30, 0, 0),  # Sun
        Body(57.9e9, 0, 3.285 * 10**23, 0, 47.87e3),  # Mercury
        Body(108.2e9, 0, 4.867 * 10**24, 0, 35.02e3),  # Venus
        Body(149.6e9, 0, 5.972 * 10**24, 0, 29.78e3),  # Earth
        Body(227.9e9, 0, 6.39 * 10**23, 0, 24.07e3),  # Mars
    ]

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        simulate(bodies)
        render(bodies)
        clock.tick(144)  # Limit to 144 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
