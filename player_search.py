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
            'San Antonio Spurs': 'SAS',
            'Boston Celtics': 'BOS',
            'Denver Nuggets': 'DEN',
            'Minnesota Timberwolves': 'MIN',
            'Cleveland Cavaliers': 'CLE',
            'Philadelphia 76ers': 'PHI',
            'Phoenix Suns': 'PHO',
            'Sacramento Kings': 'SAC',
            'Indiana Pacers': 'IND',
            'Dallas Mavericks': 'DEN',
            'Miami Heat': 'MIA',
            'Orlando Magic': 'ORL',
            'Chicago Bulls': 'CHI',
            'Atlanta Hawks': 'ATL',
            'Toronto Raptors': 'TOR',
            'Charlotte Hornets': 'CHA',
            'Washington Wizards': 'WAS',
            'Detroit Pistons': 'DET',
            'Utah Jazz': 'UTA',
            'Houston Rockets': 'HOU',
            'Memphis Grizzlies': 'MEM',
            'Portland Trail Blazers': 'POR',
            'Milwaukee Bucks': 'MIL',
        }
        self.first_team_abbreviation = []
        self.second_team_abbreviation = []
        self.only_teams = []

    def format_teams(self, team_labels):
        for label in team_labels:
            label_split = label.split('+', 1)
            first_team = label_split[0].rstrip()
            second_team = label_split[1].lstrip()

            if self.team_abbreviations.get(first_team):
                self.first_team_abbreviation.append(self.team_abbreviations.get(first_team))
                first_is_a_team = True
            else:
                self.first_team_abbreviation.append(first_team)
                first_is_a_team = False

            if self.team_abbreviations.get(second_team):
                self.second_team_abbreviation.append(self.team_abbreviations.get(second_team))
                second_is_a_team = True
            else:
                self.second_team_abbreviation.append(second_team)
                second_is_a_team = False

            if first_is_a_team and second_is_a_team:
                self.only_teams.append(True)
            elif not first_is_a_team and second_is_a_team:
                self.only_teams.append(False)
                self.second_team_abbreviation.pop()
                self.second_team_abbreviation.append(second_team)

            elif first_is_a_team and not second_is_a_team:
                self.only_teams.append(False)
                self.first_team_abbreviation.pop()
                self.first_team_abbreviation.append(first_team)
            else:
                self.only_teams.append(False)

        return self.first_team_abbreviation, self.second_team_abbreviation, self.only_teams

    @staticmethod
    def get_page(first_team, second_team):
        return requests.get("https://www.basketball-reference.com/friv/players-who-played-for-multiple-teams"
                            "-franchises.fcgi?level=franch&t1=" + first_team + "&t2=" + second_team + "&t3"
                                                                                                      "=--&t4=--")

    @staticmethod
    def get_page_with_stats(first_team, second_team):
        if second_team[len(second_team)-1] != '+':
            print('URL with stat combination: https://www.statmuse.com/nba/ask?q=' + first_team + '+' + second_team +
                  '+players')
            return requests.get('https://www.statmuse.com/nba/ask?q=' + first_team + '+' + second_team + '+players')
        else:
            print('URL with stat combination: https://www.statmuse.com/nba/ask?q=' + first_team + '+' + second_team +
                  'players')
            return requests.get('https://www.statmuse.com/nba/ask?q=' + first_team + '+' + second_team + 'players')

    @staticmethod
    def get_needed_headers(player_response):
        soup = bs4.BeautifulSoup(player_response.text, 'html.parser')
        return soup.find_all('th', class_='left')

    @staticmethod
    def get_needed_headers_with_stats(player_response):
        soup1 = bs4.BeautifulSoup(player_response.text, 'html.parser')
        return soup1.find('td', class_='text-left px-2 py-1 sticky left-0 bg-white')

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

    def add_players_with_stats(self, td_tag):
        if td_tag:
            a_tag = td_tag.find('a')
            if a_tag:
                print("Added player: " + a_tag.text)
                self.players.append(a_tag.text)
            else:
                print("No <a> tag found in the paragraph.")
        else:
            print("Paragraph not found.")
            self.players.append("No players in that criteria found.")
