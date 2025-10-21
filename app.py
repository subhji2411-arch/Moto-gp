from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to access

# In-memory store (for demo). 
# On Render restart, reset hoga. Production me DB use karo.
scores = {}

@app.route("/")
def home():
    return "Moto Racer Leaderboard API"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    name = data.get("name")
    score = int(data.get("score",0))
    if not name: return jsonify({"error":"No name"}),400
    # Update score if higher
    if name not in scores or score > scores[name]:
        scores[name] = score
    return jsonify({"success":True,"best":scores[name]})

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    top = sorted(scores.items(), key=lambda x:x[1], reverse=True)
    return jsonify({"leaderboard":top[:10]})  # top 10

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)