import pygame


class Head(pygame.sprite.Sprite):

    def __init__(self, screen, *args):
        super(Head, self).__init__(*args)
        self.image = pygame.Surface((50, 50)).convert()
        self.rect = self.image.get_rect()
        self.screen = screen  # Rect not a Surface
        self.x = 2
        self.y = 1

    def update(self):
        keys = pygame.key.get_pressed()
        # {0 = 0/1}
        x = keys[pygame.K_LEFT] * -1 + keys[pygame.K_RIGHT]
        y = keys[pygame.K_UP] * -1 + keys[pygame.K_DOWN]
        self.rect.move_ip(x, y)
        # if self.rect.left < self.screen.left:
        #     self.x = 2
        # elif self.rect.right > self.screen.right:
        #     self.x = -2
        #
        # if self.rect.top < self.screen.top:
        #     self.y = 1
        # elif self.rect.bottom > self.screen.bottom:
        #     self.y = -1


class TimeDisplay(pygame.sprite.Sprite):

    def __init__(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.image = self.font.render("0", True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.move_ip((10, 10))
        self.timer = 0

    def update(self, td):
        self.timer += td
        if self.timer > 100:
            self.timer = 0
            self.image = self.font.render(str(td), True, (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.move_ip((10, 10))


def main_loop():
    pygame.init()
    display = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
    screen_rect = display.get_rect()
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(pygame.font.get_default_font(), 40)
    title = font.render("Hello, World", False, (0, 0, 255))
    title_rect = title.get_rect()
    title_rect.center = screen_rect.center
    timer = TimeDisplay()
    group = pygame.sprite.GroupSingle()
    Head(screen_rect, group)
    while running:
        td = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        group.update()
        timer.update(td)
        group.sprite.image.fill((255, 200, 122))
        display.fill((255, 0, 0))
        group.draw(display)
        display.blit(title, title_rect)
        display.blit(timer.image, timer.rect)
        pygame.display.update()


if __name__ == "__main__":
    main_loop()
