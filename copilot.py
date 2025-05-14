"""This script contains the necessary functions to interact with the copilot application"""

# importing libraries
import numpy as np
import datetime
import threading
import traceback
import logging

# importing user defined modules
from Enums.input_info import input_enum
from utils import utils_firebase, utils


def choose_copilot_with_least_questions(conciergeId, organization_id):
    all_data = utils_firebase.get_chatbot_data(conciergeId, organization_id)
    min_question_count = np.Infinity
    choosen_copilot_id = None

    if all_data is None:
        logging.info("Firebase : No data in database")
        return None

    for copilot_id in all_data['copilot']:
        active_questions = 0

        # Don't choose a copilot that is not active
        if all_data['copilot'][copilot_id]['status'] != 'active':
            continue

        if 'queue' not in all_data['copilot'][copilot_id]:
            min_question_count = 0
            choosen_copilot_id = copilot_id
            continue

        for question_id in all_data['copilot'][copilot_id]['queue']:
            if all_data['copilot'][copilot_id]['queue'][question_id]['status'] == 'active':
                active_questions += 1

        if active_questions < min_question_count:
            min_question_count = active_questions
            choosen_copilot_id = copilot_id

    return choosen_copilot_id


def number_of_copilots(conciergeId, organization_id):
    try:
        all_data = utils_firebase.get_chatbot_data(conciergeId, organization_id)
        num_copilots = 0

        if all_data is None:
            logging.info("Firebase : No data in database")
            return None

        if 'copilot' not in all_data:
            return 0
        for copilot_id in all_data['copilot']:
            if all_data['copilot'][copilot_id]['status'] == 'active':
                num_copilots = num_copilots + 1
        return num_copilots

    except Exception as e:
        utils.exception_handling("Error happened while counting number of copilots", [conciergeId, organization_id], e, traceback.format_exc())


def choose_copilot_with_no_questions(conciergeId, organization_id):
    all_data = utils_firebase.get_chatbot_data(conciergeId, organization_id)

    if all_data is None:
        logging.info("Firebase : No data in database")
        return None

    for copilot_id in all_data['copilot']:
        if 'queue' not in all_data['copilot'][copilot_id] and all_data['copilot'][copilot_id]['status'] == 'active':
            return copilot_id

    return None


def main(conciergeId, organization_id, question_id, question, best_answer, answers, reference_docs, confidence_score, data, metadata, citations, traceability_response):
    num_of_copilots = number_of_copilots(conciergeId, organization_id)

    note_to_remove = f'<p style="font-size: 0.8rem; font-family: ui-sans-serif, system-ui, sans-serif, \'Apple Color Emoji\', \'Segoe UI Emoji\', \'Segoe UI Symbol\', \'Noto Color Emoji\';"><b>{data[input_enum.SPT_NOTE.value]}</b></p>'
    if note_to_remove in best_answer:
        best_answer = best_answer.replace(note_to_remove, "").strip()
        logging.info(f"Note removed. Updated selected_answer: {best_answer}")
        
    if num_of_copilots == 0:
        answer_dict = {}
        for answer in answers:
            answer_dict[answer] = {'answer': answers[answer]['answer'],
                                   'confidence_score': answers[answer]['confidence_score']}
        
        slack_webhook_url = data[input_enum.SLACK_WEBHOOK_URL.value] 
        question = {
            'question': question,
            'status': 'active',
            'selected_answer': best_answer,
            'answers': answer_dict,
            'created_at': str(datetime.datetime.now(datetime.timezone.utc).isoformat()),
            'conciergeId': conciergeId,
            'organization_id': organization_id,
            'prompt': data['prompt'],
            'confidenceScoreThreshold': data['confidenceScoreThreshold'],
            'confidenceScore': confidence_score,
            'chatHistory': data['chatHistory'],
            'modelType': data['modelType'],
            'requestId': data['requestId'],
            'referenceDocs': reference_docs,
            'metadata': metadata,
            'slack_webhook_url': slack_webhook_url if slack_webhook_url else None,
            'is_stream': data['isStreamResponseOn'],
            'traceability_response': traceability_response,
            'conciergeName': data['conciergeName'],
            'assistant_type': data[input_enum.ASSISTANT_TYPE.value],
            'citations': citations
        }
        threading.Thread(target=utils_firebase.add_question_to_copilot_timed_out_question_queue, args=(conciergeId, organization_id, question_id, question,)).start()
        return False

    elif num_of_copilots is None:
        logging.info("Firebase : No data in database")
        return False

    else:
        copilot_id = choose_copilot_with_no_questions(conciergeId, organization_id)

        if copilot_id is None:
            # Put the question in copilot question queue
            threading.Thread(target=utils_firebase.add_question_to_copilot_question_queue_with_both_answer, args=(conciergeId, organization_id, question_id, question, best_answer, answers, reference_docs, confidence_score, data, metadata, citations, traceability_response)).start()
            return True

        else:
            # Put in the copilot queue
            threading.Thread(target=utils_firebase.add_question_to_copilot_with_both_answer, args=(conciergeId, organization_id, copilot_id, question_id, question, best_answer, answers, reference_docs, confidence_score, data, metadata, citations, traceability_response)).start()
            return True
