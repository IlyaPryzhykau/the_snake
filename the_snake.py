import pygame
from random import randint
from typing import Optional, Tuple, List

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (144, 238, 144)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)
BAD_APPLE_COLOR = (255, 165, 0)

# Цвет змейки
SNAKE_COLOR = (164, 164, 0)
HEAD_SNAKE_COLOR = (184, 134, 11)

# Цвет камня
ROCK_COLOR = (64, 64, 64)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс"""

    def __init__(self,
                 position: Optional[Tuple[int, int]] = None,
                 body_color: Optional[Tuple[int, int, int]] = None) -> None:
        """
        Инициализация игрового объекта.

        :param position: Начальная позиция объекта.
        :param body_color: Цвет тела объекта.
        """
        self.position = position
        self.body_color = body_color

    def draw(self,
             surface: pygame.Surface,
             size: Tuple[int, int] = (GRID_SIZE, GRID_SIZE)) -> None:
        """
        Метод отрисовки объекта на игровой поверхности.

        :param surface: Игровая поверхность.
        :param size: Размер объекта.
        """
        if self.position is not None and self.body_color is not None:
            rect = pygame.Rect((self.position[0], self.position[1]), size)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, который описывает поведение яблока"""

    def __init__(self, position=None, body_color=APPLE_COLOR) -> None:
        """
        Инициализация игрового объекта.

        :param position: Начальная позиция объекта.
        :param body_color: Цвет тела объекта.
        """
        super().__init__(position, body_color)
        self.randomize_position([])

    def randomize_position(self, occupied_positions: List[Tuple[int, int]]) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_positions:
                self.position = new_position
                break

    def draw(self, surface, size=(GRID_SIZE, GRID_SIZE)) -> None:
        """Метод отрисовки яблока на игровой поверхности."""
        super().draw(surface, size)


class Snake(GameObject):
    """Класс, который описывает поведение змеи."""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=SNAKE_COLOR) -> None:
        """
        Инициализация змеи.

        :param body_color: Цвет тела змеи.
        """
        super().__init__(position, body_color)
        self.length: int = 1
        self.positions = [self.position]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.last: Optional[Tuple[int, int]] = None
        self.reset()

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод обновления позиции змейки."""
        current_head = self.get_head_position()
        delta_x, delta_y = self.direction

        new_head = (
            (current_head[0] + delta_x * GRID_SIZE) % SCREEN_WIDTH,
            (current_head[1] + delta_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface, size=(GRID_SIZE, GRID_SIZE)) -> None:
        """Метод отрисовки змейки на игровой поверхности."""
        for pos in self.positions:
            rect = pygame.Rect(pos, size)
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки с измененным цветом
        head_rect = pygame.Rect(self.positions[0], size)
        pygame.draw.rect(surface, HEAD_SNAKE_COLOR, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [self.position]
        self.length = 1


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple()

    # Список занятых позиций на игровом поле.
    occupied_positions = [snake.position] + snake.positions

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            occupied_positions.append(snake.position)
            apple.randomize_position(occupied_positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
