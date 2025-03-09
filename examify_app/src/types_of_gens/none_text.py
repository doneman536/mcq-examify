import os
import json
import pandas as pd
import traceback
import time

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("groq_api")

llm = ChatGroq(groq_api_key=key, temperature=1, model="qwen-2.5-32b")

template = """
You are an MCQ generator.
Topic: {Topic}
Text: {Text}

If the text is None, generate MCQs based on the given topic.
If the provided text is insufficient, use your knowledge to generate relevant MCQs.

Now create {Count} MCQs in {Mode} mode as per the given topic.
The response should be in JSON format:

### Response format:
{json_format}
"""

response_format = {
    "1": {
        "Question": "question",
        "options": {
            "a": "choice 1",
            "b": "choice 2",
            "c": "choice 3",
            "d": "choice 4",
        },
    },
    "2": {},
}

answers_format = {
    "1": {
        "answer": "correct option",
        "reason": "Provide a small description about why that option is correct.",
    },
    "2": {},
}

answers_template = """
MCQs: {generated_mcqs}

As per the above, provide correct answers in the following format:

## Result format:
{answers_format}
"""

def generate_mcqs(topic, text=None, count=5, mode="low"):
    quiz_generate_prompt = PromptTemplate(
        input_variables=["Topic", "Text", "Count", "Mode", "json_format"],
        template=template,
    )

    quiz_answers_prompt = PromptTemplate(
        input_variables=["generated_mcqs"],
        template=answers_template,
    )

    chain1 = LLMChain(llm=llm, prompt=quiz_generate_prompt, output_key="generated_mcqs")
    chain2 = LLMChain(llm=llm, prompt=quiz_answers_prompt, output_key="mcq_answers")

    main_chain = SequentialChain(
        chains=[chain1, chain2],
        input_variables=["Topic", "Text", "Count", "Mode", "json_format", "answers_format"],
        output_variables=["generated_mcqs", "mcq_answers"],
    )

    response = main_chain.invoke(
        {
            "Topic": topic,
            "Text": text,  # Ensure `text` is defined or replace with `None`
            "Count": count,
            "Mode": mode,
            "json_format": response_format,
            "answers_format": answers_format,
        }
    )

    raw_json = response["generated_mcqs"]

    if raw_json.startswith("```json"):
        raw_json = raw_json[7:]
    if raw_json.endswith("```"):
        raw_json = raw_json[:-3]

    try:
        mcqs = json.loads(raw_json.strip())
    except json.JSONDecodeError:
        mcqs = raw_json


    raw_answers_json = response['mcq_answers']

    if raw_answers_json.startswith("```json"):
        raw_answers_json = raw_answers_json[7:]
    if raw_answers_json.endswith("```"):
        raw_answers_json = raw_answers_json[:-3]


    mcqs_answers = json.loads(raw_answers_json)

    return mcqs, mcqs_answers




def safe_generate_mcqs(topic, text=None, count=5, mode="low", retries=5, delay=2):
    for attempt in range(1, retries + 1):
        try:
            return generate_mcqs(topic, text, count, mode)
        except Exception as e:
            print(f"Error: {e}. Retrying {attempt}/{retries}...")
        time.sleep(delay)
    raise RuntimeError("MCQ generation failed after multiple attempts.")




