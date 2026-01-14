import os
from dotenv import load_dotenv

from bson import ObjectId

from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

app = Flask(__name__)
# Driver Code from MongoDB Official Docs

uri = f"mongodb+srv://prasannamharikrishnan_db_user:{os.getenv("MONGO_DB_PASS")}@quiz-management.68dx1ks.mongodb.net/?appName=quiz-management"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["quiz_management"]

collection = db["quizzes"]

@app.route("/api/quiz", methods=["POST"])
def create_quiz():
    try:
        data = request.json
        document = {
            "title" : data["title"],
            "is_published" : False,
            "questions" : data["questions"]
        }
        response = collection.insert_one(document)

        print(response.acknowledged, response.inserted_id)

        return jsonify({"status": "Quiz Creation Successful"}), 200
    except Exception as e:
        return jsonify({"status": str(e)}), 500

@app.route("/api/quiz/publish/<q_id>", methods=["PATCH"])
def publish_quiz(q_id):
    try:
        response = collection.update_one(
            {
                "_id": ObjectId(q_id)
            },
            {
                "$set" : {
                    "is_published" : True
                }
            }
        )
        print(response.acknowledged, response.did_upsert)
        return jsonify({"status": "Quiz Published Successful"}), 200
    except Exception as e:
        return jsonify({"status": str(e)}), 500

@app.route("/api/quizzes")
def get_quizzes():
    try:
        response = collection.find({"is_published": True}, {"title":1})
        quizzes = [{"id":str(quiz["_id"]), "title":quiz["title"]} for quiz in response]
        return jsonify(quizzes), 200
    except Exception as e:
        return jsonify({"status": str(e)}), 500

@app.route("/api/quiz/<q_id>")
def get_quiz(q_id):
    try:
        quiz = collection.find_one({"_id": ObjectId(q_id)})
        quiz["_id"] = str(quiz["_id"])
        for q, answer in quiz["questions"].items():
            answer.pop("answers", None)
        return jsonify(quiz), 200
    except Exception as e:
        return jsonify({"status": str(e)}), 500

@app.route("/api/quiz/submit",methods=["POST"])
def submit_quiz():
    try:
        data = request.json
        quiz = collection.find_one({"_id": ObjectId(data["id"])})

        score = 0
        total_questions = len(quiz["questions"])

        for quiz_id, answer_id in data["answers"].items():
            user_selection = answer_id
            correct_answer = quiz["questions"][quiz_id]["answers"]
            if sorted(user_selection) == sorted(correct_answer):
                score += 1

        return jsonify({
            "score" : score,
            "total" : total_questions,
            "percentage" : (score / total_questions) * 100
        }), 200
    except Exception as e:
        return jsonify({"status": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True,port=5000)