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
        self.first_team_abbreviation = []
        self.second_team_abbreviation = []

    def format_teams(self, team_labels):
        for label in team_labels:
            label_split = label.split('+', 1)
            first_team = label_split[0].rstrip()
            second_team = label_split[1].lstrip()

            self.first_team_abbreviation.append(self.team_abbreviations.get(first_team, first_team[:3].upper()))
            self.second_team_abbreviation.append(self.team_abbreviations.get(second_team, second_team[:3].upper()))

        return self.first_team_abbreviation, self.second_team_abbreviation

    @staticmethod
    def get_page(first_team, second_team):
        return requests.get("https://www.basketball-reference.com/friv/players-who-played-for-multiple-teams"
                            "-franchises.fcgi?level=franch&t1=" + first_team + "&t2=" + second_team + "&t3"
                                                                                                      "=--&t4=--")

    @staticmethod
    def get_needed_headers(player_response):
        soup = bs4.BeautifulSoup(player_response.text, 'html.parser')
        return soup.find_all('th', class_='left')

    @staticmethod
    def get_players_from_headers(th_elements):
        # Extract the text from the <th> element
        players = []
        for th_element in th_elements:
            if th_element:
                players.append(th_element.get_text(strip=True))
            else:
                print("Th element not found.")

        return players

    def filter_players(self, players):
        for player in reversed(players):
            if player not in self.players:
                self.players.append(player)
                break
