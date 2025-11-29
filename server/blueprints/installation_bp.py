from flask import Blueprint, request, jsonify
from storage.settings import Settings
from storage.result import Result
from copy import deepcopy
from installation.install_thread import InstallThread

installation_bp = Blueprint('installation', __name__)

@installation_bp.route("/run_installation", methods=["POST"])
def run_installation():
    settings = Settings.get_instance()
    install_thread = InstallThread(settings)
    install_thread.start()

    res = Result.get_instance().__dict__.copy()
    res['success'] = True

    return jsonify(res)
