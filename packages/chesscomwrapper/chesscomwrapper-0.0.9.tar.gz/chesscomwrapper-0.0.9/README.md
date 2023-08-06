## chesscomwrapper 
This is a wrapper for the chess.com API. **It is a work in progress and is not complete.**

The purpose of this package is to provide a simple way to access the chess.com API. It is not meant to be a complete wrapper for the API, but rather a simple way to access the data you need.

The API is documented here: https://www.chess.com/news/view/published-data-api and it is the source of the data used in this package.

### Installation
To install this package, run the following command in your terminal:
`pip install chesscomwrapper`

### Usage
To use this package, import it into your project and create a new instance of the ChesscomWrapper class. You can then use the methods to access the data you need.



## Player
This instance of the Player class will contain the data for the player you requested.
# Example
```
chesscomWrapper = ChesscomWrapper()
player = chesscomWrapper.getPlayer()
```
## Club
This instance of the Club class will contain the data for the club you requested.

# Example
```
chesscomWrapper = ChesscomWrapper()
club = chesscomWrapper.getClub()
```
## Country
This instance of the Country class will contain the data for the country you requested.
# Example
```
chesscomWrapper = ChesscomWrapper()
country = chesscomWrapper.getCountry()
```
## DailyPuzzle
This instance of the DailyPuzzle class will contain the data for the puzzle of the current day.
# Example
```
chesscomWrapper = ChesscomWrapper()
dailyPuzzle = chesscomWrapper.getDailyPuzzle()
```
## RandomPuzzle
This instance of the RandomPuzzle class will contain the data for a random puzzle.
# Example
```
chesscomWrapper = ChesscomWrapper()
randomPuzzle = chesscomWrapper.getRandomPuzzle()
```
## StreamersInfo
This instance of the StreamersInfo class will contain the data for the streamers.
# Example
```
chesscomWrapper = ChesscomWrapper()
streamersInfo = chesscomWrapper.getStreamersInfo()
```
## Leaderboards
This instance of the Leaderboards class will contain the data for the leaderboards.
# Example
```
chesscomWrapper = ChesscomWrapper()
leaderboards = chesscomWrapper.getLeaderboards()
```
## Tournament
This instance of the Tournament class will contain the data for the tournament you requested.
# Example
```
chesscomWrapper = ChesscomWrapper()
tournament = chesscomWrapper.getTournament()
```
## TeamMatch
This instance of the TeamMatch class will contain the data for the team match you requested.
# Example
```
chesscomWrapper = ChesscomWrapper()
teamMatch = chesscomWrapper.getTeamMatch()
```
## TitledPlayers
This instance of the TitledPlayers class will contain the data for the titled players.
# Example
```
chesscomWrapper = ChesscomWrapper()
titledPlayers = chesscomWrapper.getTitledPlayers()
```