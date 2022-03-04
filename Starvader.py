import pygame, sys, random, os, json
pygame.init()

WINDOW_SIZE = (600, 400)

from pygame.locals import *

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Starvader")

# Save
def save(data):
    with open('./save.json', 'w+') as save_file:
        json.dump(data, save_file, indent=4)

def load_save():
    save_data = {}

    try:
        with open('./save.json', 'r') as save_file:
            save_data = json.load(save_file)
    except Exception as e:
        pass

    return save_data

# Font
font = pygame.font.Font("data/fonts/Inconsolata/static/Inconsolata/Inconsolata-Regular.ttf", 20)
big_font = pygame.font.Font("data/fonts/Inconsolata/static/Inconsolata/Inconsolata-Regular.ttf", 40)
little_font = pygame.font.Font("data/fonts/Inconsolata/static/Inconsolata/Inconsolata-Regular.ttf", 10)


# Images
bg_image = pygame.image.load("data/images/bg.png").convert()
bg_image = pygame.transform.scale(bg_image, (600, 400))

def game():
    # clock
    clock = pygame.time.Clock()

    # Images
    player_image = pygame.image.load("data/images/player.png").convert()
    player_image.set_colorkey((0, 0, 0))
    player_image = pygame.transform.scale(player_image, (80, 60))

    player_projectile_image = pygame.image.load("data/images/player-projectile.png").convert()
    player_projectile_image = pygame.transform.scale(player_projectile_image, (10, 40))

    enemy_image = pygame.image.load("data/images/enemy.png").convert()
    enemy_image.set_colorkey((0, 0, 0))
    enemy_image = pygame.transform.scale(enemy_image, (70, 50))

    # Player
    player = pygame.Rect((WINDOW_SIZE[0] / 2) - (player_image.get_width() / 2) , 300, player_image.get_width(), player_image.get_height())

    top = False
    bottom = False
    left = False
    right = False

    velocity = 4

    # Enemies
    enemies_number_max = 2
    enemy_killed_score_added = 100
    enemies = []

    enemy_velocity = 2

    # Projectiles
    player_projectile_velocity = 10

    player_projectiles = []

    # Score
    score = 0

    # Loop
    running = True
    while running:

        # Draw images
        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, player)

        # Display score
        score_text = font.render(f"Score: {str(score)}", 0, (255, 255, 255))
        screen.blit(score_text, (2, 2))

        # World borders collision
        if player.x < 0: left = False
        if player.y < 0: top = False
        if player.x + player.width > WINDOW_SIZE[0]: right = False
        if player.y + player.height > WINDOW_SIZE[1]: bottom = False

        # Player movement
        if top: player.y -= velocity
        if bottom: player.y += velocity
        if left: player.x -= velocity
        if right: player.x += velocity

        # Enemies
        if len(enemies) < enemies_number_max:
            enemies.append(pygame.Rect(random.randint(0, WINDOW_SIZE[0] + 1), 0 - enemy_image.get_height(), enemy_image.get_width(), enemy_image.get_height()))
        for enemy in enemies:
            projectiles_collide_index = enemy.collidelist(player_projectiles)
            if projectiles_collide_index != -1:
                enemies.pop(enemies.index(enemy))
                player_projectiles.pop(projectiles_collide_index)
                score += enemy_killed_score_added

            if player.x - enemy.x > 40: enemy.x += enemy_velocity
            elif player.x - enemy.x < 40: enemy.x -= enemy_velocity
            if player.y - enemy.y > 40: enemy.y += enemy_velocity
            elif player.y - enemy.y < 40: enemy.y -= enemy_velocity

            screen.blit(enemy_image, enemy)

        # Player projectiles
        for projectile in player_projectiles:
            if projectile.x + projectile.width < 0:
                player_projectiles.pop(player_projectiles.index(projectile))
            else:
                screen.blit(player_projectile_image, projectile)
                projectile.y -= player_projectile_velocity

        # Player collision
        if player.collidelist(enemies) != -1:
            running = False

        # Events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_UP: top = True
                if event.key == K_DOWN: bottom = True
                if event.key == K_LEFT: left = True
                if event.key == K_RIGHT: right = True
                if event.key == K_SPACE:
                    player_projectiles.append(pygame.Rect(player.x + (player.width / 2) - (player_projectile_image.get_width() / 2), player.y, player_projectile_image.get_width(), player_projectile_image.get_height()))
            if event.type == KEYUP:
                if event.key == K_UP: top = False
                if event.key == K_DOWN: bottom = False
                if event.key == K_LEFT: left = False
                if event.key == K_RIGHT: right = False

        pygame.display.update()
        clock.tick(30)

    return score


def menu():
    # Clock
    clock = pygame.time.Clock()

    # Load save
    save_data = load_save()

    # Buttons
    play_button = pygame.Rect((WINDOW_SIZE[0] / 2) - (125 / 2), 120, 125, 50)

    # Texts
    rule_text = little_font.render("Toucher les ennemies avec vos projectiles sans vous laissez vous toucher pour gagner", 0, (255, 255, 255))
    title = big_font.render("Starvader", 0, (255, 255, 255))
    play_button_text = font.render("Jouer", 0, (0, 0, 0))
    highest_score_text = font.render(f"Highest score: {save_data.get('highest_score')}", 0, (255, 255, 255))
    latest_score_text = font.render(f"Latest score: {save_data.get('latest_score')}", 0, (255, 255, 255))

    # Loop
    running = True
    while running:

        # Draw images
        screen.blit(bg_image, (0, 0))

        # Draw buttons
        pygame.draw.rect(screen, (255, 255, 255), play_button)

        # Render text
        screen.blit(title, ((WINDOW_SIZE[0] / 2) - (big_font.size("Starvader")[0] / 2), 20))
        screen.blit(rule_text, ((WINDOW_SIZE[0] / 2) - (little_font.size("Toucher les ennemies avec vos projectiles sans vous laissez vous toucher pour gagner")[0] / 2), 80))
        screen.blit(play_button_text, ((WINDOW_SIZE[0] / 2) - (font.size("Jouer")[0] / 2), 120 - (font.size("Jouer")[1] / 2) + (play_button.height / 2)))
        screen.blit(highest_score_text, ((WINDOW_SIZE[0] / 2) - (font.size(f"Highest score: {save_data.get('highest_score')}")[0] / 2), 200))
        screen.blit(latest_score_text, ((WINDOW_SIZE[0] / 2) - (font.size(f"Latest score: {save_data.get('latest_score')}")[0] / 2), 250))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0] and play_button.collidepoint(pygame.mouse.get_pos()):
                    save_draft = {}
                    score = game()
                    save_draft["latest_score"] = score

                    if score > save_data.get("highest_score"):
                        save_draft["highest_score"] = score
                    else:
                        save_draft["highest_score"] = save_data["highest_score"]

                    save(save_draft)

                    running = False

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    while True:
        menu()
