import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000 # change to units for debris
    G = 6.67438e-11
    SCALE = 200 / AU   #scale of planets in the window [800*800], 1AU = 100 pixels aprox.
    TIMESTEP = 3600*24 # 1 sec to 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = False
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2   # to place the planets at the centre of the window
        y = self.y * self.SCALE + HEIGHT / 2   # ""

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x,y), self.radius)
        if not self.sun:

            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    def attraction(self, other):      # defines the force of attraction between current object and other object
        other_x, other_y = other.x, other.y  #   define other object
        distance_x = other_x - self.x   # distance between current object and other object
        distance_y = other_y - self.y   # ""
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance   # when the other obkect we calculate the distance to is the sun, update the distance to sun

        force = self.G * self.mass * other.mass / distance ** 2  # force of gravity
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:   # to not calculate the force with ourself
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP  # increasing the vel by timestep
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run =  True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, BLUE, 1.98892*10**30)
    sun.sun = True

    #debri.y_vel = 0
    #debri = 0
    planets = [sun]

    for i in range(100):

        #debri.y_vel = debri.y_vel + 1
        #debri = debri + 1

        debris_dist = random.uniform(-1 * Planet.AU, -1.524 * Planet.AU)
        debris_vel = random.uniform(-47.4 * 100, 24.077 * 100)
        debris_mass = random.uniform(3.30 * 10**23, 5.9742 * 10**24)

        #debri[i] = Planet(debris_dist, 0, 1, DARK_GREY, debris_mass)
        #debri.y_vel[i] = debris_vel

        locals()["debri%d" % i] = Planet(debris_dist, 0, 1, DARK_GREY, debris_mass)
        locals()["debri%d.y_vel" % i] = debris_vel

        planets.append(locals()["debri%d" % i])

    #earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    #earth.y_vel = 29.783 * 1000

    #mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    #mars.y_vel = 24.077 * 1000

    #mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    #mercury.y_vel = -47.4 * 1000

    #venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    #venus.y_vel = -35.02 * 1000

    #planets = [sun, earth, mars, mercury, venus] # list of all debris

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        #pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()
