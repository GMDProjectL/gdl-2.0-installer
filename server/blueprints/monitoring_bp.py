from flask import Blueprint, jsonify
from storage.logs import Logs
from storage.result import Result
from storage.stage import Stage
from storage.progress import Progress

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route("/logs")
def get_logs():
    logs = Logs.get_instance()
    old_logs = logs.new_lines.copy()
    logs.new_lines.clear()
    return jsonify(old_logs)

@monitoring_bp.route("/result")
def get_result():
    return jsonify(Result.get_instance().__dict__)

@monitoring_bp.route("/stage")
def get_stage():
    return jsonify(Stage.get_instance().__dict__)

@monitoring_bp.route("/progress")
def get_progress():
    return jsonify(Progress.get_instance().__dict__)
