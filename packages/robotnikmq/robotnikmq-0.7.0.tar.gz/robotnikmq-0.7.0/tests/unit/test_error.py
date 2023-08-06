from robotnikmq.error import InvalidConfiguration


def test_invalid_configuration():
    try:
        raise InvalidConfiguration()
    except InvalidConfiguration as exc:
        assert str(exc) == "InvalidConfiguration: Robotnik is improperly configured: ()"
