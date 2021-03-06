from scraper.common_util import Common
from scraper.model.stats.head_to_head import HeadToHead


class Commentary:
    def __init__(self, link, match_squad_ref):
        self.__short_name_to_full_name_map = {}
        self.__full_match_commentary = []
        self.__per_innings_head_to_head_object_cache = [{}, {}, {}, {}]

        # {"player_name" : "team_name", ......}
        self.__local_squad = {}
        for team in match_squad_ref:
            for player in match_squad_ref[team]:
                self.__local_squad[player] = team

        soup = Common.get_soup_object(link)
        commentary_blocks = soup.find_all('p', class_='cb-col cb-col-90 cb-com-ln')
        for commentary_block in reversed(commentary_blocks):
            ball_commentary = commentary_block.text.split(',')
            self.__full_match_commentary.append(ball_commentary)

    def get_per_innings_head_to_head_data(self):
        curr_batsman_team = None
        current_innings_num = 0
        for ball_commentary in self.__full_match_commentary:
            players = ball_commentary[0].split(" to ")
            if len(players) < 2:
                continue
            batsman = self.__get_player_full_name_from_short_name(players[1].strip())
            batsman_team = self.__local_squad[batsman]
            bowler = self.__get_player_full_name_from_short_name(players[0].strip())
            bowler_team = self.__local_squad[bowler]
            if curr_batsman_team is None :
                curr_batsman_team = batsman_team
            if curr_batsman_team != batsman_team:
                current_innings_num += 1
                curr_batsman_team = batsman_team
            head_to_head = self.__get_head_to_head_object(batsman, batsman_team, bowler, bowler_team,
                                                          current_innings_num)
            if len(ball_commentary) >= 3:
                outcome = self.__get_outcome_of_a_ball(ball_commentary[1], ball_commentary[2])
            elif len(ball_commentary) >= 2:
                outcome = self.__get_outcome_of_a_ball(ball_commentary[1], "")
            else:
                continue
            head_to_head.add_score(outcome['balls'], outcome['runs'], outcome['wicket'])
        # Get list of head_to_head objects of this match per innings
        per_innings_head_to_head_data = []
        for innings_head_to_head_object_cache in self.__per_innings_head_to_head_object_cache:
            innings_head_to_head_data = []
            for batsman in innings_head_to_head_object_cache:
                for bowler in innings_head_to_head_object_cache[batsman]:
                    innings_head_to_head_data.append(innings_head_to_head_object_cache[batsman][bowler])
            per_innings_head_to_head_data.append(innings_head_to_head_data)
        return per_innings_head_to_head_data

    def __get_player_full_name_from_short_name(self, name):
        if name not in self.__short_name_to_full_name_map.keys():
            close_match = Common.get_close_match(name, self.__local_squad.keys())
            self.__short_name_to_full_name_map[name] = close_match
        return self.__short_name_to_full_name_map[name]

    def __get_head_to_head_object(self, batsman, batsman_team, bowler, bowler_team, innings_num):
        innings_head_to_head_object_cache = self.__per_innings_head_to_head_object_cache[innings_num]
        if batsman in innings_head_to_head_object_cache:
            if bowler not in innings_head_to_head_object_cache[batsman]:
                innings_head_to_head_object_cache[batsman][bowler] = \
                    HeadToHead(batsman, batsman_team,bowler, bowler_team)
        else:
            innings_head_to_head_object_cache[batsman] = {}
            innings_head_to_head_object_cache[batsman][bowler] = \
                HeadToHead(batsman, batsman_team,bowler, bowler_team)
        return innings_head_to_head_object_cache[batsman].get(bowler)

    def __get_outcome_of_a_ball(self, ball_outcome_str, ball_outcome_str_extra):
        outcome_match = False
        outcome = {'runs': 0, 'balls': 0, 'wicket': False, 'no_ball': False}
        ball_data_string = ball_outcome_str.strip()
        ball_data_string_extra = ball_outcome_str_extra.strip()
        for item in Common.ball_outcome_mapping:
            if item in ball_data_string:
                outcome = Common.ball_outcome_mapping[item].copy()
                outcome_match = True
                break
        if not outcome_match:
            print(ball_data_string, ball_data_string_extra)
        if outcome['no_ball']:
            outcome_extra = self.__get_outcome_of_a_ball(ball_data_string_extra, "")
            outcome['runs'] = outcome_extra['runs']
        if outcome['wicket'] and ("Run Out!!" in ball_data_string):
            # get number of runs taken before getting out for Run Out!!
            #  out de Grandhomme Run Out!! de Grandhomme isn't the quickest between the wickets.
            #  out Negi Run Out!! 1 run completed.
            outcome['wicket'] = False
            if " completed." in ball_data_string:
                outcome_extra = self.__get_outcome_of_a_ball(
                    ball_data_string.split("Run Out!!")[1].split(" completed.")[0].strip(), "")
                outcome['runs'] = outcome_extra['runs']
        return outcome
