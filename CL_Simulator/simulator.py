import random

teams = [
    {"name": 'Arsenal', "rating": 97},
    {"name": 'PSG', "rating": 98},
    {"name": 'Bayern', "rating": 95},
    {"name": 'Inter', "rating": 90},
    {"name": 'Real Madrid', "rating": 94},
    {"name": 'Dortmund', "rating": 89},
    {"name": 'Chelsea', "rating": 91},
    {"name": 'Sporting', "rating": 88}
]

#     ({"name": 'Manchester City', "rating": 94},    {"name": 'Atalanta', "rating": 87},
#      {"name": 'Newcastle', "rating": 89},)
#     {"name": 'Atlético Madrid', "rating": 88},    {"name": 'Liverpool', "rating": 93},
# {"name": 'Galatasaray', "rating": 82},
#     {"name": 'PSV', "rating": 81},    {"name": 'Tottenham', "rating": 88},    {"name": 'Leverkusen', "rating": 89},
#     {"name": 'Barcelona', "rating": 90},    {"name": 'Qarabag', "rating": 67},    {"name": 'Napoli', "rating": 85},
# {"name": 'Juventus', "rating": 82},
#     {"name": 'Monaco', "rating": 75},    {"name": 'Paphos', "rating": 62},
#     {"name": 'Saint-Gilloise', "rating": 72},    {"name": 'FC Bruges', "rating": 78},
#     {"name": 'Athletic Bilbao', "rating": 78},    {"name": 'Eintracht Frankfurt', "rating": 80},
#     {"name": 'FC Copenhagen', "rating": 79},    {"name": 'Benfica', "rating": 87},
#     {"name": 'Slavia Praha', "rating": 72},    {"name": 'Bodo/Glimt', "rating": 76},
#     {"name": 'Olympiakos', "rating": 75},    {"name": 'Villareal', "rating": 71},
#     {"name": 'Kairat', "rating": 65},    {"name": 'Ajax', "rating": 80}
# ]


class Team:
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating   # you can store strength, ELO, etc.

    def __repr__(self):
        return f"Team({self.name}, rating={self.rating})"


class League:
    def __init__(self):
        self.teams = []
        self.fixtures = []

    def add_team(self, team):
        if len(self.teams) >= 8:
            raise ValueError("League already has 36 teams.")
        self.teams.append(team)

    def list_teams(self):
        for t in self.teams:
            print(t)

    def get_team_by_name(self, name):
        for team in self.teams:
            if team.name.lower() == name.lower():  # case-insensitive match
                return team
        return None  # if not found

    def generate_schedule(self, matches_per_team=4):
        self.fixtures = []
        team_names = [team.name for team in self.teams]

        matches_played = {team: 0 for team in team_names}
        opponents_played = {team: set() for team in team_names}

        while any(matches_played[t] < matches_per_team for t in team_names):
            # chooses 2 different teams
            t1, t2 = random.sample(team_names, 2)

            # print("Trying:", t1, t2)

            if (t2 not in opponents_played[t1] and
                matches_played[t1] < matches_per_team and
                matches_played[t2] < matches_per_team):

                if random.random() < 0.5:
                    home, away = t1, t2
                else:
                    home, away = t2, t1


                home_team_dict = self.get_team_by_name(home)
                away_team_dict = self.get_team_by_name(away)

                self.fixtures.append((home_team_dict, away_team_dict))



                matches_played[t1] += 1
                matches_played[t2] += 1
                opponents_played[t1].add(t2)
                opponents_played[t2].add(t1)

                if matches_played[t1] == 8:
                    team_names.remove(t1)

                if matches_played[t2] == 8:
                    team_names.remove(t2)

                print(f'Home {home} and Away {away}')
                print(f'{home} played {matches_played[home]} and {away} played {matches_played[away]}')


                print(len(self.fixtures))




league = League()




for club in teams:
    league.add_team(Team(name=club["name"], rating=club["rating"]))

league.generate_schedule()

print(league.fixtures)

def simulate_match(team1, team2):
    rating1 = team1["rating"]
    rating2 = team2["rating"]

    exp1 = 1.2 + (rating1 - rating2) * 0.03
    exp2 = 1.2 + (rating2 - rating1) * 0.03

    exp1 = max(0.2, exp1)
    exp2 = max(0.2, exp2)

    goals1 = max(0, int(random.gauss(exp1, 1)))
    goals2 = max(0, int(random.gauss(exp2, 1)))

    winner = (
        team1["name"] if goals1 > goals2
        else team2["name"] if goals2 > goals1
        else "Draw"
    )

    return {
        "Home Team": team1["name"],
        "Away Team": team2["name"],
        "Home Goals": goals1,
        "Away Goals": goals2,
        "Winner": winner
    }


def score_beautifier(result):
    print(f'{result["Home Team"]} {result["Home Goals"]} - {result["Away Team"]} {result["Away Goals"]}')

