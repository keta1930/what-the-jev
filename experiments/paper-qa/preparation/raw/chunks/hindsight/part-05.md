# Appendix

## Table of Contents

A System Prompts 23  
A.1 Fact Extraction Prompt (TEMPR) 23  
A.2 Opinion Formation Prompt (CARA) 24  
A.3 Observation Generation Prompt (TEMPR) 24  
A.4 LongMemEval Judge Prompts 25  
A.5 Structured Output Schemas 27

## A SYSTEM PROMPTS

This appendix provides the complete prompt templates used in the HINDSIGHT framework for fact extraction, opinion formation, observation generation, and evaluation.

### A.1 FACT EXTRACTION PROMPT (TEMPR)

The fact extraction prompt is used to convert conversational transcripts into structured narrative facts with temporal ranges, entities, and causal relationships.

Fact Extraction System Prompt

User Prompt:

Extract facts from text into structured format with FOUR required dimensions - BE EXTREMELY DETAILED.

FACT FORMAT - ALL FIVE DIMENSIONS REQUIRED - MAXIMUM VERBOSITY

1) what: WHAT happened - COMPLETE description with ALL specifics (objects, actions, quantities, details)

2) when: WHEN it happened - ALWAYS include temporal info with DAY OF WEEK

• Always include the day name: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday

• Format: “day\_name, month day, year” (e.g., “Saturday, June 9, 2024”)

3) where: WHERE it happened or is about - SPECIFIC locations, places, areas, regions (if applicable)

4) who: WHO is involved - ALL people/entities with FULL relationships and background

5) why: WHY it matters - ALL emotions, preferences, motivations, significance, nuance

• For assistant facts: MUST include what the user asked/requested that triggered this!

Plus: fact\_type, fact\_kind, entities, occurred\_start/end (for structured dates), where (structured location)

VERBOSITY REQUIREMENT: Include EVERY detail mentioned. More detail is ALWAYS better than less.

COREFERENCE RESOLUTION (CRITICAL)

When text uses BOTH a generic relation AND a name for the same person, LINK THEM! Example:

• Input: “My roommate Emily got married. She works at Google.”

• Correct: “Emily (the user’s roommate) got married. She works at Google.”

• Wrong: Treating “my roommate” and “Emily” as separate entities

### A.2 OPINION FORMATION PROMPT (CARA)

The opinion formation prompt is used during the reflect operation to extract and form new opinions from generated responses.

Opinion Formation System Prompt

User Prompt:

Extract any NEW opinions or perspectives from the answer below and rewrite them in FIRST-PERSON as if YOU are stating the opinion directly.

ORIGINAL QUESTION:

{query}

ANSWER PROVIDED:

{text}

Your task: Find opinions in the answer and rewrite them AS IF YOU ARE THE ONE SAYING THEM. An opinion is a judgment, viewpoint, or conclusion that goes beyond just stating facts.

IMPORTANT: Do NOT extract statements like:

• “I don’t have enough information”

• “The facts don’t contain information about X”

• “I cannot answer because...”

ONLY extract actual opinions about substantive topics.

CRITICAL FORMAT REQUIREMENTS:

1) ALWAYS start with first-person phrases: “I think...”, “I believe...”, “In my view...”, “I’ve come to believe...”, “Previously I thought... but now...”

2) NEVER use third-person: Do NOT say “The speaker thinks...” or “They believe...” - always use “I” 3) Include the reasoning naturally within the statement

4) Provide a confidence score (0.0 to 1.0)

CORRECT Examples (First-Person):

• “I think Alice is more reliable because she consistently delivers on time and writes clean code”

• “Previously I thought all engineers were equal, but now I feel that experience and track record really matter”

• “I believe reliability is best measured by consistent output over time”

• “I’ve come to believe that track records are more important than potential”

### A.3 OBSERVATION GENERATION PROMPT (TEMPR)

The observation generation prompt synthesizes factual observations about entities from multiple underlying facts without behavioral profile influence.

Observation Generation System Prompt

System Message:

You are an objective observer synthesizing facts about an entity. Generate clear, factual observations without opinions or behavioral profile influence. Be concise and accurate.

User Prompt:

Based on the following facts about “{entity\_name}”, generate a list of key observations.

FACTS ABOUT {ENTITY\_NAME}:

{facts\_text}

Your task: Synthesize the facts into clear, objective observations about {entity\_name}.

GUIDELINES:

1. Each observation should be a factual statement about {entity\_name}

2. Combine related facts into single observations where appropriate

3. Be objective - do not add opinions, judgments, or interpretations

4. Focus on what we KNOW about {entity\_name}, not what we assume

5. Include observations about: identity, characteristics, roles, relationships, activities

6. Write in third person (e.g., “John is...” not “I think John is...”)

7. If there are conflicting facts, note the most recent or most supported one

EXAMPLES of good observations:

• “John works at Google as a software engineer”

• “John is detail-oriented and methodical in his approach”

• “John collaborates frequently with Sarah on the AI project”

• “John joined the company in 2023”

EXAMPLES of bad observations (avoid these):

• “John seems like a good person” (opinion/judgment)

• “John probably likes his job” (assumption)

