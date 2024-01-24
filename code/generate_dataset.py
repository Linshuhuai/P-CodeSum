import time
import os
import numpy as np
import openai
from tqdm import tqdm
from api_gpt3 import get_response
from evaluator.bleu import sentence_bleu
from evaluator.rouge import Rouge
from utils import read_examples, choice

openai.api_key = ""
input_dir = "./data/"
output_dir = "./data/"
model = [
    "gpt-3.5-turbo",
    "text-davinci-003",
    "text-davinci-002",
    "gpt-3.5-turbo-instruct",
]
# dataset = "jain-slee"
datasets = ["omnibus", "Payum", "badger", "contracts", "h2o-3", "jain-slee"]
description_dict = [
    "# An elaborate, high quality docstring for the above function: ",
    "# Here's what the above function is doing: ",
    "# Explanation of what the code does\\n# ",
    "# Summarization of the above code\\n# ",
    "# Short, project-specific code summarization that accurately captures the essence of above code\\n# ",
    "# Overview of the main functionality and purpose of the above code in a specific code project\\n# ",
    "",
    "# Here's a function and what the function is doing: ",
    "Can you generate high quality docstring for the above function?",
]

rouge_calculator = Rouge()
bleu_total = []
rouge_total = []

# 自动读取所有 project 的样例
for dataset in datasets:
    examples = read_examples(
        input_dir + dataset + "/examples.jsonl", 10, "summarize"
    )  # 读取上下文样例
    queries = read_examples(
        input_dir + dataset + "/seeds.jsonl", 30, "summarize"
    )  # 读取 query seeds

    for idx in range(0, 30):
        print(f"{dataset}'s query index: {idx}")
        fw = open(
            os.path.join(
                "./data/"
                + dataset
                + "/text-davinci-003/data_5_25/data_"
                + format(idx)
                + "_5_25.jsonl"
            ),
            "w",
        )
        bleu_q = []
        rouge_q = []
        prompt_q = queries[idx].source + description_dict[0]
        reference = queries[idx].target
        example_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in tqdm(range(25), desc="Processing", unit="item"):
            prompt = ""
            selected_examples = choice(5, example_list)
            for example_idx in selected_examples:
                prompt = (
                    prompt
                    + examples[example_idx].source
                    + description_dict[0]
                    + examples[example_idx].target
                    + "\n"
                )

            # send request to OpenAI
            # hypothesis = get_response(model[1], prompt + prompt_q).replace("\n", "\\n")
            hypothesis = get_response(model[3], prompt + prompt_q).replace(
                "\n", "\\n"
            )  # text-davinci-003弃用, 替换为 gpt-3.5-turbo-instruct
            # Compute bleu-4 scores
            bleu = sentence_bleu([reference], hypothesis)
            # Compute ROUGE scores
            rouge = rouge_calculator.calc_score([hypothesis], [reference])
            # write idx and bleu/rouge to files
            fw.write(
                format(idx)
                + " "
                + format(selected_examples)
                + " "
                + format(bleu)
                + " "
                + format(rouge)
                + "\n"
            )
            bleu_q.append(bleu)
            rouge_q.append(rouge)
            time.sleep(20)

        fw.write(
            "total: "
            + format(np.average(np.array(bleu_q)))
            + " "
            + format(np.average(np.array(rouge_q)))
            + "\n"
        )
        fw.close()
