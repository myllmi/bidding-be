from flask import Flask, json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from view.bidding_view import bidding_bp
from view.candidate_view import candidate_bp
from view.profile_view import profile_bp
from view.project_view import project_bp
from view.resume_view import resume_bp

app = Flask(__name__)
app.register_blueprint(resume_bp, url_prefix='/resume')
app.register_blueprint(bidding_bp, url_prefix='/bidding')
app.register_blueprint(project_bp, url_prefix='/project')
app.register_blueprint(profile_bp, url_prefix='/profile')
app.register_blueprint(candidate_bp, url_prefix='/candidate')
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, Bidding!</p>"


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response
