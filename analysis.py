from ibm_watson import ToneAnalyzerV3

from collections import defaultdict
import datetime


from constants import IBM_WATSON_URL, IBM_WATSON_VERSION, IBM_WATSON_APIKEY, MINUTES_FOR_A_CHAT_SESSION
from database import message_details
from helpers import get_time_difference_from_now


# IBM Watson Tone Analyzer set up
tone_analyser = ToneAnalyzerV3(
    version=IBM_WATSON_VERSION,
    iam_apikey=IBM_WATSON_APIKEY,
    url=IBM_WATSON_URL
)


def tone_analysing(text_msg):
    """This function returns a list with calculated values of positive and negative after analysis of the text_msg"""
    # dict to store the emotions returned by IBM Watson for the text_msg
    emotion_dict = defaultdict(int)
    # initialize positive and negative values which are calculated using the emotion_dict
    positive = 0
    negative = 0
    # break the loop once category_id emotion_tone is found
    emotion_tone_flag = 0
    tone_analysis = tone_analyser.tone(
        {'text': text_msg},
        content_type='application/json'
    ).get_result()
    for tones in tone_analysis['document_tone']['tone_categories']:
        # run only if the category_id emotion_tone is not found
        if emotion_tone_flag == 0:
            if tones['category_id'] == 'emotion_tone':
                emotion_tone_flag = 1
                # find and set respective tones in the emotion_dict
                for tone in tones['tones']:
                    if tone['tone_id'] == 'sadness':
                        emotion_dict['sadness'] = tone['score']
                    if tone['tone_id'] == 'anger':
                        emotion_dict['anger'] = tone['score']
                    if tone['tone_id'] == 'disgust':
                        emotion_dict['disgust'] = tone['score']
                    if tone['tone_id'] == 'fear':
                        emotion_dict['fear'] = tone['score']
                    if tone['tone_id'] == 'joy':
                        positive = tone['score']
    negative = max(emotion_dict['sadness'], emotion_dict['anger'], emotion_dict['disgust'], emotion_dict['fear'])
    return [round(positive, 2), round(negative, 2)]


def generate_response(sender_id):
    """This function is responsible for generating appropriate response after passing sender_id as the _id.
    All the messages sent by a particular sender are analyzed.
    """
    sender_msg_lst = []
    # find the object with _id as the sender_id passed
    sender = message_details.find_one({'_id': sender_id})
    for message in sender.get('messages'):
        # every message sent by the sender is collected in sender_msg_lst
        sender_msg_lst.append(message)
    response = calculate_weighted_factor(sender_msg_lst)
    return response


def calculate_weighted_factor(sender_msg_lst):
    """This function calculates the weighted positive and negative values based on the time passed since sending the
    message, it works on the idea that messages sent recently are more relevant than older messages. A weighted ratio is
    calculated after averaging the weighted positive and negative values derived from the sender's messages.
    """
    # positive and negative sum of all individual messages sent by the sender
    positive_sum = 0
    negative_sum = 0
    current_time = datetime.datetime.utcnow()
    # the number of messages sent by the sender in the session
    messeges_within_session_count = 0
    for msg_dict in sender_msg_lst:
        # find the minutes passed from the current time for each message
        minutes_passed = round(get_time_difference_from_now(msg_dict['timestamp'], current_time), 0)
        # if the minutes_passed is greater than the session minutes then don't consider those messages for calculation
        if minutes_passed > MINUTES_FOR_A_CHAT_SESSION:
            msg_dict['positive'] *= 0
            msg_dict['negative'] *= 0
        else:
            # formula to calculate the weighted factor
            weighted_factor = (MINUTES_FOR_A_CHAT_SESSION - minutes_passed)/MINUTES_FOR_A_CHAT_SESSION
            # multiply the positive and negative values with the weighted_factor
            msg_dict['positive'] *= weighted_factor
            msg_dict['negative'] *= weighted_factor
            messeges_within_session_count += 1

        positive_sum += msg_dict['positive']
        negative_sum += msg_dict['negative']

    weighted_ratio = round((positive_sum-negative_sum)/messeges_within_session_count, 2)
    print(weighted_ratio)
    response = get_response_dict(weighted_ratio)
    return response


def get_response_dict(weighted_ratio):
    """This function takes in the weighted_ratio and responds with an appropriate response to be sent back to the sender
    response structure:
    {'response': "Oh! That's great!", 'mood': 'Positive'}
    """
    if 1 >= weighted_ratio > 0.15:
        response = "Oh! That's great!"
        mood = 'Positive'
    elif 0.15 >= weighted_ratio > 0:
        response = "That is fine."
        mood = 'Positive-Neutral'
    elif weighted_ratio == 0:
        response = "Interesting"
        mood = 'Neutral'
    elif 0 > weighted_ratio >= -0.15:
        response = "That's not nice"
        mood = "Negative-Neutral"
    else:
        response = "I feel so bad about this."
        mood = "Negative"
    return {'response': response, 'mood': mood}