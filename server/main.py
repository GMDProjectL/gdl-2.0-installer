import json
from traceback import format_exc
from flask import Flask, jsonify, request
from storage.settings import Settings
from storage.logs import Logs
from storage.result import Result
from storage.stage import Stage
from storage.progress import Progress
from copy import deepcopy

settings = Settings.get_instance()
logs = Logs.get_instance()
result = Result.get_instance()
stage = Stage.get_instance()
progress = Progress.get_instance()

app = Flask(__name__)

@app.route("/")
def main_page():
    return (
        "<title>GDL Installer Server Debug Page</title>" +
        "<h2>GDL installer server. <u>Do not touch anything</u> unless you know what you're doing.</h2>" +
        f"The following settings are set:<br /> <pre>{json.dumps(settings.__dict__, indent=4)}</pre> <br /><br />" +
        f"Logs queue:<br /> <pre>{json.dumps(logs.__dict__, indent=4)}</pre> <br /><br />" +
        f"Result buffer:<br /> <pre>{json.dumps(result.__dict__, indent=4)}</pre> <br /><br />" +
        f"Stage buffer:<br /> <pre>{json.dumps(stage.__dict__, indent=4)}</pre> <br /><br />" +
        f"Progress buffer:<br /> <pre>{json.dumps(progress.__dict__, indent=4)}</pre> <br /><br />"
    )

@app.route("/apply_settings", methods=["POST"])
def apply_settings():
    if not request.is_json:
        result.error = True
        result.message = "Sorry, but you haven't provided the correct JSON."
        return jsonify(result.__dict__)
    
    try:
        for key, value in request.json.items():
            if not hasattr(settings, key):
                raise Exception(f'"{key}" doesn\'t exist in settings.')
            settings.__setattr__(key, value)
    except:
        result.error = True
        result.message = format_exc()
        return jsonify(result.__dict__)
    
    res = deepcopy(result.__dict__)
    res['success'] = True
    
    return jsonify(res)

@app.route("/logs")
def get_logs():
    return jsonify(logs.new_lines)

@app.route("/result")
def get_result():
    return jsonify(result.__dict__)

@app.route("/stage")
def get_stage():
    return jsonify(stage.__dict__)

@app.route("/progress")
def get_progress():
    return jsonify(progress.__dict__)