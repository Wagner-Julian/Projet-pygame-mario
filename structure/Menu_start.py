import pygame
import sys
import random

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre
# Définir les dimensions de la fenêtre

largeur_fenetre = 800
hauteur_fenetre = 600

ecran = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("AKUMU")

# Définir les couleurs
white = (255, 255, 255)
red = (255, 0, 0)
dark_red = (139, 0, 0)
black = (0, 0, 0)


# Charger l'image de fond et l'image de chargement
background_image = pygame.image.load('structure/Images Pygames/Leonardo_Phoenix_Create_a_2D_video_game_scenery_set_in_a_dark_2.jpg')
background_image = pygame.transform.scale(background_image, (largeur_fenetre, hauteur_fenetre))

loading_image = pygame.image.load('structure/Images Pygames/chargement.webp')
loading_image = pygame.transform.scale(loading_image, (largeur_fenetre, hauteur_fenetre))

blood_splatter = pygame.image.load('structure/Images Pygames/blood-splatter-png-44476 (1).png')
blood_splatter = pygame.transform.scale(blood_splatter, (400, 100))

# Variables pour l'effet de foudre
lightning_active = False
lightning_duration = 5  # Durée de chaque éclair (en frames)
lightning_timer = 0
lightning_interval = random.randint(60, 180)  # Intervalle aléatoire entre les éclairs
lightning_position = (0, 0)

# Fonction pour dessiner le texte et retourner son rectangle
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
    return textrect

# Fonction pour dessiner un éclair
def draw_lightning(surface, start_pos):
    num_segments = random.randint(20, 20)
    x, y = start_pos

    for _ in range(num_segments):
        end_x = x + random.randint(-30, 30)
        end_y = y + random.randint(20, 40)
        pygame.draw.line(surface, red, (x, y), (end_x, end_y), random.randint(2, 4))
        x, y = end_x, end_y

# Fonction pour le menu de démarrage avec animation de survol et éclairs en fond
def start_menu():
    font = pygame.font.Font(None, 74)
    pulse_font = pygame.font.Font(None, 80)
    pulse_counter = 0  # Compteur pour animer le titre "Akumu"
    global lightning_active, lightning_timer, lightning_interval, lightning_position
    
    while True:
        ecran.blit(background_image, (0, 0))  # Dessiner l'image de fond

        # Animation "dark" pour le titre "Akumu"
        if pulse_counter % 60 < 30:
            draw_text('AKUMU', pulse_font, dark_red, ecran, largeur_fenetre// 2, hauteur_fenetre // 4)
        else:
            draw_text('AKUMU', font, white, ecran, largeur_fenetre // 2, hauteur_fenetre // 4)

        # Obtenir la position de la souris
        mouse_pos = pygame.mouse.get_pos()

        # Dessiner les boutons avec effet sanglant au survol
        play_button_rect = draw_text('Jouer', font, red, ecran, largeur_fenetre// 2, hauteur_fenetre // 2)
        if play_button_rect.collidepoint(mouse_pos):
            ecran.blit(blood_splatter, (play_button_rect.x - 20, play_button_rect.y - 20))
            draw_text('Jouer', font, dark_red, ecran, largeur_fenetre// 2, hauteur_fenetre // 2)

        quit_button_rect = draw_text('Quitter', font, red, ecran, largeur_fenetre// 2, hauteur_fenetre // 2 + 100)
        if quit_button_rect.collidepoint(mouse_pos):
            ecran.blit(blood_splatter, (quit_button_rect.x - 20, quit_button_rect.y - 20))
            draw_text('Quitter', font, dark_red, ecran, largeur_fenetre// 2, hauteur_fenetre // 2 + 100)

        # Gestion de l'animation de foudre
        if lightning_active:
            draw_lightning(ecran, lightning_position)  # Dessiner un éclair au hasard
            lightning_timer -= 1
            if lightning_timer <= 0:
                lightning_active = False  # Désactiver l'éclair après le temps défini
                lightning_interval = random.randint(60, 180)  # Réinitialiser l'intervalle
        else:
            lightning_interval -= 1
            if lightning_interval <= 0:
                lightning_active = True
                lightning_timer = lightning_duration
                lightning_position = (random.randint(0, largeur_fenetre), random.randint(0, hauteur_fenetre // 2))

        # Vérifier les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if play_button_rect.collidepoint(mouse_pos):
                        loading_ecran()
                    if quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        pulse_counter += 1

# Fonction pour afficher l'écran de chargement
def loading_ecran():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ecran.blit(loading_image, (0, 0))
        draw_text('Chargement...', pygame.font.Font(None, 50), black, ecran, largeur_fenetre// 2, hauteur_fenetre // 2 + 100)

        pygame.display.flip()
        pygame.time.delay(2000)
        main_game()
        break

# Fonction principale du jeu
def main_game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ecran.fill(white)
        draw_text('Jeu en cours...', pygame.font.Font(None, 50), black, ecran, largeur_fenetre// 2, hauteur_fenetre // 2)
        pygame.display.flip()

# Appel de la fonction du menu de démarrage
start_menu()
