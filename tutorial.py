"""
Make the damn snake thing work.
"""

import pygame
import random

# Classes
class Config(object):
    """
    Configuration object to hold necessary configuration. Loads and saves config files.
    """
    # TODO: Implement load and save configuration.

    def __init__(self):

        # colors
        self.head_color = pygame.Color(255, 0, 0, 255)
        self.body_color = pygame.Color(255, 63, 63, 255)
        self.food_color = pygame.Color(181, 0, 181, 255)
        self.background_color = pygame.Color(0, 127, 0, 255)

        # game
        self.starting_facing = 1, 0

        # keys
        self.down = pygame.K_DOWN
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT
        self.up = pygame.K_UP
        self.quit = pygame.K_ESCAPE

        # system
        self.width = 40
        self.height = 30
        self.scale = 10
        self.background = pygame.Surface(self.resolution)
        self.background.fill(self.background_color)
        self.frame_rate = 8

    @property
    def resolution(self):
        return self.width * self.scale, self.height * self.scale

    @property
    def cell(self):
        return self.scale, self.scale


class Head(pygame.sprite.Sprite):

    def __init__(self, c, *groups):
        super(Head, self).__init__(*groups)
        self.c = c
        self.image = pygame.Surface(c.cell)
        self.image.fill(c.head_color)
        self.rect = pygame.Rect((0, 0), c.cell)
        self.facing = c.starting_facing
        self.child = None

    def update(self):
        keys = pygame.key.get_pressed()

        new_vector = (keys[self.c.left] * -1 + keys[self.c.right],
                      keys[self.c.up] * -1 + keys[self.c.down])
        if new_vector[0] or new_vector[1]:
            if not dot_product(new_vector, self.facing):
                self.facing = new_vector
        pos = self.rect.topleft
        self.rect.move_ip(self.move)
        if self.child:
            self.child.update(*pos)

    @property
    def move(self):
        return self.facing[0] * self.c.scale, self.facing[1] * self.c.scale

    @property
    def grandchild(self):
        return self.child.child

    def eat(self, body):
        if not self.child:
            pos_x, pos_y = self.rect.topleft
            x = pos_x + -self.facing[0]
            y = pos_y + -self.facing[1]
            self.child = Body(x, y, self.c, body)
        else:
            self.child.eat(body)


class Body(Head):

    def __init__(self, x, y, c, *groups):
        super(Body, self).__init__(c, *groups)
        self.image.fill(c.body_color)
        self.rect.topleft = x, y

    def update(self, x, y):
        pos = self.rect.topleft
        self.rect.topleft = x, y
        if self.child:
            self.child.update(*pos)


class Food(pygame.sprite.Sprite):

    def __init__(self, c, *groups):
        super(Food, self).__init__(*groups)
        self.image = pygame.Surface(c.cell)
        self.image.fill(c.food_color)
        x = random.randint(0, c.width - 1) * c.scale
        y = random.randint(0, c.height - 1) * c.scale
        self.rect = pygame.Rect((x, y), c.cell)

    def update(self):
        pass

# Functions
def dot_product(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def main(display, configuration):
    running = True
    player = pygame.sprite.GroupSingle()
    body = pygame.sprite.Group()
    food = pygame.sprite.GroupSingle()
    Food(configuration, food)
    Head(configuration, player)
    clock = pygame.time.Clock()
    speed = configuration.frame_rate

    while running:
        _ = clock.tick(speed)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.KEYDOWN:
                if event.key == configuration.quit:
                    running = False

        # Update Model
        player.update()

        if pygame.sprite.spritecollide(player.sprite, food, True):
            player.sprite.eat(body)
            Food(configuration, food)

        for segment in pygame.sprite.spritecollide(player.sprite, body, False):
            if segment is not player.sprite.child and segment is not player.sprite.grandchild:
                running = False
                game_over(display)

        if ((player.sprite.rect.x >= configuration.resolution[0]) or
                (player.sprite.rect.x < 0) or
                (player.sprite.rect.y >= configuration.resolution[1]) or
                (player.sprite.rect.y < 0)):
            running = False
            game_over(display)

        # Draw Frame
        display.blit(configuration.background, (0, 0))
        food.draw(display)
        player.draw(display)
        body.draw(display)
        pygame.display.update()


def game_over(display):
    _ = display
    print("Game over.")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    config = Config()
    screen = pygame.display.set_mode(config.resolution)
    main(screen, config)
    pygame.quit()