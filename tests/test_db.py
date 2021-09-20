# from application import create_app, db

# @pytest.fixture(scope='module')
# def test_home_page_post():
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/' page is is posted to (POST)
#     THEN check that a '405' status code is returned
#     """
#     flask_app = create_app('flask_test.cfg')

#     # Create a test client using the Flask application configured for testing
#     with flask_app.test_client() as test_client:
#         response = test_client.post('/')
#         assert response.status_code == 405