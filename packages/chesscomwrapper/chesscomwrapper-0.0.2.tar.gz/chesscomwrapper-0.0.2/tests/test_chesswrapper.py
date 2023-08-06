import random
import threading




from src.chessclub import Club
from src.club.clubprofile import ClubProfile
from src.chessplayer import ChessPlayer
from src.player.chessplayerstats import ChessPlayerStats
from src.player.playerarchive import PlayerArchive
from src.player.playergames import ChesscomGame
from src.player.chessplayerprofile import ChessPlayerProfile

from src.player.playertournament import PlayerTournaments
from src.player.playerclub import PlayerClub

import src.chesswrapper as chesswrapper 
import unittest


from src.tournament.tournamentinfo import TournamentInfo
from src.tournament.tournamnetroundinfo import TournamentRoundInfo
from src.tournament.tournamentroundgroup import TournamentRoundGroup
from src.tournament.tournamentroundgroupinfo import TournamentRoundGroupInfo

from src.teammatch.teammatchinfo import TeamMatchInfo
from src.teammatch.teammatchboardinfo import TeamMatchBoardInfo

from src.country.countryinfo import CountryInfo

from src.chesscomhandlers.dailypuzzlehandler import PuzzleInfo

from src.chessstreamer import ChessStreamer
from src.streamer.chessstreamerinfo import ChessStreamerInfo

from src.leaderboards.leaderboardsinfo import LeaderboardsInfo

class PlayerTest(unittest.TestCase):
    def test_player_profile(self):
        """Tests an API call to get a player's info"""

        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("nicolapanozzo")
        
        player.getProfile()
        

        "Player should be a ChessPlayer object"
        assert isinstance(player.profile, ChessPlayerProfile ), "Player should be a ChessPlayer object"
        assert player.profile.name == "Nicola Panozzo", "Username should be Nicola Panozzo, not {}".format(player.profile.name)
    
    def test_rate_limit(self):
        """Tests the rate limit"""
        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("nicolapanozzo")
        player.getProfile()
        
        
        threadPool = []
        for i in range(0, 100):
            playert = chess_instance.getPlayer("nicolapanozzo{}".format(i*random.randint(1,1000)))
            threadPool.append(threading.Thread(target=playert.getProfile))
        # start threads at the same time
        for thread in threadPool:
            thread.start()
        # wait for all threads to finish
        for thread in threadPool:
            thread.join()

        assert threadPool[60].is_alive() == False, "Thread should be dead"

    def test_player_stats(self):
        """Tests an API call to get a player's stats"""

        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("nicolapanozzo")
        player.getStats()
        "Player.stats should be a ChessPlayerStats object"
        assert isinstance(player.stats, ChessPlayerStats ), "Player should be a ChessPlayer object"
        assert player.stats.tactics.highest.rating == 2539, "Games should be 2539, not {}".format(player.stats.tactics.highest.rating)
    
    def test_player_games(self):
        """Tests an API call to get a player's games"""

        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("erik")
        player.getPlayerGames()

        "Player.games should be a list of ChesscomGame objects"
        assert isinstance(player.games[0], ChesscomGame), "Game[0] should be a ChesscomGame object"
        # assert player.games[0].pgn.game().headers["Result"] == "*", "Game result should be *, not {}".format(player.games[0].pgn.game().headers["Result"])

    def test_player_games_to_move(self):
        """Tests an API call to get a player's games"""

        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("erik")
        player.getPlayerGamesToMove()

        "Player.games should be a list of ChesscomGame objects"
        assert isinstance(player.gamesToMove[0], ChesscomGame),  "Game[0] should be a ChesscomGame object"
        assert len(player.gamesToMove) == 1

    def test_player_archives(self):
        """Tests an API call to get a player's archives"""

        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("erik")
        player.getPlayerArchives()

        "Player.archives should be a list of ChesscomGame objects"
        assert isinstance(player.archives[0], PlayerArchive),  "Game[0] should be a ChesscomGame object"
        assert len(player.archives) == 189 , "Archives should be 189, not {}".format(len(player.archives))

    def test_player_archived_games(self):
        """Tests an API call to get a player's archives"""

        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("erik")
        player.getPlayerArchives()
        player.archives[0].getGames()
        "Player.archives should be a list of ChesscomGame objects"
        assert isinstance(player.archives[0].games[0], ChesscomGame),  "Archive.games should be a list(ChesscomGame) object"
        assert player.archives[0].games[0].rated == True , "In the first game of the first archive should be rated == True, not {}".format(player.archives[0].games[0].rated)
    
    def test_player_clubs(self):
        """Tests an API call to get a player's clubs"""

        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("nicolapanozzo")
        player.getPlayerClubs()
        "Player.archives should be a list of ChesscomGame objects"
        assert isinstance(player.clubs[1], PlayerClub),  "Archive.games should be a list(ChesscomGame) object"
        assert player.clubs[1].name == "Bonobo" , "In the first game of the first archive should be rated == True, not {}".format(player.archives[0].games[0].rated)

    def test_player_tournaments(self):
        """Tests an API call to get a player's tournaments"""

        chess_instance = chesswrapper.ChessWrapper()
        player = chess_instance.getPlayer("nicolapanozzo")
        player.getPlayerTournaments()
        "Player.archives should be a list of ChesscomGame objects"
        assert isinstance(player.tournaments, PlayerTournaments),  "player.tournaments should be a PlayerTournaments object"
        assert len(player.tournaments.finished) == 1 , "the number of finished tournaments should be 1, not {}".format(len(player.tournaments.finished))

    def test_titled_players(self):
        """Tests an API call to get all the titled players"""

        chess_instance = chesswrapper.ChessWrapper()
        titled_players = chess_instance.getTitledPlayers()
        "Player.archives should be a list of ChesscomGame objects"
        assert isinstance(titled_players[0], ChessPlayer),  "Archive.games should be a list(ChesscomGame) object"
        # assert titled_players[0].name == "Magnus Carlsen" , "In the first game of the first archive should be rated == True, not {}".format(player.archives[0].games[0].rated)

