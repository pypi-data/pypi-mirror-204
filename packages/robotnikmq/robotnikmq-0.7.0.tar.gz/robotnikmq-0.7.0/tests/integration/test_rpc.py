# pylint: disable=redefined-outer-name
from collections import defaultdict
from multiprocessing import current_process
from typing import Dict, NoReturn, Union, Optional, Any

from pika.exceptions import AMQPError  # type: ignore
from typeguard import typechecked

from robotnikmq.log import log
from robotnikmq.rpc_client import RpcClient
from robotnikmq.rpc_server import RpcServer

from tests.integration.utils import sub_process

try:
    from pytest_cov.embed import cleanup_on_sigterm  # type: ignore
except ImportError:
    pass
else:
    cleanup_on_sigterm()


def test_basic_rpc_call(robotnikmq_config):
    @typechecked
    def fib(index: int) -> int:
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci", {"index": 10})
        assert result == 55


def test_basic_rpc_call_only_once(robotnikmq_config):
    @typechecked
    def fib(index: int) -> int:
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config, only_once=True)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server, terminate=False):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci", {"index": 10})
        assert result == 55


def test_basic_rpc_call_without_typehints(robotnikmq_config):
    def fib(index: int) -> int:
        """Returns the Nth fibonacci number"""
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci", {"index": 10})
        assert result == 55


def test_basic_rpc_call_with_any(robotnikmq_config):
    def fib(index: Any) -> int:
        """Returns the Nth fibonacci number"""
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci", {"index": 10})
        assert result == 55


def test_basic_rpc_call_docs(robotnikmq_config):
    @typechecked
    def fib(index: int, other: Union[int, float] = 0) -> int:
        """Returns the Nth fibonacci number"""
        if index == other:
            return int(other)
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci.__doc__")
        log.debug(result)
        assert result["description"] == fib.__doc__
        assert result["inputs"] == {"index": "int", "other": "Union[int,float]"}
        assert result["rpc_queue"] == "fibonacci"


def test_basic_rpc_call_without_docs(robotnikmq_config):
    @typechecked
    def fib(index: int) -> int:
        """Returns the Nth fibonacci number"""
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib, register_docs=False)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        try:
            client.call("fibonacci.__doc__", timeout=0.5)
            assert False
        except TimeoutError as exc:
            assert str(exc).startswith("No response has been received for Request")


def test_multiserve_rpc_call(robotnikmq_config):
    @typechecked
    def _call1() -> str:
        return "call1"

    @typechecked
    def _call2() -> str:
        return "call2"

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("call1", _call1)
        serv.register_rpc("call2", _call2)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("call1")
        assert result == "call1"
        result = client.call("call2")
        assert result == "call2"


def test_faulty_rpc_call(robotnikmq_config):
    @typechecked
    def _faulty() -> NoReturn:
        raise RuntimeError("Shit happens!")

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("test", _faulty)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("test")
        assert result.details.startswith(
            "There was an error "
            "while processing the "
            "request, please refer "
            "to server log with "
            "request ID"
        )


def test_raise_error(robotnikmq_config):
    @typechecked
    def _faulty() -> NoReturn:
        raise RuntimeError("Shit happens!")

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("test", _faulty)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        try:
            client.call("test", raise_on_error=True)
            assert False
        except RuntimeError as exc:
            assert str(exc).startswith(
                "There was an error while processing the request"
            )


def test_type_safety(robotnikmq_config):
    @typechecked
    def fib(index: int) -> int:
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        try:
            client.call("fibonacci", {"index": 10.1}, raise_on_error=True)
            assert False
        except RuntimeError as exc:
            log.debug(str(exc))
            assert str(exc).startswith("Invalid type for index")


def test_arg_safety(robotnikmq_config):
    @typechecked
    def fib(index: int) -> int:
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        try:
            client.call("fibonacci", {"indexes": 10.1}, raise_on_error=True)
            assert False
        except RuntimeError as exc:
            log.debug(str(exc))
            assert str(exc).startswith("Missing required argument index")


