from server import Server
from flask import Flask, json
from flask_restful import Resource, Api, reqparse

server = Server()
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Schedule(Resource):
    def get(self):
        return {"response_schedule": server.schedule_query.get_schedule()}


class TeamStatsRecentForm(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument("format")
        args = parser.parse_args()
        return server.team_query.get_team_form(
            args['team_name'], args['venue_name'], args['format'])


class TeamStatsBattingMostRuns(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_batting_most_runs(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingBestStrikeRate(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_best_batting_strike_rate(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingMost50s(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_50s(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


api.add_resource(Schedule, '/schedule')
api.add_resource(TeamStatsRecentForm, '/team_stats/recent_form')
api.add_resource(TeamStatsBattingMostRuns, '/team_stats/batting/most_runs')
api.add_resource(TeamStatsBattingBestStrikeRate, '/team_stats/batting/best_strike_rate')
api.add_resource(TeamStatsBattingMost50s, '/team_stats/batting/most_50s')

if __name__ == "__main__":
    app.run(host="172.20.10.2", debug=True)

#
# file_dir = os.path.split(os.path.realpath(__file__))[0]
# file_name = file_dir + '\logs.txt'
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p', filename=file_name, level=logging.INFO)
# server.setup()
