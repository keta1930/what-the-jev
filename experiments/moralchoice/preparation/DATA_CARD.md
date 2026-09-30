---
pretty_name: MoralChoice
license: cc-by-4.0
language:
- en
size_categories:
- 1K<n<10K
---

# Dataset Card for MoralChoice

- **Homepage:** Coming Soon
- **Paper:** Coming soon
- **Repository:**  [https://github.com/ninodimontalcino/moralchoice](https://github.com/ninodimontalcino/moralchoice)
- **Point of Contact:** [Nino Scherrer & Claudia Shi](mailto:nino.scherrer@gmail.com,claudia.j.shi@gmail.com?subject=[MoralChoice])


### Dataset Summary

*MoralChoice* is a survey dataset to evaluate the moral beliefs encoded in LLMs. The dataset consists of:
- **Survey Question Meta-Data:** 1767 hypothetical moral scenarios where each scenario consists of a description / context and two potential actions
  - **Low-Ambiguity Moral Scenarios (687 scenarios):** One action is clearly preferred over the other.
  - **High-Ambiguity Moral Scenarios (680 scenarios):**  Neither action is clearly preferred
- **Survey Question Templates:** 3 hand-curated question templates
- **Survey Responses:** Outputs from 28 open- and closed-sourced LLMs

A statistical workflow for analyzing the survey responses can be found in the corresponding [paper]().

🚧 **Important**: 🚧
- *Moral scenarios* and *question templates*  are already available.
- *Survey responses* will be uploaded shortly!

### Languages

*MoralChoice* is only available in English. 

## Dataset Structure

### Data Fields

#### Moral Scenarios (Survey Question Meta-Data)
``` 
- scenario_id       unique scenario identifier
- ambiguity         level of ambiguity (low or high)
- generation_type   generation type (hand-written or generated)
- context           scenario description / contextualization
- action 1          description of a potential action
- action 2          description of a potential action
- a1_{rule}         {rule} violation label of action 1
- a2_{rule}         {rule} violation label of action 2
```

#### Survey Question Templates
```
- name                 name of question template (e.g., ab, repeat, compare)
- question_header      question instruction header text
- question             question template with placeholders
```

#### Survey Responses
``` 
- scenario_id           unique scenario identifier
- model_id              model identifier (e.g., openai/gpt-4)
- question_type         question type (ab: A or B?, repeat: Repeat the preferred answer, compare: Do you prefer A over B? )
- question_ordering     question ordering label (0: default order, 1: flipped order)
- question_header       question instruction header text
- question_text         question text
- answer_raw            raw answer of model
- decision              semantic answer of model (e.g., action1, action2, refusal, invalid)
- eval_technique        evaluation technique used
- eval_top_p            evaluation parameter - top_p
- eval_temperature      evaluation parameter - temperature
- timestamp             timestamp of model access
```

## Dataset Creation

### Generation of Moral Scenarios

The construction of *MoralChoice* follows a three-step procedure:

- **Scenario Generation:** We generate seperately low- and high-ambiguity scenarios (i.e., the triple of scenario context, action 1 and action 2) guided by the 10 rules of Gert's common morality framework.
  - **Low-Ambiguity Scenarios:** Zero-Shot Prompting Setup based on OpenAI's gpt-4
  - **High-Ambiguity Scenarios:** Stochastic Few-Shot Prompting Setup based on OpenAI's text-davinci-003 using a a set of 100 hand-written scenarios
- **Scenario Curation:** We check the validity and grammar of each generated scenario manually and remove invalid scenarios. In addition, we assess lexical similarity between the generated scenarios and remove duplicates and overly-similar scenarios.
- **Auxiliarly Label Aquisition:** We acquire auxiliary rule violation labels through SurgeAI for every scenario.

For detailed information, we refer to the corresponding paper.

## Collection of LLM responses
Across all models, we employ **temperature-based sampling** with `top-p=1.0`and `temperature=1.0`. For every specific question form (unique combination of scenario, question template, answer option ordering), we collect multiple samples (5 for low-ambiguity scenarios and 10 for high-ambiguity scenarios). The raw sequence of token outputs were mapped to semantic action (see the corresponding paper for exact details). 

### Annotations
To acquire high-quality annotations, we employ experienced annotators sourced through the data-labeling company [Surge AI](https://www.surgehq.ai/).

## Considerations for Using the Data

- Limited Diversity in Scenarios (professions, contexts)
- Limited Diversity in Question-Templates
- Limited to English

### Dataset Curators

- Nino Scherrer ([Website](https://ninodimontalcino.github.io/), [Mail](mailto:nino.scherrer@gmail.com?subject=[MoralChoice]))
- Claudia Shi ([Website](https://www.claudiajshi.com/), [Mail](mailto:nino.scherrer@gmail.com?subject=[MoralChoice]))


### Citation

```
@misc{scherrer2023moralchoice,
      title={Evaluating the Moral Beliefs Encoded in LLMs}, 
      author={Scherrer, Nino and Shi, Claudia, and Feder, Amir and Blei, David},
      year={2023},
      journal={arXiv:}
}
```