from datetime import datetime
import unittest
from ..league import TeamRank, TeamScore, InputOutput
import os


class InputTest(unittest.TestCase):

    def setUp(self):
        self.input_output = InputOutput()
        
    def test_read_input_file(self):
        # print('==================')
        # print(os.getcwd())
        file_name = 'test_data.dat'
        # file_path = os.path.join('league_results', 'data_files', filename)

        expected_file_data = [
            {'Lions': 3, 'Snakes': 3},
            {'Tarantulas': 1, 'FC Awesome': 0},
            {'Lions': 1, 'FC Awesome': 1},
            {'Tarantulas': 3, 'Snakes': 1},
            {'Lions': 4, 'Grouches': 0},
        ]

        file_data = self.input_output.read_input_file(file_name)
        self.assertEqual(file_data, expected_file_data)

    def test_parse_line_input(self):
        line_input = 'Lions 1, FC Awesome 3'
        expected_parsed_input = {'Lions': 1, 'FC Awesome': 3}

        parsed_input = self.input_output.parse_line_input(line_input)
        self.assertDictEqual(parsed_input, expected_parsed_input)

 
class TeamRankTest(unittest.TestCase):

    def setUp(self):
        self.team_rank = TeamRank()

    def test_group_teams_by_score(self):
        '''        
        '''
        initial_teams_list = {
            'Team A': 12,
            'Team B': 25,
            'Team C': 13,
            'Team D': 12,
            'Team E': 7,
            'Team F': 12,
            'Team G': 4,
            'Team H': 13,
        }

        expected_team_scores = {
            12: ['Team A', 'Team D', 'Team F'],
            25: ['Team B'],
            13: ['Team C', 'Team H'],
            7: ['Team E'],
            4: ['Team G'],
        }
        
        team_scores = self.team_rank.group_teams_by_score(initial_teams_list)
        expected_keys = list(expected_team_scores.keys())
        keys = list(team_scores.keys())

        self.assertListEqual(sorted(keys), sorted(expected_keys))

        for key in keys:
            self.assertListEqual(sorted(team_scores[key]), sorted(expected_team_scores[key]))

        # self.assertEqual(team_scores, expected_team_scores)

    def test_rank_teams(self):

        team_scores = {
            12: ['Team D', 'Team A', 'Team F'],
            13: ['Team H', 'Team C'],
            25: ['Team B'],
            4: ['Team G'],
            7: ['Team E'],
        }

        expected_team_rankings = [
            ('Team B', 25),
            ('Team C', 13),
            ('Team H', 13),
            ('Team A', 12),
            ('Team D', 12),
            ('Team F', 12),
            ('Team E', 7),
            ('Team G', 4),
        ]

        team_rankings = self.team_rank.rank_teams(team_scores)
        self.assertEqual(team_rankings, expected_team_rankings)


    def test_order_teams(self):

        initial_teams_list = {
            'Team A': 12,
            'Team B': 25,
            'Team C': 13,
            'Team D': 12,
            'Team E': 7,
            'Team F': 12,
            'Team G': 4,
            'Team H': 13,
        }

        expected_team_rankings = [
            ('Team B', 25),
            ('Team C', 13),
            ('Team H', 13),
            ('Team A', 12),
            ('Team D', 12),
            ('Team F', 12),
            ('Team E', 7),
            ('Team G', 4),
        ]

        team_rankings = self.team_rank.order_teams(initial_teams_list)
        self.assertEqual(team_rankings, expected_team_rankings)


class TeamScoreTest(unittest.TestCase):

    def setUp(self):
        self.team_score = TeamScore()

    def test_tally_team_points(self):
        
        matches = [
            {'Lions': 3, 'Snakes': 3},
            {'Tarantulas': 1, 'FC Awesome': 0},
            {'Lions': 1, 'FC Awesome': 1},
            {'Tarantulas': 3, 'Snakes': 1},
            {'Lions': 4, 'Grouches': 0},
        ]

        expected_scores = {
            'Tarantulas': 6,
            'Lions': 5,
            'FC Awesome': 1,
            'Snakes': 1,
            'Grouches': 0,
        }

        scores = self.team_score.tally_team_points(matches)
        self.assertDictEqual(scores, expected_scores)

    def test_determine_team_score(self):
        test_data = [
            {
                'match': {'Team A': 1, 'Team B': 2},
                'result': {'Team A': 0, 'Team B': 3}
            },
            {
                'match': {'Team A': 1, 'Team B': 1},
                'result': {'Team A': 1, 'Team B': 1}
            },
            {
                'match': {'Team A': 0, 'Team B': 0},
                'result': {'Team A': 1, 'Team B': 1}
            },
            {
                'match': {'Team A': 3, 'Team B': 2},
                'result': {'Team A': 3, 'Team B': 0}
            },
        ]

        for test in test_data:
            result = self.team_score.determine_team_points(test['match'])
            self.assertDictEqual(result, test['result'])

        
class CompleteTest(unittest.TestCase):

    def setUp(self):
        self.input_output = InputOutput()
        self.team_rank = TeamRank()
        self.team_score = TeamScore()

    def testCompleteFileRun(self):
        expected_team_rankings = [
            ('Tarantulas', 6),
            ('Lions', 5),
            ('FC Awesome', 1),
            ('Snakes', 1),
            ('Grouches', 0),
        ]

        input_data = self.input_output.read_input_file('test_data.dat')
        team_scores = self.team_score.tally_team_points(input_data)
        team_rankings = self.team_rank.order_teams(team_scores)

        self.assertEqual(team_rankings, expected_team_rankings)