from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia
# import JSON
import pdb
# pdb.set_trace()
sparql = SPARQLWrapper('http://dbpedia.org/sparql')
sparql.setReturnFormat(JSON)

def get_similar_page_name(similar):
    results = wikipedia.search(similar)
    # for result in results:
    #     if 'Book' in result:
    #         return str(result)
    return str(results[0])

def build_query(category='book', similar=None, genre=None, subject=None, start=None, end=None):
    # don't necessary want disticnt author
    query = 'SELECT DISTINCT ?title ?abstract ?author ?isbn WHERE { '

    if similar:
        similar_page_name = get_similar_page_name(similar)
        if similar_page_name: 
            query += '?similar rdfs:label "{}"@en .\n'.format(similar_page_name)
            query += '?similar dbo:literaryGenre ?genre .\
                  ?res dbo:literaryGenre ?genre .\n'
        elif genre:
            query += '?similar dbo:literaryGenre ?genre .\
                  ?res dbo:literaryGenre ?genre .\n'

        else:
            query += '?res rdfs:label "{}"@en .\n'.format(category)

    if subject:
        query += '?res dbo:subject "{}" .\n'.format(subject)

    query += '?res dbo:isbn ?isbn .\
                ?res rdfs:label ?title .\
                ?res dbo:abstract ?abstract .\
                ?res dbo:author ?author_ .\
                ?author_ rdfs:label ?author .\n'

    if start:
        query += '?res dbo:publicationDate ?date. \
                    FILTER(YEAR(?date) > {}) .\n'.format(start)
        
        if end:
            query += 'FILTER(YEAR(?date) < {}) .\n'.format(end)

    elif end:
        query += '?res dbo:publicationDate ?date. \
                    FILTER(YEAR(?date) < {}) .\n'.format(end)

    query += '} LIMIT 10'

    sparql.setQuery(query)
    return query

def execute_query(query):
    try:
        results = sparql.query().convert()

    except Exception as e:
        print(e)
        return [['Suggestion could not be gathered at this time']]

    rows = results["results"]["bindings"]
    values = []
    for row in rows:
        values.append([row['title']['value'], row['author']['value'], row['isbn']['value'], row['abstract']['value']])

    return values

# def format_results()