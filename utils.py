from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia
import json
import pdb
from functools import lru_cache
# pdb.set_trace()
sparql = SPARQLWrapper('http://dbpedia.org/sparql')
sparql.setReturnFormat(JSON)

def get_similar_page_name(similar):
    results = wikipedia.search(similar)
    # for result in results:
    #     if 'Book' in result:
    #         return str(result)
    return str(results[0])

@lru_cache(maxsize=10)
def build_query(category='book', similar=None, genre=None, start=None, end=None):
    # don't necessary want disticnt author
    query = 'SELECT DISTINCT ?title ?author ?isbn WHERE { '

    if similar:
        similar_page_name = get_similar_page_name(similar)
        if similar_page_name: 
            query += '?similar rdfs:label "{}"@en .\n'.format(similar_page_name)
            query += '?similar dbo:literaryGenre ?genre .\
                  ?res dbo:literaryGenre ?genre .\n'
    # don't want conflicting genres. prioritize inputted but then how do you connect with similar?
    # if genre:
    #     query += '?similar dbo:literaryGenre ?genre .\
    #               ?res dbo:literaryGenre ?genre .\n'

    query += '?res dbo:isbn ?isbn .\
                ?res rdfs:label ?title .\
                ?res dbo:author ?author_ .\
                ?author_ rdfs:label ?author .}\n'

    # if start:
    #     query += 'FILTER(?year[] > {}) .\n'.format(start)

    # if end:
    #     query += 'FILTER(?year[] , {}) .}\n'.format(end)

    query += 'LIMIT 10'

    sparql.setQuery(query)
    return query

@lru_cache(maxsize=10)
def execute_query(query):
    try:
        results = sparql.query().convert()

    except Exception as e:
        print(e)
        return 'Suggestion could not be gathered at this time'

    # if len(..) == 0:
    #   print('no results')
    #   return 'No matches found. Try broadening your criteria or removing then entirely'
    # try:
    #     print(json.loads(results))
    # except:
    #     pass
    rows = results["results"]["bindings"]
    values = []
    # don't need to do this for all rows since only suggest one, would require generator
    for row in rows: # need to fix author error
        values.append([row['title']['value'], 'author_name', row['isbn']['value']])

    return values
