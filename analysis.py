from collections import defaultdict

from ibm_watson import ToneAnalyzerV3


from constants import IBM_WATSON_URL, IBM_WATSON_VERSION, IBM_WATSON_APIKEY


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
    return [positive, negative]
