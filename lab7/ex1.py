import pygame
from datetime import datetime
pygame.init()
screen = pygame.display.set_mode((829, 836))
clock = pygame.time.Clock()
c = pygame.image.load(r"mickeyclock.png")
l = pygame.image.load(r"left-hand.png")
r = pygame.image.load(r"right-hand.png")
rect = c.get_rect(center=(415, 418))
while True:
    screen.blit(c,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    t=datetime.now().time()
    a1=-(t.second*6)
    n=pygame.transform.rotate(l,a1)
    rect2=n.get_rect(center=rect.center)
    screen.blit(n,rect2.topleft)
    a2=-(t.minute*6)
    n2=pygame.transform.rotate(r,a2)
    rect3=n2.get_rect(center=rect.center)
    screen.blit(n2,rect3.topleft)
    pygame.display.flip()
    clock.tick(60)