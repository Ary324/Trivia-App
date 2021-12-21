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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

def test_get_categories(self):
        response = self.client().get('/categories')
        self.assertEqual(response.status_code,200)
        data = json.loads(response.data)
        self.assertEqual(len(data['categories']),10)

def test_get_questions(self):
        response = self.client().get('/questions')
        self.assertEqual(response.status_code,200)
        data = json.loads(response.data)
        self.assertEqual(len(data['questions']),10)

def test_add_question(self):
        res = self.client().post('/questions/add', json=self.new_question)
        self.assertEqual(res.status_code, 200)

def test_get_question_by_categories(self):
        res = self.client().get('/categories/1/questions')
        self.assertEqual(res.status_code, 200)


def test_search_questions(self):
        res = self.client().post('/questions', json=self.search)
        self.assertEqual(res.status_code, 200)

def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Question ID 2 has been deleted')
        self.assertEqual(res.status_code, 200)

 
def test_post_quiz(self):
        res = self.client().post('/quizzes', json=self.quiz)
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()