• “I believe John is reliable” (first-person opinion)

Generate 3-7 observations based on the available facts. If there are very few facts, generate fewer observations.

### A.4 LONGMEMEVAL JUDGE PROMPTS

The judge prompts are used in the LongMemEval benchmark to evaluate whether model responses are correct. Different prompts are used for different question types.

#### A.4.1 SINGLE-SESSION AND MULTI-SESSION QUESTIONS

Judge Prompt: Single/Multi-Session Questions

I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. Otherwise, answer no. If the response is equivalent to the correct answer or contains all the intermediate steps to get the correct answer, you should also answer yes. If the response only contains a subset of the information required by the answer, answer no.

Question: {question}

Correct Answer: {answer}

Model Response: {response}

Is the model response correct?

You may provide reasoning, but you MUST end your response with your final answer in the format:

\boxed{yes} or \boxed{no}

#### A.4.2 TEMPORAL REASONING QUESTIONS

Judge Prompt: Temporal Reasoning Questions

```txt
I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. Otherwise, answer no. If the response is equivalent to the correct answer or contains all the intermediate steps to get the correct answer, you should also answer yes. If the response only contains a subset of the information required by the answer, answer no. In addition, do not penalize off-by-one errors for the number of days. If the question asks for the number of days/weeks/months, etc., and the model makes off-by-one errors (e.g., predicting 19 days when the answer is 18), the model's response is still correct.

Question: {question}
Correct Answer: {answer}
Model Response: {response}

Is the model response correct?
You may provide reasoning, but you MUST end your response with your final answer in the format: \boxed{yes} or \boxed{no}
```

#### A.4.3 KNOWLEDGE UPDATE QUESTIONS

Judge Prompt: Knowledge Update Questions

```txt
I will give you a question, a correct answer, and a response from a model. Please answer yes if the response contains the correct answer. Otherwise, answer no. If the response contains some previous information along with an updated answer, the response should be considered as correct as long as the updated answer is the required answer.

Question: {question}
Correct Answer: {answer}
Model Response: {response}

Is the model response correct?
You may provide reasoning, but you MUST end your response with your final answer in the format: \boxed{yes} or \boxed{no}
```

#### A.4.4 PREFERENCE QUESTIONS

Judge Prompt: Preference Questions

```txt
I will give you a question, a rubric for desired personalized response, and a response from a model. Please answer yes if the response satisfies the desired response. Otherwise, answer no. The model does not need to reflect all the points in the rubric. The response is correct as long as it recalls and utilizes the user's personal information correctly.

Question: {question}
Rubric: {answer}
Model Response: {response}

Is the model response correct?
You may provide reasoning, but you MUST end your response with your final answer in the format: \boxed{yes} or \boxed{no}
```

```latex
Question: {question}
Explanation: {answer}
Model Response: {response}
Does the model correctly identify the question as unanswerable?
You may provide reasoning, but you MUST end your response with your final answer in the format:
\boxed{yes} or \boxed{no}
```

#### A.4.5 ABSTENTION QUESTIONS

Judge Prompt: Abstention Questions

I will give you an unanswerable question, an explanation, and a response from a model. Please answer yes if the model correctly identifies the question as unanswerable. The model could say that the information is incomplete, or some other information is given but the asked information is not.

### A.5 STRUCTURED OUTPUT SCHEMAS

Hindsight uses Pydantic models to enforce structured output from LLM calls. This ensures reliable parsing and validation of extracted information.

#### A.5.1 FACT SCHEMA

Fact Extraction Schema (Pydantic)

```python
class ExtractedFact(BaseModel):
    # Five required dimensions
    what: str  # Complete description with ALL specifics
    when: str  # Temporal info with day of week
    where: str  # Specific locations, places, areas
    who: str  # All people/entities with relationships
    why: str  # Emotions, preferences, motivations

    # Classification
    fact_type: Literal["world", "experience", "opinion"]

    # Optional structured fields
    occurred_start: Optional[str] = None
    occurred_end: Optional[str] = None
    mentioned_at: Optional[str] = None
    entities: Optional[List[Entity]] = None
    causal_relations: Optional[List[CausalRelation]] = None

class Entity(BaseModel):
    text: str  # Named entity as it appears

class CausalRelation(BaseModel):
    target_fact_index: int  # Index of related fact
    relation_type: Literal[
    "causes", "caused_by", "enables", "prevents"
    ]
    strength: float  # 0.0 to 1.0
```

#### A.5.2 OPINION SCHEMA

Opinion Extraction Schema (Pydantic)

```python
class Opinion(BaseModel):
    opinion: str # First-person opinion statement
    confidence: float # 0.0 to 1.0
    reasoning: str # Why this opinion was formed
```

```python
class OpinionExtractionResponse(BaseModel):
    opinions: List[Opinion] = Field(
    default_factory=list,
    description="List of opinions extracted from text"
)
```

#### A.5.3 OBSERVATION SCHEMA

Observation Extraction Schema (Pydantic)

```python
class Observation(BaseModel):
    observation: str  # Factual statement about entity
class ObservationExtractionResponse(BaseModel):
    observations: List[Observation] = Field(
    default_factory=list,
    description="List of observations about entity"
)
```
