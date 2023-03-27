## Prerequisites

Before running the solution, make sure you have the following software installed:

```Docker```

## Project Structure

`app.py` - Flask Application for Code Similarity Checking\
`app.py` contains the implementation of a REST API web service using Flask. The API accepts source code as text input and checks whether it is a clone or not, based on the indexed repositories.


`index_repos.py` - Repository Indexing Script\
`index_repos.py` is a Python script for downloading and indexing local repositories. It works in two modes: creating 
an inverted index based on the available Token.Names and check_similiarity. This script is responsible for preparing 
the indexed data 
used by the Flask application in app.py to check for code similarity.

`test_app.py` - Test Suite for the Flask Application\
`test_app.py` contains a set of tests that cover the main functionality of the code similarity checking algorithm. These tests focus on the calculation of the percentage of similar token names between two sets of tokens.

To run the tests, execute the following command from the command line:

`python -m unittest test_app.py`
This command will run the tests and display the results, including any failures or errors that may occur during the testing process.

## Setup
Clone or download the project containing the solution.

In the project directory, create an .env file with the following content:

```REPO_NAME=your-repo-name```\
Replace your-repo-name with the GitHub repository you want to index, such as intellij/community.

Open a terminal in the project directory and build the Docker image:

```docker build -t your-image-name .```\
Replace your-image-name with a name for your Docker image, such as code_similarity_api.

Run the Docker container:

```docker run -p 5000:5000 your-image-name```\
Replace your-image-name with the name you used in the previous step.

Your API should now be running inside a Docker container and accessible at http://127.0.0.1:5000/.

### Usage
The API provides a single /check_similarity endpoint that accepts a POST request with a 'code' parameter containing the source code to be checked.

You can use curl or any API client like Postman to send requests to the API:

```curl -X POST -F "code=<source_code_here>" http://127.0.0.1:5000/check_similarity``` \
Replace <source_code_here> with the actual source code text you want to check.

The API will return a JSON response indicating if the submitted code is similar to any file in the indexed repositories or not. If a similar file is found, the path of the file will be included in the response.

### Examples
Let's assume the indexed repository contains the following code snippet in a file:

`example_code.py`
```
def hello_world():
    print("Hello, World!")
hello_world()
```

Now, you can test the /check_similarity endpoint with the following code snippets:

Example 1 - Very similar code
```def greet():
    print("Hello, World!")

greet()
```
Request:

`curl -X POST -F "code=def greet():\n\tprint(\"Hello, World!\")\n\ngreet()" http://127.0.0.1:5000/check_similarity`

Example 2 - Different code

```
def add(x, y):
    return x + y

result = add(1, 2)
print(result)
```
Request:

`curl -X POST -F "code=def add(x, y):\n\treturn x + y\n\nresult = add(1, 2)\nprint(result)" http://127.0.0.
1:5000/check_similarity` \
In these examples, the API returns a JSON response indicating whether the submitted code is similar to any file in the indexed repositories.