class ClubTest(unittest.TestCase):
    def test_club_info(self):
        """Tests an API call to get a club's info"""

        chess_instance = chesswrapper.ChessWrapper()
        club = chess_instance.getClub("bonobo")
        club.getProfile()
        "Club.info should be a ClubInfo object"
        assert isinstance(club.profile, ClubProfile),  "Club.info should be a ClubInfo object"
        assert club.profile.name == "Bonobo" , "Club name should be Bonobo, not {}".format(club.profile.name)
        assert club.profile.average_daily_rating == 794, "Club average_daily_rating should be 794, not {}".format(club.profile.average_daily_rating)

    def test_club_members(self):
        """Tests an API call to get a club's members"""

        chess_instance = chesswrapper.ChessWrapper()
        club = chess_instance.getClub("bonobo")
        club.getMembers()
        "Club.members should be a list of ChessPlayer objects"
        assert isinstance(club.members[0].player, ChessPlayer),  "Club.members should be a list of ChessPlayer objects"
        assert club.members[0].player.username == "capitanoorsoblu" , "Club member should be capitanoorsoblu, not {}".format(club.members[0].player.username)



class TournamentTest(unittest.TestCase):
    def test_tournament_info(self):
        """Tests an API call to get a tournament's info"""

        chess_instance = chesswrapper.ChessWrapper()
        tournament = chess_instance.getTournament("https://api.chess.com/pub/tournament/-33rd-chesscom-quick-knockouts-1401-1600")
        tournament.getInfo()
        "Club.info should be a ClubInfo object"
        assert isinstance(tournament.info, TournamentInfo),  "Tournament.info should be a TournamentInfo object"
        assert tournament.info.creator == "Patzer24" , "Tournament creator should be Patzer24, not {}".format(tournament.info.creator)
        assert len(tournament.info.players) == 399, "Tournament parecipants numeber should be 399, not {}".format(len(tournament.info.players))

    def test_tournament_round_info(self):
        # """Tests an API call to get a tournament's round info"""
        chess_instance = chesswrapper.ChessWrapper()
        tournament = chess_instance.getTournament("https://api.chess.com/pub/tournament/-33rd-chesscom-quick-knockouts-1401-1600")
        tournament.getInfo()
        print(tournament.info.rounds)
        tournament.info.rounds[0].getInfo()
        print(tournament.info.rounds[0].info)
        assert isinstance(tournament.info.rounds[0].info, TournamentRoundInfo),  "Round.info should be a TournamentRoundInfo object"
        assert len(tournament.info.rounds[0].info.groups) == 67, "Tournament groups number should be 67, not {}".format(len(tournament.info.rounds[0].info.groups))
        


    def test_tournament_round_group(self):
        # """Tests an API call to get a tournament's round group info"""
        chess_instance = chesswrapper.ChessWrapper()
        tournament = chess_instance.getTournament("https://api.chess.com/pub/tournament/-33rd-chesscom-quick-knockouts-1401-1600")
        tournament.getInfo()
        print(tournament.info.rounds)
        tournament.info.rounds[0].getInfo()
        # print(tournament.info.rounds[0].info.groupsUrls)
        tournament.info.rounds[0].info.groups[0].getInfo()
        

        assert isinstance(tournament.info.rounds[0].info, TournamentRoundInfo),  "Round.info should be a TournamentRoundInfo object"
        assert isinstance(tournament.info.rounds[0].info.groups[0], TournamentRoundGroup),  "Round.info.groups[0] should be a TournamentRoundGroup object"
        assert isinstance(tournament.info.rounds[0].info.groups[0].info, TournamentRoundGroupInfo),  "Round.info.groups[0].info should be a TournamentRoundGroupInfo object"
        assert tournament.info.rounds[0].info.groups[0].info.games[0].white.username == "Rockaround" , "The first player with white in the first game of the first group of the first round Rockaround, not {}".format(tournament.info.rounds[0].info.groups[0].info.games[0].white.username)

