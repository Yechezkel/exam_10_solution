# from datetime import datetime
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
            duration_seconds: $duration_seconds
        }]->(target)
        RETURN c.interaction_id as interaction_id
        """
    # timestamp: $timestamp
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
            # "timestamp": interaction_data["interaction"]['timestamp'], todo: to convert the time ino str
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






# def get_transaction(driver, transaction_id):
#     query = """
#         MATCH (s:Account)-[t:TRANSACTION {transaction_id: $transaction_id}]->(tar:Account)
#         RETURN s.account_id as source_id,
#             tar.account_id as target_id,
#             t.amount as amount,
#             t.timestamp as timestamp,
#             t.currency as currency
#         """
#     with driver.session() as session:
#         result = session.run(query, {'transaction_id': transaction_id})
#         transaction = result.single()
#         if transaction:
#             transaction = dict(transaction)
#             transaction['timestamp'] = str(transaction['timestamp'])
#             return transaction
#         return None
#
#
# def search_transactions(driver, query_data):
#     query = """
#         MATCH (s:Account)-[t:TRANSACTION]->(tar:Account)
#         WHERE t.timestamp >= datetime($start_date)
#         AND t.timestamp <= datetime($end_date)
#         AND t.amount >= $amount
#         RETURN s.account_id as source_id,
#             tar.account_id as target_id,
#             t.amount as amount,
#             t.timestamp as timestamp,
#             t.currency as currency
#         """
#     query_data['start_date'] = datetime.strptime(query_data['start_date'], '%d/%m/%Y, %H:%M:%S')
#     query_data['end_date'] = datetime.strptime(query_data['end_date'], '%d/%m/%Y, %H:%M:%S')
#     with driver.session() as session:
#         result = session.run(query, query_data)
#         transactions = [dict(transaction) for transaction in result]
#         for transaction in transactions:
#             transaction['timestamp'] = str(transaction['timestamp'])
#         return transactions
