import pygame
import psycopg2
import random
import sys

# Настройки подключения к базе
conn = psycopg2.connect(
    dbname="postgres", user="postgres", password="tungtungsahur", host="localhost", port="5432"
)
cur = conn.cursor()

# Pygame настройки
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Шрифт для отображения очков
font = pygame.font.SysFont(None, 36)

# Змейка
snake = [(100, 100)]
snake_dir = (CELL_SIZE, 0)

# Еда
food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))

# Уровень и Скорость
level_speeds = {1: 5, 2: 10, 3: 15}
level = 1
score = 0

# Пользователь
def create_tables():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS UserScores (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES Users(id),
            level INTEGER DEFAULT 1,
            score INTEGER DEFAULT 0
        );
    """)
    conn.commit()

def get_or_create_user(username):
    cur.execute("SELECT id FROM Users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
    else:
        cur.execute("INSERT INTO Users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        cur.execute("INSERT INTO UserScores (user_id) VALUES (%s)", (user_id,))
        conn.commit()
    return user_id

def load_user_progress(user_id):
    cur.execute("SELECT level, score FROM UserScores WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    if result:
        return result
    return (1, 0)

def save_game(user_id, level, score):
    cur.execute("UPDATE UserScores SET level = %s, score = %s WHERE user_id = %s", (level, score, user_id))
    conn.commit()

# Получаем username
username = input("Enter your username: ")
create_tables()
user_id = get_or_create_user(username)
level, score = load_user_progress(user_id)
print(f"Welcome {username}! Current Level: {level}, Score: {score}")

running = True

# Основной цикл игры
while running:
    clock.tick(level_speeds.get(level, 5))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)
            elif event.key == pygame.K_p:  # пауза и сохранение
                print("Game Paused. Saving progress...")
                save_game(user_id, level, score)
    
    # Обновление змейки
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT or
        new_head in snake):
        print("Game Over!")
        save_game(user_id, level, score)

        # Отрисовка экрана Game Over
        screen.fill(WHITE)
        game_over_text = font.render("Game Over!", True, RED)
        final_score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 10))
        pygame.display.flip()

        pygame.time.delay(3000)  # 3 секунды
        running = False
        break

    snake = [new_head] + snake[:-1]

    # Проверка еды
    if new_head == food:
        snake.append(snake[-1])
        food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        score += 10
        if score % 50 == 0:
            level += 1

    # Отрисовка
    screen.fill(WHITE)
    for part in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(part[0], part[1], CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

    # Отрисовка очков и уровня
    score_text = font.render(f"Score: {score}  Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
cur.close()
conn.close()
