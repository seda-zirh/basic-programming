import pygame

pygame.init()  # init~ #this initialises pygame

win = pygame.display.set_mode((700, 480))  # win means the window of the game

pygame.display.set_caption("You're a Harry wizard")  # sets the caption for the game

# these are all the images we use and imported for the game
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('Komnata_fasolek.png')
bg_main_menu = pygame.image.load("main menu background.jpg")
char = pygame.image.load('standing.png')
wand = pygame.image.load('wand.png')
font = pygame.font.Font('font.TTF', 30)

# we used clock so we can alter time in the game and make it go slower or faster
clock = pygame.time.Clock()

# this is all the music we used for the game by using the music module for pygame
bulletSound = pygame.mixer.Sound('bullet.wav')
hitSound = pygame.mixer.Sound('hit.wav')
snapeSound = pygame.mixer.Sound('concentrate potter.wav')

music = pygame.mixer.music.load('Harry_Potter.wav')  # main background music
pygame.mixer.music.play(-1)  # by using -1 we loop the music

score = 0


class player(object):  # contains all the variables for the character
    def __init__(self, x, y, width, height):
        """this function makes your character and decides where you character stands"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5  # this is how fast you will walk
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        """this makes the window"""
        if self.walkCount + 1 >= 27:  # we use 27 because we have 27 pictures which means a framerate of 27 fps
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def hit(self):
        """ a code for what happens when you get hit"""
        self.isJump = False
        self.jumpCount = 10
        if man.left:
            self.x = 30
        if man.right:
            self.x = 600
            self.y = 410

        self.walkCount = 0
        font1 = pygame.font.Font("font.TTF", 75)
        text = font1.render('Hit', 1, (255, 255, 255))
        win.blit(text, (350, 50))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class projectile(object):
    """a class with functions that make the projectile/bullet"""

    def __init__(self, x, y, radius, color, facing):
        """ """
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        """ """
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    """a class that contains everything for the enemy"""
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        """variables for the enemy"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 6
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        """ """
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (0, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 191, 255),
                             (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        """takes care of the movement of the enemy"""
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def vanish(self):
        """this code stops the game when the enemy vanishes or when the enemy has no health"""
        if self.visible == False:
            pygame.quit()

    def hit(self):
        """code for what happens when the enemy hits you"""
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')


class wand(object):
    """a class for the wand in the game"""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        """ """
        if self.visible:
            wand = pygame.image.load('wand.png')
            win.blit(wand, (self.x, self.y))


def redrawGameWindow():
    """this function updates certain parts of the game"""
    win.blit(bg, (0, 0))
    wand_1.draw(win)
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (560, 10))
    man.draw(win)
    snape.draw(win)
    if wand_1.visible is False:
        for bullet in bullets:
            bullet.draw(win)
    if score >= 11:
        pygame.quit()

    pygame.display.update()  # update the screen so that it actually shows the adjustements


def main_menu():
    """ This is to make a screen appear as soon as you start the game"""

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                quit()

        win.blit(bg_main_menu, (0, 0))
        main_text = pygame.font.Font("font.TTF", 115)
        title = main_text.render("Harry Potter", 1, (255, 223, 0))
        win.blit(title, (150, 50))
        pygame.display.update()
        clock.tick(30)

        pygame.draw.rect(win, (250, 250, 250), (50, 50, 100, 50))
        pygame.draw.rect(win, (178, 34, 34), (550, 450, 100, 50))


# main_menu()

# mainloop
man = player(200, 410, 70, 70)
snape = enemy(50, 410, 80, 80, 600)
shootLoop = 0
bullets = []
wand_1 = wand(480, 400, 27, 27)
run = True
while run:
    clock.tick(27)
    if snape.visible is True:
        if man.hitbox[1] < snape.hitbox[1] + snape.hitbox[3] and man.hitbox[1] + man.hitbox[3] > snape.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > snape.hitbox[0] and man.hitbox[0] < snape.hitbox[0] + snape.hitbox[2]:
                snapeSound.play()
                man.hit()

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < snape.hitbox[1] + snape.hitbox[3] and bullet.y + bullet.radius > snape.hitbox[1]:
            if bullet.x + bullet.radius > snape.hitbox[0] and bullet.x - bullet.radius < snape.hitbox[0] + snape.hitbox[
                2]:
                hitSound.play()
                snape.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if 0 < bullet.x < 700:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0 and wand_1.visible is False:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5:
            bullets.append(
                projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (222, 222, 222), facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] or keys[pygame.K_a] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and man.x < 700 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    if wand_1.visible is True:
        if man.hitbox[1] < wand_1.hitbox[1] + wand_1.hitbox[3] and man.hitbox[1] + man.hitbox[3] > wand_1.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > wand_1.hitbox[0] and man.hitbox[0] < wand_1.hitbox[0] + wand_1.hitbox[2]:
                wand_1.visible = False

    redrawGameWindow()

pygame.quit()