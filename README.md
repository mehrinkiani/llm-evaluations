# llm-evaluations

This repository contains the code for blog post on LLM evaluations: https://mehrinkiani.github.io/posts/llm_evaluations/blog.html

Notebook `mistal-responses.ipynb` contains code for getting responses from `Mistral 7B-Instruct-v0.3` on a symptom to disease dataset. Mistral responses are saved at `data/llm_responses.csv`. The symptom dataset is obtained from: https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/data/Symptom2Disease.csv

After installing dependencies `pip install requirements`, Mistral responses at `data/llm_responses.csv` are evaluated using the following evaluations. 

1. Unit evaluations: 01_unit_evaluations.py
    - `$ python 01_unit_evaluations.py`
2. LLM as a judge: 02_llm_as_a_judge_evaluations.py 
    - `$inspect eval 02_llm_as_a_judge_evaluations.py --limit 10 --model "openai/gpt-4"`

Please note you will need OPENAI_API_KEY in your environment to run evaluations using an OpenAI model. 

The results of unit evaluations are in `01_unit_evaluation_results` and the result for LLM as a judge are in `logs`. 

