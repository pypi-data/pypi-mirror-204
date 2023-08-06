from ..tournament.tournamentroundplayer import TournamentRoundPlayer
from ...tournamentroundgroup import TournamentRoundGroup

class TournamentRoundInfo(object):
    def __init__(self, data):
        self.groups = [TournamentRoundGroup(group) for group in data.get('groups', [])] 
        self.players = [TournamentRoundPlayer(playerdata) for playerdata in data.get('players', [])] 
    
    
