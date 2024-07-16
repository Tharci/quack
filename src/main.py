import keyboard
import pygame


def play_sound() -> None:
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the sound file
    pygame.mixer.music.load('resources/quack.mp3')
    # Play the sound
    pygame.mixer.music.play()


if __name__ == '__main__':
    keyboard.add_hotkey('ctrl+shift+alt+q', play_sound, suppress=True)
    print("Press Ctrl+Shift+Alt+Q to play the sound.")
    keyboard.wait('ctrl+shift+alt+w', suppress=True)
