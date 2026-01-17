import keyboard
import pygame
import requests
import os
import threading
from rate_limiter import RateLimiter, RateLimitError, RateLimitResult


HA_API_KEY = os.environ['HA_API_KEY']
quack_hotkey = 'F23'
exit_hotkey = 'F24'

rate_limiter = RateLimiter(min_interval_seconds=2)

def send_quack():
    try:
        url = "https://backend.m-toth.com/ha/quack"
        r = requests.post(url, headers={"X-API-Key": HA_API_KEY}, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print(f"HA quack request error: {e}")


def play_sound() -> None:
    pygame.mixer.music.play()
    try:
        rate_limiter.enforce()
    except RateLimitError as e:
        print(e)
        return

    threading.Thread(target=send_quack, daemon=True).start()


if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.music.load('resources/quack.mp3')
    keyboard.add_hotkey('F23', play_sound)
    print(f"Press {quack_hotkey} to play the sound.")
    keyboard.wait(exit_hotkey)
