import stats
import re


class GameParser:
    teamParser = re.compile('Lineup [a-zA-Z0-9]*')

    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

    def parse(self, raport):
        splitRaport = raport.splitlines()
        for line in splitRaport:
            for m in self.teamParser.finditer(line):
                print m.string


team1 = stats.TeamStats()
team2 = stats.TeamStats()
team1.players.append("e")
parser = GameParser(team1, team2)
parser.parse("Lineup Arsenal\nLineup Leicester City\n")
