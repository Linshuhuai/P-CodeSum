# P-CodeSum

## Introduction

Automatically generating concise and readable summaries for source code has emerged as a valuable task in software development and maintenance. In recent years, code summarization has been significantly advanced by large language models (LLM). While state-of-the-art approaches have significantly demonstrated efficacy for general code snippets, they seldom concern code summarization for a specific project. In practice, however, developers are more concerned with code summaries for their working projects, i.e., project-specific code summarization (PCS). The sticking point to the PCS task is that project-specific data are severely insufficient. One promising solution is in-context learning with LLMs, which requires a set of carefully curated prompts by humans and is costly and inefficient.

We introduce P-CodeSum, a novel approach that focuses on automatically generating code summaries tailored to specific projects in few-shot scenarios.

The contributions of this work are as follows:

* We empirically study the performance of LLMs on project-specific code summarization tasks and explore key factors to high-quality prompts.

* We propose a neural prompt selector trained on data generated by LLM, obtaining project-specific examples for in-context learning in the few-shot situation.

* We conduct comprehensive experiments to evaluate P-CodeSum. Results demonstrate the high quality of prompts generated by our selector and the significant improvements that P-CodeSum brings to PCS tasks.

The training data of the neural prompt selector and its generation method are explained in [Data](#my-data).

## Data
[data]:#my-data

![Generate training data](https://github.com/Linshuhuai/P-CodeSum/blob/master/figures/DataGenerating.png)

Training the project-specific prompt selector necessitates the collection of positive and negative data samples. Recognizing the expensive time and effort associated with manual annotation of training data, we employ an LLM to automatically craft high-quality training data.

We use six project for code summarization task from [CodeXGLUE](https://github.com/microsoft/CodeXGLUE) to generate training and test data of the neural prompt selector. Here is the statistics of them: 

|Languages|Projects|# of examples|# of in-context examples|# of test examples|
|:------:|:--:|:----:|:----:|:----:|
| Python | h2oai/h2o-3 | 268 | 10 | 228 |
| Java | RestComm/jain-slee | 234 | 10 | 194 |
| Go | dgraph-io/badger | 225  | 10 | 185 |
| Javascript | disnet/contracts.js | 289 | 10 | 249 |
| PHP | Payum/Payum | 277 | 10 | 237 |
| Ruby | chef/omnibus | 199 | 10 | 159 |

The code for generating training data and the generated training data are located in the folders 'code' and 'data', respectively.
