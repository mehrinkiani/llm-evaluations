# llm-evaluations

This repository contains the code for blog post on LLM evaluations: https://mehrinkiani.github.io/posts/llm_evaluations/blog.html

Notebook contains code for getting responses from `Mistral 7B-Instruct-v0.3` on a symptom to disease dataset. The dataset is obtained from: https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/data/Symptom2Disease.csv

An Large Language Model (LLM) responses, `Mistral 7B-Instruct-v0.3` in this case, are evaluated using the following evaluations. 

1. Unit evaluations: 01_unit_evaluations.py
2. LLM as a judge: 02_llm_as_a_judge_evaluations.py 

The results of unit evaluations are in `01_unit_evaluation_results` and the result for LLM as a judge are in `logs`. 

