from ..teammatch.teammatchboard import TeamMatchBoard


class TeamMatchInfo(object):
    def __init__(self, data):
        self.id = data.get('@id', None)
        self.name = data.get('name', None)
        self.url = data.get('url', None)
        self.start_time = data.get('start_time', None)
        self.end_time = data.get('end_time', None)
        self.status = data.get('status', None)
        self.numberOfBoards = data.get('boards', None)
        self.settings = TeamMatchSettings(data.get('settings', None))
        self.teams = TeamMatchTeams(data.get('teams', None))
        # create a teammatchboard for each board in the match
        self.boards = [TeamMatchBoard(self.id + "/" + str(x)) for x in range(1,data.get('boards', None))]


class TeamMatchSettings(object):
    def __init__(self, data) -> None:
        self.rules = data.get('rules', None)
        self.time_class = data.get('time_class', None)
        self.time_control = data.get('time_control', None)
        self.min_team_players = data.get('min_team_players', None)
        self.max_team_players = data.get('max_team_players', None)
        self.min_required_games = data.get('min_required_games', None)
        self.autostart = data.get('autostart', None)

class TeamMatchTeams(object):
    def __init__(self, data) -> None:
        self.team1 = TeamMatchTeam(data.get('team1', None))
        self.team2 = TeamMatchTeam(data.get('team2', None))


class TeamMatchTeam(object):
    def __init__(self, data) -> None:
        self.id = data.get('@id', None)
        self.name = data.get('name', None)
        self.url = data.get('url', None)
        self.score = data.get('score', None)
        self.result = data.get('result', None)
        self.players = [TeamMatchPlayer(playerdata) for playerdata in data.get('players', [])]

class TeamMatchPlayer(object):
    def __init__(self, data) -> None:
        self.username = data.get('username', None)
        self.stats = data.get('stats', None)
        self.status = data.get('status', None)
        self.played_as_white = data.get('played_as_white', None)
        self.played_as_black = data.get('played_as_black', None)
        self.board = TeamMatchBoard(data.get('board', None))

