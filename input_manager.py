import pyautogui
import time
import pyperclip


class InputManager:
    def __init__(self, filtered_players):
        self.index = 0
        self.filtered_players = filtered_players

    def enter_player_name(self):
        time.sleep(1)
        pyperclip.copy(self.filtered_players[self.index])
        pyautogui.hotkey('ctrl', 'v', interval=0.25)
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('escape')
        time.sleep(1)

    def click(self, x, y):
        pyautogui.click(x, y)
        self.enter_player_name()
        self.index += 1

    def execute(self):
        # Enter the top left player
        self.click(765, 558)

        # Enter the top middle player
        self.click(950, 558)

        # Enter the top right player
        self.click(1125, 558)

        # Enter the middle left player
        self.click(765, 735)

        # Enter the center player
        self.click(950, 735)

        # Enter the middle right player
        self.click(1125, 735)

        # Enter the bottom left player
        self.click(765, 915)

        # Enter the bottom middle player
        self.click(950, 915)

        # Enter the bottom right player
        self.click(1125, 915)

    @staticmethod
    def set_up_page():
        # Scroll to the top
        time.sleep(2)
        pyautogui.click(1908, 185)
        time.sleep(2)
