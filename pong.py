import pygame as pg
import random
import sys

pg.init()

class Paddle:

    def __init__(self, x, y):
        self.rect = pg.Rect(0, 0, 10, 80) # (x_pos, y_pos, width, height)
        self.rect.center = (x, y)
        self.speed = 10

    def draw(self, screen):
        return pg.draw.rect(screen, [255, 255, 255], self.rect)

class Player(Paddle):

    def __init__(self):
        pos = (80, 300) 
        Paddle.__init__(self, pos[0], pos[1])

    def update(self):
        key = pg.key.get_pressed()

        if key[pg.K_w]:
            self.rect.y -= self.speed
        elif key[pg.K_s]:
            self.rect.y += self.speed

        self.rect.y = clamp(self.rect.y, 0, 520)

class Computer(Paddle):

    def __init__(self):
        pos = (920, 300)
        Paddle.__init__(self, pos[0], pos[1])

    def update(self, ball):
        if self.rect.top < ball.rect.y - 10:
            self.rect.y += self.speed
        if self.rect.bottom > ball.rect.y + 10:
            self.rect.y -= self.speed

        self.rect.y = clamp(self.rect.y, 0, 520)

class Ball:

    def __init__(self):
        self.rect = pg.Rect(0, 0, 14, 14)
        self.random_pos()

    def random_pos(self):
        self.rect.center = (500, 300)
        self.x_vel = random.choice([-7, 7])
        self.y_vel = random.choice([-7, 7])

    def draw(self, screen):
        return pg.draw.ellipse(screen, [255, 255, 255], self.rect)
    
    def update(self, player, comp):
        global player_score, computer_score

        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        if self.rect.left <= 0:
            self.random_pos()
            computer_score += 1
            pg.mixer.Sound.play(ping)

        if self.rect.right >= 1000:
            self.random_pos()
            player_score += 1
            pg.mixer.Sound.play(ping)

        if self.rect.top <= 0 or self.rect.bottom >= 600:
            self.y_vel *= -1
            pg.mixer.Sound.play(bounce)

        if self.rect.colliderect(player.rect) and self.x_vel < 0:
            self.x_vel *= -1
            pg.mixer.Sound.play(bounce)

        if self.rect.colliderect(comp.rect) and self.x_vel > 0:
            self.x_vel *= -1
            pg.mixer.Sound.play(bounce)

# if either closing window or pressing escape exit program
def is_close_app_event(event):
    return (event.type == pg.QUIT) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)

# limit a position to an area
def clamp(value, min, max):
    if value <= min: value = min
    if value >= max: value = max
    return value

def main():
    # initialised screen
    SCREEN = pg.display.set_mode([1000, 600])
    icon = pg.image.load("data/gfx/icon.png").convert_alpha()
    pg.display.set_icon(icon)
    pg.display.set_caption("Pong game")

    # clock
    FramePerSec = pg.time.Clock()

    # pause
    pause = False
    font = pg.font.Font("data/font/RobotoCondensed-Regular.ttf", 75)
    pause_text = font.render("PAUSE", True, [255, 255, 255])

    # objects
    player = Player()
    computer = Computer()
    ball = Ball()

    # score text
    global player_score, computer_score
    player_score = 0
    computer_score = 0
    score_font = pg.font.Font("data/font/RobotoCondensed-Regular.ttf", 20)

    # sound
    global bounce, ping
    pg.mixer.init()
    bounce = pg.mixer.Sound("data/sfx/bounce.wav")
    ping = pg.mixer.Sound("data/sfx/ping.mp3")

    # main game loop    
    while True:
        # event handler
        for event in pg.event.get():
            if is_close_app_event(event):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                pause = not pause

        # background
        SCREEN.fill([0, 0, 0])
        border = pg.Rect(0, 0, 1000, 600)
        pg.draw.rect(SCREEN, [255, 255, 255], border, 3)

        for i in range(0, SCREEN.get_height(), SCREEN.get_height() // 30):
            rect = pg.Rect(SCREEN.get_width() // 2, i, 2, SCREEN.get_height() // 60)
            pg.draw.rect(SCREEN, [255, 255, 255], rect)

        # score
        player_text = score_font.render(f"{player_score}", True, [255, 255, 255])
        SCREEN.blit(player_text, [420, 50])

        computer_text = score_font.render(f"{computer_score}", True, [255, 255, 255])
        SCREEN.blit(computer_text, [580, 50])

        if not pause:
            # updating objects
            player.update()
            computer.update(ball)
            ball.update(player, computer)

        if pause:
            SCREEN.blit(pause_text, [400, 250])

        # drawing objects
        player.draw(SCREEN)
        computer.draw(SCREEN)
        ball.draw(SCREEN)

        # updating screen
        pg.display.flip()
        FramePerSec.tick(60)

# run code if main program executed
if __name__ == '__main__':
    main()