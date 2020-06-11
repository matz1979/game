import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"*/api/*": {'origins': '*'}})
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorisation')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def read_categories():
    cate = Category.query.order_by(Category.id).all()
    form_cate = {cat.id: cat.type for cat in cate}

    if len(form_cate) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': form_cate
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_question():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate(request, selection)
    
    cate = Category.query.order_by(Category.id).all()
    categories = {cat.id:cat.type for cat in cate}
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'categories': categories,
      'current_category': None
    })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id')
  def delete_question(question_id):
    try:
      to_del = Question.query.filter(Question.id == question_id).one_or_none()

      if to_del is None:
        abort(404)
      to_del.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():

    body = request.get_json()

    try:
      question = Question(
        question = body.get('question', None),
        answer = body.get('answer', None),
        category = body.get('category', None),
        difficulty = body.get('difficulty', None)
        )
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/searchQuestions', methods=['POST'])
  def search_question():

    body = request.get_json()
    search_term = body.get('searchTerm', None)

    if search_term is None:
      abort(404)

    selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).all()
    current_question = paginate(selection, request)

    return jsonify({
        'success': True,
        'questions': current_question,
        'total_questions': len(current_question),
        'current_category': None
    })
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def list_category(category_id):
    selection = Question.query.filter(Question.category == category_id).all()
    currend_question = paginate(selection, request)

    if currend_question is None:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'questions': currend_question,
        'total_questions': len(currend_question),
        'current_category': None
      })
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz():
      body = request.get_json()
      previous_questions = body.get('previous_questions', None)
      quizCategory = body.get('quiz_category', None)

      if quizCategory['id'] == 0:
          questions = Question.query.order_by(Question.id).all()
      else:
          questions = Question.query.order_by(Question.id).filter(
              Question.category == quizCategory['id']).all()

          formatted_questions = [question.format() for question in questions]
      
      unasked_questions = []
      for question in formatted_questions:
          if question['id'] not in previous_questions:
              unasked_questions.append(question)

      next_question = None
      if len(unasked_questions) > 0:
          next_question = unasked_questions[0]

      return jsonify({
          'success': True,
          'question': next_question
      })

      if len(get_questions) == 0:
          return jsonify(None)
      else:
          questions = list(map(Question.format, get_questions))
          question = random.choice(questions)
          return jsonify(question)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'This page does not exist.'
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'The method is not allowed for the requested URL.'
      }), 405

  @app.errorhandler(422)
  def unprocessable_request(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unable to process request.'
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server error.'
    }), 500

  return app

    
