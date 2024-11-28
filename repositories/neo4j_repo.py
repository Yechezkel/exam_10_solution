import uuid

def record_interaction(driver, interaction_data):
    query = """
        MERGE (source:Device {device_id: $source_id, brand: $source_brand, model: $source_model, os: $source_os})
        MERGE (target:Device {device_id: $target_id, brand: $target_brand, model: $target_model, os: $target_os})
        CREATE (source)-[c:CONNECTED { 
            interaction_id: $interaction_id,
            method: $method,
            version: $version,
            signal_strength_dbm: $signal_strength_dbm,
            distance_meters: $distance_meters,
            duration_seconds: $duration_seconds,
            timestamp: $timestamp
        }]->(target)
        RETURN c.interaction_id as interaction_id
        """
    query_data = {
            'source_id': interaction_data["devices"][0]['id'],
            'source_brand': interaction_data["devices"][0]['brand'],
            'source_model': interaction_data["devices"][0]['model'],
            'source_os': interaction_data["devices"][0]['os'],

            'target_id': interaction_data["devices"][1]['id'],
            'target_brand': interaction_data["devices"][1]['brand'],
            'target_model': interaction_data["devices"][1]['model'],
            'target_os': interaction_data["devices"][1]['os'],

            'interaction_id': str(uuid.uuid4()),
            "method": interaction_data["interaction"]['method'],
            "version": interaction_data["interaction"]['bluetooth_version'],
            "signal_strength_dbm": interaction_data["interaction"]['signal_strength_dbm'],
            "distance_meters": interaction_data["interaction"]['distance_meters'],
            "duration_seconds": interaction_data["interaction"]['duration_seconds'],
            "timestamp": interaction_data["interaction"]['timestamp']
    }
    with driver.session() as session:
        result = session.run(query, query_data)
        return str(result.single()['interaction_id'])

def get_by_signal_strength(driver):
    query = """
            MATCH (source:Device)-[c:CONNECTED]->(target:Device)
            WHERE c.signal_strength_dbm >= -60
            RETURN source.device_id as source_id, target.device_id as target_id
            """
    with driver.session() as session:
        result = session.run(query)
        pairs_of_devices = [dict(pair) for pair in result]
        return pairs_of_devices

def count_connected_devices(driver, source_id):
    query = """
            MATCH (source_id:Device{device_id: $source_id})-[c:CONNECTED]-(neighbor:Device)
            RETURN COUNT(DISTINCT neighbor) as neighbors_count
            """
    with driver.session() as session:
        result = session.run(query, {'source_id':source_id})
        return str(result.single()['neighbors_count'])

def check_if_close(driver, source_id, target_id):
    query = """
            match (source : Device {device_id: $source_id})
            -[c:CONNECTED*5]-
            (target : Device {device_id: $target_id})
            return source limit 1
            """
    with driver.session() as session:
        result = session.run(query, {'source_id':source_id, "target_id": target_id })
        if result.single():
            return True
        return False

def get_interaction_sorted_by_time(driver, source_id):
    query = """
        call() {
            match (a:Device{device_id:$source_id})-[c:CONNECTED]->(b:Device)
            return a.device_id as source_id, b.device_id as target_id, c.timestamp as timestamp, c.interaction_id as interation_id
            union
            match (a:Device) -[c:CONNECTED]-> (b:Device{device_id: $source_id})
            return a.device_id as source_id, b.device_id as target_id, c.timestamp as timestamp, c.interaction_id as interation_id 
        }
        return source_id, target_id, timestamp, interation_id
        order by timestamp
    """
    with driver.session() as session:
        result = session.run(query, {"source_id": source_id})
        return [dict(interaction) for interaction in result]