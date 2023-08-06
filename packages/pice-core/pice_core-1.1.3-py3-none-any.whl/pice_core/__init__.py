from .log_handler import LogHandler
from .global_variables_for_test_report import g_project
import os

log_handler.log_path = os.path.abspath('.') + r"\Project\{}\test_result\test_log\log.txt".format(g_project)

logger = LogHandler.get_log_handler(__name__, "info")

css_path = os.path.dirname(os.path.abspath(__file__)) + r"/config/report.css"


