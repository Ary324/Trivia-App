import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        self.new_question = {
            'question': 'What is my name?',
            'answer': 'Arian',
            'category': 1,
            'difficulty': 1
        }

        self.search = {
            'searchTerm': 'name'
        }

        self.quiz = {
            'previous_questions': [],
            'quiz_category': {
                'id': 0
            }
        }
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_200_add_question(self):
        res = self.client().post('/questions/add', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_422_add_question(self):
       bad_question = {
           'question': 'What is the difference between orange and blue?',
           'category': 4,
           'answer': '',
           'difficulty': 2,
       }

       res = self.client().post('/questions/add', json=bad_question)
       data = json.loads(res.data)

       self.assertEqual(data['success'], False)
       self.assertEqual(data['error'], 422)

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))


    def test_get_question_by_categories(self):
        res = self.client().get('/categories/1/questions')
        self.assertEqual(res.status_code, 200)

    def test_search_questions(self):
        res = self.client().post('/questions', json={"searchTerm": "title"})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Question ID 1 has been deleted')
        self.assertEqual(data['success'], True)

    def test_404_get_questions(self):
        res = self.client().delete('/questions/10000')
        self.assertEqual(res.status_code, 404)

    def test_405_delete_categories(self):
        res = self.client().delete('/categories')
        self.assertEqual(res.status_code, 405)

    def test_post_quiz(self):
        res = self.client().post('/quizzes', json=self.quiz)
        self.assertEqual(res.status_code, 200)
    
    def test_post_quizzes_error(self):
        error_data = {
            'previous_questions':[0, 0],
            'quiz_category': {
                'id': '',
                'type': ''
            }
        }
        res = self.client().post('/quizzes', json=error_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
