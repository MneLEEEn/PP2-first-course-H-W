import pygame
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((960, 600))
songs = ['hogjim/I Bet on Losing Dogs - Mitski.mp3','hogjim/Mitski-Heaven.mp3','hogjim/Mitski-My Love Mine All Mine.mp3','hogjim/Remember My Name - Mitski.mp3']
pygame.mixer.music.load(songs[0])
pygame.mixer.music.play()
i = 0
a = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                i = (i + 1) % len(songs)
                pygame.mixer.music.load(songs[i])
                pygame.mixer.music.play()
            elif event.key == pygame.K_LEFT:
                i = (i - 1) % len(songs)
                pygame.mixer.music.load(songs[i])
                pygame.mixer.music.play()
            elif event.key == pygame.K_SPACE:
                if a:
                    pygame.mixer.music.stop()
                    a = False
                else:
                    pygame.mixer.music.play()
                    a = True
    pygame.display.flip()