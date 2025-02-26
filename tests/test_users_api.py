import uuid

import pytest
from utils.api_client import APIClient

@pytest.fixture(scope="module")
def api_client():
    return  APIClient()

def test_get_users(api_client):
    response = api_client.get("users")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_users(api_client, load_user_data):
    # user_data = {
    #     "name": "Kiran Kumar",
    #     "username": "development user",
    #     "email": "development@gmail.com"
    # }
    user_data = load_user_data["new_user"]
    unique_email = f"{uuid.uuid4().hex[:8]}@gmail.com"
    print(unique_email)
    user_data["email"] = unique_email
    response = api_client.post("users", user_data)
    print(response.json())
    assert response.status_code == 201
    assert response.json()['name'] == "Kiran Kumar"
    id = response.json()['id']
    id = id - 1
    # print(id, ' - 009')
    response = api_client.get(f"users/{str(id)}")
    print(response.json())
    assert response.status_code == 200
    assert response.json()['name'] == "Clementina DuBuque"


def test_update_users(api_client, load_user_data):
    # user_data = {
    #     "name": "Kiran K",
    #     "username": "development user",
    #     "email": "development@gmail.com"
    # }
    user_data = load_user_data["update_existing_user"]
    unique_email = f"{uuid.uuid4().hex[:8]}@gmail.com"
    print(unique_email)
    user_data["email"] = unique_email
    response = api_client.put("users/2", user_data)
    print(response.json())
    assert response.status_code == 200
    # assert response.json()['name'] == "Kiran K"
    # response = api_client.get(f"users/1")
    # print(response.json())


def test_delete_users(api_client):
    response = api_client.delete("users/1")
    print(response.json())
    assert response.status_code == 200


## my code will be updted in new test sub branch
## new test branch 01


