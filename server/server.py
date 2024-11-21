from flask import Flask, request, jsonify

app = Flask(__name__)

from yt_dlp import download

@app.route('/process', methods=['POST'])
def process_message():
    """
    Endpoint to process incoming JSON messages.
    """
    try:
        # Parse the incoming JSON payload
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Invalid or missing JSON payload"}), 400

        result = download(data['url'])

        # Process the received message (example: echo the message back)
        response_data = {
            "status": "success",
            "received": data,
            "path": result["path"]
        }

        # Return the JSON response
        return jsonify(response_data)

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Run the server on localhost and port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
