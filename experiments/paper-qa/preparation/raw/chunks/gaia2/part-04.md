# A ARE APPENDIX

## A.1 ARE FOUNDATIONS

ARE is time-driven and built on the principle that “everything is an event”. Specifically, five core concepts work together:

1. Apps are stateful API interfaces that typically interact with a data source.

2. Environments are collections of Apps, their data, and governing rules that define system behavior.

3. Events are anything that happens in the Environment. All Events are logged.

4. Notifications are messages from the Environment that inform the agent about Events. They are configurable and enable selective observability of the Environment.

5. Scenarios are sets of initial state and scheduled Events that take place in an Environment, and can include a verification mechanism.

### A.1.1 APPS

Apps are collections of tools that interact with a data source. For instance, an Emails app contains tools like send\_email and delete\_email that all operate on the same email database. Similar approaches have been explored in AppWorld (Trivedi et al., 2024) and ToolSandbox (Lu et al., 2024).

Apps maintain their own state Each app starts in the simulation with an initial state and keeps track of changes as agents use its tools or as events occur in the environment. Apps store their data internally rather than relying on external databases. This design makes it convenient to study agent tasks that require to modify the state of the environment, and ensures that experiments can be reproduced consistently.

Tool creation and taxonomy Apps are implemented by adding Python methods within an App class. When the simulation runs, these methods are automatically converted into properly formatted tool descriptions that agents can understand and use. ARE classifies tools into two types via decorators: read, which only read app states (e.g., search\_emails), and write, which modify app states (e.g., send\_email). This distinction is helpful e.g. for verification, see Appendix B.2. Tools are role-scoped—agent, user, or env.

Extensibility Beyond ad hoc app creation, ARE can also connect with external APIs through MCP compatibility (Anthropic, 2024). The framework also offers flexible options for data storage. While our current implementation stores data in memory, users can easily connect SQL databases or other storage systems without changing the core framework.

Core apps Developers can choose which apps to include in their environment or create new ones. However, every ARE environment includes two core apps that handle the basic interaction between agents and their environment:

\- AgentUserInterface is the communication channel between users and agents: messages are tool calls, and user messages generate notifications (Appendix A.1.4) that agents can process asynchronously. This enables asynchronous interactions during task execution. The interface supports two modes: blocking (the agent waits for a user reply) and non-blocking (the agent continues loop regardless of reply).

\- System provides core simulation controls like get\_current\_time (query time), wait (pause for a duration), and wait\_for\_next\_notification (pause until an event). When any wait tool is invoked, the simulation accelerates: it switches from real time to a queue-based, event-to-event loop. Scenarios that would take hours in the real world can thus run in minutes, enabling practical long-horizon testing.

### A.1.2 ENVIRONMENT

An environment is a Markov Decision Process with states, observations, actions, and transition rules. The environment state includes the states of all apps, the time manager, and the notification system. Apps define the action space by exposing their tools. The environment runs deterministically given a fixed starting state and seed, ensuring reproducible evaluations. It can host one or multiple agents simultaneously, supporting both single-agent and multi-agent setups. The environment's rules define time progression, action permissions, reward computation, and how agent actions affect the environment state.

### A.1.3 EVENTS

In ARE, an event is any agent action or app-state change. Each event is timestamped, logged. Events can be scheduled, e.g., a friend's message 1 minute after simulation start. This design yields (i) deterministic execution—events run in scheduled order; (ii) complete auditability—all actions can be replayed and analyzed; and (iii) flexible scheduling—events can be set at absolute times or relative to others.

Event lifecycle Events flow through four stages described in Figure 2: (i) creation - events are created from tool calls or scheduled by the simulation; (ii) scheduling - events enter a time-ordered EventQueue with dependency management using directed acyclic graphs, supporting both absolute timing (at specific timestamps) and relative timing (relative to other events or conditions); (iii) execution - the EventLoop processes events and captures results, state changes, and exceptions; and (iv) logging - executed events are stored in an EventLog with detailed metadata for analysis, debugging, and validation of agent behavior.

Event types There are different types of events. While most events track interactions within the environment, other special events are needed to enable dynamic scenarios and verification strategies:

