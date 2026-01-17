import keyboard
import pygame


def play_sound() -> None:
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the sound file
    pygame.mixer.music.load('resources/quack.mp3')
    # Play the sound
    pygame.mixer.music.play()


quack_hotkey = 'F23'
exit_hotkey = 'F24'

if __name__ == '__main__':
    keyboard.add_hotkey('F23', play_sound, suppress=True)
    print(f"Press {quack_hotkey} to play the sound.")
    keyboard.wait(exit_hotkey, suppress=True)
