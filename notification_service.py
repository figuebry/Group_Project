from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/send_notification", methods=["POST"])
def send_notification():

    data = request.get_json()

    notification_type = data.get("notification_type")
    recipient = data.get("recipient")
    message = data.get("message")

    if not notification_type:
        return jsonify({
            "status": "error",
            "message": "notification_type is required"
        }), 400

    if not recipient:
        return jsonify({
            "status": "error",
            "message": "recipient is required"
        }), 400

    if not message:
        return jsonify({
            "status": "error",
            "message": "message is required"
        }), 400

    notification = f"Notification for {recipient}: {message}"

    return jsonify({
        "status": "success",
        "notification_type": notification_type,
        "recipient": recipient,
        "notification": notification
    })

if __name__ == "__main__":
    app.run(port=5001, debug=True)