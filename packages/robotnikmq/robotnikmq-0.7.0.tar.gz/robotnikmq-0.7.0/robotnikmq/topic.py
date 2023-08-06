import json
from typing import Optional

from pika.exceptions import AMQPError
from pika.exchange_type import ExchangeType
from tenacity import retry, retry_if_exception_type, wait_exponential
from typeguard import typechecked

from robotnikmq.config import RobotnikConfig
from robotnikmq.core import Robotnik, Message


class Topic(Robotnik):
    """The Topic is one of two key elements of the Publish/Subscribe workflow with RobotnikMQ.
       Once configured, a topic is able to broadcast messages to any Subscribers on a given exchange
       and routing key combination.
    """
    @typechecked
    def __init__(
        self,
        exchange: str,
        config: Optional[RobotnikConfig] = None,
    ):
        super().__init__(config=config)
        self.exchange = exchange
        self.channel.exchange_declare(
            exchange=self.exchange, exchange_type=ExchangeType.topic, auto_delete=True
        )

    @retry(
        retry=retry_if_exception_type((AMQPError, OSError)),
        wait=wait_exponential(multiplier=1, min=3, max=30),
    )
    @typechecked
    def broadcast(
        self,
        msg: Message,
        routing_key: Optional[str] = None
    ) -> None:
        """Broadcasts a message with an optional routing key.

        Args:
            msg (Message): The message to be broadcast.
            routing_key (Optional[str], optional): Routing key used to broadcast the message.
                                                   Defaults to an empty string.
            on_msg_error (AMQPErrorCallback, optional): _description_. Defaults to None.
        """
        msg.routing_key = routing_key or msg.routing_key or ""
        self.log.info("Broadcasting message (routing-key: [{}]):\n{}",
                      msg.routing_key, json.dumps(msg.to_dict(), indent=4))
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=msg.routing_key,
            body=json.dumps(msg.to_dict()),
        )
        self.log.success("Broadcast:\n{}", json.dumps(msg.to_dict(), indent=4))
