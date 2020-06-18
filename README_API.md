# API-Endpoints

The base URL from this API is: <http://localhost:5000>

GET 'api/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Sample URL: <http://localhost:5000/categories>
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET 'api/questions'

- Fetches a list of questions, paginated into pages with 10 questions per page.
- The list is ordered by question.id
- Request Arguments: page (integer)
- Sample URL: <http://localhost:5000/questions?page=1>
- Returns: An object that contains a list of question
{
    'success': True
    'questions': [
        {
            'id':
            'question': '',
            'answer': '',
            'category': '',
            'difficulty': ''
        },
        {...}
    ],
    'total_question' :,
    'categories': {
        '1': 'Science',
        '2': 'Art',
        '3': 'Geography',
        '4': 'History',
        '5': 'Entertainment',
        '6': 'Sports'
    },
    'current_category': None
}

POST 'api/questions'

- Create a new question
- Request Arguments: None
- Request Body: An object with four keys
{
    'question' : '',
    'answer : '',
    'category' : '',
    'difficlty' : ''
}

- Returns:
{
    'created' : '',
    'success' : ''
}

POST 'api/searchQuestions'

- Search questions
- Request Argument: None
- Request Body: An object with one key
{
    'searchTerm' : ''
}

- Returns:
{
    'success' : '',
    'question' : '',
    'total_questions' : '',
    'current_catagory' : None
}

GET 'api/categories/<int:category_id>/questions'

- Fetches a list of questions based on a given category.
- The list is ordered by question.id
- Request Argument: category_id (integer)
- Returns:
{
    'success' : '',
    'questions : [],
    'total_questions': '',
    'current_category' None
}

DELETE 'api/questions/<int:question_id>'

- Delete a question by question ID
- Request Argument: question_id (integer)
- Returns
{
    'success' : '',
    'deleted' : ''
}

## Errors

This API use standard HTTP error response codes:

- 200 OK
- 400 Bad Request
- 404 This page does not exist
- 405 The method is not allowed for this requested URL
- 422 Unable to process request
- 500 Server error