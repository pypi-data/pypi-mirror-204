from typing import Iterable

import azure.functions as func
import typeguard

from warpzone.enums.topicenum import Topic
from warpzone.function import integrations


class OutputProcessor:
    """Post-processing output binding"""

    return_type = None

    def process(self, value):
        return value

    def _process(self, value):
        """Internal method to process output.
        If output is iterable, the processing is
        run for each item."""
        if not value:
            # None output is accepted,
            # to allow intentional function
            # breaks
            return

        if isinstance(value, Iterable):
            return [self.process(item) for item in value]
        else:
            return self.process(value)


class MessageOutput(OutputProcessor):
    def __init__(self, topic: Topic):
        typeguard.check_type(topic, Topic)
        self.topic = topic


class DataMessageOutput(MessageOutput):
    def process(self, data_msg):
        integrations.send_data(data_msg, self.topic)


class EventMessageOutput(MessageOutput):
    def process(self, event_msg):
        integrations.send_event(event_msg, self.topic)


class HttpOutput(OutputProcessor):
    return_type = func.HttpResponse

    def process(self, resp):
        return resp


class NoneOutput(OutputProcessor):
    pass
