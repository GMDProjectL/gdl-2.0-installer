import json
from flask import Flask
from storage.settings import Settings
from storage.logs import Logs
from storage.result import Result
from storage.stage import Stage
from storage.progress import Progress

from blueprints.settings_bp import settings_bp
from blueprints.installation_bp import installation_bp
from blueprints.monitoring_bp import monitoring_bp
from blueprints.test_bp import test_bp

try:
    import systemd.daemon
    systemd.daemon.notify('READY=1')
except:
    print('No systemd today.')

app = Flask(__name__)

app.register_blueprint(settings_bp)
app.register_blueprint(installation_bp)
app.register_blueprint(monitoring_bp)
app.register_blueprint(test_bp)

@app.route("/")
def main_page():
    settings = Settings.get_instance()
    logs = Logs.get_instance()
    result = Result.get_instance()
    stage = Stage.get_instance()
    progress = Progress.get_instance()

    return (
        "<title>GDL Installer Server Debug Page</title>" +
        "<h2>GDL installer server. <u>Do not touch anything</u> unless you know what you're doing.</h2>" +
        f"The following settings are set:<br /> <pre>{json.dumps(settings.__dict__, indent=4)}</pre> <br /><br />" +
        f"Logs queue:<br /> <pre>{json.dumps(logs.__dict__, indent=4)}</pre> <br /><br />" +
        f"Result buffer:<br /> <pre>{json.dumps(result.__dict__, indent=4)}</pre> <br /><br />" +
        f"Stage buffer:<br /> <pre>{json.dumps(stage.__dict__, indent=4)}</pre> <br /><br />" +
        f"Progress buffer:<br /> <pre>{json.dumps(progress.__dict__, indent=4)}</pre> <br /><br />"
    )
