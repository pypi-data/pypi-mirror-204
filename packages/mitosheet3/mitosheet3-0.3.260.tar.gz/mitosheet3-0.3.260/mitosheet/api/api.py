#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Saga Inc.
# Distributed under the terms of the GPL License.
"""
Contains handlers for the Mito API
"""
from queue import Queue
from threading import Thread
from time import perf_counter
from typing import Any, Callable, Dict, List, NoReturn, Union

from mitosheet.types import MitoWidgetType
from mitosheet.api.get_column_describe import get_column_describe
from mitosheet.api.get_column_summary_graph import get_column_summary_graph
from mitosheet.api.get_csv_files_metadata import get_csv_files_metadata
from mitosheet.api.get_dataframe_as_csv import get_dataframe_as_csv
from mitosheet.api.get_dataframe_as_excel import get_dataframe_as_excel
from mitosheet.api.get_defined_df_names import get_defined_df_names
from mitosheet.api.get_excel_file_metadata import get_excel_file_metadata
from mitosheet.api.get_imported_files_and_dataframes_from_analysis_name import \
    get_imported_files_and_dataframes_from_analysis_name
from mitosheet.api.get_imported_files_and_dataframes_from_current_steps import \
    get_imported_files_and_dataframes_from_current_steps
from mitosheet.api.get_params import get_params
from mitosheet.api.get_path_contents import get_path_contents
from mitosheet.api.get_path_join import get_path_join
from mitosheet.api.get_split_text_to_columns_preview import \
    get_split_text_to_columns_preview
from mitosheet.api.get_test_imports import get_test_imports
from mitosheet.api.get_unique_value_counts import get_unique_value_counts
from mitosheet.steps_manager import StepsManager
from mitosheet.api.get_render_count import get_render_count
from mitosheet.api.get_code_snippets import get_code_snippets
from mitosheet.api.get_available_snowflake_options_and_defaults import get_available_snowflake_options_and_defaults
from mitosheet.api.get_validate_snowflake_credentials import get_validate_snowflake_credentials
from mitosheet.api.get_ai_completion import get_ai_completion
# AUTOGENERATED LINE: API.PY IMPORT (DO NOT DELETE)
from mitosheet.telemetry.telemetry_utils import log_event_processed

# As the column summary statistics tab does three calls, we defaulted to this max
MAX_QUEUED_API_CALLS = 3

# NOTE: BE CAREFUL WITH THIS. When in development mode, you can set it to False
# so the API calls are handled in the main thread, to make printing easy.
# In newer versions of JupyterLab, to see these print statements:
# View > Show Log Console > in the console set Log Level to Debug
THREADED = True


class API:
    """
    The API provides a wrapper around a thread that responds to API calls.

    Some notes:
    -   We allow at most MAX_QUEUED_API_CALLS API calls to be in the queue, which practically
        Stops a backlog of calls from building up.
    -   All API calls should only be reads. This stops us from having to worry
        about most concurrency issues
    -   Note that printing inside of a thread does not work properly! Use sys.stdout.flush() after the print statement.
        See here: https://stackoverflow.com/questions/18234469/python-multithreaded-print-statements-delayed-until-all-threads-complete-executi
    """

    def __init__(self, steps_manager: StepsManager, mito_backend: MitoWidgetType):
        self.api_queue: Queue = Queue(MAX_QUEUED_API_CALLS)
        # Note that we make the thread a daemon thread, which practically means that when
        # The process that starts this thread terminate, our API will terminate as well.
        self.thread = Thread(
            target=handle_api_event_thread,
            args=(self.api_queue, steps_manager, mito_backend),
            daemon=True,
        )
        self.thread.start()

        # Save some variables for ease
        self.steps_manager = steps_manager
        self.mito_backend = mito_backend

    def process_new_api_call(self, event: Dict[str, Any]) -> None:
        """
        We privilege new API calls over old calls, and evict the old ones
        if the API queue is full.

        Because we are using a queue, only events that have not been started
        being processed will get removed.

        If the key 'priority' is in the event, then we handle it in the main
        thread, as we don't want to drop the event. For example, lazy loading
        data has priority!
        """
        if THREADED and "priority" not in event:
            if self.api_queue.full():
                # If the queue is full, we drop the first event, and just return a None
                lost_event = self.api_queue.get()

                self.mito_backend.mito_send({"event": "api_response", "id": lost_event["id"], "data": None})

            self.api_queue.put(event)
        else:
            handle_api_event(self.mito_backend.mito_send, event, self.steps_manager)


