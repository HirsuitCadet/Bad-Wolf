import os, pygame
from pygame.locals import *

# Définition du chemin du dossier data
data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

def filepath(filename):
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    return open(os.path.join(data_dir, filename), mode)

def load_image(filename):
    filename = filepath(filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit("Unable to load: " + filename)
    return image.convert_alpha()

def load_sound(filename, volume=0.5):
    filename = filepath(filename)
    try:
        sound = pygame.mixer.Sound(filename)
        sound.set_volume(volume)
    except:
        raise SystemExit("Unable to load: " + filename)
    return sound

def play_music(filename, volume=0.5, loop=-1):
    filename = filepath(filename)
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
    except:
        raise SystemExit("Unable to load: " + filename)

def stop_music():
    pygame.mixer.music.stop()

# Chargement des musiques par niveau
musique_niveau1 = load_sound("musique_niveau1.ogg", volume=0.5)
musique_niveau2 = load_sound("musique_niveau2.ogg", volume=0.5)

# Chargement des sons des personnages
son_cochon = load_sound("cochon.ogg", volume=0.5)
son_vache = load_sound("vache.ogg", volume=0.5)
son_poulet = load_sound("poulet.ogg", volume=0.5)
son_chien = load_sound("chien.ogg", volume=0.5)
son_fermier = load_sound("fermier.ogg", volume=0.5)

# Chargement des sons du loup
son_loup_spawn = load_sound("loup_spawn.ogg", volume=0.5)
son_loup_powerup = load_sound("loup_powerup.ogg", volume=0.5)