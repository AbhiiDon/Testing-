from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Facebook Graph API base URL
GRAPH_API_URL = "https://graph.facebook.com/v16.0"

@app.route('/lock', methods=['POST'])
def lock_group_name():
    data = request.json
    group_id = data.get('groupId')
    access_token = data.get('accessToken')
    locked_name = data.get('lockedName')

    if not group_id or not access_token or not locked_name:
        return jsonify({"message": "Missing required fields"}), 400

    # Function to get the current group name
    def get_group_name(group_id, access_token):
        url = f"{GRAPH_API_URL}/{group_id}"
        params = {"fields": "name", "access_token": access_token}
        response = requests.get(url, params=params)
        return response.json().get("name")

    # Function to set the group name
    def set_group_name(group_id, access_token, name):
        url = f"{GRAPH_API_URL}/{group_id}"
        data = {"name": name, "access_token": access_token}
        response = requests.post(url, data=data)
        return response.json()

    # Check and lock the group name
    try:
        current_name = get_group_name(group_id, access_token)
        if current_name != locked_name:
            set_group_name(group_id, access_token, locked_name)
            return jsonify({"message": "Group name locked successfully!"}), 200
        else:
            return jsonify({"message": "Group name is already locked."}), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
