import pygame
import constants as c
import sprites
import pandas as pd


# Data for future AI
game_data = []


# functions
def text_to_screen(msg, color, size, x, y):
    # write text to screen
    font = pygame.font.Font(c.font_nm, size)
    text_surf = font.render(msg, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = (x, y)
    c.screen.blit(text_surf, text_rect)


def collect_game_data(snake, food, action):
    """
    Save the current game state and player's action.
    """

    distance_x = food.rect.x - snake.rect.x
    distance_y = food.rect.y - snake.rect.y

    row = {
        "snake_x": snake.rect.x,
        "snake_y": snake.rect.y,
        "food_x": food.rect.x,
        "food_y": food.rect.y,
        "distance_x": distance_x,
        "distance_y": distance_y,
        "snake_length": snake.length,
        "action": action
    }

    game_data.append(row)


def save_game_data():
    """
    Save collected game data to CSV.
    """

    if not game_data:
        return

    df = pd.DataFrame(game_data)

    df.to_csv(
        "game_ai_data.csv",
        index=False
    )

    print("\nData saved to game_ai_data.csv")
    print("Number of collected rows:", len(df))

    print("\nAction distribution:")
    print(df["action"].value_counts())


def start_screen():
    while True:
        c.screen.fill(c.SAND)
        c.screen.blit(c.start_screen_img, [10, 50])
        text_to_screen(
            "→ Eat the apples to get bigger",
            c.BROWN,
            27,
            c.WIDTH / 2 - 10,
            100
        )
        text_to_screen(
            "→ Don't run into anything",
            c.BROWN,
            27,
            c.WIDTH / 2 - 37,
            140
        )
        text_to_screen(
            "→ Use arrow keys to move",
            c.BROWN,
            27,
            c.WIDTH / 2 - 27,
            180
        )
        text_to_screen(
            "Press SPACE to play",
            c.BROWN,
            32,
            c.WIDTH / 2,
            c.HEIGHT / 2 + 180
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    initGame()

            if event.type == pygame.QUIT:
                save_game_data()
                pygame.quit()
                quit()


def game_over_screen():
    while True:
        c.screen.fill(c.SAND)
        text_to_screen(
            "Game Over!",
            c.BROWN,
            60,
            c.WIDTH / 2,
            (c.HEIGHT / 2) - 70
        )
        text_to_screen(
            "→ Press P to play again",
            c.GREEN,
            25,
            (c.WIDTH / 2) - 2,
            c.HEIGHT / 2
        )
        text_to_screen(
            "→ Press Q to QUIT",
            c.GREEN,
            25,
            (c.WIDTH / 2) - 21,
            c.HEIGHT / 2 + 40
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    save_game_data()
                    pygame.quit()
                    quit()

                if event.key == pygame.K_p:
                    initGame()

            if event.type == pygame.QUIT:
                save_game_data()
                pygame.quit()
                quit()


def pause_screen():
    while True:
        text_to_screen(
            "Paused",
            c.BROWN,
            35,
            c.WIDTH / 2,
            c.HEIGHT / 2 - 35
        )
        c.screen.blit(
            c.pause_button_img,
            [c.WIDTH / 2 - 15, c.HEIGHT / 2]
        )
        text_to_screen(
            "Press P again to continue playing",
            c.BROWN,
            20,
            c.WIDTH / 2,
            c.HEIGHT / 2 + 60
        )
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return

            if event.type == pygame.QUIT:
                save_game_data()
                pygame.quit()
                quit()


def initGame():
    # initialize sprites
    global all_sprites
    global snake
    global foods
    global food

    all_sprites = pygame.sprite.Group()
    foods = pygame.sprite.Group()

    snake = sprites.Player()
    all_sprites.add(snake)

    food = sprites.Food()
    foods.add(food)
    all_sprites.add(food)

    gameLoop()


# game loop
def gameLoop():
    global food
    game = True

    while game:
        # fps
        c.clock.tick(c.FPS)

        # process input
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                save_game_data()
                game = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    pause_screen()

                # Collect data when the player chooses a direction
                elif event.key == pygame.K_LEFT:
                    collect_game_data(
                        snake,
                        food,
                        "L"
                    )

                elif event.key == pygame.K_RIGHT:
                    collect_game_data(
                        snake,
                        food,
                        "R"
                    )

                elif event.key == pygame.K_UP:
                    collect_game_data(
                        snake,
                        food,
                        "U"
                    )

                elif event.key == pygame.K_DOWN:
                    collect_game_data(
                        snake,
                        food,
                        "D"
                    )

        # if snake touches edges, game over!
        if (
            snake.rect.right >= c.WIDTH
            or snake.rect.left < 0
            or snake.rect.top < 0
            or snake.rect.bottom >= c.HEIGHT
        ):
            game_over_screen()

        all_sprites.update()

        c.screen.fill(c.SAND)
        all_sprites.draw(c.screen)

        # snake length
        head = []
        head.append(snake.rect.x)
        head.append(snake.rect.y)
        snake.posList.append(head)

        if len(snake.posList) > snake.length:
            del snake.posList[0]

        # if snake runs over itself, game over!
        for i in snake.posList[:-1]:
            if i == head:
                game_over_screen()

        # draw snake length and tail
        for i in snake.posList[:-2]:

            if snake.direction == "L":
                c.screen.blit(
                    pygame.transform.rotate(
                        c.snake_tail_img,
                        270
                    ),
                    [i[0], i[1]]
                )

            if snake.direction == "R":
                c.screen.blit(
                    pygame.transform.rotate(
                        c.snake_tail_img,
                        90
                    ),
                    [i[0], i[1]]
                )

            if snake.direction == "U":
                c.screen.blit(
                    pygame.transform.rotate(
                        c.snake_tail_img,
                        180
                    ),
                    [i[0], i[1]]
                )

            if snake.direction == "D":
                c.screen.blit(
                    pygame.transform.rotate(
                        c.snake_tail_img,
                        360
                    ),
                    [i[0], i[1]]
                )

        # check for collisions
        collision = pygame.sprite.spritecollide(
            snake,
            foods,
            True
        )

        if collision:
            snake.collision()

            food = sprites.Food()
            foods.add(food)
            all_sprites.add(food)

        # draw border
        for x in range(0, c.WIDTH + 6, 5):
            pygame.draw.rect(
                c.screen,
                c.BROWN,
                [x, 0, 5, 5]
            )
            pygame.draw.rect(
                c.screen,
                c.BROWN,
                [x, c.HEIGHT + 5, 5, 5]
            )

        for x in range(0, c.HEIGHT + 5, 5):
            pygame.draw.rect(
                c.screen,
                c.BROWN,
                [0, x, 5, 5]
            )
            pygame.draw.rect(
                c.screen,
                c.BROWN,
                [c.WIDTH + 5, x, 5, 5]
            )

        # update screen with score
        text_to_screen(
            "Score: " + str(snake.score),
            c.BROWN,
            24,
            70,
            40
        )

        pygame.display.update()

    pygame.quit()
    quit()


start_screen()