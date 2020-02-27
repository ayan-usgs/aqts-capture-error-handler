"""
Module for working with the AWS Step Functions API

"""
import json

import boto3

from .utils import search_dictionary_list


ENTRY_FAIL_MAPPING = {
    'MapStateFailed': 'MapStateEntered',
    'TaskStateEntered': 'TaskStateEntered'
}


def get_execution_history(execution_arn, region='us-west-2'):
    sfn = boto3.client('stepfunctions', region_name=region)
    history = sfn.get_execution_history(executionArn=execution_arn)
    return history


def backtrack_to_failure(execution_history):
    event = execution_history['events'][-1]
    task_type = ''
    while 'Failed' not in task_type:
        previous_event_id = event['previousEventId']
        search_result = search_dictionary_list(execution_history['events'], 'id', previous_event_id)[0]
        task_type = search_result['type']
        event = search_result
    return event


def find_root_failure_state(execution_history):
    execution_events = execution_history['events']
    event = backtrack_to_failure(execution_history)
    failed_event_type = event['type']
    while event['type'] != ENTRY_FAIL_MAPPING[failed_event_type]:
        state_previous_event_id = event['previousEventId']
        search_result = search_dictionary_list(execution_events, 'id', state_previous_event_id)[0]
        event = search_result
    state_event_details = event['stateEnteredEventDetails']
    root_input = json.loads(state_event_details['input'])
    root_input['resumeState'] = state_event_details['name']
    return root_input
