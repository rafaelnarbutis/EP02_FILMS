from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri)

create_film_cypher = "CREATE (a:Film {title: $title})"

create_person_cypher = "CREATE (a:Person {name: $name, category_job: $category_job})"

create_genre_cypher = "CREATE (a:Genre {type: $type})"

create_rate_cypher = "CREATE (a:Rate {value: $value})"

create_person_of_cypher = """MATCH (a:Film) WHERE a.title = $title
                             MATCH (p:Person) WHERE p.name = $name
                             CREATE (a)-[:MADE_BY]->(p)"""

create_genre_of_cypher = """MATCH (a:Film) WHERE a.title = $title
                            MATCH (g:Genre) WHERE g.type = $type 
                            CREATE (a)-[:OF_GENRE]->(g)"""

create_rate_of_cypher = """MATCH (a:Film) WHERE a.title = $title
                           MATCH (r:Rate) WHERE r.value = $value
                           CREATE (a)-[:WITH_RATE]->(r)"""


def create_film(tx, title): tx.run(create_film_cypher, title=title)


def create_person(tx, name, category_job): tx.run(create_person_cypher, name=name, category_job=category_job)


def create_genre(tx, type): tx.run(create_genre_cypher, type=type)

def create_rate(tx, value): tx.run(create_rate_cypher, value=value)


def create_person_of(tx, title, name): tx.run(create_person_of_cypher, title=title, name=name)


def create_genre_of(tx, title, type): tx.run(create_genre_of_cypher, title=title, type=type)


def create_rate_of(tx, title, value): tx.run(create_rate_of_cypher, title=title, value=value)


with driver.session() as session:
    session.execute_write(create_film, "Men in Black")
    session.execute_write(create_film, "Gemini Man")

    session.execute_write(create_person, "Will Smith", "ACTOR")
    session.execute_write(create_person, "Mary Elizabeth Winstead", "ACTOR")
    session.execute_write(create_person, "Tommy Lee Jones", "ACTOR")

    session.execute_write(create_person_of, "Men in Black", "Will Smith")
    session.execute_write(create_person_of, "Men in Black", "Tommy Lee Jones")

    session.execute_write(create_person_of, "Gemini Man", "Will Smith")
    session.execute_write(create_person_of, "Gemini Man", "Mary Elizabeth Winstead")

    session.execute_write(create_genre, "ACTION")

    session.execute_write(create_genre_of, "Men in Black", "ACTION")
    session.execute_write(create_genre_of, "Gemini Man", "ACTION")

    session.execute_write(create_rate, 4.7)
    session.execute_write(create_rate, 4.3)

    session.execute_write(create_rate_of, "Men in Black", 4.7)
    session.execute_write(create_rate_of, "Gemini Man", 4.3)

driver.close()