\- Agent/User/Env events are generated by tool calls. Agent Events are initiated by the agent (e.g., sending a message), User Events by the user (e.g., replying to the agent), and Environment Events by the simulation itself to introduce external changes (e.g., a scheduled message from a friend).

\- Conditional events periodically check predefined conditions and complete when criteria are met (e.g., cancel a ride only if one was booked).

\- Validation events check milestone achievement or constraint violations for verification, and fail the simulation if not completed on timeout (e.g., stop if no ride is booked within 30 seconds of the user request).

\- Oracle events are pre-scheduled “ground truth” actions used by a verifier for comparison.

Dependencies and scheduling Events are modeled as Directed Acyclic Graphs (DAGs) as illustrated in Figure 11. An event can only be triggered upon successful completion of all its predecessors (e.g., e1 processes immediately at simulation start, e4 needs both e2 and e3 to be completed). This data structure also supports multiple branches running simultaneously to model independent events. Conditional and Validation events can be used in the DAG to trigger other events and make the environment more dynamic.

### A.1.4 NOTIFICATION SYSTEM

At each environment step, processed events can trigger notifications according to a notification policy (see Figure 2), similar to mobile device notifications. Apart from tool outputs, notifications are the only signals agents receive from the environment. Notifications are queued by timestamp and exposed to agents through a notification queue, enabling asynchronous interactions. In our orchestration (see Appendix B.3), notifications are injected into the agent's context at the beginning of each agent step.

Notification policy The notification system follows a configurable policy—i.e., a whitelist of events authorized to emit notifications. ARE pre-defines three verbosity levels: low (only user messages are notified), medium (emails, messages and calendar events are notified), and high (everything is notified), creating a graduated spectrum of environmental observability.

![](images/1b967693cbd5b7307a5fe9e79a29a45bf593bed2d714738659ed3eaad5ba2a3f.jpg)

[Image: This image displays a flowchart illustrating a process flow starting from a node labeled "start," which branches into two parallel paths. The upper path leads to a blue box "E1," splitting into a solid line connecting to "E2" and a dashed line connecting to a grey box "E3"; both "E2" and "E3" then merge via dashed arrows into a grey box labeled "E4." The lower path flows directly from "start" to a blue box "E5," which connects via a solid line to "Cond1." Finally, "Cond1" connects via a dashed line to a diamond-shaped decision node "Val," which features a self-looping dashed arrow and terminates in two outcomes: "True" indicated by a green checkmark and "False" indicated by a red cross.]  
Figure 11: Event dependency graph illustrating ARE scheduling patterns. Events E1 and E5 execute in parallel after simulation start, and E2/E3 executing in parallel after their prerequisites, both need to be executed for E4 to execute. Conditional execution is shown through Cond1 leading to validation (Val) with true/false outcomes.

Notifications and agent proactivity Notifications are not the only way for agents to observe environment changes. For example, even if the notification policy doesn't alert the agent when messages arrive from contacts, the agent can still proactively check for new messages by browsing the user's inbox. Notifications add realism and complexity to environments, potentially creating different agent behaviors based on whether the environment is notification-rich or notification-poor. This system enables researchers to tackle new capabilities such as proactivity.

### A.1.5 SCENARIOS

ARE shifts from static, single-turn tasks to dynamic scenarios. Scenarios attempt to capture real-world complexity through temporal dynamics, events, and multi-turn interactions. This enables evaluation of agent capabilities that cannot be assessed through traditional request-response paradigms. In practice, scenarios are implemented in a scenario.py containing the apps, scheduled events, and arbitrary verification logic.

Scenario runtime Scenarios typically start with an environment instance and a send\_message\_to\_agent tool call, waking the agent up. The environment operates on discrete time steps, executing scheduled events and managing state transitions until the agent reaches an exit condition, see Figure 11. All interactions with the user are through the AgentUserInterface, with verification triggered upon task completion.

Scenario example Consider this two-turn scenario (see Figure 2 and Figure 12): a user asks the agent via AgentUserInterface “Can you ask my mom to send me our family streaming password?”. The agent is initialized from this first notification, starts checking messages, and requests the password in the Chats app; the tool calls modify the Chats app state and are recorded in the EventLog. The agent confirms to user that the request was sent, after which the environment pauses execution and applies first-turn validation.

