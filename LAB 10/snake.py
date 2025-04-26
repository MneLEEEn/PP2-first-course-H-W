import pygame, sys, random, time
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="postgres",
    user="postgres",
    password="123nurbolik006"
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL
    );
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        score INT,
        level INT
    );
""")
conn.commit()

username = input("Enter your username: ")
cur.execute("SELECT id FROM users WHERE username = %s", (username,))
user = cur.fetchone()

if user:
    user_id = user[0]
else:
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()

print("Welcome", username, "! Your user ID is", user_id)


SCREEN_WIDTH, SCREEN_HEIGHT = 620, 400
BLOCK_SIZE = 20  
SPEED = 10 

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Инициализация Pygame
pygame.init()

# Установка шрифта
font = pygame.font.Font(None, 30)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")

# Функция для вывода текста на экран
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Функция для генерации случайной позиции еды
def generate_food(snake_body):
    while True:
        x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake_body:  # Проверяем, что еда не появляется на змейке
            return x, y

# Функция отрисовки змейки и еды
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_position):
    pygame.draw.rect(screen, RED, (food_position[0], food_position[1], BLOCK_SIZE, BLOCK_SIZE))

# Основная функция игры
def game():
    # Начальное положение змейки
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = "RIGHT"  # Начальное направление
    food = generate_food(snake)  # Генерация еды
    score = 0  # Очки
    level = 1  # Уровень
    speed = SPEED  # Скорость игры

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)  # Очищаем экран

        # Обработка событий (клавиши для движения)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Движение змейки
        head_x, head_y = snake[0]  # Получаем координаты головы
        if direction == "UP":
            head_y -= BLOCK_SIZE
        elif direction == "DOWN":
            head_y += BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += BLOCK_SIZE

        # Проверка столкновений со стенами
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            running = False  # Игра заканчивается

        # Проверка столкновений с собой
        if (head_x, head_y) in snake:
            running = False  # Игра заканчивается

        # Добавление нового сегмента змейки (головы)
        snake.insert(0, (head_x, head_y))

        # Проверка, съела ли змейка еду
        if (head_x, head_y) == food:
            score += 1
            food = generate_food(snake)  # Генерируем новую еду
            # Каждые 3 очка увеличиваем уровень и ускоряем змейку
            if score % 3 == 0:
                level += 1
                speed += 2  # Увеличиваем скорость
        else:
            snake.pop()  # Удаляем последний сегмент змейки (если еда не съедена)

        # Отрисовка змейки и еды
        draw_snake(snake)
        draw_food(food)

        # Отображение счета и уровня
        draw_text(f"Счет: {score}", 10, 10)
        draw_text(f"Уровень: {level}", SCREEN_WIDTH - 150, 10)

        pygame.display.update()
        clock.tick(speed)  # Контроль скорости игры

    # Если игрок проиграл, показываем сообщение и выходим
    screen.fill(BLACK)
    draw_text("Вы проиграли!", SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 10, RED)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Запуск игры
game()
cur.close()
conn.close()
