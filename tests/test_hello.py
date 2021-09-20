# https://stackoverflow.com/a/48120470/720276
import pytest
from application import application

def test_hello():
    response = application.test_client().get('/')

    assert response.status_code == 200


# def test_hello():
#     response = application.test_client().get('/')

#     assert response.status_code == 200

