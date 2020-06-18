import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate(request, selection):
  '''
  Implement the pagination to the frontend.
  Show 10 Questions per page

  Args:
    param request : read the request
    param selection : db query
    
  Returns:
    current_questions : List from the db

  '''
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  '''
  Create and configurate the Flask Application and contain all endpoints

  Args:
    param test_config : defaulf None

  Returns:
    param app : run the flask server
  '''
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"*/api/*": {'origins': '*'}})
  
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorisation')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  
  @app.route('/categories', methods=['GET'])
  def read_categories():
    '''
    Read the categories table and return all Categories in JSON format

    Args:
      : Null

    Returns:
      param success : true if the request was successful otherwise return a 404 error
      param categories : list of all categories
    '''

    selection = Category.query.order_by(Category.id).all()
    current_questions = paginate(selection, request)
  
    if len(current_questions) == 0:
      abort(404)
    else:
      return jsonify({
        'success': True,
        'categories': current_questions
      })

  @app.route('/questions', methods=['GET'])
  def get_question():
    '''
    Read the questions table and return all questions in the database

    Args:
      : Null

    Returns:
      param success : true if the request was successful otherwise return a 404 error
      param questions : list of all questions
      param total_questions : length of the list questions
      param categories : categories
      param current_category : None
    '''

    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate(request, selection)
    
    categories = {cat.id:cat.type for cat in selection}
    
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(selection),
      'categories': categories,
      'current_category': None
    })
 
  @app.route('/questions/<int:question_id')
  def delete_question(question_id):
    '''
    Delete one or more questions from the question table by ID

    Args:
      param question_id : ID of the question to delete

    Returns:
      param deleted : The ID from the deleted question(s) 
      param success : true if the request was successful otherwise return a 404 or 422 error
    '''

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

  @app.route('/questions', methods=['POST'])
  def add_question():
    '''
    Add a new Question the questions table the arguments are
    from the frondend form

    Args:
      param question : new question
      param answer : answer to the new question
      param category : the category for the new question
      param difficulty : the difficulty of the new question

    Returns:
      param created : ID from the new question
      param success :  true if the request was successful otherwise return a 422 error
    '''

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
  
  @app.route('/searchQuestions', methods=['POST'])
  def search_question():
    '''
    Search a question in the questions table

    Args:
      param searchTerm : search string given from the frontend form

    Returns:
      param success : true if the request was successful otherwise return a 404 error
      param questions : the result of search
      param total_questions : sum of the result
      param current_category : None
    '''

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
  

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def list_category(category_id):
    '''
    Return questions based on category

    Args:
      param category_id : ID of the category

    Returns:
      param success : true if the request was successful otherwise return a 404 error
      param questions : list of questions based on category
      param total_questions : sum of the questions
      param current_category : None
    '''
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
  
  @app.route('/quizzes', methods=['POST'])
  def get_quiz():
    '''
    Return the questions and categories from the database to the game
    the arguments are submitted from the frondend form

    Args:
      param category : category to play
      param previous_questions : the previous answered questions

    Returns:
      param success : true if the request was successful otherwise return a 404 error
      param question : random questions
    '''

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
  
  @app.errorhandler(400)
  def bad_request(error):
    '''
    Return the Error messages if an error ocurres in the Routes

    Args:
      param error : error from route

    Returns:
      param success : False
      param error : 400
      param message : Bad request
    '''
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    '''
    Return the Error messages if an error ocurres in the Routes

    Args:
      param error : error from route

    Returns:
      param success : False
      param error : 404
      param message : This page does not exist
    '''
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'This page does not exist.'
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    '''
    Return the Error messages if an error ocurres in the Routes

    Args:
      param error : error from route

    Returns:
      param success : False
      param error : 405
      param message : The method is not allowed for the requested URL
    '''
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'The method is not allowed for the requested URL.'
      }), 405

  @app.errorhandler(422)
  def unprocessable_request(error):
    '''
    Return the Error messages if an error ocurres in the Routes

    Args:
      param error : error from route

    Returns:
      param success : False
      param error : 422
      param message : Unable to process request
    '''
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unable to process request.'
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    '''
    Return the Error messages if an error ocurres in the Routes

    Args:
      param error : error from route

    Returns:
      param success : False
      param error : 500
      param message : Server error
    '''
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Server error.'
    }), 500

  return app

    
