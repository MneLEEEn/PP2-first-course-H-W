import pygame
pygame.init()
W, H = 600, 400
sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Red ball")
clock = pygame.time.Clock()
FPS = 60
x = W // 2
y = H // 2
speed = 20
radius = 25
flLeft = flRight = False
flUp = flDown = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                flLeft = True
            elif event.key == pygame.K_RIGHT:
                flRight = True
            if event.key == pygame.K_UP:
                flUp = True
            elif event.key == pygame.K_DOWN:
                flDown = True
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                flLeft = flRight = False
            if event.key in [pygame.K_UP,pygame.K_DOWN]:
                flUp = flDown = False
    a, b =pygame.display.get_window_size()
    if radius <= x <= a:
        if flLeft:
            x -= speed
        elif flRight:
            x += speed
    elif x < radius:
        x = radius
    elif x > a - radius:
        x = a - radius
    if radius <= y <= b:
        if flUp:
            y -= speed
        elif flDown:
            y += speed
    elif y < radius:
        y = radius
    elif y > b - radius:
        y = b - radius

    sc.fill((255, 255, 255))
    pygame.draw.circle(sc, (255, 0, 0), (x, y), 25)
    pygame.display.update()
    clock.tick(FPS)