def handle_api_event_thread(
    queue: Queue, steps_manager: StepsManager, mito_backend: MitoWidgetType
) -> NoReturn:
    """
    This is the worker thread function, that actually is
    responsible for handling at the API call events.

    It lives forever, and just handles events as it
    receives them from the queue
    """
    while True:
        # Note that this blocks when there is nothing in the queue,
        # and waits till there is something there - so no infinite
        # loop as it is waiting!
        event = queue.get()
        # We place the API handling inside of a try catch,
        # because otherwise if an error is thrown, then the entire thread crashes,
        # and then the API never works again
        try:
            handle_api_event(mito_backend.mito_send, event, steps_manager)
        except:
            # Log in error if it occurs
            log_event_processed(event, steps_manager, failed=True)


def handle_api_event(
    send: Callable, event: Dict[str, Any], steps_manager: StepsManager
) -> None:
    """
    Handler for all API calls. Note that any response to the
    API must return the same ID that the incoming message contains,
    so that the frontend knows how to match the responses.
    """
    result: Union[str, List[str], int] = ''
    params = event['params']
    start_time = perf_counter()
    failed = False

    try:
        if event["type"] == "get_path_contents":
            result = get_path_contents(params)
        elif event["type"] == "get_path_join":
            result = get_path_join(params)
        elif event["type"] == "get_dataframe_as_csv":
            result = get_dataframe_as_csv(params, steps_manager)
        elif event["type"] == "get_column_summary_graph":
            result = get_column_summary_graph(params, steps_manager)
        elif event["type"] == "get_column_describe":
            result = get_column_describe(params, steps_manager)
        elif event["type"] == "get_params":
            result = get_params(params, steps_manager)
        elif event["type"] == "get_excel_file_metadata":
            result = get_excel_file_metadata(params, steps_manager)
        elif event["type"] == "get_csv_files_metadata":
            result = get_csv_files_metadata(params, steps_manager)
        elif event["type"] == "get_unique_value_counts":
            result = get_unique_value_counts(params, steps_manager)
        elif event["type"] == "get_split_text_to_columns_preview":
            result = get_split_text_to_columns_preview(params, steps_manager)
        elif event["type"] == "get_dataframe_as_excel":
            result = get_dataframe_as_excel(params, steps_manager)
        elif event["type"] == "get_defined_df_names":
            result = get_defined_df_names(params, steps_manager)
        elif event["type"] == 'get_imported_files_and_dataframes_from_current_steps':
            result = get_imported_files_and_dataframes_from_current_steps(params, steps_manager)
        elif event["type"] == 'get_imported_files_and_dataframes_from_analysis_name':
            result = get_imported_files_and_dataframes_from_analysis_name(params, steps_manager)
        elif event["type"] == "get_test_imports":
            result = get_test_imports(params, steps_manager)
        elif event["type"] == "get_render_count":
            result = get_render_count(params, steps_manager)
        elif event["type"] == "get_code_snippets":
            result = get_code_snippets(params, steps_manager)
        elif event["type"] == "get_available_snowflake_options_and_defaults":
            result = get_available_snowflake_options_and_defaults(params, steps_manager)
        elif event["type"] == "get_validate_snowflake_credentials":
            result = get_validate_snowflake_credentials(params, steps_manager)
        elif event["type"] == "get_ai_completion":
            result = get_ai_completion(params, steps_manager)
        # AUTOGENERATED LINE: API.PY CALL (DO NOT DELETE)
        else:
            raise Exception(f"Event: {event} is not a valid API call")

    except:
        failed = True
    
    # Log processing this event (with potential failure)
    log_event_processed(event, steps_manager, failed=failed, start_time=start_time)

    send({"event": "api_response", "id": event["id"], "data": result})
