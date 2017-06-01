class TeamStats:
    def __init__(self):
        self.score = 0
        self.name = ""
        self.stats = {'players': [], 'subs': [], 'goals': [], 'cards': []}

    def players(self):
        print("PLAYERS:")
        for player in self.stats['players']:
            print(player)

    def addGoal(self, goal):
        wasPlayer = 0
        for g in self.stats['goals']:
            if goal['player'] in g['player']:
                g['minute'].append(goal['minute'][0])
                g['og'].append(goal['og'][0])
                wasPlayer = 1
                break
        if not wasPlayer:
            self.stats['goals'].append(goal)

    def get_goals(self):
        print("GOALS:")
        for goal in self.stats['goals']:
            result = ''
            for minute in goal['minute']:
                result += minute + "' "
            result += goal['player']
            print(result)

    def get_cards(self):
        print("CARDS:")
        for card in self.stats['cards']:
            print(card['minute'] + "' " + card['player'] + " " + card['color'])

    def get_subs(self):
        print("SUBS:")
        for sub in self.stats['subs']:
            print(sub['minute'] + "' " + sub['in'] + " for " + sub['out'])

    def get_score(self):
        print(self.score)

