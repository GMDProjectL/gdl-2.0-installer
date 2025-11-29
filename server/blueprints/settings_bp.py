from flask import Blueprint, request, jsonify
from storage.settings import Settings
from storage.result import Result
from storage.logs import Logs

settings_bp = Blueprint('settings', __name__)

@settings_bp.route("/apply_settings", methods=["POST"])
def apply_settings():
    if not request.is_json:
        Result.get_instance().error = True
        Result.get_instance().message = "Sorry, but you haven't provided the correct JSON."
        return jsonify(Result.get_instance().__dict__)

    try:
        settings = Settings.get_instance()
        for key, value in request.json.items():
            if not hasattr(settings, key):
                raise Exception(f'"{key}" doesn\'t exist in settings.')
            setattr(settings, key, value)
    except Exception as e:
        Result.get_instance().error = True
        Result.get_instance().message = str(e)
        return jsonify(Result.get_instance().__dict__)

    res = Result.get_instance().__dict__.copy()
    res['success'] = True
    return jsonify(res)
