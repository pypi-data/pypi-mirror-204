from arrow import get as to_arrow
from pytest import raises

from robotnikmq.core import Message


def test_message_init():
    msg = Message(contents={'stuff': 'something'})
    assert msg.contents['stuff'] == 'something'


def test_message_read_route():
    msg = Message(contents={'stuff': 'something'}, routing_key='test.route')
    assert msg.route == 'test.route'


def test_message_getitem():
    msg = Message(contents={'stuff': 'something'}, routing_key='test.route')
    assert msg['stuff'] == 'something'


def test_message_contains():
    msg = Message(contents={'stuff': 'something'}, routing_key='test.route')
    assert 'stuff' in msg


def test_message_keys():
    msg = Message(contents={'stuff': 'something'}, routing_key='test.route')
    assert set(msg.keys()) == {'stuff'}


def test_message_values():
    msg = Message(contents={'stuff': 'something'}, routing_key='test.route')
    assert set(msg.values()) == {'something'}


def test_message_iter():
    msg = Message(contents={'stuff': 'something'}, routing_key='test.route')
    assert list(i for i in msg) == [('stuff')]


def test_message_to_dict():
    msg = Message(contents={'stuff': 'something'})
    assert msg.to_dict()['timestamp'] == msg.timestamp.int_timestamp


def test_message_to_json():
    msg = Message(contents={'stuff': 'something'})
    print(msg.to_json())
    assert msg.to_json().startswith('{"routing_key": "", "contents": {"stuff": "something"}, "msg_')


def test_message_from_json():
    msg = Message.of('{"routing_key": "", "contents": {"stuff": "something"}, "msg_id": "11bcdb39-'
                     '56a1-4244-a567-0a5e8eaa125f", "timestamp": 1614471764}')
    assert msg.timestamp == to_arrow(1614471764)


def test_not_jsonable():
    with raises(ValueError):
        Message(contents={'set': {1, 2, 3, 4}})
