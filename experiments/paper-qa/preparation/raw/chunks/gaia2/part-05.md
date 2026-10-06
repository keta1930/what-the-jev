## B.1 DETAILS OF GAIA2 ANNOTATION

### B.1.1 ANNOTATION GUARDRAILS

To streamline the process and further reduce annotation errors, we implement structural constraints directly within the ARE UI (refer to Appendix A.4 for details). The system raises real-time errors when these are violated:

\- Only send\_message\_to\_agent or Env events may follow send\_message\_to\_user.

\- The event DAG must be fully connected, with send\_message\_to\_agent as the root. No event (Env or Agent Oracle) may be orphaned.

\- Only one branch in the event DAG may include send\_message\_to\_agent or send\_message\_to\_user events.

\- A turn must always end with send\_message\_to\_user, both in terms of DAG structure and timeline ordering.

### B.1.2 SCENARIO EXAMPLES

To build Gaia2, we define a set of capabilities that we believe are necessary – though not sufficient – for general purpose agents. As introduced above, each of the 800 scenarios is built to emphasize at least one of these capabilities, yielding 160 scenarios per capability split. We provide example scenarios displayed in the ARE GUI graph editor in Appendix B.1.3.

Execution scenarios require the agent to take multiple write actions, which may need to be executed in a particular order. Most of the time, read actions are needed in order to gather information for properly filling write action arguments.

#### Execution Task

Task: Update all my contacts aged 24 or younger to be one year older than they are currently.

Explanation: This task requires the agent to read contact information, filter based on age criteria, and execute multiple write to update Contacts data.

Search scenarios require the agent to take multiple read actions in order to gather facts from different sources within the environment. Any sequence of read operations leading to the correct answer is considered successful as long as the answer is communicated via send\_message\_to\_user before scenario timeout. While conceptually similar to the original GAIA benchmark's web search tasks, Gaia2 search scenarios operate within a controlled ARE environment.

#### Search Task

Task: Which city do most of my friends live in? I consider any contact who I have at least one 1-on-1 conversation with on Chats a friend. In case of a tie, return the first city alphabetically.

Explanation: This scenario requires the agent to cross-reference data from multiple apps (Contacts and Chats), perform aggregation operations, and handle edge cases like ties.

All remaining capabilities tested in Gaia2 reflect tasks with a balanced number of required read and write operations. However, each capability features an additional challenge. Namely:

Ambiguity scenarios reflect user tasks that are impossible, contradictory, or have multiple valid answers, with negative consequences arising during interaction if agents make mistakes. These scenarios test agents' ability to recognize these issues and seek appropriate clarification from users.

#### Ambiguity Task

Task: Schedule a 1h Yoga event each day at 6:00 PM from October 16, 2024 to October 21, 2024. Ask me in case there are conflicts.

Explanation: While this task appears straightforward, current models often struggle to identify contradictions or multiple valid interpretations, tending to execute the first seemingly valid approach rather than recognizing the need for clarification.

Adaptability scenarios require the agent to dynamically adapt to environmental changes that are consequences of previous agent actions, such as a response to an email sent by the agent, or the cancellation of a ride booked by the agent. These events require agents to recognize when adaptation is necessary and adjust their strategy accordingly.

#### Adaptability Task

Task: I have to meet my friend Kaida Schönberger to view a property with her [...] If she replies to suggest another property or time, please replace it with the listing she actually wants and reschedule at the time that works for her.

