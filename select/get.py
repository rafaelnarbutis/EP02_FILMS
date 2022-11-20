from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri)

def get_films_of(tx, name):
    films = []
    result = tx.run("MATCH (a:Film)-[:MADE_BY]->(f:Person) "
                    "WHERE  f.name = $name "
                    "RETURN a.title AS film", name=name)
    for record in result:
        films.append(record["film"])
    return films

with driver.session() as session:
     films = session.execute_read(get_films_of, "Will Smith")
     for friend in films:
         print(friend)

driver.close()