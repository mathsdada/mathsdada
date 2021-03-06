class BattingStats:
    def __init__(self, cursor):
        self.cursor = cursor

    def insert(self, batsman_id, match_id, innings_num, runs_scored, balls_played, num_fours, num_sixes, team_id):
        sql = """INSERT INTO batting_stats VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cursor.execute(sql,
                            (batsman_id, match_id, innings_num, runs_scored, balls_played, num_fours, num_sixes,
                             team_id))
