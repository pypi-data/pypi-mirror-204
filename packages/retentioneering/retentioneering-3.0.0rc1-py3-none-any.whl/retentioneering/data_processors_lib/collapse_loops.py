from __future__ import annotations

from typing import Literal, Optional

import pandas as pd

from retentioneering.data_processor import DataProcessor
from retentioneering.eventstream.types import EventstreamType
from retentioneering.params_model import ParamsModel


class CollapseLoopsParams(ParamsModel):
    """
    A class with parameters for :py:class:`.CollapseLoops` class.
    """

    suffix: Optional[Literal["loop", "count"]]
    time_agg: Literal["max", "min", "mean"] = "min"


class CollapseLoops(DataProcessor):
    """
    Find ``loops`` and create new synthetic events in the paths of all users having such sequences.

    A ``loop`` - is a sequence of repetitive events.
    For example *"event1 -> event1"*

    Parameters
    ----------
    suffix : {"loop", "count"}, optional

        - If ``None``, event_name will be event_name without any changes.\n
        For example *"event1 - event1 - event1"* --> event1.

        - If ``loop``, event_name will be event_name_loop.\n
        For example *"event1 - event1 - event1"* --> event1_loop.

        - If ``count``, event_name will be event_name_loop_{number of events}.\n
        For example *"event1 - event1 - event1"* --> event1_loop_3.

    time_agg : {"max", "min", "mean"}, default "min"
        Aggregation method to calculate timestamp values for new groups.

    Returns
    -------
    Eventstream
        Eventstream with:

        - raw events: the returned events will be marked ``_deleted=True`` and soft-deleted from input eventstream.
        - new synthetic events: the returned events will be added to the input eventstream with columns below.

        +------------------------+----------------+--------------------------------------------+
        | **event_name**         | **event_type** | **timestamp**                              |
        +------------------------+----------------+--------------------------------------------+
        | event_name_loop        | group_alias    | min/max/mean(group of repetitive events))  |
        +------------------------+----------------+--------------------------------------------+
        | event_name_loop_{count}| group_alias    | (min/max/mean(group of repetitive events)) |
        +------------------------+----------------+--------------------------------------------+
        | event_name             | group_alias    | (min/max/mean(group of repetitive events)) |
        +------------------------+----------------+--------------------------------------------+


    See Also
    --------
    .StepMatrix

    Notes
    -----
    See :doc:`Data processors user guide</user_guides/dataprocessors>` for the details.
    """

    params: CollapseLoopsParams

    def __init__(self, params: CollapseLoopsParams):
        super().__init__(params=params)

    def apply(self, eventstream: EventstreamType) -> EventstreamType:
        from retentioneering.eventstream.eventstream import Eventstream

        user_col = eventstream.schema.user_id
        time_col = eventstream.schema.event_timestamp
        type_col = eventstream.schema.event_type
        event_col = eventstream.schema.event_name

        suffix = self.params.suffix
        time_agg = self.params.time_agg
        df = eventstream.to_dataframe(copy=True)
        df["ref"] = df[eventstream.schema.event_id]

        df["grp"] = df[event_col] != df.groupby(user_col)[event_col].shift(1)
        # Столбец в котором считается порядковый номер по группам одинаковых событий
        df["cumgroup"] = df.groupby(user_col)["grp"].cumsum()
        df["count"] = df.groupby([user_col, "cumgroup"]).cumcount() + 1
        df["collapsed"] = df.groupby([user_col, "cumgroup", event_col])["count"].transform(max)
        df["collapsed"] = df["collapsed"].apply(lambda x: False if x == 1 else True)

        loops = (
            df[df["collapsed"] == 1]
            .groupby([user_col, "cumgroup", event_col])
            .agg({time_col: time_agg, "count": "max"})
            .reset_index()
        )

        if suffix == "loop":
            loops[event_col] = loops[event_col].map(str) + "_loop"
        elif suffix == "count":
            loops[event_col] = loops[event_col].map(str) + "_loop_" + loops["count"].map(str)
        loops[type_col] = "group_alias"
        loops["ref"] = None

        df_to_del = df[df["collapsed"] == 1]

        df_loops = pd.concat([loops, df_to_del])
        eventstream = Eventstream(
            raw_data_schema=eventstream.schema.to_raw_data_schema(),
            raw_data=df_loops,
            relations=[{"raw_col": "ref", "eventstream": eventstream}],
        )
        if not df_to_del.empty:
            eventstream._soft_delete(df_to_del)

        return eventstream
