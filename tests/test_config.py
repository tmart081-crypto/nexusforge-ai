from config.modules import MODULES
from config.models import all_model_keys, get_model_config


def test_all_modules_have_required_fields():
    required = {"key", "title", "icon", "page", "section", "milestone"}
    for module in MODULES:
        assert required.issubset(module.keys())


def test_fifteen_modules_declared():
    assert len(MODULES) == 15


def test_exactly_one_default_page():
    defaults = [m for m in MODULES if m.get("default")]
    assert len(defaults) == 1


def test_model_registry_lookup():
    for key in all_model_keys():
        cfg = get_model_config(key)
        assert "task" in cfg and "model" in cfg
