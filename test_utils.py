import pytest

from utils import build_query, execute_query

params = dict(
    similar = "Harry Potter and the Philosopher's Stone",
    genre = None,
    subject = None,
    start = 1982,
    end = 2018
)

def test_build_query(**params):
    query = build_query(**params)
    print(query)
    # assert build_query == ''

    results = execute_query(query)
    # assert result
    print(results)
    # print(results)
    # assert results

test_build_query(**params)