from typing import Any

from yaml import safe_load
from pytest import mark, raises

from legion_cli.config import AppConfig

TESTDATA = [
    ('{"user_name": "Eugene", "hello_suffix": "?"}', "Eugene", "?", None),
    ('{"hello_suffix": "?"}', None, "?", TypeError),
    ('{"user_name": "Eugene"}', "Eugene", None, None),
]


@mark.parametrize("config,exp_name,exp_suffix,exc", TESTDATA)
def test_config_loading(config: Any, exp_name: Any, exp_suffix: Any,
                        exc: BaseException) -> None:
    if exc is not None:
        with raises(exc):
            config = AppConfig(**safe_load(config))
            assert config.user_name == exp_name
            assert config.hello_suffix == exp_suffix
    else:
        config = AppConfig(**safe_load(config))
        assert config.user_name == exp_name
        assert config.hello_suffix == exp_suffix