At turn two, the user asks a follow up question: "As soon as I receive the password from my mother, transfer it to my father". The agent resumes upon the send\_message\_to\_agent notification, and looks for the mother's reply in the Chats app (where it previously requested it). In the meantime, a scheduled environment event is triggered and an Email from the mother containing the code is received. The agent reacts to this email notification by stopping searching the Chats app, processes the Email, extracts the code, forward it to the father, and report success to the user. Final verification reviews the complete interaction in the EventLog, and the environment issues a termination signal to end execution.

## A.2 NOTIFICATION POLICIES IN ARE

The notification system in ARE follows a configurable policy where researchers can choose which Env events are notified to the Agent. The Mobile environment pre-defines three notification policies with different levels of verbosity, which we describe in detail in Table 4. Note that messages sent by the user via send\_message\_to\_agent are systematically notified to the agent, regardless of the verbosity level.

Table 4: Pre-set notification policies in Mobile (Compressed).

<table><tr><td>Verbosity</td><td>Notified Environment Tools</td><td>Description</td></tr><tr><td>low</td><td>None</td><td>No environment events are notified.</td></tr><tr><td>medium</td><td>Email: create_and_add_email, send_email_to_user_only, reply_to_email_from_userChats/Messages: create_and_add_messageShopping: cancel_order, update_order_statusCabs: cancel_ride, user_cancel_ride, end_rideCalendar: add_calendar_event_by_attendee, delete_calendar_event_by_attendee</td><td>Notifies events that are consequences of agent actions, analogous to mobile notifications. Default in Gaia2.</td></tr><tr><td>high</td><td>All medium tools plus:Shopping: add_product, add_item_to_product, add_discount_codeRentAFlat: add_new_apartmentCabs: update_ride_status</td><td>Notifies all environment events, including those independent of agent actions (e.g., new products).</td></tr></table>

![](images/a086d24570d2f4e2db445b0f10997b5bc655223d4c436c33b51e134fdd4aee90.jpg)

