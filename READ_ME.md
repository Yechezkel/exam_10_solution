# Phone Tracker API

This project is a Flask-based API that provides several endpoints for managing and querying phone interaction data. Below is a list of available endpoints and their details.


---

## Endpoints

### 1. **Record Interaction**  
**URL:** `/phone_tracker`  
**Method:** `POST`  
**Description:** Records an interaction between two devices.
**Usage:** [Post Interaction](http://localhost:5000/phone_tracker)

---

### 2. **Get Devices with Signal Strength Stronger Than -60**  
**URL:** `/phone_tracker/signal_strength_stronger_than_-60`  
**Method:** `GET`  
**Description:** Retrieves devices that have signal strength stronger than -60.  
**Usage:** [Get Signal Strength](http://localhost:5000/phone_tracker/signal_strength_stronger_than_-60)

---

### 3. **Count Connected Devices**  
**URL:** `/phone_tracker/count_connected_devices`  
**Method:** `GET`  
**Description:** Counts the number of devices connected to a specific source device.  
**Usage:** [Count Connected Devices](http://localhost:5000/phone_tracker/count_connected_devices)

---

### 4. **Check If Two Devices Are Close**  
**URL:** `/phone_tracker/check_if_close`  
**Method:** `GET`  
**Description:** Checks if two devices are close to each other.  
**Usage:** [Check If Close](http://localhost:5000/phone_tracker/check_if_close)

---

### 5. **Get Interactions Sorted by Time**  
**URL:** `/phone_tracker/get_interaction_sorted_by_time`  
**Method:** `GET`  
**Description:** Retrieves interactions involving a specific device, sorted by time.  
**Usage:** [Get Interactions by Time](http://localhost:5000/phone_tracker/get_interaction_sorted_by_time)

---

## Notes
- Ensure the server is running locally before accessing the endpoints.
- For `POST` and `GET` requests that require a request body, provide the necessary data in the request payload. This includes `source_id`, `target_id`, or other required fields.
- Handle proper error responses as indicated by the API.

---

## Setup
1. Clone the repository.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt


