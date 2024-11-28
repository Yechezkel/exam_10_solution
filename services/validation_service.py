
def validate_interaction_data(interaction_data):
    required_keys_in_device = ['id', 'brand', 'model', 'os']
    required_keys_in_interaction = ['method','bluetooth_version','signal_strength_dbm','distance_meters','duration_seconds','timestamp']
    for key in required_keys_in_device:
        if key not in interaction_data["devices"][0] or key not in interaction_data["devices"][1]:
            return False
    for key in required_keys_in_interaction:
        if key not in interaction_data["interaction"]:
            return False
    return True