[Image: This sequence diagram depicts the interaction workflow involving three participants: User, Environment, and Agent. The process initiates with a user message that prompts the environment to inject a notification into the agent's context, leading to chat search and sending activities during an "Agent Running" phase. Following a response forward to the user, the system pauses for validation before processing a follow-up message triggered by a "new Email" notification. This second phase involves reading conversations and transferring emails while the agent runs again, concluding with a final validation step and the agent being terminated.]  
Figure 12: Sequence diagram of a multi-turn scenario in ARE. The agent is paused between turns, i.e., between calling send\_message\_to\_user and receiving send\_message\_to\_agent, and adapts its strategy in response to an asynchronous notification from the environment, a new email.

## A.3 UNIVERSE GENERATION

Dependency management & consistency To ensure cross-app coherence, we implement a structured dependency resolution system. During generation, each app queries the existing universe state to maintain consistency—for example, when generating emails, the system first retrieves all available contacts to ensure referenced individuals exist in the Contacts app. Similarly, calendar events that mention other people are validated against the contact list, and ride history in the Cabs app references locations that align with the user's established geographic context.

We handle dependency conflicts through a priority-based resolution system where foundational apps (e.g., Contacts) take precedence over dependent apps (e.g., Messages, Emails) as show in Figure 13.

However, several complex inter-app dependencies remain unhandled in our current implementation. These include temporal consistency across apps (ensuring message timestamps align with calendar availability), semantic relationship tracking (maintaining consistent relationship dynamics between contacts across different communication channels), and cross-modal content references (ensuring photos mentioned in messages exist in the file system). Addressing these limitations represents important future work for achieving fully coherent synthetic Mobile environments.

![](images/3c9cc52afcf328204607cf200077827e9462d127e23e26345321b8efc629a0be.jpg)

[Image: The image presents a flowchart illustrating a system architecture for populating mobile application data. The process flows from blue 'Seed' and 'Persona Generation' blocks into a central 'Contacts' block. Branching from 'Contacts' are five data categories: 'Chats', 'Messages', 'Calendar', 'RentAFlat', and 'Cab', with 'RentAFlat' further connecting to 'CityApp'. On the far left, two disconnected blocks labeled 'Shopping' and 'Files' are visible.]  
Figure 13: The dependency graph of Mobile apps. Shopping and File system are independent apps. Contacts is the root for rest of the apps.

Contacts We populate contacts using personas as the foundation. To begin, we sample seed personas from the persona hub Ge et al. (2024). However, these personas are brief and lack grounding in the universe's location. To address this, we expand and contextualize them by incorporating the universe location into the prompt. We sample a user persona from the generated contacts which serves as the basis for populating the rest of the universe. A universe is based on a user persona.

An example user persona is:

```json
{
    "first_name": "Helena",
    "last_name": "Mueller",
    "gender": "Female",
    "age": 43,
    "nationality": "German",
    "city_living": "Berlin",
    "job": "Marketing Manager",
    "description": "Helena Mueller is a vibrant and energetic 43-year-old marketing manage living in Berlin, Germany.",
    "phone": "+49 157 6543210",
    "email": "helena.mueller@gai2mail.com"
}
```  
Chats & Messages In Chats & Messages apps, we generate both group conversations and individual chats. We sample contacts between whom we have to generate the conversations. Then, we

provide the participants personas and prompt the model to generate a conversation with at least 10 messages alternating between participants. We prompt the model to generate conversations that are natural and reflect the participants' backgrounds and also ask it to include references to possible shared experiences, interests, or cultural elements.

Emails Similar to messages, we prompt the LLM to generate both ‘inbox’ and ‘sent’ emails. For inbox emails, the sender is sampled from the contact list, while for sent emails, the recipients are selected. We provide the LLM with the user’s persona and the sampled non-user persona to generate the emails. We specifically prompt the LLM to analyze details such as age, gender, cultural background, occupation, education level, personality traits, communication style, current life circumstances, relationships and social networks, as well as interests and hobbies, and come up with a valid reason for writing the email.

Calendar We provide the LLM with the user persona and a summary of the previous week, prompting it to generate calendar events for the current week. Next, we use these newly generated events to prompt the LLM to create a weekly summary. This process is repeated iteratively to populate the calendar over a specified timeframe, such as three months.

RentAFlat & City For apartment listings, we provide the universe countries and prompt the LLM to generate apartment listings. The City app is designed to retrieve crime rates for specific zip codes. Using the zip codes generated for apartment listings, we prompt the LLM to produce crime rate data as a floating-point value in the range of 1–100.

Shopping For the Shopping app, we integrate publicly available Amazon product dataset. For each universe, we sample 500 products and generate discount codes applicable to select items.

Cabs We prompt the LLM with the user country information and generate the user's ride history.

Files We employ a traditional file system hierarchy, loading it with publicly available Wikipedia data, datasets, and images. Additionally, we also add our files that do not contain personal information. We choose to keep the file system the same for all universes.

## A.4 ARE GRAPHICAL USER INTERFACE

Running scenarios with ARE generates rich agent execution traces that include reasoning steps, tool calls, their outputs, notifications, and, on the environment side, temporal event flows that unfold over simulated time periods. It is important for practitioners to be able to debug these interactions, whose complexity requires specialized tooling. Existing development tools largely fall into one of these categories: interactive debugging platforms (Epperson et al., 2025; Rorseth et al., 2025; Pang et al., 2025) and data annotation/curation platforms, each with distinct UI approaches. Commercial observability tools such as Arize Phoenix $^{3}$ and Langfuse $^{4}$ primarily offer visual timeline views and trace/span visualizations to help developers analyze agent execution, focusing on understanding behavior after the fact rather than direct interaction or editing. Academic prototypes such as AGDebugger (Epperson et al., 2025) and LADYBUG (Rorseth et al., 2025) provide interactive debugging with user interfaces that enable browsing conversation histories, editing messages, and tracing execution steps, while Hippo (Pang et al., 2025) uses an interactive tree to visualize and control chain-of-thought reasoning without focusing on tool calls, agentic behavior nor annotations.

Although there are many specialized tools for data annotation, such as commercial platforms like Labelbox $^{5}$ , they mainly focus on simplifying human-in-the-loop annotation. These tools offer features like multimodal chat editors and customizable worksheet UIs, enabling data labelers to refine trajectories from interactive LLM sessions. Despite their power for data collection and curation, a significant gap remains: They are designed to annotate traces of interactions and lack key points for reproducibility and broad evaluation: 1) They annotate full multi-turn conversations, when we want to gather tasks, environment events, and agent task success criteria; 2) they lack structured annotations within a fully simulated and reproducible environment, which is key to capturing both agent interaction with tools and external events, for realistic, reproducible agent traces.

