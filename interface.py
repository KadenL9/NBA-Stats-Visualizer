# Implements tkinter for user interface
# Contains all the code pertaining to the front end of the application
import tkinter
from tkinter import ttk, messagebox
from api import API, STATS
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy


# colors
LIGHTPURPLE = '#d032db'
TEAL = '#03fce8'
BLACK = '#000000'
LIGHTBLUE = 'lightblue'
GRAPHGREEN = '#1eeb25'
GRAPHRED = '#ff2424'
GRAPHGRAY = '#8f8888'
GRAPHBLUE = '#03fcfc'
GRAPHPURPLE = '#c203fc'
WHITE = '#ffffff'
GRAPHGOLD = '#d17219'

# fonts
TEXT10 = ('Helvetica', 10, 'bold')
TITLE15 = ('Helvetica', 15, 'bold')
STAT12 = ('Helvetica', 12, 'bold')



class Interface:
	def __init__(self):
		# create our basic tkinter window
		self._window = tkinter.Tk()

		# window configuration
		self._window.title('NBA Statistics Analyzer v1')
		self._window.geometry('1920x1080')

		self._window.configure(bg=BLACK)

		# create API object for the interface
		self._api = API()

		# add everything to our window
		self._add_frames()
		self._add_elements()


	def run(self) -> None:
		'''Runs the program and allows user to see the interface'''
		self._window.mainloop()


	def _add_frames(self) -> None:
		'''Adds all the frames to the interface'''
		self._create_title_frame()
		self._create_search_frame()
		self._create_bio_frame()
		self._create_panel1_frame()
		self._create_panel2_frame()


	def _create_title_frame(self) -> None:
		'''Creates the frame that contains the title of our application'''
		self._title_frame = tkinter.LabelFrame(self._window, bg=BLACK, bd=0)
		self._title_frame.grid(row=0, column=0, padx=20)


	def _create_search_frame(self) -> None:
		'''Creates the search frame which contains the player search and select'''
		self._search_frame = tkinter.LabelFrame(self._window, bg=BLACK, padx=10, pady=10)
		self._search_frame.grid(row=1, column=0)


	def _create_bio_frame(self) -> None:
		'''Creates the bio frame which contains player bio and information'''
		self._bio_frame = tkinter.LabelFrame(self._window, bg=BLACK, bd=0)
		self._bio_frame.grid(row=2, column=0)


	def _create_panel1_frame(self) -> None:
		'''Creates the frame which contains all the graphs and stuff in panel 1'''
		self._panel1 = tkinter.LabelFrame(self._window, bg=BLACK)
		self._panel1.grid(row=0, column=1, rowspan=3) 


	def _create_panel2_frame(self) -> None:
		'''Creates the frame which contains all the number stuff'''
		self._panel2 = tkinter.LabelFrame(self._window, bg=BLACK)
		self._panel2.grid(row=0, column=2, rowspan=3)


	def _add_elements(self) -> None:
		'''Adds all the elements to the application'''
		# elements in the title frame
		self._create_title()

		# elements in the search frame
		self._create_select_title()
		self._create_search_bars()
		self._create_enter_search_button()
		self._create_clear_button()
		self._create_available_players()
		self._create_select_player_button()
		self._create_stat_label()
		self._create_stat_dropdown()

		# elements in the bio frame
		self._create_bio_title()
		self._create_career_stats_title()
		self._create_career_stats_display()
		self._create_age_display()
		self._create_team_display()
		self._create_misc_display()

		# elements in the panel1 frame
		self._create_yby_plot()
		self._create_game_log()
		self._create_gamelog_buttons()
		self._create_hit_rates()

		# elements in the panel2 frame
		self._create_season_log()
		self._create_5_log()
		self._create_hit_rates_log()


	def _create_title(self) -> None:
		'''Creates the title of our application'''
		self._title = tkinter.Label(self._title_frame, text='NBA Statistics',
									fg=TEAL,
									bg=BLACK,
									font=('Helvetica', 30, 'bold'),
									width=12)
		self._title.grid(row=0, column=0)
		self._title2 = tkinter.Label(self._title_frame, text='Analyzer v1',
									 fg=TEAL,
									 bg=BLACK,
									 font=('Helvetica', 30, 'bold'),
									 width=12)
		self._title2.grid(row=1, column=0)


	def _create_select_title(self) -> None:
		'''Creates the player select title'''
		self._select_title = tkinter.Label(self._search_frame, text='---Player Select---', bg=BLACK, font=TITLE15,
										   fg=TEAL)
		self._select_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))


	def _create_search_bars(self) -> None:
		'''Creates the search bar that allows user to search for players by first, last, or full name'''
		self._first_name = tkinter.StringVar()
		self._first_name_search_bar = tkinter.Entry(self._search_frame, textvariable=self._first_name, 
													fg='gray', width=24, font=('Helvetica', 14), bg=BLACK,
													insertbackground=TEAL)
		self._first_name_search_bar.insert(0, 'First Name')
		self._first_name_search_bar.grid(row=1, column=0, columnspan=2)

		self._last_name = tkinter.StringVar()
		self._last_name_search_bar = tkinter.Entry(self._search_frame, textvariable=self._last_name,
												   fg='gray', width=24, font=('Helvetica', 14), bg=BLACK,
												   insertbackground=TEAL)
		self._last_name_search_bar.insert(0, 'Last Name')
		self._last_name_search_bar.grid(row=2, column=0, columnspan=2, pady=(0, 10))

		self._add_placeholders()


	def _add_placeholders(self) -> None:
		'''allow first and last name search bars to have placeholders'''
		# helper functions that will be binded to the entry widgets
		def _enter_first_name_entry(event):
			if self._first_name_search_bar.get() == 'First Name':
				self._first_name_search_bar.delete(0, tkinter.END)
				self._first_name_search_bar.configure(fg=LIGHTBLUE)

		def _exit_first_name_entry(event):
			if self._first_name_search_bar.get() == '':
				self._first_name_search_bar.insert(0, 'First Name')
				self._first_name_search_bar.configure(fg='gray')

		def _enter_last_name_entry(event):
			if self._last_name_search_bar.get() == 'Last Name':
				self._last_name_search_bar.delete(0, tkinter.END)
				self._last_name_search_bar.configure(fg=LIGHTBLUE)

		def _exit_last_name_entry(event):
			if self._last_name_search_bar.get() == '':
				self._last_name_search_bar.insert(0, 'Last Name')
				self._last_name_search_bar.configure(fg='gray')

		# bind the functions to the widgets
		self._first_name_search_bar.bind('<FocusIn>', _enter_first_name_entry)
		self._first_name_search_bar.bind('<FocusOut>', _exit_first_name_entry)
		self._last_name_search_bar.bind('<FocusIn>', _enter_last_name_entry)
		self._last_name_search_bar.bind('<FocusOut>', _exit_last_name_entry)


	def _create_enter_search_button(self) -> None:
		'''Creates the button that allows user to start the search for the player'''
		self._submit_button = tkinter.Button(self._search_frame, text='Search', command=self._display_matching_players, width=15,
											 bg=LIGHTBLUE, fg=BLACK, font=TEXT10, activebackground=TEAL,
											 activeforeground=BLACK)
		self._submit_button.grid(row=3, column=0, sticky=tkinter.W, pady=(0, 10))


	def _create_clear_button(self) -> None:
		'''Creates the button that allows user to clear the search area'''
		self._clear_button = tkinter.Button(self._search_frame, text='Clear', command=self._clear_search, width=15,
											bg=LIGHTBLUE, fg=BLACK, font=TEXT10, activebackground=TEAL,
											activeforeground=BLACK)
		self._clear_button.grid(row=3, column=1, sticky=tkinter.E, pady=(0, 10))


	def _clear_search(self) -> None:
		self._first_name_search_bar.delete(0, tkinter.END)
		self._first_name_search_bar.configure(fg='gray')
		self._first_name_search_bar.insert(0, 'First Name')

		self._last_name_search_bar.delete(0, tkinter.END)
		self._last_name_search_bar.configure(fg='gray')
		self._last_name_search_bar.insert(0, 'Last Name')

		self._panel1.focus_set()


	def _display_matching_players(self) -> None:
		'''When search player button clicked, displays all matching players on side'''
		firstname = self._first_name.get()
		if firstname == 'First Name':
			firstname = None

		lastname = self._last_name.get()
		if lastname == 'Last Name':
			lastname = None

		players = self._api.search_players(first_name=firstname, last_name=lastname)
		self._player_listbox.delete(0, tkinter.END)
		self._player_listbox.insert(0, *players)


	def _create_available_players(self) -> None:
		'''Adds players to a listbox with available players that can grab stats from'''
		self._player_listbox = tkinter.Listbox(self._search_frame, height=5, selectmode=tkinter.SINGLE, width=38,
											   font=TEXT10, bg=BLACK, fg=LIGHTBLUE, selectbackground=TEAL,
											   selectforeground=BLACK, highlightcolor=LIGHTBLUE)
		self._player_listbox.grid(row=4, column=0, columnspan=2, pady=(0, 10))


	def _create_stat_label(self) -> None:
		'''Just a title for the stat dropdown'''
		self._stat_label_border = tkinter.LabelFrame(self._search_frame, bg=BLACK, bd=0)
		self._stat_label_border.grid(row=6, column=0, columnspan=2, pady=(0, 10))

		self._stat_label = tkinter.Label(self._stat_label_border, text='---Stat Selector---', bg=BLACK, fg=TEAL,
										 font=TITLE15)
		self._stat_label.grid(row=0, column=0, padx=10)


	def _create_stat_dropdown(self) -> None:
		'''Creates a dropdown menu that chooses a single stat to look at; defaults to points'''	
		style = ttk.Style()
		style.configure('TCombobox', background=LIGHTBLUE)
		self._stat_dropdown = ttk.Combobox(self._search_frame, values=STATS, state='readonly', height=4)
		self._stat_dropdown.set('Points')
		self._stat_dropdown.bind('<<ComboboxSelected>>', self._dropdown_callback)
		self._stat_dropdown.grid(row=7, column=0, columnspan=2, pady=(0, 70))


	def _dropdown_callback(self, event) -> None:
		if self._api.has_selected_player():
			self._update_plots()
			self._update_panel2()


	def _create_select_player_button(self) -> None:
		'''Creates a button that is pressed when a player is selected'''
		self._player_select_button = tkinter.Button(self._search_frame, text='Select Player', command=self._select_player, 
													width=20, pady=1, bg=LIGHTBLUE, fg=BLACK, font=TEXT10,
													activebackground=TEAL, activeforeground=BLACK)
		self._player_select_button.grid(row=5, column=0, columnspan=2, pady=(0, 20))


	def _select_player(self) -> None:
		''' Run when a player is selected; updates career stats and displays new info'''
		selection = self._player_listbox.curselection()
		if len(selection) > 0:
			player = self._player_listbox.get(selection[0])
			player_id = API.get_player_id(player)

			# leave if same player is selected because we don't need to do anything
			if player_id == self._api.get_pid():
				return

			if not self._api.get_player_info_by_id(player_id):
				errormessage = f'Unable to grab {player}\'s data'
				tkinter.messagebox.showerror(title='ERROR', message=errormessage)
				return

			self._update_bio_info()
		else:
			errormessage = 'A player must be selected.'
			tkinter.messagebox.showerror(title='ERROR', message=errormessage)
			return


	def _update_bio_info(self) -> None:
		'''Basically updates all bio information whenever a new player is selected'''
		self._update_career_stats()
		self._update_age()
		self._update_team()
		self._update_misc()

		self._update_plots()

		self._update_panel2()


	def _create_bio_title(self) -> None:
		'''Basically create a title for the player bio section'''
		self._bio_title_panel = tkinter.LabelFrame(self._bio_frame, bg=BLACK, bd=0)
		self._bio_title_panel.grid(row=0, column=0, columnspan=2, pady=(10, 10))
		self._bio_title = tkinter.Label(self._bio_title_panel, text='---Player Bio---', font=TITLE15, bg=BLACK,
										fg=TEAL)
		self._bio_title.grid(row=0, column=0)


	def _create_career_stats_title(self) -> None:
		'''Basically create a title for the career stats of a player'''
		self._career_stats_title_panel = tkinter.LabelFrame(self._bio_frame, bg=BLACK, bd=0)
		self._career_stats_title_panel.grid(row=5, column=0, columnspan=2)

		self._career_stats_title = tkinter.Label(self._career_stats_title_panel, text='---Career Stats---', font=TITLE15,
												 bg=BLACK, fg=TEAL)
		self._career_stats_title.grid(row=0, column=0, pady=(0, 10))


	def _create_career_stats_display(self) -> None:
		'''Creates the display for the player's career stats'''
		self._career_ppg_panel = tkinter.LabelFrame(self._bio_frame)
		self._career_ppg_panel.grid(row=6, column=0, sticky=tkinter.W, padx=(15, 0), pady=(0, 15))
		self._career_ppg_label = tkinter.Label(self._career_ppg_panel, text='PPG', bg=BLACK,
											   font=STAT12, fg=LIGHTBLUE, width=6)
		self._career_ppg_label.grid(row=0, column=0)
		self._career_ppg = tkinter.StringVar()
		self._career_ppg.set('N/A')
		self._career_ppg_display = tkinter.Label(self._career_ppg_panel, textvariable=self._career_ppg, bg=BLACK,
												 font=STAT12, fg=WHITE, width=6)
		self._career_ppg_display.grid(row=1, column=0)

		self._career_rpg_panel = tkinter.LabelFrame(self._bio_frame)
		self._career_rpg_panel.grid(row=6, column=0, columnspan=2, pady=(0, 15))
		self._career_rpg_label = tkinter.Label(self._career_rpg_panel, text='RPG', bg=BLACK,
											   font=STAT12, fg=LIGHTBLUE, width=6)
		self._career_rpg_label.grid(row=0, column=0)
		self._career_rpg = tkinter.StringVar()
		self._career_rpg.set('N/A')
		self._career_rpg_display = tkinter.Label(self._career_rpg_panel, textvariable=self._career_rpg, bg=BLACK,
												 font=STAT12, fg=WHITE, width=6)
		self._career_rpg_display.grid(row=1, column=0)

		self._career_apg_panel = tkinter.LabelFrame(self._bio_frame)
		self._career_apg_panel.grid(row=6, column=1, sticky=tkinter.E, padx=(0, 15), pady=(0, 15))
		self._career_apg_label = tkinter.Label(self._career_apg_panel, text='APG', bg=BLACK,
											   font=STAT12, fg=LIGHTBLUE, width=6)
		self._career_apg_label.grid(row=0, column=0)
		self._career_apg = tkinter.StringVar()
		self._career_apg.set('N/A')
		self._career_apg_display = tkinter.Label(self._career_apg_panel, textvariable=self._career_apg, bg=BLACK,
												 font=STAT12, fg=WHITE, width=6)
		self._career_apg_display.grid(row=1, column=0)

		self._career_bpg_panel = tkinter.LabelFrame(self._bio_frame)
		self._career_bpg_panel.grid(row=7, column=0, padx=(45, 0), pady=(0, 20))
		self._career_bpg_label = tkinter.Label(self._career_bpg_panel, text='BPG', bg=BLACK,
											   font=STAT12, fg=LIGHTBLUE, width=6)
		self._career_bpg_label.grid(row=0, column=0)
		self._career_bpg = tkinter.StringVar()
		self._career_bpg.set('N/A')
		self._career_bpg_display = tkinter.Label(self._career_bpg_panel, textvariable=self._career_bpg, bg=BLACK,
												 font=STAT12, fg=WHITE, width=6)
		self._career_bpg_display.grid(row=1, column=0)

		self._career_spg_panel = tkinter.LabelFrame(self._bio_frame)
		self._career_spg_panel.grid(row=7, column=1, padx = (0, 45), pady=(0, 20))
		self._career_spg_label = tkinter.Label(self._career_spg_panel, text='SPG', bg=BLACK,
											   font=STAT12, fg=LIGHTBLUE, width=6)
		self._career_spg_label.grid(row=0, column=0)
		self._career_spg = tkinter.StringVar()
		self._career_spg.set('N/A')
		self._career_spg_display = tkinter.Label(self._career_spg_panel, textvariable=self._career_spg, bg=BLACK, 
												 font=STAT12, fg=WHITE, width=6)
		self._career_spg_display.grid(row=1, column=0)


	def _update_career_stats(self) -> None:
		'''Update the career stats when a new player is selected'''
		if self._api.has_selected_player():
			self._career_ppg.set(self._api.get_career_average_stat('PTS'))
			self._career_rpg.set(self._api.get_career_average_stat('REB'))
			self._career_apg.set(self._api.get_career_average_stat('AST'))
			self._career_bpg.set(self._api.get_career_average_stat('BLK'))
			self._career_spg.set(self._api.get_career_average_stat('STL'))
		else:
			self._career_ppg.set('N/A')
			self._career_rpg.set('N/A')
			self._career_apg.set('N/A')
			self._career_bpg.set('N/A')
			self._career_spg.set('N/A')


	def _create_age_display(self) -> None:
		'''Create the display for the age and birthday of the selected player'''
		self._age_panel = tkinter.LabelFrame(self._bio_frame)
		self._age_panel.grid(row=2, column=0)
		self._age_label = tkinter.Label(self._age_panel, text='Current Age', bg=BLACK, font=TEXT10,
										fg=LIGHTBLUE, width=17)
		self._age_label.grid(row=0, column=0)
		self._age = tkinter.StringVar()
		self._age.set('N/A')
		self._age_display = tkinter.Label(self._age_panel, textvariable=self._age, bg=BLACK, font=TEXT10,
										  fg=WHITE, width=17)
		self._age_display.grid(row=1, column=0)

		self._bday_panel = tkinter.LabelFrame(self._bio_frame)
		self._bday_panel.grid(row=2, column=1)
		self._bday_label = tkinter.Label(self._bday_panel, text='Birthday', bg=BLACK, font=TEXT10,
										 fg=LIGHTBLUE, width=17)
		self._bday_label.grid(row=0, column=0)
		self._bday = tkinter.StringVar()
		self._bday.set('N/A')
		self._bday_display = tkinter.Label(self._bday_panel, textvariable=self._bday, bg=BLACK, font=TEXT10,
										   fg=WHITE, width=17)
		self._bday_display.grid(row=1, column=0)


	def _update_age(self) -> None:
		'''Update age display when selected player changes'''
		if self._api.has_bio():
			birthdate = datetime.strptime(self._api.get_bio_info('BIRTHDATE'), '%Y-%m-%dT%H:%M:%S')
			age = datetime.now() - birthdate
			self._age.set(int(age.days // 365.25))
			self._bday.set(birthdate.strftime('%B %d, %Y'))
		else:
			self._age.set('N/A')
			self._bday.set('N/A')


	def _create_team_display(self) -> None:
		'''Create the display for current team, teams played for, draft year, and experience'''
		self._current_team_panel = tkinter.LabelFrame(self._bio_frame)
		self._current_team_panel.grid(row=4, column=0, columnspan=2, pady=(0, 20))
		self._current_team_label = tkinter.Label(self._current_team_panel, text='Current Team', bg=BLACK,
												 font=TEXT10, fg=LIGHTBLUE, width=35)
		self._current_team_label.grid(row=0, column=0)
		self._current_team = tkinter.StringVar()
		self._current_team.set('Unemployed')
		self._current_team_display = tkinter.Label(self._current_team_panel, textvariable=self._current_team, bg=BLACK,
												   font=TEXT10, fg=WHITE, width=35)
		self._current_team_display.grid(row=1, column=0)

		self._draft_panel = tkinter.LabelFrame(self._bio_frame)
		self._draft_panel.grid(row=3, column=0)
		self._draft_label = tkinter.Label(self._draft_panel, text='Draft Position', bg=BLACK, font=TEXT10, fg=LIGHTBLUE, width=17)
		self._draft_label.grid(row=0, column=0)
		self._draft = tkinter.StringVar()
		self._draft.set('Undrafted')
		self._draft_display = tkinter.Label(self._draft_panel, textvariable=self._draft, bg=BLACK, font=TEXT10,
										    fg=WHITE, width=17)
		self._draft_display.grid(row=1, column=0)

		self._experience_panel = tkinter.LabelFrame(self._bio_frame)
		self._experience_panel.grid(row=3, column=1)
		self._experience_label = tkinter.Label(self._experience_panel, text='Years Experience', bg=BLACK,
											   font=TEXT10, fg=LIGHTBLUE, width=17)
		self._experience_label.grid(row=0, column=0)
		self._experience = tkinter.StringVar()
		self._experience.set('0')
		self._experience_display = tkinter.Label(self._experience_panel, textvariable=self._experience, bg=BLACK,
												 font=TEXT10, fg=WHITE, width=17)
		self._experience_display.grid(row=1, column=0)



	def _update_team(self) -> None:
		'''Update the information pertaining to the team display'''
		if self._api.has_bio():
			if self._api.get_bio_info('TEAM_CITY') == '':
				self._current_team.set('Unemployed')
			else:
				self._current_team.set(f'{self._api.get_bio_info('TEAM_CITY')} {self._api.get_bio_info('TEAM_NAME')}')

			draft_number = self._api.get_bio_info('DRAFT_NUMBER')
			if draft_number == 'Undrafted':
				self._draft.set('Undrafted')
			else:
				round = self._api.get_bio_info('DRAFT_ROUND')
				draft_year = self._api.get_bio_info('DRAFT_YEAR')
				self._draft.set(f'{draft_year} Round {round} Pick {draft_number}')

			self._experience.set(self._api.get_bio_info('SEASON_EXP'))
		else:
			self._current_team.set('Unemployed Hobo')
			self._draft.set('Undrafted Clown')
			self._experience_display.set('0')


	def _create_misc_display(self) -> None:
		'''Create the display for miscellaneous stuff like face shot, height, and weight'''
		self._weight_panel = tkinter.LabelFrame(self._bio_frame)
		self._weight_panel.grid(row=1, column=0)
		self._weight_label = tkinter.Label(self._weight_panel, text='Weight', fg=LIGHTBLUE, bg=BLACK, font=TEXT10, width=17)
		self._weight_label.grid(row=0, column=0)
		self._weight = tkinter.StringVar()
		self._weight.set('N/A')
		self._weight_display = tkinter.Label(self._weight_panel, textvariable=self._weight, bg=BLACK, font=TEXT10,
											 fg=WHITE, width=17)
		self._weight_display.grid(row=1, column=0)

		self._height_panel = tkinter.LabelFrame(self._bio_frame)
		self._height_panel.grid(row=1, column=1)
		self._height_label = tkinter.Label(self._height_panel, text='Height', fg=LIGHTBLUE, bg=BLACK, font=TEXT10, width=17)
		self._height_label.grid(row=0, column=0)
		self._height = tkinter.StringVar()
		self._height.set('N/A')
		self._height_display = tkinter.Label(self._height_panel, textvariable=self._height, bg=BLACK, font=TEXT10,
											 fg=WHITE, width=17)
		self._height_display.grid(row=1, column=0)


	def _update_misc(self) -> None:
		'''Update miscellaneous information when player is updated'''
		if self._api.has_bio():
			self._weight.set(f'{self._api.get_bio_info('WEIGHT')} lbs')

			height = self._api.get_bio_info('HEIGHT').split('-')
			self._height.set(f'{height[0]} ft {height[1]} in')
		else:
			self._weight.set('N/A')
			self._height.set('N/A')


	def _update_plots(self) -> None:
		'''Update plots when stat specified changes'''
		self._update_yby_plot()
		self._update_game_log()
		self._update_hit_rates()


	def _create_yby_plot(self) -> None:
		'''Create the plot that shows year by year data averages'''
		# create the figure
		self._yby_fig = Figure(figsize = (12, 4), dpi = 80)
		self._yby_fig.subplots_adjust(bottom=0.2)
		self._yby_fig.set_facecolor(BLACK)

		# set up default values
		self._yby_years = ['2015-16', '2016-17', '2017-18', '2018-19', '2019-20',
						   '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
		self._yby_data = [0] * 10
		self._yby_career_avg = [0] * 10

		# create the plot
		self._yby_plot = self._yby_fig.add_subplot(111)
		self._yby_plot.set_facecolor(BLACK)
		self._yby_plot.tick_params(axis='x', labelrotation=45)
		self._yby_plot.tick_params(color=WHITE, labelcolor=WHITE)
		self._yby_plot.set_xlabel('Season', color=WHITE)
		self._yby_plot.set_ylabel('Points', color=WHITE)
		self._yby_plot.set_ylim((0, 30))
		self._yby_plot.spines['bottom'].set_color(WHITE)
		self._yby_plot.spines['left'].set_color(WHITE)


		self._yby_plot.plot(self._yby_years, self._yby_data, marker='o', label='Per Year', color=GRAPHGOLD)
		self._yby_plot.plot(self._yby_years, self._yby_career_avg, label='Career Average', linestyle='--', color=WHITE)
		self._yby_plot.legend(facecolor=BLACK, labelcolor=WHITE)

		# add plot as widget
		self._yby_canvas = FigureCanvasTkAgg(self._yby_fig, master=self._panel1)
		self._yby_canvas.draw()
		self._yby_canvas.get_tk_widget().pack(pady = 20)


	def _update_yby_plot(self) -> None:
		'''Update the year by year plot when player/stat changes'''
		self._yby_fig.clear()
		self._yby_fig.subplots_adjust(bottom=0.2)

		self._yby_plot = self._yby_fig.add_subplot(111)
		self._yby_plot.set_facecolor(BLACK)
		self._yby_plot.set_xlabel('Season', color=WHITE)
		self._yby_plot.set_ylabel(self._stat_dropdown.get(), color=WHITE)
		self._yby_plot.tick_params(axis='x', labelrotation=45)
		self._yby_plot.tick_params(color=WHITE, labelcolor=WHITE)
		self._yby_plot.spines['bottom'].set_color(WHITE)
		self._yby_plot.spines['left'].set_color(WHITE)

		if not self._api.has_selected_player():
			self._yby_years = ['2015-17', '2017-17', '2017-18', '2018-19', '2019-20',
						   '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']
			self._yby_data = [0] * 10
			self._yby_career_avg = [0] * 10
			self._yby_plot.set_ylim((0, 30))
		else:
			self._yby_years = []
			self._yby_data = []
			self._yby_career_avg = []

			for year, data in self._api.per_year_convert(self._stat_dropdown.get()):
				self._yby_years.append(year)
				self._yby_data.append(data)

			career_avg = self._api.career_convert(self._stat_dropdown.get())
			self._yby_career_avg = [career_avg] * len(self._yby_years)

		self._yby_plot.plot(self._yby_years, self._yby_data, label = 'Per Year', marker='o', color=GRAPHGOLD)
		self._yby_plot.plot(self._yby_years, self._yby_career_avg, label='Career Average', color=WHITE, linestyle='--')
		self._yby_plot.legend(facecolor=BLACK, labelcolor=WHITE)


		self._yby_canvas.draw()


	def _create_game_log(self) -> None:
		'''Create the bar graph that shows the game log for the current year'''
		self._gl_panel = tkinter.LabelFrame(self._panel1, bg=BLACK)
		self._gl_panel.pack()

		self._gl_fig = Figure(figsize = (12, 4), dpi = 80)
		self._gl_fig.subplots_adjust(bottom=0.2)
		self._gl_fig.set_facecolor(BLACK)

		self._gl_dates = ['Aug 23', 'Aug 25', 'Aug 26', 'Aug 29', 'Aug 31']
		self._gl_data = [0] * 5
		self._gl_avg = [0] * 5

		self._gl_plot = self._gl_fig.add_subplot(111)
		self._gl_plot.set_facecolor(BLACK)
		self._gl_plot.tick_params(axis='x', labelrotation=45, labelsize=5)
		self._gl_plot.tick_params(color=WHITE, labelcolor=WHITE)
		self._gl_plot.set_xlabel('Game', color=WHITE)
		self._gl_plot.set_ylabel('Points', color=WHITE) 
		self._gl_plot.set_ylim((0, 50))
		self._gl_plot.spines['bottom'].set_color(WHITE)
		self._gl_plot.spines['left'].set_color(WHITE)
		
		self._gl_plot.bar(self._gl_dates, self._gl_data, label='Game Log', color=GRAPHPURPLE)
		self._gl_plot.plot(self._gl_dates, self._gl_avg, label='Season Average', linestyle='--', color=WHITE)
		self._gl_plot.legend(facecolor=BLACK, labelcolor=WHITE)

		self._gl_canvas = FigureCanvasTkAgg(self._gl_fig, master=self._gl_panel)
		self._gl_canvas.draw()
		self._gl_canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)


	def _update_game_log(self, max_games: int = None) -> None:
		'''Update the bar graph displaying game log when player/stat changes'''
		self._gl_fig.clear()
		self._gl_fig.subplots_adjust(bottom=0.2)

		self._gl_plot = self._gl_fig.add_subplot(111)
		self._gl_plot.set_facecolor(BLACK)
		self._gl_plot.set_xlabel('Game', color=WHITE)
		self._gl_plot.set_ylabel(self._stat_dropdown.get(), color=WHITE)
		self._gl_plot.tick_params(axis='x', labelrotation=45, labelsize=5)
		self._gl_plot.tick_params(labelcolor=WHITE, color=WHITE)
		self._gl_plot.spines['bottom'].set_color(WHITE)
		self._gl_plot.spines['left'].set_color(WHITE)

		if not self._api.has_gamelog():
			self._gl_dates = ['Aug 23', 'Aug 25', 'Aug 26', 'Aug 29', 'Aug 31']
			self._gl_data = [0] * 5
			self._gl_avg = [0] * 5
			self._gl_plot.set_ylim((0, 50))
		else:
			self._gl_dates = []
			self._gl_data = []
			self._gl_avg = []

			for date, data in self._api.current_season_gamelog(self._stat_dropdown.get(), max_games):
				self._gl_dates.append(date)
				self._gl_data.append(data)

			if len(self._gl_data) <= 0:
				avg = 0
			else:
				avg = round(sum(self._gl_data) / len(self._gl_data), 1)
			self._gl_avg = [avg] * len(self._gl_data)

		
		self._gl_plot.bar(self._gl_dates, self._gl_data, label='Game Log', color=GRAPHPURPLE)
		self._gl_plot.plot(self._gl_dates, self._gl_avg, label='Season Average', linestyle='--', color=WHITE)
		self._gl_plot.legend(facecolor=BLACK, labelcolor=WHITE)


		self._gl_plot.set_ylim(bottom=0)

		self._gl_canvas.draw()


	def _create_gamelog_buttons(self) -> None:
		'''Create the buttons that allows user to switch between season, last5, last10 games on gamelog graph'''
		self._gl_season_button = tkinter.Button(self._gl_panel, text='Season', width=15, bg=LIGHTBLUE, fg=BLACK, font=TEXT10,
												activebackground=TEAL, activeforeground=BLACK, command=self._update_game_log)
		self._gl_season_button.grid(row=1, column=0, pady=(0, 30))

		self._gl_last10_button = tkinter.Button(self._gl_panel, text='Last 10', width=15, bg=LIGHTBLUE, fg=BLACK, font=TEXT10,
												activebackground=TEAL, activeforeground=BLACK, command=self._last10_change)
		self._gl_last10_button.grid(row=1, column=1, pady=(0, 30))

		self._gl_last5_button = tkinter.Button(self._gl_panel, text='Last 5', width=15, bg=LIGHTBLUE, fg=BLACK, font=TEXT10,
											   activebackground=TEAL, activeforeground=BLACK, command=self._last5_change)
		self._gl_last5_button.grid(row=1, column=2, pady=(0, 30))


	def _last10_change(self) -> None:
		self._update_game_log(10)


	def _last5_change(self) -> None:
		self._update_game_log(5)


	def _create_hit_rates(self) -> None:
		'''Display the hit rates in stacked horizontal bar graphs as percentages'''
		self._hit_fig = Figure(figsize = (12, 3), dpi = 80)
		self._hit_fig.subplots_adjust(left=0.2)
		self._hit_fig.set_facecolor(BLACK)

		self._hit_cat = ['Last 5', 'Last 10', 'Current Season', 'Career']
		self._hit_hit = [45] * 4
		self._hit_tied = [10] * 4
		self._hit_miss = [45] * 4

		self._hit_plot = self._hit_fig.add_subplot(111)
		self._hit_plot.set_xlim((0, 100))
		self._hit_plot.get_xaxis().set_visible(False)
		self._hit_plot.set_frame_on(False)
		self._hit_plot.tick_params(axis='y', length=0, labelcolor=WHITE)

		self._hit_plot.barh(self._hit_cat, self._hit_miss, label='Hit', height=0.4, color=GRAPHRED)
		self._hit_plot.barh(self._hit_cat, self._hit_tied, label='Tied', height=0.4, left=self._hit_hit, color=GRAPHGRAY)
		start = [self._hit_miss[x] + self._hit_tied[x] for x in range(len(self._hit_miss))]
		self._hit_plot.barh(self._hit_cat, self._hit_hit, label='Miss', height=0.4, left=start, color=GRAPHGREEN)
		self._hit_plot.legend()

		self._hit_canvas = FigureCanvasTkAgg(self._hit_fig, master=self._panel1)
		self._hit_canvas.draw()
		self._hit_canvas.get_tk_widget().pack()


	def _update_hit_rates(self) -> None:
		'''Updates the hit rates when line changes, stat changes, or player changes'''
		self._api.get_hit_rates(self._stat_dropdown.get())
		LINE = round(self._api.career_convert(self._stat_dropdown.get()))

		self._hit_fig.clear()
		self._hit_fig.subplots_adjust(left=0.2)

		self._hit_plot = self._hit_fig.add_subplot(111)
		self._hit_plot.set_facecolor(BLACK)
		self._hit_plot.set_xlim((0, 100))
		self._hit_plot.get_xaxis().set_visible(False)
		self._hit_plot.set_frame_on(False)
		self._hit_plot.tick_params(axis='y', length=0, labelcolor=WHITE)

		self._hit_hit = [0] * 4
		self._hit_tied = [0] * 4
		self._hit_miss = [0] * 4
		datasets = [self._api.get_last5_counts(), 
					self._api.get_last10_counts(),
					self._api.get_season_counts(),
					self._api.get_career_counts()]

		for x in range(len(datasets)):
			for stat, occ in datasets[x].items():
				if stat > LINE:
					self._hit_hit[x] += occ
				elif stat < LINE:
					self._hit_miss[x] += occ
				else:
					self._hit_tied[x] += occ

			self._hit_hit[x] 

			self._hit_hit[x] = round(self._hit_hit[x] * 100 / sum(datasets[x].values()), 1)
			self._hit_tied[x] = round(self._hit_tied[x] * 100 / sum(datasets[x].values()), 1)
			self._hit_miss[x] = round(self._hit_miss[x] * 100 / sum(datasets[x].values()), 1)


		self._hit_plot.barh(self._hit_cat, self._hit_miss, label='Hit', height=0.5, color=GRAPHRED)
		self._hit_plot.barh(self._hit_cat, self._hit_tied, label='Tied', height=0.5, left=self._hit_miss, color=GRAPHGRAY)
		start = [self._hit_miss[x] + self._hit_tied[x] for x in range(len(self._hit_miss))]
		self._hit_plot.barh(self._hit_cat, self._hit_hit, label='Miss', height=0.5, left=start, color=GRAPHGREEN)
		self._hit_plot.legend()

		self._hit_canvas.draw()


	def _update_panel2(self) -> None:
		'''Update everything in panel 2'''
		self._update_season_log()
		self._update_5_log()


	def _create_season_log(self) -> None:
		'''Create a display sheet of the per season stats for the player'''
		self._season_log_panel = tkinter.LabelFrame(self._panel2, height=520, width=140, bg=BLACK, bd=0)
		self._season_log_panel.grid_propagate(0)
		self._season_log_panel.grid(row=0, column=0)

		self._season_log_title = tkinter.Label(self._season_log_panel, text='Season Averages', bg=BLACK, fg=TEAL, font=STAT12)
		self._season_log_title.grid(row=0, column=0, columnspan=2)


	def _update_season_log(self) -> None:
		'''Update log when either the player or stat type changes'''
		for widget in self._season_log_panel.winfo_children():
			widget.destroy()

		self._season_log_title = tkinter.Label(self._season_log_panel, text='Season Averages', bg=BLACK, fg=TEAL, font=STAT12)
		self._season_log_title.grid(row=0, column=0, columnspan=2)

		data = self._api.per_year_convert(self._stat_dropdown.get())

		for x in range(len(data)):
			year, stat = data[x]
			tkinter.Label(self._season_log_panel, text=year, bg=BLACK, font=TEXT10, fg=LIGHTBLUE, width=8).grid(row=x + 1, column=0)
			tkinter.Label(self._season_log_panel, text=stat, bg=BLACK, font=TEXT10, fg=WHITE, width=8).grid(row=x + 1, column=1)


	def _create_5_log(self) -> None:
		'''Creates a box that displays the last 5 games in the game log'''
		self._game_log_panel = tkinter.LabelFrame(self._panel2, height=200, width=140, bg=BLACK, bd=0)
		self._game_log_panel.grid_propagate(0)
		self._game_log_panel.grid(row=1, column=0)

		self._game_log_title = tkinter.Label(self._game_log_panel, text='Game Log', bg=BLACK, fg=TEAL, font=STAT12)
		self._game_log_title.grid(row=0, column=0, columnspan=2)


	def _update_5_log(self) -> None:
		'''Updates the box that displays 5 games at a time'''
		for widget in self._game_log_panel.winfo_children():
			widget.destroy()

		self._game_log_title = tkinter.Label(self._game_log_panel, text='Game Log', bg=BLACK, fg=TEAL, font=STAT12)
		self._game_log_title.grid(row=0, column=0, columnspan=2)

		print('updated beyotch')


	def _create_hit_rates_log(self) -> None:
		'''Display hit rates, percentages, etc'''
		self._hit_rate_panel = tkinter.LabelFrame(self._panel2, height = 200, width = 140)
		self._hit_rate_panel.grid_propagate(0)
		self._hit_rate_panel.grid(row=2, column=0)

		self._hit_rate_title = tkinter.Label(self._hit_rate_panel, text='Hit Rates', bg=BLACK, fg = TEAL, font = STAT12)
		self._hit_rate_title.grid(row=0,column=0,columnspan=2)


	def _update_hit_rates_log(self) -> None:
		pass