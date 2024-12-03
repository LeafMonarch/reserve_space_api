from flask import Flask, jsonify, request

app = Flask(__name__)

data = {
    "01/12/2024": [
        {"P1105": "Booked"}, {"P1106": "Available"}, {"P1107": "Booked"}, {"P1108": "Available"}
    ],
    "02/12/2024": [
        {"P1105": "Available"}, {"P1106": "Available"}, {"P1107": "Available"}, {"P1108": "Booked"}
    ],
    "03/12/2024": [
        {"P1105": "Available"}, {"P1106": "Booked"}, {"P1107": "Available"}, {"P1108": "Available"}
    ]
}

@app.route('/room_availability', methods=['GET'])
def get_room_availability():
    date = request.args.get('date')
    
    if date in data:
        return jsonify({date: data[date]})
    else:
        return jsonify({"error": "Date not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
