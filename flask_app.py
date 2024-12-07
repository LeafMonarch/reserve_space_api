from flask import Flask, jsonify, request

app = Flask(__name__)

# Data structure to hold room availability and bookings
data = {
    "2024-12-01": [
        {"room_id": "P1105", "status": "Booked", "student_id": "12345", "image_url": "https://www.dkit.ie/assets/uploads/images/Library_585x300_v3.jpg"},
        {"room_id": "P1106", "status": "Available", "student_id": None, "image_url": "https://www.dkit.ie/assets/uploads/images/Library_585x300_v3.jpg"},
        {"room_id": "P1107", "status": "Booked", "student_id": "67890", "image_url": "https://www.dkit.ie/assets/uploads/images/Library_585x300_v3.jpg"},
        {"room_id": "P1108", "status": "Available", "student_id": None, "image_url": "https://www.dkit.ie/assets/uploads/images/Library_585x300_v3.jpg"},
    ],
    "2024-12-02": [
        {"room_id": "P1105", "status": "Available", "student_id": None, "image_url": "https://www.dkit.ie/assets/uploads/images/Library_585x300_v3.jpg"},
        {"room_id": "P1106", "status": "Available", "student_id": None, "image_url": "https://www.dkit.ie/assets/uploads/images/Library_585x300_v3.jpg"},
        {"room_id": "P1107", "status": "Available", "student_id": None, "image_url": "https://www.dkit.ie/assets/uploads/images/Library_585x300_v3.jpg"},
        {"room_id": "P1108", "status": "Booked", "student_id": "11111", "image_url": "https://www.dkit.ie/assets/uploads/images/Library_585x300_v3.jpg"},
    ],
}

# Route to get room availability for a specific date
@app.route('/room_availability', methods=['GET'])
def get_room_availability():
    date = request.args.get('date')
    print(f"Received date: {date}")  # Add this for debugging
    if date in data:
        return jsonify({"date": date, "rooms": data[date]})
    else:
        return jsonify({"error": "Date not found"}), 404

# Route to book a room
@app.route('/book_room', methods=['POST'])
def book_room():
    request_data = request.get_json()
    date = request_data.get('date')
    room_id = request_data.get('room_id')
    student_id = request_data.get('student_id')

    if not all([date, room_id, student_id]):
        return jsonify({"error": "Missing required fields"}), 400

    if date not in data:
        return jsonify({"error": "Date not found"}), 404

    for room in data[date]:
        if room["room_id"] == room_id:
            if room["status"] == "Booked":
                return jsonify({"error": "Room already booked"}), 400
            room["status"] = "Booked"
            room["student_id"] = student_id
            return jsonify({"success": True, "message": "Room booked successfully"})

    return jsonify({"error": "Room not found"}), 404

# Route to fetch bookings for a specific student
@app.route('/my_bookings', methods=['GET'])
def get_student_bookings():
    student_id = request.args.get('student_id')

    if not student_id:
        return jsonify({"error": "Student ID is required"}), 400

    bookings = []
    for date, rooms in data.items():
        for room in rooms:
            if room["student_id"] == student_id:
                bookings.append({
                    "date": date, 
                    "room_id": room["room_id"], 
                    "status": room["status"],
                    "image_url": room.get("image_url", "https://via.placeholder.com/150")})

    return jsonify({"student_id": student_id, "bookings": bookings})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
