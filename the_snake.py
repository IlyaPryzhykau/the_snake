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

    def __init__(self, body_color: Tuple[int, int, int] = None) -> None:
        """
        Инициализация игрового объекта.

        :param body_color: Цвет тела объекта.
        """
        self.position: tuple[int, int] = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color: tuple[int, int, int] = body_color

    def draw(self, surface: pygame.Surface) -> None:
        """
        Абстрактный метод отрисовки объекта.

        :param surface: Игровая поверхность.
        """
        pass


class Apple(GameObject):
    """Класс, который описывает поведение яблока"""

    def __init__(self, body_color=APPLE_COLOR) -> None:
        """
        Инициализация яблока.

        :param body_color: Цвет тела яблока.
        """
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface) -> None:
        """Метод отрисовки яблока на игровой поверхности."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Rock(Apple):
    """Класс, который описывает поведение камня."""

    def __init__(self, body_color=ROCK_COLOR) -> None:
        """
        Инициализация камня.

        :param body_color: Цвет тела камня.
        """
        super().__init__(body_color)


class BadApple(Apple):
    """Класс, который описывает поведение плохого яблока."""

    def __init__(self, body_color=BAD_APPLE_COLOR) -> None:
        """
        Инициализация плохого яблока.

        :param body_color: Цвет тела плохого яблока.
        """
        super().__init__(body_color)


class Snake(GameObject):
    """Класс, который описывает поведение змеи."""

    def __init__(self, body_color=SNAKE_COLOR) -> None:
        """
        Инициализация змеи.

        :param body_color: Цвет тела змеи.
        """
        super().__init__(body_color)
        self.length: int = 1
        self.positions: List[Tuple[int, int]] = [self.position]
        self.direction: Tuple[int, int] = RIGHT
        self.next_direction: Optional[Tuple[int, int]] = None
        self.last: Optional[Tuple[int, int]] = None

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод обновления позиции змейки."""
        current_head = self.get_head_position()
        dx, dy = self.direction

        new_head = (
            (current_head[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (current_head[1] + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface) -> None:
        """Метод отрисовки змейки на игровой поверхности."""
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, HEAD_SNAKE_COLOR, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if len(self.positions) > self.length:
            last_rect = pygame.Rect(
                (self.positions[-1][0], self.positions[-1][1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
            self.positions.pop()

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
    rock_1 = Rock()
    rock_2 = Rock()
    bad_apple = BadApple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == bad_apple.position:
            if snake.length > 1:
                snake.length -= 1
            while bad_apple.position in snake.positions:
                bad_apple.randomize_position()

        if (
                snake.get_head_position() in snake.positions[1:]
                or snake.get_head_position() == rock_1.position
                or snake.get_head_position() == rock_2.position
        ):
            snake.reset()
            rock_1.randomize_position()
            rock_2.randomize_position()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            rock_1.randomize_position()
            rock_2.randomize_position()
            while (
                    apple.position in snake.positions
                    or apple.position == rock_1.position
                    or apple.position == rock_2.position
                    or apple.position == bad_apple.position
            ):
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)
        rock_1.draw(screen)
        rock_2.draw(screen)
        bad_apple.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
