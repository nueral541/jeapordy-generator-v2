import anthropic
import time

key = '--INSERT YOUR API KEY HERE--'

client = anthropic.Anthropic(api_key = key)

def question_gen():
    game_info = ask_categories()
    return handle_api(game_info)

def ask_categories():
    print("Welcome to the Trivia Generator!")
    print("First we need some information on your game.")
    category1 = input("Please enter the first category: ")
    diificulty1 = input("Please enter the difficulty of the first category (1-10): ")
    category2 = input("Please enter the second category: ")
    diificulty2 = input("Please enter the difficulty of the second category (1-10): ")
    category3 = input("Please enter the third category: ")
    diificulty3 = input("Please enter the difficulty of the third category (1-10): ")
    category4 = input("Please enter the fourth category: ")
    diificulty4 = input("Please enter the difficulty of the fourth category (1-10): ")
    category5 = input("Please enter the fifth category: ")
    diificulty5 = input("Please enter the difficulty of the fifth category (1-10): ")

    game_info = [{"name": category1, "difficulty": diificulty1},
            {"name": category2, "difficulty": diificulty2},
            {"name": category3, "difficulty": diificulty3},
            {"name": category4, "difficulty": diificulty4},
            {"name": category5, "difficulty": diificulty5}]
    
    return game_info

def handle_api(game_info):
    system_prompt = '''
    You are an informative and intelligent AI solely for the purpose of generating trivia questions.
    You will be presented with a category and a difficulty level from 1 to 10, one being tended to a complete beginner while 10 being an advanced professional in the field.
    You will then proceed to generate 5 questions and answers relating to the category and difficulty level.
    Each question and answer will be in the form of a Jeopardy game. One question will be worth 100, then 200, then 300, then 400, and finally 500. You will adjust the difficulty as needed based on the points for each question.
    You will return a list of questions, answers, and point values for all 5 questions.
    Do NOT repeat questions.
    You must OMIT any introductory or extraneous text before or after the list. Only the JSON array should be returned.
    The output will ONLY be as shown in the example below:
    [
        {
            "question": "the question worth 100 points about the category given",
            "answer": "the answer to the first question",
            "points": 100
        },
        {
            "question": "the question worth 200 points about the category given",
            "answer": "the answer to the second question",
            "points": 200
        },
        {
            "question": "the question worth 300 points about the category given",
            "answer": "the answer to the third question",
            "points": 300
        },
        {
            "question": "the question worth 400 points about the category given",
            "answer": "the answer to the fourth question",
            "points": 400
        },
        {
            "question": "the question worth 500 points about the category given",
            "answer": "the answer to the fifth question",
            "points": 500
        }
    ]
    '''

    questions = {}

    for category in game_info:

        user_prompt = f'Category: {category['name']}, Difficulty: {category['difficulty']}.'
        full_prompt = f'{anthropic.HUMAN_PROMPT}{system_prompt}\n\n{user_prompt}{anthropic.AI_PROMPT}'

        response = ask_claude(full_prompt)

        questions[category['name']] = {
            str(response[0]['points']): {'question': response[0]['question'], 'answer': response[0]['answer']},
            str(response[1]['points']): {'question': response[1]['question'], 'answer': response[1]['answer']},
            str(response[2]['points']): {'question': response[2]['question'], 'answer': response[2]['answer']},
            str(response[3]['points']): {'question': response[3]['question'], 'answer': response[3]['answer']},
            str(response[4]['points']): {'question': response[4]['question'], 'answer': response[4]['answer']}
        }

    return questions

def ask_claude(full_prompt, retries=5, delay=10):

    time.sleep(2)

    for attempt in range(retries):
        try:
            response = client.completions.create(
                model="claude-2",
                prompt=full_prompt,
                max_tokens_to_sample=512,
                temperature=0.7,
            )
            # Validate JSON output
            return extract_json(response.completion)
        except anthropic.InternalServerError as e:
            print(f"Error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    
    raise Exception("Failed to get a valid response from the API after multiple attempts.")

def extract_json(raw_response):
    """ Extract JSON from AI response """
    import json
    try:
        start_idx = raw_response.index('[')  # Find start of JSON
        end_idx = raw_response.rindex(']') + 1  # Find end of JSON
        return json.loads(raw_response[start_idx:end_idx])  # Parse the JSON
    except Exception as e:
        raise ValueError(f"Failed to parse JSON: {e}\nResponse was: {raw_response}")
