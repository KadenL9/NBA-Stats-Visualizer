# file to try different stuff with the API and interface
from api import API
from nba_api.stats.static import players, teams
import json
from nba_api.stats.endpoints.playerdashboardbyyearoveryear import *
from nba_api.stats.endpoints import playergamelog
import tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

api = API()
test_player_id = API.get_player_id('Lebron James')


'''
---GET CAREER STATS---
'''
api.get_player_info_by_id(test_player_id)
#print(json.dumps(api.get_bio()['resultSets'][0]['headers'], indent = 2))

api.get_hit_rates('Pts+Rebs+Asts')
#print(json.dumps(api.get_bio(), indent = 2))
#api.current_season_gamelog('Turnovers')
#careerstats = api.get_careerstats()
#print(json.dumps(careerstats, indent = 4))
''''
print(careerstats['headers'])
print(careerstats['rowSet'][0])
for header, value in zip(careerstats['headers'], careerstats['rowSet'][0]):
	print(f'{header}: {value}')

'''
'''stats = playergamelog.PlayerGameLog(test_player_id, season = '2019-20')
j = json.loads(stats.get_json())
'''
#print(json.dumps(j, indent = 4))

'''gameset = j['resultSets'][0]['rowSet']
for game in gameset:
	print(game[-3])
'''

'''
GET current team of player
'''
#team = teams.find_team_name_by_id('1610612737')
#team = teams.get_teams()


'''for g in api.get_year_by_year_stat_avg('PTS'):
	print(g)'''
'''
for season in stats['resultSets'][1]['rowSet']:
	print('---------------------------')
	for header, value in zip(stats['resultSets'][1]['headers'], season):
		print(f'{header}: {value}')

'''


class Plot:
	def __init__(self):
		self._window = tkinter.Tk()

		self._window.geometry('1920x1080')
		self._api = API()
		self._api.get_player_info_by_id(test_player_id)

		self.build_multiple_plots()

	def run(self) -> None:
		self._window.mainloop()

	'''def build_plot(self) -> None:
		self._fig = Figure(figsize=(10, 6), dpi=70)
		self._x = []
		self._y = []
		for year, ppg in self._api.get_year_by_year_stat_avg('PTS'):
			self._x.append(year)
			self._y.append(ppg)

		plot1 = self._fig.add_subplot(111)
		plot1.tick_params(axis='x', labelrotation = 45)
		plot1.plot(self._x, self._y)

		self._canvas = FigureCanvasTkAgg(self._fig, master = self._window)
		self._canvas.draw()
		self._canvas.get_tk_widget().pack()'''

	def build_multiple_plots(self) -> None:
		self._fig = Figure(figsize=(10, 6), dpi=70)
		self._x = []
		self._y = []
		for year, ppg in self._api.get_year_by_year_stat_avg('PTS'):
			self._x.append(year)
			self._y.append(ppg)
		self._z = [self._api.get_career_average_stat('PTS')] * len(self._x)
		plot1 = self._fig.add_subplot(111)
		plot1.tick_params(axis='x', labelrotation = 45)
		plot1.plot(self._x, self._y)
		plot1.plot(self._x, self._z)



		self._canvas = FigureCanvasTkAgg(self._fig, master = self._window)
		self._canvas.draw()
		self._canvas.get_tk_widget().pack()


#Plot().run()



	'''def test_plot(self) -> None:
		self._fig = Figure(figsize = (5, 5), dpi = 100)
		self._x = [1, 2, 3]
		self._y = [10, 20, -10]


		plot1 = self._fig.add_subplot(111)

		plot1.plot(self._x, self._y)

		self._canvas = FigureCanvasTkAgg(self._fig, master=self._panel1)
		self._canvas.draw()

		self._canvas.get_tk_widget().pack()


	def _update_plot(self) -> None:
		self._fig.clear()
		plot1 = self._fig.add_subplot(111)
		self._y = []
		self._y = [ppg for year, ppg in self._api.get_year_by_year_stat_avg('PTS')]
		plot1.plot(self._y)
		self._canvas.draw()'''


