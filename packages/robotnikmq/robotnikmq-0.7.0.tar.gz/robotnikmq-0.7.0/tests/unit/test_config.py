from os import chdir
from os.path import realpath
from pathlib import Path
from tempfile import TemporaryDirectory

from pytest import raises, mark, param

from robotnikmq.config import config_of, server_config, _existing_file_or_none
from robotnikmq.core import Robotnik
from robotnikmq.error import NotConfigured


HERE = Path(realpath(__file__)).parent
ROBOTNIK_CONFIG_CONTENTS = """
tiers:
- - host: 127.0.0.1
    password: hackme
    port: 1
    user: legion
    vhost: /legion
  - host: 1
    password: hackme
    port: 5671
    user: legion
    vhost: /legion
- - host: 127.0.0.1
    password: hackme
    port: 5671
    user: legion
    vhost: /legion
"""
BAD_CONFIG_CONTENTS1 = """
tiers:
- - ca_cert: /does/not/exist.cert
    cert: /definitely/does/not/exist.cert
    host: 127.0.0.1
    key: /yup/still/doesnt/exist.key
    password: hackme
    port: 1
    user: legion
    vhost: /legion
"""


def test_configuration_loading():
    with TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        config_file = tmp_dir / "robotnikmq.yaml"
        config_file.open("w+").write(ROBOTNIK_CONFIG_CONTENTS)
        print(config_file.open().read())
        config = config_of(config_file)
        assert len(config.tiers) == 2


def test_a_server():
    with TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        config_file = tmp_dir / "robotnikmq.yaml"
        config_file.open("w+").write(ROBOTNIK_CONFIG_CONTENTS)
        print(config_file.open().read())
        config = config_of(config_file)
        assert config.a_server(1).port == 5671


def test_loading_config_file_in_same_dir():
    with TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        prev_dir = Path.cwd()
        try:
            chdir(tmp_dir)
            config_file = tmp_dir / "robotnikmq.yaml"
            config_file.open("w+").write(ROBOTNIK_CONFIG_CONTENTS)
            robotnik = Robotnik()
            assert robotnik.config.a_server(1).port == 5671
        finally:
            chdir(prev_dir)


def test_loading_no_config():
    with TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        prev_dir = Path.cwd()
        with raises(NotConfigured):
            try:
                chdir(tmp_dir)
                robotnik = Robotnik(config_paths=[Path.cwd() / "robotnikmq.yaml"])
                assert False
            finally:
                chdir(prev_dir)


def test_as_dict():
    with TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        config_file = tmp_dir / "robotnikmq.yaml"
        config_file.open("w+").write(ROBOTNIK_CONFIG_CONTENTS)
        print(config_file.open().read())
        config = config_of(config_file)
        assert config.as_dict()["tiers"][1][0]["port"] == 5671


def test_no_config_file():
    with TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        config_file = tmp_dir / "robotnikmq.yaml"
        with raises(NotConfigured):
            config_of(config_file)


def test_no_ca_cert_file():
    with TemporaryDirectory() as tmp_name:
        tmp_dir = Path(tmp_name)
        config_file = tmp_dir / "robotnikmq.yaml"
        config_file.open("w+").write(BAD_CONFIG_CONTENTS1)
        with raises(FileNotFoundError):
            config_of(config_file)


def test_server_config():
    config = server_config(
        host="127.0.0.1",
        port=1,
        user="legion",
        password="hackme",
        vhost="/legion",
    )
    assert config.port == 1


def test_conn_params_of_server_config():
    config = server_config(
        host="127.0.0.1",
        port=1,
        user="legion",
        password="hackme",
        vhost="/legion",
    )
    assert config.conn_params().port == 1


@mark.parametrize(
    ("input", "expected_output"),
    [
        (Path.cwd(), Path.cwd()),
        (str(Path.cwd()), Path.cwd()),
        (None, None),
        param("/does/not/exist", None, marks=mark.xfail(raises=FileNotFoundError)),
    ],
)
def test_existing_file_or_none(input, expected_output):
    assert _existing_file_or_none(input) == expected_output
