# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

 ## Endpoints

### GET /categories

- Returns a list of all categories, success value, and total number of categories. 
- page number: an optional query string parameter for specifing a page number, returns 10 categories for the specified page.


{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    },  
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true, 
  "total_categories": 6
}


### GET /questions

- returns the list of questions along with a list of categories
- result are paginated with 10 questions per page 
- page number: an optional query string parameter for specifing a page number, returns 10 questions for the specified page.
 
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    ...
  ], 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 19
}


### DELETE /questions/`question_id`

- Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value
- If the question of the given ID does not exist, error of status code 404 is returned.
- question id: a required url path parameter for specifing the id of the question to be deleted, id should be an integer

{
  "deleted": 25, 
  "success": true
}


### POST /questions

- Creates a new question using the submitted question, answer, difficulty and category. All the parameters are required. Returns the created question and success value.

 "Content-Type: application/json" -d '{"question":"What is colour of Liverpool FC","answer":"Red","difficulty":1,"category":6}'`

 
{
  "created": {
    "answer": "Red", 
    "category": 6, 
    "difficulty": 1, 
    "id": 25, 
    "question": "What is colour of Liverpool FC?"
  }, 
  "success": true
}
 

- If `search_term` is included in request body, the result of search for questions based on the given search term is returned, which returns a list of matched questions, success value, total number of result, and current category as `null`
- Error of status code 404 is thrown when there is not question on the given page.

 "Content-Type: application/json" -d '{"search_term":"Dutch"}
 
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
 

### GET /categories/`category_id`/questions

- Returns a list of questions in the given category, ID of the category, success value, and total number of questions
- Results are paginated in group of 10. Include a request argument to choose page number, starting from 1.
- Error of status code 404 is thrown when there is not question on the given page.


- category id: a required url path parameter for specifing the id of the category, id should be an integer


 
{
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 3, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
 

### POST /quizzes

- Returns one of the randomly chosen questions in the given category and success value.
- If `previous_questions` is provided in request body, they are excluded from selecting process.
- `question` is returned as `null` if there is no more questions which has not previously played in the category.

 
"Content-Type: application/json" -d '{"quiz_category":{"type":"Sports","id":6},"previous_questions":[20]}'`

 
{
  "question": {
    "answer": "Lionel Messi", 
    "category": 6, 
    "difficulty": 1, 
    "id": 21, 
    "question": "Who is most famous football player?"
  }, 
  "success": true
}
 


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
