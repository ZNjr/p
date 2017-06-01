import stats
import re


def isOwnGoal(raportLine):
    return re.search(r"\(og\)", raportLine, re.I)


def cardColor(card):
    if re.match(r"red|r", card, re.I):
        return "R"
    else:
        return "Y"


class GameParser:
    headParser = re.compile(
        r"^(?:((?:[a-z]+ ){1,3})(?:vs|v.|) ((?:[a-z]+ ){1,3})(?:@|venue|at) ((?:[a-z]+ )+)on ([1-9][0-9]? (?:(?:[a-z]+)|(?:[1-9][0-9])) \d{4}))$",
        re.I | re.M)

    playersParser = re.compile(r"^([1-9][0-9]?\s+([a-z.]+(\s(([a-z.]*)|([a-z.]+\s[a-z.]+)))?))$", re.M | re.I)

    minute = "(?:(\d{1,3}(?:\+\d+)?)(?:m|'|`|min))"

    goalParser = re.compile(r"^(" + minute + " +(?:g+o+a+l+).*)$", re.M | re.I)
    cardParser = re.compile(r"^(" + minute + " +(?:card +(yellow|y|red|r)).*)$", re.M | re.I)
    subParser = re.compile(
        r"^(" + minute + " +(?:substitution|sub) +(?:out|off)((?: +[a-z.]+)+) +(?:in|on)((?: +[a-z.]+)+))",
        re.M | re.I)

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.head = {'home': "", 'away': "", 'scores': "", 'venue': "", 'data': ""}
        self.parsed = 0

    def parse(self, raport):
        header = self.headParser.findall(raport)
        self.insertGameStats(header[0])
        players = self.playersParser.findall(raport)
        self.insertPlayersData(players)
        subs = self.subParser.findall(raport)
        self.insertSubStats(subs)
        gools = self.goalParser.findall(raport)
        self.insertGoalsStats(gools)
        cards = self.cardParser.findall(raport)
        self.insertCardsStats(cards)
        self.parsed = 1
        self.team1.parse = 1
        self.team2.parse = 1

    def insertPlayersData(self, players):
        ct = 0
        for player in players:
            if ct < 11:
                self.team1.stats['players'].append(player[1])
            else:
                self.team2.stats['players'].append(player[1])
            ct = ct + 1

    # teamOfFoundPlayer return (team , player)
    def teamOfFoundPlayer(self, raportLine):
        for player in self.team1.stats['players']:
            if player in raportLine:
                return {'team': self.team1, 'player': player}
        for player in self.team2.stats['players']:
            if player in raportLine:
                return {'team': self.team2, 'player': player}
        for sub in self.team1.stats['subs']:
            if sub['in'] in raportLine:
                return {'team': self.team1, 'player': sub['in']}
        for sub in self.team2.stats['subs']:
            if sub['in'] in raportLine:
                return {'team': self.team2, 'player': sub['in']}

    def insertGameStats(self, gameStats):
        self.head['home'] = gameStats[0].strip()
        self.head['away'] = gameStats[1].strip()
        self.head['venue'] = gameStats[2].strip()
        self.head['data'] = gameStats[3]
        self.team1.name = self.head['home']
        self.team2.name = self.head['away']

    def insertGoalsStats(self, goals):
        home = 0
        away = 0
        for goal in goals:
            playerDate = self.teamOfFoundPlayer(goal[0])
            player = playerDate['player']
            team = playerDate['team']
            ogTeam = self.team1
            if team is self.team1:
                ogTeam = self.team2
            if isOwnGoal(goal[0]):
                if team is self.team1:
                    away = away + 1
                if team is self.team2:
                    home = home + 1
                ogTeam.addGoal({'player': player, 'minute': [goal[1]], 'og': [1]})
            else:
                if team is self.team1:
                    home = home + 1
                if team is self.team2:
                    away = away + 1
                team.addGoal({'player': player, 'minute': [goal[1]], 'og': []})
            self.head['scores'] = str(home) + ":" + str(away)
            self.team1.score = home
            self.team2.score = away

    def insertCardsStats(self, cards):
        for card in cards:
            playerData = self.teamOfFoundPlayer(card[0])
            player = playerData['player']
            team = playerData['team']
            team.stats['cards'].append({'player': player, 'minute': card[1], 'color': cardColor(card[2])})

    def insertSubStats(self, subs):
        for sub in subs:
            playerData = self.teamOfFoundPlayer(sub[0])
            team = playerData['team']
            team.stats['subs'].append({'minute': sub[1], 'out': sub[2].strip(), 'in': sub[3].strip()})

    def print_summary(self):
        if not self.parsed:
            print("NO INFO AVAILABLE!")
            return
        print("HOME: " + self.head['home'])
        print("AWAY: " + self.head['away'])
        print("SCORE: " + self.head['scores'])
        print("VENUE: " + self.head['venue'])
        print("DATA: " + self.head['data'] + "\n")
        self.team1.print_summary()
        print("")
        self.team2.print_summary()