"""

1. Where are you calling the api_client() function?
In your test_users_api.py module, the api_client function is not being explicitly called in the,
usual sense (like calling a method on an object). Instead, api_client is defined as a fixture, 
using the @pytest.fixture decorator.

Fixture in pytest is a special function that can provide setup code (before a test runs) and teardown code (after a test runs).
The api_client function is automatically invoked by pytest before running any test that requires it as an argument.
In test_get_users, pytest will automatically call the api_client() function to obtain the APIClient instance and
pass it as an argument to the test function.

-----------------------------------------------------------------------------------------------------------------------

2. After importing APIClient Class, where am I creating the object for APIClient class?
In your api_client() fixture, you're creating an instance of the APIClient class like this:

python

@pytest.fixture(scope="module")
def api_client():
    return  APIClient()
    
Here, the api_client fixture returns an instance of the APIClient class, which is created by calling APIClient().

-----------------------------------------------------------------------------------------------------------------------

3. For the test_get_users() function, one argument is there. Is that argument the api_client() function 
in the test_users_api module?

Yes, the argument api_client in the test_get_users() function is the result of the api_client() fixture.

When pytest sees test_get_users(api_client), it knows it needs to inject the value returned by the api_client fixture
into the api_client argument of the test function.
Since the api_client fixture creates an instance of APIClient, this instance will be passed to test_get_users.
So, api_client inside the test function will hold the APIClient instance and can be used to make the GET request
to the users endpoint.


How pytest fixtures work in general:
When you declare a fixture with @pytest.fixture(scope="module") (or any other scope, like function, class, or session),
pytest treats it as a resource that can be injected into your test functions.

So, whenever pytest sees that a test function requires an argument that matches a fixture's name, it automatically calls
the fixture and injects its returned value into the test function.

Answer to your question:
1. When pytest sees a test function (like test_get_users):

Pytest will check the test function’s parameters.
If one of the parameters matches the name of a fixture (in this case, the parameter is api_client and the fixture is api_client), pytest will automatically call the fixture (api_client) and inject whatever that fixture returns (the APIClient instance in your case) into the test function.

2. Fixture Injection:

The @pytest.fixture(scope="module") decorator tells pytest how long to keep the fixture instance around.
* Scope: "module" means the fixture will be created once per module (i.e., once per test_users_api.py).
* You can have multiple tests in the same module, and they can all use the same instance of the fixture without needing to create it every time.
* So, whenever pytest encounters a test in test_users_api.py (or any other test_*.py file) that has a parameter matching a fixture, it injects the returned value from that fixture into the test.

Example Breakdown:
Fixture Declaration (api_client fixture in test_users_api.py):

python

@pytest.fixture(scope="module")
def api_client():
    return APIClient()  # This creates and returns an APIClient instance
Test Function (test_get_users):

python

def test_get_users(api_client):  # api_client is an argument here
    response = api_client.get("users")
    assert response.status_code == 200
    assert len(response.json()) > 0
When pytest runs test_get_users, it sees that the api_client parameter exists in the test function. Since api_client is also the name of the fixture defined earlier in the same module, pytest will:

Call the api_client() fixture function.
Inject the instance of APIClient that the fixture returns into the api_client parameter of test_get_users.
Conclusion:
Yes, whenever pytest sees a test function with a parameter that matches a fixture name, it automatically calls that fixture and injects its returned value into the test function. This happens across the entire module (or wherever the fixture is defined with a scope like module, function, class, etc.), and the fixture provides the necessary setup resources to the test.

In other words:

When pytest sees test_get_users(api_client), it looks for a fixture called api_client and uses the return value of that fixture to populate the api_client parameter in the test_get_users function.
This is how pytest handles automatic dependency injection for test functions using fixtures.

-----------------------------------------------------------------------------------------------------------------------

4. Explain what happens when I execute pytest -s command in the terminal. Where do all the actions or functions get triggered?
Let's walk through the execution of the pytest -s command and see how pytest works with your code:

1. pytest discovers tests: When you run pytest -s, pytest will start by searching for test files in your project.
It looks for files that match the pattern test_*.py or *_test.py.

2. pytest_configure hook is triggered: The pytest_configure hook in conftest.py will be triggered
first (since it's hooked into pytest's configuration system).

This hook sets the report directory and filename for the HTML report.
It gets the current timestamp to create a unique filename for the report.
The htmlpath option is set in the config object, which will control where pytest stores the HTML test report after the run.

3. Fixtures are set up:

When pytest starts running the tests, it will look for any fixture dependencies.
The api_client() fixture in test_users_api.py is marked with scope="module". This means it will be set up once 
per module (i.e., the test_users_api.py module) and reused across all tests within that module.

The api_client fixture is executed, and it creates an instance of APIClient which is then injected
 into the test_get_users function.

4. Executing tests:

pytest will then execute your test functions. In your case, it will run test_get_users.

Inside the test_get_users function:

The api_client (which is an instance of APIClient) is already available as an argument.
The test will call api_client.get("users") to send a GET request to the https://jsonplaceholder.typicode.com/users endpoint.
It then verifies that the response status code is 200 and that the response body (the list of users) is non-empty
using assert statements.

5. Setup and Teardown (Fixture Finalization):

After the test runs, the setup_teardown fixture will be executed for each test.
It will first print "Setting up the resources" before running the test.
After the test has finished, it will print "Tearing down the resources" due to the yield statement.

6. Test Results:

After all tests have run, pytest will generate the report (based on the configuration you set in pytest_configure),
which will be saved in the reports directory as an HTML file.

7. Final Output:

Finally, pytest will display the test results in the terminal (including passed, failed, and skipped tests), and
the HTML report will be available in the specified directory.



5. Explain everything in detail
Let's go over your code with a bit more detail.

conftest.py:
pytest_configure(config): This hook is used to customize pytest's configuration before any tests are run. It sets up the
path for saving the HTML report, and this is done at the start of the test run.

setup_teardown() fixture: This fixture is automatically invoked before and after every test. It prints messages to indicate
the setup and teardown process for resources. The yield keyword is used to pause the fixture and allow the test function
to run between setup and teardown.
----------------------------------------------------------
api_client.py:
The APIClient class is designed to interact with an external API (https://jsonplaceholder.typicode.com).
The get method sends a GET request to the specified endpoint and returns the response.
-----------------------------------------------------------
test_users_api.py:
api_client() fixture: The fixture creates an instance of the APIClient class, making it available to the test functions.
test_get_users(): This is the test function where the API client is used to fetch data from the users endpoint.
The test verifies that:

    *The API request returns a 200 HTTP status code.
    *The response body contains more than 0 users.
    
Key Points:

*  Fixtures: Fixtures are essential in pytest as they provide a clean and manageable way of setting up and tearing down
resources for your tests.
* Dependency Injection: The arguments of the test functions (api_client in test_get_users) are automatically provided by
pytest's fixture system.
* Separation of Concerns: Your code follows good practices by separating concerns: APIClient focuses on API communication, 
conftest.py handles setup/teardown, and test_users_api.py contains your actual test logic.

This overall structure allows pytest to run your tests efficiently, manage the setup/teardown automatically, and make the
 testing process smooth.
 
 
"""