class TeamMatchTest(unittest.TestCase):
    def test_team_match_info(self):
        """Tests an API call to get a team match's info"""

        chess_instance = chesswrapper.ChessWrapper()
        team_match = chess_instance.getTeamMatch("https://api.chess.com/pub/match/53")
        team_match.getInfo()
        "TeamMatch.info should be a TeamMatchInfo object"
        assert isinstance(team_match.info, TeamMatchInfo),  "TeamMatch.info should be a TeamMatchInfo object"
        assert team_match.info.teams.team1.name == "International Flagbearers" , "TeamMatch team1 should be International Flagbearers, not {}".format(team_match.info.teams.team1.name)
        assert team_match.info.teams.team2.name == "Team Italia" , "TeamMatch team2 should be Team Italia, not {}".format(team_match.info.teams.team2.name)
    
    def test_team_match_board_info(self):
        """Tests an API call to get a team match's info"""

        chess_instance = chesswrapper.ChessWrapper()
        team_match = chess_instance.getTeamMatch("https://api.chess.com/pub/match/53")
        team_match.getInfo()
        team_match.info.boards[0].getInfo()
        
        assert isinstance(team_match.info.boards[0].info, TeamMatchBoardInfo),  "TeamMatch.info.boards[0].info should be a TeamMatchBoardInfo object"
        assert team_match.info.boards[0].info.board_scores.result == "0.5-1.5" , "The result should be 0.5-1.5, not {}".format(team_match.info.boards[0].info.board_scores.result)

