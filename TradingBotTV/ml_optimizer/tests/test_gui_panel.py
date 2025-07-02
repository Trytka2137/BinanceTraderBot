import importlib
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def test_gui_module_has_create_app():
    mod = importlib.import_module("TradingBotTV.gui_panel")
    assert hasattr(mod, "create_app")
