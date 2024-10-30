# Interact with NBA DATA API
# Obtain all relevant information from the API and process it
# Also contains processor that processes information
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo, playergamelog
from nba_api.stats.endpoints import playerdashboardbyyearoveryear
import json
from collections import defaultdict


CURRENT_SEASON = 2023
STATS = ['Points', 'Rebounds', 'Assists', 'Pts+Rebs+Asts', '3-PT Made', 'FGA', 'FTM', 'Offensive Rebounds', 
		 'Defensive Rebounds', 'Pts+Rebs', 'Pts+Asts', 'Blocks', 'Steals', 'Rebs+Asts', 'Blks+Stls', 'Turnovers']

CONVERT = {'Points': 'PTS',
		   'Rebounds': 'REB',
		   'Assists': 'AST',
		   '3-PT Made': 'FG3M',
		   'FGA': 'FGA',
		   'FTM': 'FTM',
		   'Offensive Rebounds': 'OREB',
		   'Defensive Rebounds': 'DREB',
		   'Blocks': 'BLK',
		   'Steals': 'STL',
		   'Turnovers': 'TOV'}


class API:
	def __init__(self):
		self._career = None
		self._bio = None
		self._pid = None
		self._year_by_year = None
		self._gamelog = None

		# hit rate counts
		self._last5 = defaultdict(int)
		self._last10 = defaultdict(int)
		self._season = defaultdict(int)
		self._careerlog = defaultdict(int)


	@staticmethod
	def search_players(*, first_name: str = None, last_name: str = None) -> list[int]:
		'''Given the first and/or last name, returns a list of player ids that match'''
		if first_name == None and last_name == None:
			return []

		if first_name is not None and last_name is not None:
			matching_first_name = players.find_players_by_first_name(first_name)
			matching_last_name = players.find_players_by_last_name(last_name)

			active_first_name = [player['full_name'] for player in matching_first_name if player['is_active']]
			active_last_name = [player['full_name'] for player in matching_last_name if player['is_active']]

			return list(set(active_first_name).intersection(set(active_last_name)))
		else:
			if first_name == None:
				matching_players = players.find_players_by_last_name(last_name)
			else:
				matching_players = players.find_players_by_first_name(first_name)

			return [player['full_name'] for player in matching_players if player['is_active']]


	@staticmethod
	def get_player_id(full_name: str) -> int:
		'''Given the full name of a player, returns the id of the player'''
		matching = players.find_players_by_full_name(f'^{full_name}$')

		# edge case; there shouldn't be any players with the same exact name in the current nba
		if len(matching) >= 2:
			raise Exception('There can\'t be 2 players with the same id')

		if len(matching) == 0:
			return 0

		return matching[0]['id']


	def get_careerstats(self) -> 'json object':
		'''Returns the raw json data of the player's career, for testing'''
		return self._career


	def get_bio(self) -> 'json object':
		'''Returns the raw json data of the player's bio; for testing'''
		return self._bio


	def get_year_by_year(self) -> 'json object':
		'''Returns the raw json data of a player's year by year data, for testing'''
		return self._year_by_year


	def get_pid(self) -> int:
		'''Returns the player id'''
		return self._pid


	def get_gamelog(self) -> 'json object':
		'''Returns the game log of the current season for the player'''
		return self._gamelog


	def get_last5_counts(self) -> dict:
		'''Returns the stat counter for the last 5 games'''
		return self._last5


	def get_last10_counts(self) -> dict:
		'''Returns the stat counter for the last 10 games'''
		return self._last10


	def get_season_counts(self) -> dict:
		'''Returns the stat counter for the current season'''
		return self._season


	def get_career_counts(self) -> dict:
		'''Returns the stat counter for the career'''
		return self._careerlog


	def has_selected_player(self) -> bool:
		'''Returns if a player has been selected or not'''
		return self._career is not None


	def has_bio(self) -> bool:
		'''Returns whether or not bio info was grabbed'''
		return self._bio is not None


	def has_year_by_year(self) -> bool:
		'''returns whether or not year by year averages were obtained'''
		return self._year_by_year is not None


	def has_gamelog(self) -> bool:
		'''returns whether or not the gamelog has been grabbed'''
		return self._gamelog is not None


	def has_hits(self) -> bool:
		'''returns whether or not the api has grabbed all the hits'''
		return self._last5 == {} and self._last10 == {} and self._season == {} and self._careerlog == {} 


	def get_player_info_by_id(self, pid: int) -> bool:
		'''Given a player's id, grabs all the data for the selected player'''
		if pid == self._pid:
			return True

		try:
			careerstats = playercareerstats.PlayerCareerStats(player_id=pid, per_mode36='PerGame')
			careerstats = json.loads(careerstats.get_json())
		
			self._career = careerstats

			playerbio = commonplayerinfo.CommonPlayerInfo(player_id=pid)
			self._bio = json.loads(playerbio.get_json())

			year_by_year_data = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(pid)
			self._year_by_year = json.loads(year_by_year_data.get_json())

			latter = CURRENT_SEASON - 2000 + 1
			if latter < 10:
				latter = f'0{latter}'

			gamelog_data = playergamelog.PlayerGameLog(pid, season = f'{CURRENT_SEASON}-{latter}')
			self._gamelog = json.loads(gamelog_data.get_json())
			self._pid = pid

			return True
		except:
			return False


	def get_career_average_stat(self, stat_type: str) -> int | None:
		'''Returns the career stat that we are looking for and None if it doesn't exist'''
		if not self._career:
			return None

		careerstats = self._career['resultSets'][1]
		return careerstats['rowSet'][0][careerstats['headers'].index(stat_type)]


	def career_convert(self, stat_type: str) -> list[tuple] | None:
		'''Take dropdown input and return data accordingly'''
		try:
			if stat_type == 'Pts+Rebs+Asts':
				points = self.get_career_average_stat(CONVERT['Points'])
				rebounds = self.get_career_average_stat(CONVERT['Rebounds'])
				assists = self.get_career_average_stat(CONVERT['Assists'])

				return points + rebounds + assists
			elif stat_type == 'Pts+Rebs':
				points = self.get_career_average_stat(CONVERT['Points'])
				rebounds = self.get_career_average_stat(CONVERT['Rebounds'])

				return points + rebounds
			elif stat_type == 'Pts+Asts':
				points = self.get_career_average_stat(CONVERT['Points'])
				assists = self.get_career_average_stat(CONVERT['Assists'])

				return points + assists
			elif stat_type == 'Rebs+Asts':
				rebounds = self.get_career_average_stat(CONVERT['Rebounds'])
				assists = self.get_career_average_stat(CONVERT['Assists'])

				return rebounds + assists
			elif stat_type == 'Blks+Stls':
				blocks = self.get_career_average_stat(CONVERT['Blocks'])
				steals = self.get_career_average_stat(CONVERT['Steals'])

				return blocks + steals
			else:
				return self.get_career_average_stat(CONVERT[stat_type])
		except:
			return None


	def get_bio_info(self, info_type: str) -> str | None:
		'''Returns the type of information about a player's bio we are querying'''
		if not self._bio:
			return None

		try:
			playerbio = self._bio['resultSets'][0]
			index = playerbio['headers'].index(info_type)

			return playerbio['rowSet'][0][index]
		except:
			return None


	def get_year_by_year_stat(self, stat_type: str) -> list[tuple] | None:
		'''Returns a list of tuples that contain the cumulative stat per year'''
		try:
			datapoints = []

			headers = self._year_by_year['resultSets'][1]['headers']
			year_index = headers.index('GROUP_VALUE')
			stat_index = headers.index(stat_type)

			dat = self._year_by_year['resultSets'][1]['rowSet']
			for season in dat:
				datapoints.append((season[year_index], season[stat_index]))

			return datapoints
		except:
			return None


	def get_year_by_year_stat_avg(self, stat_type: str) -> list[tuple] | None:
		'''Returns the list of tuples that contains average stat per year'''
		try:
			datapoints = []

			headers = self._year_by_year['resultSets'][1]['headers']
			year_index = headers.index('GROUP_VALUE')
			stat_index = headers.index(stat_type)
			games_index = headers.index('GP')

			dat = self._year_by_year['resultSets'][1]['rowSet']
			for season in dat:
				avg = round(season[stat_index] / season[games_index], 1)
				if len(datapoints) > 0 and season[year_index] == datapoints[-1][0]:
					continue

				datapoints.append((season[year_index], avg))

			datapoints.reverse()

			return datapoints
		except:
			return None
	

	def per_year_convert(self, stat_type: str) -> list[tuple] | None:
		'''Take dropdown input and return data accordingly, e.g. PRA, RA'''
		try:
			if stat_type == 'Pts+Rebs+Asts':
				points = self.get_year_by_year_stat_avg(CONVERT['Points'])
				rebounds = self.get_year_by_year_stat_avg(CONVERT['Rebounds'])
				assists = self.get_year_by_year_stat_avg(CONVERT['Assists'])

				pra = []
				for pts, reb, ast in zip(points, rebounds, assists):
					pra.append((pts[0], pts[1] + reb[1] + ast[1]))

				return pra
			elif stat_type == 'Pts+Rebs':
				points = self.get_year_by_year_stat_avg(CONVERT['Points'])
				rebounds = self.get_year_by_year_stat_avg(CONVERT['Rebounds'])

				pr = []
				for pts, reb in zip(points, rebounds):
					pr.append((pts[0], pts[1] + reb[1]))

				return pr
			elif stat_type == 'Pts+Asts':
				points = self.get_year_by_year_stat_avg(CONVERT['Points'])
				assists = self.get_year_by_year_stat_avg(CONVERT['Assists'])

				pa = []
				for pts, ast in zip(points, assists):
					pa.append((pts[0], pts[1] + ast[1]))

				return pa
			elif stat_type == 'Rebs+Asts':
				rebounds = self.get_year_by_year_stat_avg(CONVERT['Rebounds'])
				assists = self.get_year_by_year_stat_avg(CONVERT['Assists'])

				ra = []
				for reb, ast in zip(rebounds, assists):
					ra.append((reb[0], reb[1] + ast[1]))

				return ra
			elif stat_type == 'Blks+Stls':
				blocks = self.get_year_by_year_stat_avg(CONVERT['Blocks'])
				steals = self.get_year_by_year_stat_avg(CONVERT['Steals'])

				stocks = []
				for blk, stl in zip(blocks, steals):
					stocks.append((blk[0], blk[1] + stl[1]))

				return stocks
			else:
				return self.get_year_by_year_stat_avg(CONVERT[stat_type])
		except:
			return None


	def current_season_gamelog(self, stat_type: str, max_games: int = None) -> list[str | int] | None:
		'''Returns a list of the stat_type for a player for the number of games specified'''
		headers = self._gamelog['resultSets'][0]['headers']
		gameset = self._gamelog['resultSets'][0]['rowSet']

		games = 0
		stat_log = []
		for game in gameset:
			if max_games is not None and games >= max_games:
				break
			date = game[3].split(',')[0]
			if stat_type == 'Pts+Rebs+Asts':
				points = game[headers.index(CONVERT['Points'])]
				rebounds = game[headers.index(CONVERT['Rebounds'])]
				assists = game[headers.index(CONVERT['Assists'])]

				stat_log.append((date, points + rebounds + assists))
			elif stat_type == 'Pts+Rebs':
				points = game[headers.index(CONVERT['Points'])]
				rebounds = game[headers.index(CONVERT['Rebounds'])]

				stat_log.append((date, points + rebounds))
			elif stat_type == 'Pts+Asts':
				points = game[headers.index(CONVERT['Points'])]
				assists = game[headers.index(CONVERT['Assists'])]

				stat_log.append((date, points + assists))
			elif stat_type == 'Rebs+Asts':
				rebounds = game[headers.index(CONVERT['Rebounds'])]
				assists = game[headers.index(CONVERT['Assists'])]

				stat_log.append(rebounds + assists)
			elif stat_type == 'Blks+Stls':
				blocks = game[headers.index(CONVERT['Blocks'])]
				steals = game[headers.index(CONVERT['Steals'])]

				stat_log.append((date, blocks + steals))
			else:
				stat_log.append((date, game[headers.index(CONVERT[stat_type])]))

			games += 1

		stat_log.reverse()

		return stat_log


	def get_hit_rates(self, stat_type: str) -> list[dict]:
		'''Sets dictionaries equal to all the counts for the different hit rate metrics'''
		self._last5.clear()
		self._last10.clear()
		self._season.clear()
		self._careerlog.clear()

		games = 0
		current_year = CURRENT_SEASON
		s = self._bio['resultSets'][0]
		first_year = int(s['rowSet'][0][s['headers'].index('FROM_YEAR')])
		
		headers = self._gamelog['resultSets'][0]['headers']

		for year in range(current_year, first_year - 1, -1):
			latter = year - 2000 + 1
			if latter < 10:
				latter = f'0{latter}'

			season = f'{year}-{latter}'
			
			data = playergamelog.PlayerGameLog(self._pid, season = season)
			gamelog = json.loads(data.get_json())['resultSets'][0]['rowSet']

			for game in gamelog:
				if stat_type == 'Pts+Rebs+Asts':
					points = game[headers.index(CONVERT['Points'])]
					rebounds = game[headers.index(CONVERT['Rebounds'])]
					assists = game[headers.index(CONVERT['Assists'])]
					stat = points + rebounds + assists
				elif stat_type == 'Pts+Rebs':
					points = game[headers.index(CONVERT['Points'])]
					rebounds = game[headers.index(CONVERT['Rebounds'])]
					stat = points + rebounds
				elif stat_type == 'Pts+Asts':
					points = game[headers.index(CONVERT['Points'])]
					assists = game[headers.index(CONVERT['Assists'])]
					stat = points + assists
				elif stat_type == 'Rebs+Asts':
					rebounds = game[headers.index(CONVERT['Rebounds'])]
					assists = game[headers.index(CONVERT['Assists'])]
					stat = rebounds + assists
				elif stat_type == 'Blks+Stls':
					blocks = game[headers.index(CONVERT['Blocks'])]
					steals = game[headers.index(CONVERT['Steals'])]
					stat = blocks + steals
				else:
					stat = game[headers.index(CONVERT[stat_type])]

				if games < 5:
					self._last5[stat] += 1

				if games < 10:
					self._last10[stat] += 1

				if year == CURRENT_SEASON:
					self._season[stat] += 1

				self._careerlog[stat] += 1

				games += 1
