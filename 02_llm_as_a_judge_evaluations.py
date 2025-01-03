"""
Evals for for symptom to disease diagnosis.

The Symptom2Disease.csv dataset contains 1200 examples. There are two scoring methods supported corresponding to the two @task definitions below:

1. validate - score using the validity checker 
2. critique - score using the critique prompt 

Please note you will need OPENAI_API_KEY to run OpenAI gpt4 as a judge: https://platform.openai.com/api-keys
"""

import json

from inspect_ai import task, Task
from inspect_ai.dataset import csv_dataset, FieldSpec
from inspect_ai.model import get_model
from inspect_ai.scorer import accuracy, scorer, Score, CORRECT, INCORRECT
from inspect_ai.solver import system_message, solver, generate
from inspect_ai.util import resource


from utils.utils import json_completion


@task
def critique():
    return eval_task(scorer=critique_scorer())


def eval_task(scorer):
    # read dataset
    dataset = csv_dataset(
        csv_file="data/llm_responses.csv",
        sample_fields=FieldSpec(input="prompt", target="response"),
        shuffle=True,
    )

    # create eval task
    return Task(
        dataset=dataset,
        plan=[
            system_message(
                "Medical AI predicts disease based on symptoms entered by user."
            ),
            prompt_with_schema(),
            generate(),
        ],
        scorer=scorer,
    )


@solver
def prompt_with_schema():
    prompt_template = resource("utils/prompt.txt")

    async def solve(state, generate):
        # build the prompt
        state.user_prompt.text = prompt_template.replace(
            "{{prompt}}", state.user_prompt.text
        )
        return state

    return solve


@scorer(metrics=[accuracy()])
def critique_scorer(model="openai/gpt-4-turbo"):

    async def score(state, target):
        # build the critic prompt
        prediction = target.target[0]
        critic_prompt = (
            resource("utils/02_critique.txt")
            .replace("{{prompt}}", state.user_prompt.text)
            .replace("{{prediction}}", prediction)
        )

        # run the critique
        result = await get_model(model).generate(critic_prompt)
        try:
            parsed = json.loads(json_completion(result.completion))
            value = CORRECT if parsed["outcome"] == "good" else INCORRECT
            explanation = parsed["critique"]
        except (json.JSONDecodeError, KeyError):
            value = INCORRECT
            explanation = f"JSON parsing error:\n{result.completion}"

        # return value and explanation (critique text)
        return Score(
            value=value,
            explanation=explanation,
            answer=json_completion(state.output.completion),
        )

    return score
