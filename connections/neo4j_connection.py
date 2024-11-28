from neo4j import GraphDatabase


# todo: to figure this function to the correct url
def get_connection_to_neo4j():
    try:
        driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))
        with driver.session() as session:
            result = session.run("RETURN 'Connected to Neo4j' AS message")
            if result.single()["message"]:
                print("Connected to neo4j by bolt://neo4j:7687 ")
                return driver
    except Exception as e1:
        try:
            driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
            with driver.session() as session:
                result = session.run("RETURN 'Connected to Neo4j' AS message")
                if result.single()["message"]:
                    print("Connected to neo4j by bolt://localhost:7687 ")
                    return driver
        except Exception as e2:
            raise Exception( f"Failed to connect to neo4j.  bolt://neo4j:7687  exception: {e1} ,  bolt://localhost:7687 exception: {e2}")

neo4j_driver = get_connection_to_neo4j()