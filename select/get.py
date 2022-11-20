from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri)

def get_films_match(tx, title):
    ts = []
    films = []
    result = tx.run("MATCH (a:Film)-[:MADE_BY]->(f:Person) "
                    "WHERE  a.title = $title "
                    "RETURN f.name AS person", title=title)
    for record in result:
        ts.append(record["person"])

    if len(ts) > 0:
        result = tx.run("MATCH (a:Film)-[:MADE_BY]->(f:Person) "
                        "WHERE  f.name = $name AND a.title <> $title "
                        "RETURN a.title AS film", name=ts[0], title=title);
        for record in result:
            films.append(record["film"])

    return films

def get_films_by_name(tx, title):
    films = []
    result = tx.run("MATCH (a:Film) "
                    "WHERE  a.title = $title "
                    "RETURN a.title AS film", title=title)
    for record in result:
        films.append(record["film"])
    return films

with driver.session() as session:
     film_name_input    = input("Write your favorite film name: ")
     films_matched      = session.execute_read(get_films_match, film_name_input)
     for film in films_matched:
         print(film)

driver.close()