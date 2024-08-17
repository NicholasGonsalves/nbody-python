from typing import List
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dataclasses import dataclass

G = 6.67430 * (10**-11)
dt = 60 * 60 * 24  # Time step: 1 day


@dataclass
class Body:
    x: float
    y: float
    mass: int
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


def update(_frame, bodies, scat):
    simulate(bodies)
    scat.set_offsets([(body.x, body.y) for body in bodies])
    return (scat,)


if __name__ == "__main__":

    bodies = [
        Body(0, 0, 1.989 * 10**30, 0, 0),  # Sun
        Body(57.9e9, 0, 3.285 * 10**23, 0, 47.87e3),  # Mercury
        Body(108.2e9, 0, 4.867 * 10**24, 0, 35.02e3),  # Venus
        Body(149.6e9, 0, 5.972 * 10**24, 0, 29.78e3),  # Earth
        Body(227.9e9, 0, 6.39 * 10**23, 0, 24.07e3),  # Mars
    ]

    fig, ax = plt.subplots()
    ax.set_xlim(-3e11, 3e11)
    ax.set_ylim(-3e11, 3e11)
    ax.grid()

    scat = ax.scatter([body.x for body in bodies], [body.y for body in bodies], s=5)

    ani = FuncAnimation(
        fig, update, fargs=(bodies, scat), frames=1000, interval=1, blit=False
    )
    plt.show()
