from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.breakingnews import BreakingNews

breakingnews_api = Blueprint('breakingnews_api', __name__,
                   url_prefix='/api/breakingnews')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(breakingnews_api)

class BreakingNewsAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            title = body.get('title')
            if title is None or len(title) < 2:
                return {'message': f'Title is missing, or is less than 2 characters'}, 210
            # validate network
            network = body.get('network')
            if network is None or len(network) < 2:
                return {'message': f'Network is missing, or is less than 2 characters'}, 210
            # look for day
            day = body.get('day')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = BreakingNews(title=title, 
                      network=network)
            
            ''' Additional garbage error checking '''
            # convert to date type
            if day is not None:
                try:
                    uo.day = datetime.strptime(day, '%m-%d-%Y').date()
                except:
                    return {'message': f'Date of birth format error {day}, must be mm-dd-yyyy'}, 210
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            news = uo.create()
            # success returns json of user
            if news:
                return jsonify(news.read())
            # failure returns error
            return {'message': f'Processed {title}, either a format error or User ID {network} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            news = BreakingNews.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in news]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')