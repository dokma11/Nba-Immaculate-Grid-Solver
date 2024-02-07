import requests
import bs4


class PlayerSearch:
    def __init__(self):
        self.players = []
        self.team_abbreviations = {
            'Brooklyn Nets': 'NJN',
            'Golden State Warriors': 'GSW',
            'Los Angeles Lakers': 'LAL',
            'Los Angeles Clippers': 'LAC',
            'New Orleans Pelicans': 'NOP',
            'New York Knicks': 'NYK',
            'Oklahoma City Thunder': 'OKC',
            'San Antonio Spurs': 'SAS'
        }

    def format_teams(self, team_labels):
        for label in team_labels:
            label_split = label.split('+', 1)
            first_team = label_split[0].rstrip()
            second_team = label_split[1].lstrip()

            first_team_abbreviation = self.team_abbreviations.get(first_team, first_team[:3].upper())
            second_team_abbreviation = self.team_abbreviations.get(second_team, second_team[:3].upper())

            return first_team_abbreviation, second_team_abbreviation

    @staticmethod
    def get_page(first_team, second_team):
        return requests.get("https://www.basketball-reference.com/friv/players-who-played-for-multiple-teams"
                            "-franchises.fcgi?level=franch&t1=" + first_team + "&t2=" + second_team + "&t3"
                                                                                                      "=--&t4=--")

    @staticmethod
    def get_players(player_response):
        player_response.raise_for_status()
        soup = bs4.BeautifulSoup(player_response.text, 'html.parser')
        return soup.find_all('th', class_='left')

    def filter_players(self, th_elements):
        # Extract the text from the <th> element
        player = []
        for th_element in th_elements:
            if th_element:
                player.append(th_element.get_text(strip=True))
            else:
                print("Th element not found.")

        i = 1
        not_appended = True
        while not_appended:
            if player[len(player) - i] not in self.players:
                self.players.append(player[len(player) - i])
                not_appended = False
            else:
                i += 1
