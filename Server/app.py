from flask import Flask, request, jsonify, abort, render_template
import uuid

app = Flask(__name__)
sessions = {}


@app.route("/session/<session_id>")
def session_view(session_id):
    data = sessions.get(session_id)
    if data is None:
        abort(404)
    return jsonify(data)


@app.route("/session/<session_id>/update", methods=["POST"])
def update_session_map(session_id):
    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Invalid JSON"}), 415

    sessions[session_id] = json_data
    return jsonify({"status": "ok"})


@app.route("/session/<session_id>/view")
def session_page(session_id):
    if session_id not in sessions:
        abort(404)
    return render_template("map.html", session_id=session_id)


if __name__ == '__main__':
    app.run(debug=True)
