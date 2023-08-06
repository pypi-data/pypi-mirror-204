from contextlib import contextmanager

from pytest import mark

from robotnikmq.rpc_server import RpcError, RpcResponse


@contextmanager
def does_not_raise():
    yield


@mark.parametrize('json_input,exp_details,expectation', [
    ('{"request_id": "71b14a62-2a58-4af1-a31d-f8a6020d416f","type":"error","details":"shit happens"}', "shit happens", does_not_raise()),
    ('{"request_id": "71b14a62-2a58-4af1-a31d-f8a6020d416f","details":"shit happens"}', None, does_not_raise()),
    ('not valid json', None, does_not_raise())
])
def test_rpc_error_from_json(json_input, exp_details, expectation):
    with expectation:
        res = RpcError.from_json(json_input)
        assert (exp_details is None and res is None) or res.details == exp_details


@mark.parametrize('json_input,exp_data,expectation', [
    ('{"request_id": "71b14a62-2a58-4af1-a31d-f8a6020d416f","type":"response","data":"shit"}', "shit", does_not_raise()),
    ('{"request_id": "71b14a62-2a58-4af1-a31d-f8a6020d416f","data":"shit"}', None, does_not_raise()),
    ('not valid json', None, does_not_raise())
])
def test_rpc_response_from_json(json_input, exp_data, expectation):
    with expectation:
        res = RpcResponse.from_json(json_input)
        assert (exp_data is None and res is None) or res.data == exp_data