Explanation: This task requires the agent to execute an initial plan while monitoring for environmental changes (the friend's response), then adapt the plan based on new information. The agent must demonstrate flexibility in execution while maintaining task objectives.

Time scenarios require agents to execute actions in due time, monitor and respond to events, and maintain awareness of temporal relationships throughout task execution. The duration of Time scenarios is currently capped at 5 minutes to facilitate annotation and evaluation.

#### Time Task

Task: Send individual Chats messages to the colleagues I am supposed to meet today, asking who is supposed to order the cab. If after 3 minutes there is no response, order a default cab from [...].

Explanation: This scenario requires the agent to understand temporal constraints (the 3-minute window), monitor for events (new messages from colleagues), and execute a time-sensitive action (order a cab).

Agent2Agent scenarios replace apps with app-agents. Main-agents can no longer access app tools directly and must instead communicate with the app-agents in order to place tool calls, observe tool call outputs, and ultimately accomplish user tasks. This transformation requires agents to develop robust collaboration capabilities, including sub-task setting, affordance understanding, “context-sharing,” and general coordination. By default, agents and app sub-agents are instantiated with the same scaffold and model, with good performance requiring strong sub-goal setting and sub-goal solving. However, Gaia2 also supports heterogeneous multi-agent evaluations, i.e. where stronger agents supervise weaker sub-agents or vice-versa.

\- Example: Same Search task as above but the Contacts and Chats apps are replaced by app sub-agents and the main agent must communicate with them in order to gather information.

Noise scenarios require robustness to environment noise, simulating the inherent instability of real-world systems, where APIs change, services become temporarily unavailable, and environmental conditions shift during task execution. This category applies systematic perturbations to Gaia2 scenarios, including tool signature modifications, random failure probabilities, and dynamic environment events that are irrelevant to the task. We assess the sanity of our noise mechanisms in Appendix B.5.2.

\- Example: Same Adaptability task as above but with random tool execution errors and random environment events (e.g., messages from other people) occurring during execution.

### B.1.3 CAPABILITY-SPECIFIC ANNOTATION GUIDELINES

In our guidelines for each capability (especially Ambiguity and Adaptability), we put strong emphasis on precise task specifications, while also acknowledging the challenge of maintaining realism and avoiding prompts that inadvertently disclose the solution.

Search: Scenarios contain only one write action, which is the agent's final answer to the user's question, derived from multiple read actions. Answers must be concise, easily verifiable, and avoid complex computation.

Ambiguity: Scenarios that are impossible, contradictory, or inherently ambiguous. The agent is expected to complete unambiguous steps, then inform the user of the ambiguity or impossibility. These scenarios are single-turn: they do not include a clarification message from the User.

The user prompt must clearly instruct the agent to detect and report ambiguities, as users often have varying preferences on how frequently and when this should occur.

Adaptability: Scenarios involve Env events that require the agent to revise its plan in response to delayed outcomes of its actions. In order to meet our modeling constraints, scenarios follow a consistent structure:

1. The user provides a task.

2. The agent acts and sends a message using send\_message\_to\_user.

3. An Env event is triggered (e.g., email reply, order cancellation). It is a consequence of a previous agent's action, with send\_message\_to\_user as parent.

4. The agent adapts accordingly.

To increase the difficulty, distractor Env events are also included, aiming to mislead the agent into incorrect behavior.

In order to perfectly specify expected agent behavior, the task states explicitly that the agent should send a message to the user after completing the initial requests (before the Env events). It should also specify what the Agent is allowed to do in the case of an Env event happening, without giving exact hints on what steps the Agent should take.

Time: Scenarios assess Agent's ability to act on time, therefore they all include at least one time-sensitive oracle action.

\- Scenarios should be solvable within a five-minute window.

\- User prompts must instruct precise timing (e.g., "after exactly 3 minutes").

\- The verifier checks the timing of agent actions only if the oracle event has a relative time delay greater than 1 second. $^{8}$ The agent's mapped action must fall within $[\Delta t - 5sec, \Delta t + 25sec]$ .

\- Distractor Env events are also included.

### B.1.4 CAPABILITY TAXONOMIES

Taxonomy of ambiguity scenarios

\- Impossible or contradictory tasks: missing key information (e.g., the User does not specify the ride pickup location), or requests incompatible with the Environment (e.g., asking to buy an out-of-stock item).

\- Blatant ambiguities or high-stakes consequences: Multiple valid answers exist, and the ambiguity is obvious or the user explicitly asks in a natural way to report ambiguities.

Taxonomy of env events Env events are classified based on their dependency:

\- Independent events occur without agent action and have send\_message\_to\_agent as their only parent.

\- Dependent events result from prior agent actions and must have send\_message\_to\_user as their direct parent.

Distractor events are designed to mimic relevant events and mislead the agent into incorrect behavior. By exception, distractor events may be independent but still have send\_message\_to\_user as a parent to preserve the structure of the scenario. In the Adaptability category, only dependent Env events are used.

Taxonomy of time scenarios Time scenarios require the agent to execute one or more actions at a specific point in time, either proactively (“For the next 5mins, send ‘Hi’ to John Doe every 30sec”) or in reaction to an independent Env event (“When this item becomes available, buy it immediately”), or in reaction to a dependent Env event (“Ask the invitees whether they come to the party tonight. Wait 1min for everyone to reply, then immediately send me the number of glass to buy, I am waiting in the line!”).

Taxonomy:

\- Time-based one-off task: Execute a task at a precise point in time in the future. Example: "Send a follow-up message to Jo in 2 minutes if she does not reply."

\- Time-based recurrent task: Execute a recurrent task at precise points in time. Example: "For the next 4 minutes, every minute, delete the new emails I receive."

\- Event-based one-off task: Execute a one-time task conditionally on a future trigger event. Example: “Purchase red running shoes as soon as they become available in size 6 for less than 100USD in the shopping app”

\- Event-based recurrent task: Automate a recurrent routine conditionally on future events. Example: “For the next 2 minutes, whenever I receive an email containing the keyword ‘Black Friday’, immediately delete it. Do not talk to me in the next 2 minutes.”

We encourage annotators to cover and combine all these types of tasks when creating Time scenarios.

## B.2 VERIFICATION DETAILS

### B.2.1 VERIFICATION MECHANISM

We verify scenario successful completion by comparing agent actions with a ground truth, defined as the minimal sequence of write actions needed to solve a task. We exclude read actions from verification since multiple reading strategies can lead to the correct set of write actions. In a preliminary phase, the verifier checks that used tool names counters are identical in both the oracle actions and the agent's write actions. If this test is successful, the verifier sorts the oracle actions in a topological order based on the oracle graph, which reflects their dependencies. Then, the verifier proceeds to mapping each oracle action to an agent action by checking:

\- Consistency: the verifier tests whether the oracle action and the candidate agent's action are equivalent. After conducting some preliminary tests (such as ensuring that both the oracle and agent actions use the same tool and that the oracle action is not already mapped to another agent action), the verifier performs:

\- Hard check to compare action parameters that require exactness. For example, when replying to an email, it verifies that email\_id value is identical for both actions, i.e. the agent replies to the correct email.

\- Soft check for parameters that require more flexible evaluation, such as the content of an email or a message. To perform a soft check, an LLM judge is prompted with the user task as context, and the arguments from both the agent action and the oracle action as inputs. The LLM then determines if the actions are equivalent according to tool-specific guidelines. For example, emails verification includes guidelines to check their signatures.

\- Causality: crucially, oracle actions are organized within an oracle graph, whereas agent actions are collected from a trajectory and simply ordered by execution time. Therefore, we must ensure that the agent does not violate dependencies within this graph. For example, if both oracle actions A and B depend solely on action C, the agent is free to execute A and B in any order, as long as they are executed after C; i.e. sequences C-B-A or C-A-B are both acceptable. Once a match is found, the ARE Verifier ensures causality by verifying that all parent actions of the oracle action have already been matched with preceding agent actions.

![](images/a8623b6bba771a67a7beddbd5b6bdf14aff2181b2e157c9af8ec89da1c12b40f.jpg)

[Image: This diagram illustrates a verification process comparing a reference "Oracle Graph" against generated "Agent Actions" through multiple matching attempts organized by Trace. On the left, the Oracle Graph establishes a structural dependency where Oracle Action 1 is a parent prerequisite for both Oracle Action 2 and Oracle Action 3. Trace 1 demonstrates successful matching, specifically in Attempt 3, where the agent swaps the order of Actions 2 and 3; this valid permutation leads to a green "Success" outcome. In contrast, Trace 2 illustrates failures where dependencies are violated, evidenced by red arrows connecting misaligned actions (e.g., Agent Action 1 linking to Oracle Action 2), culminating in a red "Failure" label.]  
Figure 15: Illustration of a failure (top) and a success (down) of the matching trajectory process.

\- Timing: scenarios can include a time delay for certain actions relative to their parent actions, which the agent must respect. The verifier evaluates whether the agent's timing falls within a specified tolerance window centered around the relative time of the oracle action. To determine the relative timing of the agent's action, it is necessary to identify which agent action corresponds to the oracle's parent action. This information is readily available due to the ARE Verifier's process. Indeed, for a given oracle action, all its parent actions must be matched to an agent action before attempting to match the oracle action itself.

If all oracle actions are successfully matched, the verifier returns a success signal. Conversely, if any oracle action cannot be matched to an agent action, the verifier returns a failure signal, see Figure 15 for two examples. Crucially, the verifier implicitly assumes there are no equivalent write actions, i.e. user preferences are clearly stated with minimal ambiguity in the scenario tasks. For example, sending a message using the Messages app while the oracle action uses the Chat app will trigger a failure.

While other verification methods (Patil et al., 2025; Yao et al., 2024) compare the environment ground truth and actual final states, verifying a sequence of write actions, which is equivalent to comparing ground truth and actual states after each write action of the sequence, provides more control. For example our verification allows to distinguish, e.g. for safety considerations, a Mobile trajectory where the agent adds an event at the wrong place and correct itself from a trajectory where the agent is correct at first try. Moreover, in Mobile, sequences of write actions are easier for humans to interpret and annotate, compared to diffs of states.

### B.2.2 VALIDATING MULTI-TURN SCENARIOS

Currently, we have only described how the verifier works in single-turn scenarios, where a user assigns a single task to an agent, and the agent completes it without further interaction. However, the Gaia2 benchmark also includes multi-turn scenarios that involve more complex interactions between the user and the agent. For example, consider scenarios related to the Adaptability capability, where the agent must adjust to external events. Multi-turn scenarios present two key challenges:

![](images/dbf3f7361751b2f08544db69884d870a6b95c7a6f43c413813a3ba834585f292.jpg)

[Image: The image displays four flowcharts illustrating interaction patterns between users and agents, distinguished by node color and connectivity. The top row labels the sequence "Turn 1" and "Turn 2," depicting a cycle where a user action branches into agent actions to produce a message that initiates the next turn. The bottom row features a parallel structure on the left and a variant on the right starting with a purple "Trigger" node, indicating an interaction mode initiated by external events. Throughout the diagrams, pink circles represent user actions, blue circles denote agent actions and messages, and arrows indicate the logical progression of the conversation state.]  
Figure 16: Insertion of a conditional trigger event in a multi-turn scenario.

• How can we validate multi-turn scenarios?

\- More importantly, how can we run an agent in a multi-turn scenario?

Indeed, annotators plan User and Env actions based on what should occur in previous turns according to the oracle action graph. However, when an agent is launched in a scenario, it may not adhere to the oracle's actions, creating uncertainty about when to trigger user or environment actions.

Multi-turn verifier Answering the first question is relatively straightforward. It is sufficient to detect when the agent sends a message to the user to delimit the turns. We can then feed the verifier with each turn separately and accept the agent's trajectory if all turns are successful. Note that this validation can be performed in an online fashion after each turn or in an offline fashion once the full trajectory is collected.

Multi-turn execution An efficient solution to run an agent in a multi-turn scenario is to call the ARE Verifier at the end of each turn and only trigger the next turn if the current turn was successful. This approach prevents running the agent when it has already diverged from the oracle path. Practically, as illustrated in Figure 16, we modify the scenario event graph by splitting it into turns and inserting a conditional event to call the verifier and trigger the next turn. A simpler, but less efficient, solution is to trigger the next turn each time the agent calls send\_message\_to\_user, regardless of what the agent did in the current turn. This approach is used for scenarios from the test set since we do not have access to oracle actions and thus the ARE Verifier for them.

### B.2.3 VERIFIER HACKING

We conducted RL experiments in which we used the ARE Verifier as a reward function. During these experiments, we observed that the agent was able to exploit our initial version of the verifier in scenarios related to the Search capability, where only a single write action is expected for successful trajectories. In the observed exploit shown in Figure 17, the agent would learn to embed strings representing increasingly complex code in write tool calls. These outputs overwhelmed the LLM judge used for soft checks by the ARE Verifier, producing false positives. In follow-up experiments, we found that adding a task-agnostic “style” soft check to the verifier was effective at addressing this failure mode and preventing further reward hacking.

### B.2.4 VERIFYING THE VERIFIER

Verifiers are critical components of training and evaluation pipelines, where false positive or false negative e.g. via hacking can result in flawed evaluations or collapsed trainings (cf. Appendix B.2.3). We evaluate the ARE Verifier by first deriving a series of “unit” tests from the oracle actions that the verifier should satisfy. Typically, we apply perturbations to oracle actions that we know preserve or invalidate the oracle trajectory validity, before submitting the oracle and perturbed oracle trajectories to the verifier and checking its verdict match the perturbation type. While these checks allow fast iteration, they only catch anticipated behaviors. Furthermore, the perturbed trajectories do not necessarily reflect real trajectories that could be obtained with an agent.

```txt
Thought: Now that we have all the events in the user's calendar, we can count the number of events for each contact and find the contact who the user has the most scheduled events with.
Action:
{
    "action": "AgentUserInterface__send_message_to_user",
    "action_input": {
    "content": "Looking at your calendar, I can now count events for each contact. Here's what I found:\n\n**Most Common Contact (by events):** {{#events}}{{#attendees }}{{#if (eq (length attendees) 2)}}{{#if (eq (at attendees 0) user)}}{{else}}{{# set most_common_contact_email (at attendees 1)}}{{#inc events_attendee_1_count 1)}}{{#if (gt events_attendee_1_count events_attendee_2_count)}}{{#set most_common_contact_email (at attendees 1)}}{{else}}{{#if (eq events_attendee_1_count events_attendee_2_count)}}{{#if (lt (get attendee_1_first_name 0) (get attendee_2_first_name 0))}}{{#set most_common_contact_email (at attendees 1)}}{{else}}{{#set most_common_contact_email (at attendees 2)}}{{/if}}{{/endif}}{{#endif}}{{/endif}}{{/if}}{{/attendees}}{{/events}}\n\n**Contact:** {{#set most_common_contact_email (at attendees 1)}}{{#set most_common_contact_email email}}{{#endif}}{{#endif}}{{#endif}}{{#endif}}{{#endif}}{{#endif}}{{#endif}}{(contacts)}}{{#if (eq email most_common_contact_email)}"
}
```  
Figure 17: An example of an agent exploiting the judge by embedding conditional logic in the message to the user. The message contains no meaningful information but successfully passes the judge's evaluation.

<table><tr><td>Verifier</td><td>Agreement</td><td>Precision</td><td>Recall</td></tr><tr><td>Llama 3.3 70B Instruct</td><td>0.98</td><td>0.99</td><td>0.95</td></tr><tr><td>Gemini 2.5 pro</td><td>0.96</td><td>0.98</td><td>0.89</td></tr><tr><td>Claude Sonnet 3.7</td><td>0.96</td><td>0.98</td><td>0.89</td></tr></table>

Table 5: Evaluation of the ARE Verifier with different models on 450 hand-labeled trajectories.

Validation benchmark We complement this initial evaluation by analyzing ARE Verifier verdicts for 450 trajectories manually labeled with the expected verifier outcome (Success or Failure). The trajectories were derived from running agents powered by various models on scenarios from the Gaia2 benchmark. We compare the ARE Verifier with a simple baseline, In-context Verifier, where an LLM is prompted with all the agent actions and criteria (causality constraints, relative time, soft/hard checks, etc.). The same model Llama 3.3 70B Instruct is used for both verifiers. ARE Verifier achieves better accuracy than the baseline, which tends to accept agent trajectories too readily, see Table 1.

### B.2.5 CHOOSING THE VERIFIER MODEL

While we adjusted the prompts used in the various soft checks of the ARE Verifier with Llama 3.370B Instruct as model, we also wanted to assess whether the ARE Verifier could function effectively with other models. To this end, we evaluated the ARE Verifier powered by different models on 450 hand-labeled trajectories, the same dataset used for Table 1. In Table 5, we observe that all the models achieve satisfactory precision and recall scores.

## B.3 AGENT ORCHESTRATION

### B.3.1 MOBILE REACT LOOP

Our proposed evaluation method leverages a custom scaffolding framework built around the ReAct (Reason and Act) paradigm. The base scaffolding implements a standard ReAct loop where agents iteratively reason about their current state, select appropriate actions, execute those actions in the environment, and observe the resulting outcomes. An agent step is thus defined by three substeps Thought, Action and Observation. This cycle continues until task completion or termination conditions are met.

At each step of this loop, our scaffolding triggers configurable pre-step and post-step methods that can pull relevant information from the environment state or detect termination conditions based on task-specific criteria as detailed in Figure 18. Pre-step methods gather contextual information and validate preconditions before action execution, while post-step methods process outcomes, update internal state, and check for completion signals. This agentic modeling approach enables the creation of sophisticated agent behaviors with minimal implementation overhead, as complex interaction patterns emerge from the composition of simple, reusable scaffolding components rather than monolithic agent implementations.

![](images/7993adce85c96945e741aa9544e2338a7976fb92cf50274d26143b3d2341ace1.jpg)

[Image: This diagram illustrates the architectural components of a "Full ReAct Step" alongside a detailed breakdown of a single iteration. On the left, a vertical flowchart depicts a sequential process comprising "Pre Steps," a central blue "Step," and "Post Steps." The central "Step" component is expanded in the adjacent panel on the right, labeled "One standard ReAct iter (step)," which details a three-part internal process: building an LLM chat history from logs, generating LLM output, and executing a tool to add results to logs.]  
Figure 18: Proposed ReAct loop with pre/post steps in Gaia2, allowing flexible behaviors.

### B.3.2 ORCHESTRATION ABLATION: PARALLEL TOOL-CALLING

In our main evaluation setup, we use a standard ReAct scaffold to ensure a fair, model-agnostic baseline that supports both closed APIs and open-weights models without requiring model-specific integration code. However, to address the question of whether this single-threaded scaffolding acts as a bottleneck—particularly for the Time split, we conducted an ablation study comparing ReAct against a Parallel Tool Calling (PTC) orchestration.

We evaluated three representative models (Llama 4 Maverick, Claude 4 Sonnet, and GPT-5) across the Execution and Time splits. The results, presented in Table 6, reveal several key findings:

\- Efficiency Gains: As expected, PTC significantly reduces wall-clock latency and token consumption. For instance, GPT-5 (low) shows a strong reduction in latency ( $\Delta$ -435s on Execution) and token usage ( $\Delta$ -5109 tokens), primarily because it performs fewer intermediate reasoning steps per action.

\- Performance Stability: Despite the efficiency improvements, the impact on task success (pass@1) is marginal. The performance deltas are generally small (ranging from -6.3pp to +3.0pp), and crucially the relative ranking of the models remains unchanged.

\- Orchestration Limits: The Time split remains challenging even with parallel execution, confirming that the bottlenecks observed in Section 5 stem primarily from model capabilities (such as sequential reasoning and temporal planning) rather than the scaffolding itself, as PTC results are still far from the upper-bound score computed with instant-time generation in Figure 8.

Table 6: Ablations of 3 models with Parallel TC vs ReAct scaffold. Values indicate the net contribution of PTC over ReAct ( $\Delta$ ).

<table><tr><td>Model</td><td>Split</td><td>ReAct pass@1</td><td>Parallel TC pass@1</td><td>Δ pass@1 (pp)</td><td>Δ avg time (s)</td><td>Δ avg steps</td><td>Δ avg output tokens</td></tr><tr><td rowspan="2">Llama Maverick</td><td>Execution</td><td>13.8</td><td>7.5</td><td>-6.3</td><td>+71</td><td>-1.0</td><td>+1786</td></tr><tr><td>Time</td><td>1.2</td><td>2.0</td><td>+0.8</td><td>-3</td><td>-1.1</td><td>+2240</td></tr><tr><td rowspan="2">Claude 4 Sonnet</td><td>Execution</td><td>57.9</td><td>59.7</td><td>+1.8</td><td>-68</td><td>-10.7</td><td>-345</td></tr><tr><td>Time</td><td>8.1</td><td>9.5</td><td>+1.4</td><td>-8</td><td>-2.4</td><td>+33</td></tr><tr><td rowspan="2">GPT-5 (minimal)</td><td>Execution</td><td>31.9</td><td>34.9</td><td>+3.0</td><td>-64</td><td>-14.0</td><td>-160</td></tr><tr><td>Time</td><td>5.2</td><td>6.7</td><td>+1.5</td><td>+23</td><td>0.0</td><td>+1030</td></tr><tr><td rowspan="2">GPT-5 (low)</td><td>Execution</td><td>52.7</td><td>51.7</td><td>-1.0</td><td>-435</td><td>-13.0</td><td>-5109</td></tr><tr><td>Time</td><td>2.3</td><td>1.0</td><td>-1.3</td><td>-207</td><td>-1.9</td><td>-4425</td></tr></table>

These results confirm that our qualitative conclusions are not artifact of the scaffold and that more research on completely novel orchestration is needed.

## B.4 EXPERIMENTAL SETUP AND IMPLEMENTATION DETAILS

We report Gaia2 scores on a representative set of models, covering both proprietary and open-source systems, and including both reasoning-oriented and non-reasoning models.

For evaluation, we use a ReAct scaffold that requires a Thought: and an Action: at each step. Since some models do not reliably follow this format, we add custom stop sequences <end\_action> and Observation: for models that tend to continue past a single tool call (Claude, Kimi, Qwen). This issue is largely alleviated by provider-specific ToolCalling APIs; we encourage reporting results with either interface (ReAct or ToolCalling).

Due to cost and time constraints, we did not evaluate every available model. For instance, Claude 4 Opus was excluded because of its very high latency and cost (\$15/M input tokens and \$75/M output tokens).

We note the following special configurations for specific third-party models:

\- Gemini 2.5 Pro: dynamic reasoning enabled via budget\_reasoning\_tokens = -1.

\- Grok-4: reasoning budget capped at 16k tokens per completion. We encountered frequent issues with xAI's API, in particular Empty Response errors, which introduced high variance in results.

\- GPT-5: temperature and top-p set to 1; no custom stop sequences were applied (not supported by the API).

When evaluating reasoning models (e.g., GPT-5, Claude-4, Qwen), we use the same ReAct prompts but adapt the inference client to handle reasoning-style outputs. To maintain a uniform evaluation and preserve the (Thought, Action) structure, we discard intermediate reasoning at each step and exclude it from the context of subsequent steps. While this approach aligns with the intended usage of some models (e.g., Qwen), it may not be optimal for others that interleave tool use with reasoning (e.g., GPT-5, Claude). We encourage the community to explore alternative setups to better assess the theoretical limits of the benchmark.

## B.5 ADDITIONAL EXPERIMENTS

### B.5.1 SUB-AGENT SPAWNING IN AGENT2AGENT MODE

In our Agent2Agent experiments, we record the number of instantiated sub-agents in Figure 19. Counts are fairly consistent across model families, yet the top A2A performers also spawn more sub-agents, suggesting stronger task decomposition.

![](images/b1e1c043f14082d8df1cafe1888e76f08d02fe2d5382ad7e38d7fb34aa04736d.jpg)

[Image: This bar chart illustrates the average number of spawned LLM agent instances per Gaia2-Mini scenario for eleven different models, specifically under an 'r=1' condition. The vertical axis measures 'spawned LLM agent instances' from 2.6 to 4.0, showing that Gemini 2.5-Pro and Claude-4 Sonnet have the highest averages around 3.8, while GPT-5 (minimal) has the lowest at approximately 3.25. Most models cluster between 3.4 and 3.8 instances, with black error bars indicating the variability for each entry.]  
Figure 19: Average number of agents spawned in Agent2Agent evaluations on Gaia2-mini tasks across models. In any Agent2Agent scenario, main-agents can (in principle) spawn an unlimited number of app-agents before scenario timeout. In practice, behavior in Agent2Agent settings is relatively consistent across model families.

### B.5.2 INFLUENCE OF NOISE LEVEL ON GAIA2 RESULTS

In this experiment, we vary the probability of tool errors and frequency of random environment events and measure resulting model results on Gaia2. While our lowest level of noise does not significantly impact model performance, increasing noise results in deteriorating performance across models. This aligns with our intuitions.

Table 7: Model performance on Gaia2-mini across different noise levels. \*Default setting.

<table><tr><td rowspan="2"></td><td colspan="4">Noise level</td></tr><tr><td>None</td><td>Low</td><td>Medium*</td><td>High</td></tr><tr><td>Claude-4 Sonnet</td><td>31.2</td><td>35.0</td><td>23.8</td><td>8.1</td></tr></table>
