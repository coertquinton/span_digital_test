import os

class TeamRank:
    
    def group_teams_by_score(self, team_scores):
        
        teams_by_score = {}

        for team, score in team_scores.items():
            if score not in teams_by_score:
                teams_by_score[score] = [team]
            else:
                teams_by_score[score].append(team)

        return teams_by_score

    def rank_teams(self, team_scores):
        ranked_teams = []

        for key in sorted(team_scores, reverse=True):
            for team in sorted(team_scores[key]):
                ranked_teams.append((team, key))

        return ranked_teams

    def order_teams(self, initial_team_list):
        teams_by_score = self.group_teams_by_score(initial_team_list)
        ranked_teams = self.rank_teams(teams_by_score)
        return ranked_teams


class TeamScore:

    def tally_team_points(self, matches):
        teams_points = {}
        for match in matches:
            result = self.determine_team_points(match)
            for team, score in result.items():
                if team not in teams_points:
                    teams_points[team] = score
                else:
                    teams_points[team] += score

        return teams_points

    def determine_team_points(self, match):
        
        team_A, team_B = match.keys()
        score_A, score_B = match[team_A], match[team_B]

        if score_A == score_B:
            return {team_A: 1, team_B: 1}
        elif score_A > score_B:
            return {team_A: 3, team_B: 0}
        else:
            return {team_A: 0, team_B: 3}


class InputOutput:

    def read_input_file(self, file_name):

        directory_name = os.path.join('league_results', 'data_files')
        data_lines = []
        try:
            with open(os.path.join(directory_name, file_name), 'r') as f:
                for line in f:
                    data_lines.append(self.parse_line_input(line))
            
        except FileNotFoundError:
            print('')
            print('Error')
            print('File %s not found in directory %s' %(file_name, directory_name))
        finally:
            return data_lines

    def read_cmd_line_input(self):
        data_lines = []

        print('')
        print('Please enter the match data or type "done" and press enter.')
        print('Match Data Format:  <TEAM_A> <TEAM_A_SCORE>, <TEAM_B> <TEAM_B_SCORE>')
        match = input('Enter match data:')
        
        while match.lower() != 'done':

            try:
                parsed_input = self.parse_line_input(match)
                data_lines.append(parsed_input)
            except ValueError:
                print('-- Error.  Data not excepted for %s' % str(match))

            print('Please enter the match data or type "done" and press enter.')
            match = input('Enter match data:')

        return data_lines

    def print_cmd_line_output(self, team_positions):
        print('')
        print('League Table')
        print('------------')
        for count, team_position in enumerate(team_positions, 1):
            team, points = team_position
            print('%s. %s, %s points' % (str(count), team, str(points)))        


    def parse_line_input(self, line_input):
        itemA, itemB = [item.strip() for item in line_input.split(',')]
        team_a, score_a = itemA.rsplit(' ', 1)
        team_b, score_b = itemB.rsplit(' ', 1)
    
        return {team_a: int(score_a), team_b: int(score_b)}


def main():    
    text_input = prompt_main_input()

    while text_input != 'exit':
        team_sore = TeamScore()
        team_rank = TeamRank()
        input_output = InputOutput()

        if text_input in ["file input", "cmd line"]:
            data_lines = []
            if text_input == 'file input':
                file_name = input('Please enter the name of the League Results file:')
                data_lines = input_output.read_input_file(file_name)
                
            if text_input == "cmd line":
                data_lines = input_output.read_cmd_line_input()
            
            team_points_tally = team_sore.tally_team_points(data_lines)
            league_rankings = team_rank.order_teams(team_points_tally)
            input_output.print_cmd_line_output(league_rankings)
        else:
            print('Invalid command entered.')

        text_input = prompt_main_input()

def prompt_main_input():
    print('')      
    print('Please type "file input", "cmd line" or "exit" and then press enter')
    text_input = input('Enter "file input", "cmd line" or "exit": ')
    return text_input
    
if __name__ == "__main__":
    print('League Table Program')
    main()