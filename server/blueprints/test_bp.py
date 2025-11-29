from flask import Blueprint, jsonify, request
from storage.result import Result
from storage.stage import Stage
from storage.progress import Progress
from storage.logs import Logs

test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route("/give_error", methods=["POST"])
def give_error():
    if not request.is_json:
        result = Result.get_instance()
        result.error = True
        result.message = "Sorry, but you haven't provided the correct JSON."
        return jsonify(result.__dict__)

    result = Result.get_instance()
    result.error = True
    result.message = request.json['message']

    return jsonify(result.__dict__)

@test_bp.route("/give_success", methods=["POST"])
def give_success():
    if not request.is_json:
        result = Result.get_instance()
        result.error = True
        result.message = "Sorry, but you haven't provided the correct JSON."
        return jsonify(result.__dict__)

    result = Result.get_instance()
    result.success = True

    return jsonify(result.__dict__)

@test_bp.route("/set_stage", methods=["POST"])
def set_stage():
    if not request.is_json:
        result = Result.get_instance()
        result.error = True
        result.message = "Sorry, but you haven't provided the correct JSON."
        return jsonify(result.__dict__)

    stage = Stage.get_instance()
    stage.stage = request.json['stage']

    return jsonify(Result.get_instance().__dict__)

@test_bp.route("/set_progress", methods=["POST"])
def set_progress():
    if not request.is_json:
        result = Result.get_instance()
        result.error = True
        result.message = "Sorry, but you haven't provided the correct JSON."
        return jsonify(result.__dict__)

    progress = Progress.get_instance()
    progress.progress = request.json['progress']

    return jsonify(Result.get_instance().__dict__)

@test_bp.route("/send_logs", methods=["POST"])
def send_logs():
    if not request.is_json:
        result = Result.get_instance()
        result.error = True
        result.message = "Sorry, but you haven't provided the correct JSON."
        return jsonify(result.__dict__)

    logs = Logs.get_instance()
    logs.new_lines.append(request.json['logs'])

    return jsonify(Result.get_instance().__dict__)