def test_union_type_safety(robotnikmq_config):
    @typechecked
    def fib(index: Union[int, float]) -> int:
        index = int(index)
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        try:
            client.call("fibonacci", {"index": "10.1"}, raise_on_error=True)
            assert False
        except RuntimeError as exc:
            log.debug(str(exc))
            assert str(exc).startswith("Invalid type for index")


def test_union_rpc_call(robotnikmq_config):
    @typechecked
    def fib(index: Union[int, float]) -> int:
        index = int(index)
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci", {"index": 10})
        assert result == 55


def test_default_rpc_call(robotnikmq_config):
    @typechecked
    def fib10(index: Union[int, float] = 10) -> int:
        index = int(index)
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib10(index - 1) + fib10(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib10)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci", {})
        assert result == 55
        result = client.call("fibonacci", {"index": 10})
        assert result == 55
        result = client.call("fibonacci")
        assert result == 55


def test_optional_rpc_call(robotnikmq_config):
    @typechecked
    def fib(index: Optional[int] = None) -> int:
        index = index if index is not None else 10
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci", {})
        assert result == 55
        result = client.call("fibonacci", {"index": 10})
        assert result == 55
        result = client.call("fibonacci")
        assert result == 55


def test_faulty_input_rpc_call(robotnikmq_config):
    @typechecked
    def fib(index: int) -> int:
        if index == 0:
            return 0
        if index == 1:
            return 1
        return fib(index - 1) + fib(index - 2)

    @typechecked
    def _fib(args: Dict[str, int]) -> Dict[str, int]:
        return {"result": fib(args["index"])}

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", _fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        result = client.call("fibonacci", str_args="invalid_json")
        assert result.details == ("Input could not be decoded as JSON")


def test_rpc_with_amqp_error(robotnikmq_config):
    @typechecked
    def fib(index: int) -> int:
        raise AMQPError("Shit happens with AMQP!")

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        try:
            result = client.call("fibonacci", {"index": 20}, timeout=0.5)
            log.debug(result)
            assert False
        except TimeoutError as exc:
            assert str(exc).startswith("No response has been received for Request")


def test_rpc_with_keyboard_interrupt(robotnikmq_config):
    @typechecked
    def fib(index: int) -> int:
        raise KeyboardInterrupt()

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("fibonacci", fib)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        try:
            result = client.call("fibonacci", {"index": 20}, timeout=0.5)
            log.debug(result)
            assert False
        except TimeoutError as exc:
            assert str(exc).startswith("No response has been received for Request")


def test_rpc_call_to_multiple_servers(robotnikmq_config):
    @typechecked
    def _process_name() -> Dict[str, str]:
        return {"process-name": current_process().name}

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("process_name", _process_name)
        serv.run()

    with sub_process(server, name="Server 1"):
        with sub_process(server, name="Server 2"):
            with sub_process(server, name="Server 3"):
                with sub_process(server, name="Server 4"):
                    with sub_process(server, name="Server 5"):
                        client = RpcClient(robotnikmq_config)
                        results = defaultdict(int)
                        for _ in range(100):
                            results[
                                client.call("process_name", timeout=0.5)["process-name"]
                            ] += 1
                        log.debug(results)
                        assert len(results) == 5


def test_dict_input(robotnikmq_config):
    @typechecked
    def _dictify(my_dict: Dict[str, str]) -> str:
        return f'{"".join([k + v for k, v in my_dict.items()])}'

    def server():
        serv = RpcServer(robotnikmq_config)
        serv.register_rpc("dictify", _dictify)
        serv.run()

    with sub_process(server):
        client = RpcClient(robotnikmq_config)
        assert (
            client.call("dictify", {"my_dict": {"stuff": "moar"}}, timeout=0.5)
            == "stuffmoar"
        )
