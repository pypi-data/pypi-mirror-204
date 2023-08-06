class UnableToConnect(Exception):
    def __str__(self):
        return f"{self.__class__.__name__}: Robotnik is unable to connect: {self.args}"


class MalformedMessage(Exception):
    def __init__(self, msg_input: str):
        self.malformed_input = msg_input
        super().__init__()

    def __str__(self):
        return f'Unable to decode RobotnikMQ message from: "{self.malformed_input}"'


class InvalidConfiguration(Exception):
    def __str__(self):
        return (
            f"{self.__class__.__name__}: Robotnik is improperly configured: {self.args}"
        )


class NotConfigured(Exception):
    msg = "Robotnik is not configured"
