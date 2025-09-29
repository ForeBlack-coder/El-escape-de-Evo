import pygame
import sys
import os
import random
import math

# iniciar programa
pygame.init()

# pantalla completa
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
intro_shown = False

# Rutas
def resource_pack(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

# fondos
asset_background = resource_pack('assets/images/background.png')
background = pygame.image.load(asset_background)
# Escalar el fondo para pantalla completa
background = pygame.transform.scale(background, (screen_width, screen_height))

asset_win_background = resource_pack('assets/images/win_background.jpg')
win_background = pygame.image.load(asset_win_background)
# Escalar el fondo de victoria manteniendo proporción
win_bg_scaled = pygame.transform.scale(win_background, (int(screen_width * 0.8), int(screen_height * 0.6)))

intro_image = resource_pack('assets/images/linea-blanca.png')
imagen = pygame.image.load(intro_image)
# Escalar la imagen de intro para pantalla completa
imagen = pygame.transform.scale(imagen, (int(screen_width * 0.8), int(screen_height * 0.6)))

# icono
asset_icon = resource_pack('assets/images/icon.png')
icon = pygame.image.load(asset_icon)

# musica
asset_intro = resource_pack('assets/music/intro_theme.mp3')
pygame.mixer.music.load(asset_intro)

# jugador
asset_player = resource_pack('assets/images/player.png')
playerimg = pygame.image.load(asset_player)

# proyectil
asset_bullet = resource_pack('assets/images/bullet.png')
bulletimg = pygame.image.load(asset_bullet)

# fuente texto game over
asset_over_font = resource_pack('assets/font/Grizzly Attack - PERSONAL USE.ttf')
over_font = pygame.font.Font(asset_over_font, int(64 * screen_height / 610))
# fuente texto titulo
asset_title_font = resource_pack('assets/font/Broken Dreams.otf')
title_font = pygame.font.Font(asset_title_font, int(64 * screen_height / 610))

# fuente texto puntos
asset_level_font = resource_pack('assets/font/DJGROSS.ttf')
level_font = pygame.font.Font(asset_level_font, int(32 * screen_height / 610))

# fuente texto game win
asset_win_font = resource_pack('assets/font/DJGROSS.ttf')
win_font = pygame.font.Font(asset_win_font, int(64 * screen_height / 610))

# titulo de ventana
pygame.display.set_caption("Camacho vs Masistas del Espacio")

# icono de ventana
pygame.display.set_icon(icon)

# sonido de fondo
pygame.mixer.music.play(-1)

# velocidad del juego
clock = pygame.time.Clock()

# posicion inicial ajustada para pantalla completa
playerX = screen_width // 2 - 50
playerY = screen_height - 110
playerX_change = 0
playerY_change = 0  # Nueva variable para movimiento vertical

# lista de enemigos
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 7

# posiciones de los enemigos
for i in range(no_of_enemies):
    enemy1 = resource_pack('assets/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1))

    enemy2 = resource_pack('assets/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2))

    # posicion aleatoria en X y Y del enemigo ajustada para pantalla completa
    enemyX.append(random.randint(0, screen_width - 100))
    enemyY.append(random.randint(-50, 200))

    # velocidad de movimiento del enemigo
    enemyX_change.append(12)
    enemyY_change.append(40)

# posicion de la bala
bulletX = 200
bulletY = playerY - 30
bulletY_change = 30
bullet_state = "ready"

# puntuacion 
score = 0
def show_score():
    score_value = level_font.render("SCORE " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))

# dibujar al jugador
def player(x, y):
    screen.blit(playerimg, (x, y))

# dibujar al enemigo
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# dispara bala
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

# colision
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 65:
        return True
    else:
        return False

# game over
def game_over_text():
    over_text = over_font.render("DENGE DENGE DENGE", True, (237, 44, 44))
    screen.blit(over_text, (screen_width/2 - over_text.get_width()/2, screen_height/2 - 100))
    over_text = over_font.render("CARA DE DENGUE", True, (237, 44, 44))
    screen.blit(over_text, (screen_width/2 - over_text.get_width()/2, screen_height/2))

# game win
def show_win_text():
    # Centrar el fondo de victoria
    win_bg_x = (screen_width - win_bg_scaled.get_width()) // 2
    win_bg_y = (screen_height - win_bg_scaled.get_height()) // 2
    screen.blit(win_bg_scaled, (win_bg_x, win_bg_y))
    
    win_text = win_font.render("GANASTE", True, (54, 255, 0))
    screen.blit(win_text, (screen_width/2 - win_text.get_width()/2, screen_height/2 - 50))
    win_text = win_font.render("SCORE: " + str(score), True, (54, 255, 0))
    screen.blit(win_text, (screen_width/2 - win_text.get_width()/2, screen_height/2 + 50))

def show_intro_text():
    global intro_shown
    if not intro_shown:  # Mostrar solo si no se ha mostrado antes
        # Centrar la imagen de intro
        intro_x = (screen_width - imagen.get_width()) // 2
        intro_y = (screen_height - imagen.get_height()) // 2
        screen.blit(imagen, (intro_x, intro_y))
        intro_text = level_font.render("", True, (0, 0, 0))
        screen.blit(intro_text, (screen_width/2 - intro_text.get_width()/2, screen_height/2 - 100))
        intro_text = level_font.render("NO DEJES QUE LOS MASISTAS", True, (0, 0, 0))
        screen.blit(intro_text, (screen_width/2 - intro_text.get_width()/2, screen_height/2 - 100))
        intro_text = level_font.render("PASEN EL BLOQUEO", True, (0, 0, 0))
        screen.blit(intro_text, (screen_width/2 - intro_text.get_width()/2, screen_height/2 - 50))
        pygame.display.update()
        pygame.time.wait(3000)  # Espera 3 segundos antes de continuar
        intro_shown = True  # Cambiar el valor para evitar que se muestre nuevamente

# funcion principal
def gameloop():
    global score
    global playerX
    global playerY
    global playerX_change
    global playerY_change
    global bulletX
    global bulletY
    global bullet_state

    in_game = True
    while in_game:

        # manejar eventos, actualizar y renderizar el juego
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_game = False
                    pygame.quit()
                    sys.exit()
                # Controles de movimiento horizontal
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_change = -5
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = 5
                # Controles de movimiento vertical
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    playerY_change = -5
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    playerY_change = 5
                # Disparo
                elif event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            elif event.type == pygame.KEYUP:
                # Detener movimiento horizontal
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    playerX_change = 0
                # Detener movimiento vertical
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    playerY_change = 0
                    
        # posicion del jugador actualizada para movimiento completo
        playerX += playerX_change
        playerY += playerY_change

        # límites horizontales
        if playerX <= 0:
            playerX = 0
        elif playerX >= screen_width - 100:
            playerX = screen_width - 100
            
        # límites verticales (permitir movimiento en toda la pantalla pero con márgenes)
        if playerY <= 0:
            playerY = 0
        elif playerY >= screen_height - 100:
            playerY = screen_height - 100

        # bucle de enemigos
        for i in range(no_of_enemies):
            # distancia entre el enemigo y el jugador ajustada para pantalla completa
            if enemyY[i] > screen_height - 260:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                pygame.display.update()
                # tiempo de espera de mensaje
                pygame.time.wait(7000)
                # devuelta al menu
                main_menu()
                break
            # movimiento del enemigo
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= screen_width - 100:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            # colision de enemigo
            collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = playerY - 30
                bullet_state = "ready"
                score += 1
                enemyX[i] = random.randint(0, screen_width - 100)
                enemyY[i] = random.randint(0, 150)
                
            enemy(enemyX[i], enemyY[i], i)
        # tiempo de recarga de la bala
        if bulletY <= 0:
            bulletY = playerY - 30
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)

        show_score()
         # llegar al score máximo para ganar
        if score >= 50:
            show_win_text()
            pygame.display.update()
            pygame.time.wait(7000)
            score = 0
            in_game = False
            # regresa al menu
            main_menu()
            break
        pygame.display.update()
        clock.tick(60)
    gameloop()

# función para mostrar el menú
def show_menu():
    title = title_font.render("Camacho vs masistas", True, (49, 213, 54))
    screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - 200))
    title = title_font.render("del espacio", True, (49, 213, 54))
    screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - 130))

# función para mostrar el botón (centrados para pantalla completa)
def show_button(text, x, y, width, height, color, hover_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    button_text = over_font.render(text, True, (255, 255, 255))
    screen.blit(button_text, (x + width/2 - button_text.get_width()/2, y + height/2 - button_text.get_height()/2))

# funciones para las acciones de los botones
def start_game():
    show_intro_text()
    pygame.display.update()
    gameloop()

def quit_game():
    pygame.quit()
    sys.exit()

# función principal del menú
def main_menu():
    # Calcular posiciones centradas para los botones
    button_width = int(200 * screen_width / 915)
    button_height = int(50 * screen_height / 610)
    button_x = (screen_width - button_width) // 2
    play_button_y = screen_height // 2
    quit_button_y = screen_height // 2 + button_height + 20
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        show_menu()
        show_button("Jugar", button_x, play_button_y, button_width, button_height, (0, 128, 0), (0, 255, 0), start_game)
        show_button("Salir", button_x, quit_button_y, button_width, button_height, (21, 12, 156), (29, 7, 255), quit_game)
        pygame.display.update()
        clock.tick(60)

main_menu()