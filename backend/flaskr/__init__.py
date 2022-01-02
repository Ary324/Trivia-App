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
      categories = {category.id:category.type for category in cats}

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
     'current_catgory': "",
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

    if data['question'] == 0 or data['answer'] == 0 \
      or data['difficulty'] == 0 or data['category'] == 0:
      abort(422)

    question = Question(**data)
    question.insert()
    
    result = {
      'success': True,
    }

    return jsonify(result)

  @app.route('/questions', methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)

    if search_term:
      search_results = Question.query.filter(
      Question.question.ilike(f'%{search_term}%')).all()

    result = {
      'success': True,
      'questions': [
        question.format() for question in search_results
      ],
      'total_questions': len(search_results),
      'current_category': None,
      'category': request.get_json()['category'],
      'page': request.args.get('page', 1, type=int)
    }

    return jsonify(result)

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_category(category_id):
    categories = Category.query.all()
    category_type = Category.query.get(category_id).format()['type']
    selection = Question.query.filter_by(category=category_id).all()
    current_questions = paginate(request, selection)

    if len(current_questions) == 0:
      abort(404)

    result = {
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'current_category': category_type,
      'page': request.args.get('page', 1, type=int)
    }

    return jsonify(result)
 
  
  @app.route('/quizzes', methods=['POST'])
  def get_questions_for_quiz():

    body = request.get_json()
    previous = body.get('previous_questions')
    category = body.get('quiz_category')
    
    if request.get_json()['quiz_category']['id'] == 0:
      selection = Question.query.all()
    else:
      selection = Question.query.filter_by(category=request.get_json()['quiz_category']['id']).all()
    questions = list(map(Question.format, selection))
    
    if len(questions) == 0:
        question = Question("","",None, None).format()

    def check_if_used(question):
      used = False
      for q in previous:
        if (q == question.id):
          used = True

      return used

    question = random.choice(questions)

    while (check_if_used(question)):
      question = random.choice(questions)

      if (len(previous) == len(questions)):
        return jsonify({
          'success': True
        })



    result = {
      'success': True,
      'question': question
    }

    return jsonify(result)

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad Request'
    }), 400

  @app.errorhandler(401)
  def access_denied(error):
    return jsonify({
      'success': False,
      'error': 401,
      'message': 'Not Authorized'
    }), 401

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Not Found'
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'Method Not Allowed'
    }), 405

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable Entity'
    }), 422
  
  return app
app = create_app

    