class CountryTest(unittest.TestCase):
    def test_country_info(self):
        """Tests an API call to get a country's info"""

        chess_instance = chesswrapper.ChessWrapper()
        country = chess_instance.getCountry("IT")
        country.getInfo()
        "Country.info should be a CountryInfo object"
        assert isinstance(country.info, CountryInfo),  "Country.info should be a CountryInfo object"
        assert country.info.name == "Italy" , "Country name should be Italy, not {}".format(country.info.name)
    
    def test_country_players(self):
        """Tests an API call to get a country's players"""

        chess_instance = chesswrapper.ChessWrapper()
        country = chess_instance.getCountry("IT")
        country.getPlayers()

        "Country.players should be a list of ChessPlayer objects"
        assert isinstance(country.players[0], ChessPlayer),  "Country.players should be a list of ChessPlayer objects"
        assert country.players[0].username == "--hugo--" , "Country player should be --hugo--, not {}".format(country.players[0].username)

    def test_country_clubs(self):
        """Tests an API call to get a country's players"""

        chess_instance = chesswrapper.ChessWrapper()
        country = chess_instance.getCountry("IT")
        country.getClubs()
        country.clubs[0].getProfile()

        print(country.clubs[0].profile.name)
        "Country.players should be a list of ChessPlayer objects"
        assert isinstance(country.clubs[0], Club),  "country.clubs[0] should be a Club"
        assert country.clubs[0].id == "italys-finest" , "Country club id should be italys-finest, not {}".format(country.clubs[0].id)

class PuzzleTest(unittest.TestCase):
    def test_daily_puzzle(self):
        """Tests an API call to get a puzzle's info"""

        chess_instance = chesswrapper.ChessWrapper()
        puzzle = chess_instance.getDailyPuzzle()
        "Puzzle.info should be a PuzzleInfo object"
        assert isinstance(puzzle.info, PuzzleInfo),  "Puzzle.info should be a PuzzleInfo object"
        assert puzzle.info.title == "Loose Piece Yo-Yo" , "Puzzle id should be 'Loose Piece Yo-Yo', not {}".format(puzzle.info.title)

    def test_random_puzzle(self):
        """Tests an API call to get a puzzle's info"""

        chess_instance = chesswrapper.ChessWrapper()
        puzzle = chess_instance.getRandomPuzzle()
        print(puzzle.info.title)
        "Puzzle.info should be a PuzzleInfo object"
        assert isinstance(puzzle.info, PuzzleInfo),  "Puzzle.info should be a PuzzleInfo object"
        # assert puzzle.info.title == "Loose Piece Yo-Yo" , "Puzzle id should be 'Loose Piece Yo-Yo', not {}".format(puzzle.info.title)

class StreamerTest(unittest.TestCase):
    def test_streamers(self):
        """Tests an API call to get streamers' info"""

        chess_instance = chesswrapper.ChessWrapper()
        streamers = chess_instance.getStreamers()
        "Streamers should be a list of Streamer objects"
        assert isinstance(streamers[0], ChessStreamer),  "Streamers should be a list of Streamer objects"
        assert isinstance(streamers[0].info, ChessStreamerInfo),  "Streamers should be a list of Streamer objects"
        assert streamers[0].info.username == "lularobs" , "Streamer should be lularobs, not {}".format(streamers[0].username)

class LeaderboardsTest(unittest.TestCase):
    def test_leaderboard(self):
        """Tests an API call to get a leaderboard's info"""
            
        chess_instance = chesswrapper.ChessWrapper()
        leaderboards = chess_instance.getLeaderboards()
        
        "Leaderboard.info should be a LeaderboardInfo object"
        assert isinstance(leaderboards.info, LeaderboardsInfo),  "Leaderboard.info should be a LeaderboardInfo object"
        assert leaderboards.info.daily[0].rank == 1 , "Leaderboard rank of first player should be 1, not {}".format(leaderboards.info.daily[0].rank)