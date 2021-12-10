import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  return questions[start:end]


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={"*": {"origin": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                           'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods',
                           'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    cats = Category.query.all()
    if cats is None:
      abort(404)
    else:
      categories = [category.format() for category in cats]

      return jsonify({
        'categories': categories
      })

  @app.route('/questions', methods=['GET'])
  def get_question():
    selection = Question.query.all()
    current_questions = paginate(request, selection)
    cats = Category.query.all()
    categories = [category.format() for category in cats]

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
     'questions': current_questions,
     'categories': categories,
     'total_questions': len(selection),
     'current_catgory': categories,
     'page': request.args.get('page', 1, type=int)
   })



  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).first()
      question.delete()
    except:
      abort(404)
    finally:
      result = {
        'success': True,
        'message': f'Question ID {question_id} has been deleted'
      }

    return jsonify(result)

  @app.route('/questions/add', methods=['POST'])
  def add_question():
    data = {
      'question': request.get_json()['question'],
      'answer': request.get_json()['answer'],
      'category': request.get_json()['category'],
      'difficulty': request.get_json()['difficulty']
    }

    check_for_duplicate = Question.query.filter(Question.question == data['question']).all()
    if len(check_for_duplicate) > 0:
      abort(422)

    question = Question(**data)
    question.insert()
    
    result = {
      'success': True,
    }

    return jsonify(result)

  @app.route('/questions', methods=['POST'])
  def search_questions():
    selection = Question.query.filter(Question.question.ilike(f"%{request.get_json()['searchTerm']}%")).all()
    current_questions = paginate(request, selection)
    categories = Category.query.all()

    if len(current_questions) == 0:
      abort(404)

    result = {
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'categories': categories,
      'page': request.args.get('page', 1, type=int)
    }

    return jsonify(result)

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_category(category_id):
    selection = Question.query.filter_by(category=category_id).all()
    current_questions = paginate(request, selection)
    categories = Category.query.all()

    if len(current_questions) == 0:
      abort(404)

    result = {
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'categories': categories,
      'current_category': category_id,
      'page': request.args.get('page', 1, type=int)
    }

    return jsonify(result)
  

 

  

  # '''
  # @TODO: 
  # Create a GET endpoint to get questions based on category. 

  # TEST: In the "List" tab / main screen, clicking on one of the 
  # categories in the left column will cause only questions of that 
  # category to be shown. 
  # '''


  # '''
  # @TODO: 
  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters 
  # and return a random questions within the given category, 
  # if provided, and that is not one of the previous questions. 

  # TEST: In the "Play" tab, after a user selects "All" or a category,
  # one question at a time is displayed, the user is allowed to answer
  # and shown whether they were correct or not. 
  # '''

  # '''
  # @TODO: 
  # Create error handlers for all expected errors 
  # including 404 and 422. 
  # '''
  
  return app

    