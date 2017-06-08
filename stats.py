class TeamStats:
    def __init__(self):
        self.score = 0
        self.name = ""
        self.stats = {'players': [], 'subs': [], 'goals': [], 'cards': []}
        self.parse = 0

    def get_players(self):
        if not self.parse:
            return "NO INFO AVAILABLE!"
        players = "PLAYERS:"
        for player in self.stats['players']:
            players += "\n" + player
        return players

    def addGoal(self, goal):
        wasPlayer = 0
        for g in self.stats['goals']:
            if goal['player'] in g['player']:
                g['minute'].append("," + goal['minute'][0])
                g['og'].append(goal['og'][0])
                wasPlayer = 1
                break
        if not wasPlayer:
            self.stats['goals'].append(goal)

    def get_goals(self):
        if not self.parse:
            return "NO INFO AVAILABLE!"
        result = "GOALS:"
        for goal in self.stats['goals']:
            result += "\n"
            for minute in goal['minute']:
                result += minute + "'"
            result += " " + goal['player']
            if goal['og'][0]:
                result += " (OG)"
        return result

    def get_cards(self):
        if not self.parse:
            return "NO INFO AVAILABLE!"
        cards = "CARDS:"
        for card in self.stats['cards']:
            cards += ("\n" + card['minute'] + "' " + card['player'] + " " + card['color'])
        return cards

    def get_subs(self):
        if not self.parse:
            return "NO INFO AVAILABLE!"
        subs = "SUBS:"
        for sub in self.stats['subs']:
            subs += ("\n" + sub['minute'] + "' " + sub['in'] + " for " + sub['out'])
        return subs

    def get_score(self):
        if not self.parse:
            return "NO INFO AVAILABLE!"
        return str(self.score)

    def print_summary(self):
        if not self.parse:
            print("NO INFO AVAILABLE!")
            return
        print("TEAM " + self.name)
        print(self.get_players())
        print(self.get_goals())
        print(self.get_cards())
        print(self.get_subs())
