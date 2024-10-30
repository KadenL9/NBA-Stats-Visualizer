# Test API class to ensure that API is working and correct info is obtained
import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from api import API
import unittest


class APITests(unittest.TestCase):
	def setUp(self):
		self.api = API()


	def test_search_players_returns_an_empty_list_when_no_first_or_last_name_specified(self):
		self.assertEqual(self.api.search_players(), [])


	def test_search_players_returns_an_empty_list_when_nonexisting_player_specified(self):
		self.assertEqual(self.api.search_players(first_name='Gordon', last_name='Ramsey'), [])


	def test_search_players_returns_an_empty_list_when_old_player_is_specified(self):
		self.assertEqual(self.api.search_players(first_name='Larry', last_name='Jordan'), [])


	def test_search_players_returns_an_empty_list_when_nonexisting_first_name_specified(self):
		self.assertEqual(self.api.search_players(first_name='China'), [])


	def test_search_players_returns_an_empty_list_when_nonexisting_last_name_specified(self):
		self.assertEqual(self.api.search_players(last_name='Taiwan'), [])


	def test_search_players_returns_correct_players_when_first_name_specified(self):
		self.assertEqual(self.api.search_players(first_name='Lebron'), ['LeBron James'])


	def test_search_players_returns_correct_players_when_last_name_specified(self):
		self.assertEqual(self.api.search_players(last_name='Micic'), ['Vasilije Micic'])


	def test_search_players_returns_correct_players_when_full_name_specified(self):
		self.assertEqual(self.api.search_players(first_name='Johnny', last_name='Davis'), ['Johnny Davis'])


	def test_search_players_cannot_use_positional_arguments(self):
		try:
			self.api.search_players('Stephen', 'Curry')
		except:
			return
		raise AssertionError('Should have raised an error')


	def test_get_player_id_returns_the_correct_player_id_for_the_given_player(self):
		self.assertEqual(self.api.get_player_id('Stephen Curry'), 201939)


	def test_get_player_id_returns_0_if_player_does_not_exist(self):
		self.assertEqual(self.api.get_player_id('Larry Legend'), 0)


	def test_get_player_id_raises_an_error_when_players_with_the_same_name_is_entered(self):
		try:
			self.api.get_player_id('John Williams', 0)
		except:
			return
		raise AssertionError('Should have raised an error')


	def test_get_player_info_by_id_returns_careerstats_resource(self):
		careerstats = self.api.get_player_info_by_id(201939)
		self.assertEqual(self.api.get_careerstats()['resource'], 'playercareerstats')


	def test_get_player_info_by_id_returns_empty_json_data_if_invalid_id(self):
		self.api.get_player_info_by_id(0)
		self.assertEqual(len(self.api.get_careerstats()['resultSets'][0]['rowSet']), 0)


	def test_get_player_info_by_id_returns_careerstats_of_correct_player(self):
		self.api.get_player_info_by_id(201939)
		self.assertEqual(self.api.get_careerstats()['parameters']['PlayerID'], 201939)


	def test_get_player_info_by_id_returns_True_if_successful(self):
		self.assertTrue(self.api.get_player_info_by_id(201939))


	def test_get_player_info_by_id_returns_False_if_not_successful(self):
		self.assertFalse(self.api.get_player_info_by_id(-100))


	def test_get_player_info_by_id_returns_bio_of_correct_player(self):
		self.api.get_player_info_by_id(201939)
		self.assertEqual(self.api.get_bio()['resultSets'][0]['rowSet'][0][1], 'Stephen')


	def test_get_career_average_stat_returns_the_correct_stat(self):
		self.api.get_player_info_by_id(201939)

		stat_headers = ['PLAYER_ID', 'LEAGUE_ID', 'Team_ID', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT',
				  		'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
				  		'STL', 'BLK', 'TOV', 'PF', 'PTS']
		stats = [201939, '00', 0, 956, 950, 34.2, 8.5, 17.9, 0.473, 3.9, 9.2, 0.426, 3.9, 4.3,
				 0.91, 0.7, 4.1, 4.7, 6.4, 1.5, 0.2, 3.1, 2.3, 24.8]

		for x in range(len(stat_headers)):
			self.assertEqual(self.api.get_career_average_stat(stat_headers[x]), stats[x])


if __name__ == '__main__':
	unittest.main()