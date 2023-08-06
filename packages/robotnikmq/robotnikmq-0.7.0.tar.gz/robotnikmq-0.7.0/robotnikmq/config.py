"""
Functions and objects related to the Configuration of RobotnikMQ
"""
from pathlib import Path
from random import choice
from ssl import create_default_context
from typing import Union, List, Optional, Dict, Any

from pika import ConnectionParameters, SSLOptions  # type: ignore
from pika.credentials import PlainCredentials  # type: ignore
from pydantic import BaseModel  # type: ignore
from pydantic import validator
from typeguard import typechecked
from yaml import safe_load  # type: ignore

from robotnikmq.error import (
    NotConfigured,
    InvalidConfiguration,
)
from robotnikmq.log import log


@typechecked
def _existing_file_or_none(path: Union[str, Path, None]) -> Optional[Path]:
    """
    Validates that a given path exists (either a string or Path object) and returns it or throws an exception.

    Parameters:
        path (Union[str, Path]): Description

    Raises:
        FileDoesNotExist: Description

    Returns:
        Path: Validated path that exists as of when the function was run
    """
    return Path(path).resolve(strict=True) if path is not None else None


class ServerConfig(BaseModel):
    """
    Configuration object representing the configuration information required to connect to a single server
    """

    host: str
    port: int
    user: str
    password: str
    vhost: str
    ca_cert: Optional[Path] = None
    cert: Optional[Path] = None
    key: Optional[Path] = None
    _conn_params: Optional[ConnectionParameters] = None

    _existing_ca_cert = validator("ca_cert", pre=True, always=True, allow_reuse=True)(
        _existing_file_or_none
    )
    _existing_cert = validator("cert", pre=True, always=True, allow_reuse=True)(
        _existing_file_or_none
    )
    _existing_key = validator("key", pre=True, always=True, allow_reuse=True)(
        _existing_file_or_none
    )

    class Config:
        json_encoders = {
            Path: str,
        }

    @typechecked
    def conn_params(self) -> ConnectionParameters:
        if self._conn_params is not None:
            return self._conn_params
        if self.ca_cert is not None and self.cert is not None and self.key is not None:
            context = create_default_context(cafile=str(self.ca_cert))
            context.load_cert_chain(self.cert, self.key)
            return ConnectionParameters(
                host=self.host,
                port=self.port,
                virtual_host=self.vhost,
                credentials=PlainCredentials(self.user, self.password),
                ssl_options=SSLOptions(context, self.host),
            )
        context = create_default_context()
        return ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.vhost,
            credentials=PlainCredentials(self.user, self.password),
        )

    @typechecked
    @staticmethod
    def from_connection_params(conn_params: ConnectionParameters) -> "ServerConfig":
        return ServerConfig(
            host=conn_params.host,
            port=conn_params.port,
            user=getattr(conn_params.credentials, "username", ""),
            password=getattr(conn_params.credentials, "password", ""),
            vhost=conn_params.virtual_host,
        )


@typechecked
def server_config(
    host: str,
    port: int,
    user: str,
    password: str,
    vhost: str,
    ca_cert: Union[str, Path, None] = None,
    cert: Union[str, Path, None] = None,
    key: Union[str, Path, None] = None,
) -> ServerConfig:
    """Generates a [`ServerConfig`][robotnikmq.config.ServerConfig] object while validating that the necessary certificate information.

    Args:
        host (str): Description
        port (int): Description
        user (str): Description
        password (str): Description
        vhost (str): Description
        ca_cert (Union[str, Path]): Description
        cert (Union[str, Path]): Description
        key (Union[str, Path]): Description
    """
    if ca_cert is not None and cert is not None and key is not None:
        ca_cert, cert, key = Path(ca_cert), Path(cert), Path(key)
        return ServerConfig(
            host=host,
            port=port,
            user=user,
            password=password,
            vhost=vhost,
            ca_cert=ca_cert,
            cert=cert,
            key=key,
        )
    elif ca_cert is None and cert is None and key is None:
        return ServerConfig(
            host=host,
            port=port,
            user=user,
            password=password,
            vhost=vhost,
        )
    else:
        raise InvalidConfiguration(
            "Either all public key encryption fields (cert, key, ca-cert) must be provided, or none of them."
        )


class ConnectionConfig(BaseModel):
    attempts: int = 10
    wait_random_min_seconds: int = 2
    wait_random_max_seconds: int = 5


@typechecked
def conn_config(attempts: int, min_wait: int, max_wait: int) -> ConnectionConfig:
    return ConnectionConfig(
        attempts=attempts,
        wait_random_min_seconds=min_wait,
        wait_random_max_seconds=max_wait,
    )


class RobotnikConfig(BaseModel):
    tiers: List[List[ServerConfig]]
    connection: ConnectionConfig = ConnectionConfig()

    @typechecked
    def tier(self, index: int) -> List[ServerConfig]:
        return self.tiers[index]

    @typechecked
    def a_server(self, tier: int) -> ServerConfig:
        return choice(self.tier(tier))

    @typechecked
    def as_dict(self) -> Dict[str, Any]:
        return self.dict()

    @typechecked
    @staticmethod
    def from_tiered(
        tiers: List[List[ServerConfig]],
    ) -> "RobotnikConfig":
        return RobotnikConfig(tiers=tiers)

    @typechecked
    @staticmethod
    def from_connection_params(conn_params: ConnectionParameters) -> "RobotnikConfig":
        return RobotnikConfig(
            tiers=[[ServerConfig.from_connection_params(conn_params)]]
        )


@typechecked
def config_of(config_file: Optional[Path]) -> RobotnikConfig:
    if config_file is None or not config_file.exists():
        log.critical("No valid RobotnikMQ configuration file was provided")
        raise NotConfigured("No valid RobotnikMQ configuration file was provided")
    return RobotnikConfig(**safe_load(config_file.open().read()))