To address this, we propose a single ARE Graphical User Interface (UI), a web-based platform that enables developers to interact with the environment, visualize scenarios (see Figure 14), and understand agent behavior and failures through detailed trace analysis and replay capabilities, and enable zero-code scenario annotation.

![](images/e6d94c48ef1d290dcffea60e2095d534ce7e23adb6cbf71668b9d9d27e5919aa.jpg)

[Image: This interface displays a scenario execution dashboard featuring a node-based flowchart at the top connecting various functional modules like 'Calendar', 'Emails', and 'AgentPrompts' through directional arrows. Below the graph, a 'Run scenario' panel summarizes the agent's completed actions in natural language, such as cancelling a 'Film Production Day' event and sending notifications. Adjacent to this is a 'Logs' panel detailing the technical execution trace, including system prompts, thought processes, and tool calls organized in a hierarchical tree structure.]  
Figure 14: ARE scenario view with event DAG (top), scenario run (bottom left) and agent logs (bottom right).

### A.4.1 ENVIRONMENT EXPLORATION

Easily exploring the environment is crucial for understanding the context available to agents when debugging scenarios execution, and annotating new verifiable scenarios. The UI provides a comprehensive visualization of the simulated environment, displaying all available apps/tools and their current states. Interactive app views allow users to browse app contents and interact with their tools, e.g. email inboxes in Mobile, in real-time. Views are automatically generated for new apps, which therefore doesn't require a UI rewrite.

### A.4.2 AGENT TRACE VISUALIZATION AND REPLAY

The UI presents agent multi-step interaction traces in a structured timeline view that clearly delineates agent thoughts, actions, and tool responses. Each trace element is timestamped and categorized, allowing users to follow the agent's reasoning process, similar to the Phoenix $^{6}$ trace views also used by smolagents $^{7}$ , but extended with debugging capabilities. Developers can roll back time by jumping back to a past event, editing thought, tool call, etc., from that step and replaying the scenario to see what would happen with a slightly different approach, similar to setting breakpoints and stepping through code in a standard code debugger.

### A.4.3 SCENARIO VISUALIZATION

The UI provides interactive visualization of scenarios and their event DAGs introduced in Section 3, showing how scenario events are interconnected, and their execution status in real-time. The event graph visualization supports both scenario development and execution analysis. Before running a scenario, users can examine event triggers, dependencies, and timing constraints of the scenario.

During execution of a scenario by an agent, the interface highlights completed events and shows the progression through the dependency graph. Developers can run through the scenario with a given agent, see how it behaves and debug the scenario or the agent (see Figure 14). ARE is able to simulate time progression, so users can decide to jump in time for scenarios that span long time frames (e.g. weeks, months).

### A.4.4 ANNOTATION INTERFACE

Beyond visualization, the UI includes an annotation interface – not released at this time – that significantly reduces the cost of scenario creation and QA. This includes a graph editor that allows to easily build a scenario event DAG. For each node, the annotator can configure tool calls, the node's parents, and optionally timing. For example, to create a Mobile scenario, the annotator adds nodes representing a user initial ask (e.g. “email my travel plans”), oracle action solving the task (e.g. “agent sent an email”), environment events that will interfere with the agent's work (e.g. “received an email from travel agent”), and potentially further turns. To ensure quality and consistency across annotations, we incorporate automated checks of the created events DAG. These checks detect and flag logical inconsistencies in event flows to annotators, such as a node without parents or contradictory node timings. The annotation interface achieves an approximate five times improvement in annotation time for Mobile scenarios, compared to manual approaches.

# B GAIA2 APPENDIX
