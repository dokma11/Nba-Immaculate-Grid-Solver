import requests
import bs4
from player_search import PlayerSearch
from input_manager import InputManager
from gui import Gui
from tkinter import messagebox

gui = Gui()
gui.root.mainloop()

res = ""
if gui.return_value != "":
    res = requests.get(gui.return_value)

res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

button_elements = soup.find_all('button', class_='w-full h-full')

aria_labels = [button.get('aria-label') for button in button_elements]

print(aria_labels)

ps = PlayerSearch()

first_team_list, second_team_list = ps.format_teams(aria_labels)

for i in range(len(first_team_list)):
    response = ps.get_page(first_team_list[i], second_team_list[i])
    ps.filter_players(ps.get_players_from_headers(ps.get_needed_headers(response)))

for player in ps.players:
    print(player)

messagebox.showinfo("Results", "The correct players have been found. Now the application will fill out the grid")

im = InputManager(ps.players)

im.set_up_page()
im.execute()

messagebox.showinfo("Final", "The application has finished. Hope you enjoyed!")
