import json
from flask import Flask, jsonify
from storage.settings import Settings
from storage.logs import Logs
from storage.result import Result
from storage.stage import Stage
from storage.progress import Progress

settings = Settings.get_instance()
logs = Logs.get_instance()
result = Result.get_instance()
stage = Stage.get_instance()
progress = Progress.get_instance()

app = Flask(__name__)

@app.route("/")
def main_page():
    return (
        "<h2>GDL installer server. <u>Do not touch anything</u> unless you know what you're doing.</h2>" +
        f"The following settings are set:<br /> <pre>{json.dumps(settings.__dict__, indent=4)}</pre> <br /><br />" +
        f"Logs queue:<br /> <pre>{json.dumps(logs.__dict__, indent=4)}</pre> <br /><br />" +
        f"Result buffer:<br /> <pre>{json.dumps(result.__dict__, indent=4)}</pre> <br /><br />" +
        f"Stage buffer:<br /> <pre>{json.dumps(stage.__dict__, indent=4)}</pre> <br /><br />" +
        f"Progress buffer:<br /> <pre>{json.dumps(progress.__dict__, indent=4)}</pre> <br /><br />"
    )

@app.route("/get_logs")
def get_logs():
    return jsonify(logs.new_lines)

@app.route("/get_result")
def get_result():
    return jsonify(result.__dict__)

@app.route("/get_stage")
def get_stage():
    return jsonify(stage.__dict__)

@app.route("/get_progress")
def get_progress():
    return jsonify(progress.__dict__)