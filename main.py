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

first_team_list, second_team_list, only_teams = ps.format_teams(aria_labels)

for i in range(len(first_team_list)):
    if only_teams[i]:
        response = ps.get_page(first_team_list[i], second_team_list[i])
        ps.filter_players(ps.get_players_from_headers(ps.get_needed_headers(response)))
    else:
        if '+' in first_team_list[i]:
            first_team_list[i] = first_team_list[i].replace('+', '%2B')
        first_team = first_team_list[i].replace(' ', '+')

        if '+' in second_team_list[i]:
            second_team_list[i] = second_team_list[i].replace('+', '%2B')
        second_team = second_team_list[i].replace(' ', '+')

        response = ps.get_page_with_stats(first_team, second_team)

        response.raise_for_status()
        print(response.status_code)

        ps.add_players_with_stats(ps.get_needed_headers_with_stats(response))

for player in ps.players:
    print(player)

messagebox.showinfo("Results", "The correct players have been found. Now the application will fill out the grid")

im = InputManager(ps.players)

im.set_up_page()
im.execute()

messagebox.showinfo("Final", "The application has finished. Hope you enjoyed!")
