import json

import pandas as pd

from warpzone.servicebus.data.client import DataMessage
from warpzone.servicebus.events.client import EventMessage


def assert_event_msg_similar(
    left: EventMessage,
    right: EventMessage,
    check_message_id: bool = False,
):
    """
    Assert if two event messages are similar, meaning equal
    - event
    - subject
    - message id [optional]
    """
    assert (
        left.event == right.event
    ), f"Events are different: {left.event} != {right.event}"
    assert (
        left.subject == right.subject
    ), f"Subjects are different: {left.subject} != {right.subject}"
    if check_message_id:
        assert (
            left.message_id == right.message_id
        ), f"Message ids are different: {left.message_id} != {right.message_id}"


def assert_data_msg_similar(
    left: DataMessage,
    right: DataMessage,
    check_message_id: bool = False,
):
    """
    Assert if two data messages are similar, meaning equal
    - content
    - subject
    - message id [optional]
    """
    assert (
        left.subject == right.subject
    ), f"Subjects are different: {left.subject} != {right.subject}"
    assert (
        left.extension == right.extension
    ), f"Extensions are different: {left.extension} != {right.extension}"
    if check_message_id:
        assert (
            left.message_id == right.message_id
        ), f"Message ids are different: {left.message_id} != {right.message_id}"

    if left.extension == "parquet":
        # for parquet files, check if the resulting pandas DataFrames are equal
        pd.testing.assert_frame_equal(
            left=left.to_pandas(),
            right=right.to_pandas(),
        )
    elif left.extension == "json":
        # for json files, check if the parsed data is equal
        left_json, right_json = json.loads(left.content), json.loads(right.content)
        assert (
            left_json == right_json
        ), f"JSON is different: {left_json} != {right_json}"
    else:
        # for other files, check if the bytes are equal
        assert (
            left.content == right.content
        ), f"Content is different: {left.content} != {right.content}"
