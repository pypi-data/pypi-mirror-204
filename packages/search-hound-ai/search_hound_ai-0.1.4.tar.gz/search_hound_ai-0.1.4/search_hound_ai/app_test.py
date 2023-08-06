import os
from pytest import raises
from search_hound_ai.app import ValidateEnv


def test_ValidateEnv():
    # Test case 1: When OPENAI_API_KEY is set
    os.environ['OPENAI_API_KEY'] = 'test_key'
    assert ValidateEnv() == None

    # Test case 2: When OPENAI_API_KEY is empty
    os.environ['OPENAI_API_KEY'] = ''
    with raises(SystemExit):
        ValidateEnv()
