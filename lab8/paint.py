import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Paint")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the tools
tool = "brush"
brush_size = 10
eraser_size = 10
color = BLACK

# Set up the drawing surface
drawing_surface = pygame.Surface((screen_width, screen_height))
drawing_surface.fill(WHITE)

# Set up the font
font = pygame.font.Font(None, 30)

def draw_continuous(tool, size, color):
    if tool == "brush":
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.circle(drawing_surface, color, mouse_pos, size)
    elif tool == "circle":
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.circle(drawing_surface, color, mouse_pos, 50)
    elif tool == "rectangle":
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(drawing_surface, color, pygame.Rect(mouse_pos, (100, 50)))
    elif tool == "eraser":
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            pygame.draw.circle(drawing_surface, WHITE, mouse_pos, size)

# Set up the game loop
running = True
while running:
    draw_continuous(tool, brush_size, color)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_s:
                pygame.image.save(drawing_surface, "drawing.png")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if tool == "brush":
                    pygame.draw.circle(drawing_surface, color, event.pos, brush_size)
                elif tool == "circle":
                    pygame.draw.circle(drawing_surface, color, event.pos, 50)
                elif tool == "rectangle":
                    pygame.draw.rect(drawing_surface, color, pygame.Rect(event.pos, (100, 50)))
                elif tool == "eraser":
                    pygame.draw.circle(drawing_surface, WHITE, event.pos, eraser_size)

    # Draw the background
    screen.fill(WHITE)

    # Draw the drawing surface
    screen.blit(drawing_surface, (0, 0))

    # Draw the tool and color indicators
    tool_text = font.render("Tool: " + tool.capitalize(), True, BLACK)
    screen.blit(tool_text, (10, 10))
    color_text = font.render("Color: " + str(color), True, BLACK)
    screen.blit(color_text, (10, 40))

    # Draw the brush/eraser size indicator
    if tool == "brush" or tool == "eraser":
        size_text = font.render("Size: " + str(brush_size), True, BLACK)
        screen.blit(size_text, (10, 70))

    # Draw the color selection buttons
    pygame.draw.rect(screen, RED, pygame.Rect(screen_width - 80, 10, 30, 30))
    pygame.draw.rect(screen, GREEN, pygame.Rect(screen_width - 40, 10, 30, 30))
    pygame.draw.rect(screen, BLUE, pygame.Rect(screen_width - 80, 50, 30, 30))
    pygame.draw.rect(screen, BLACK, pygame.Rect(screen_width - 40, 50, 30, 30))

    # Handle input
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if screen_width - 80 <= mouse_pos[0] <= screen_width - 50 and 10 <= mouse_pos[1] <= 40:
            color = RED
        elif screen_width - 40 <= mouse_pos[0] <= screen_width - 10 and 10 <= mouse_pos[1] <= 40:
            color = GREEN
        elif screen_width - 80 <= mouse_pos[0] <= screen_width - 50 and 50 <= mouse_pos[1] <= 80:
            color = BLUE
        elif screen_width - 40 <= mouse_pos[0] <= screen_width - 10 and 50 <= mouse_pos[1] <= 80:
            color = BLACK

    # Update the screen
    pygame.display.flip()

# Quit pygame
pygame.quit()