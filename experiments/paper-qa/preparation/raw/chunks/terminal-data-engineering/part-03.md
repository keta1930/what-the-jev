# A. Appendix  


>Table 10: Skills Summary by Domain  


| Domain|Skill Types|Example Skill|
| ---|---|---|
| Security|Systems, Data Processing, Web Security, Algorithmic, Testing|Craft exploit payloads to bypass authentication and identify vulnerabilities|
| Software Engineering|Algorithmic, Systems, Data Processing, Web Security, Testing, Mathematical|Implement graph traversal (BFS/DFS) for dependency resolution|
| File Operations|File I/O, Navigation, Data Parsing, Transformation, Archives, Resources, Network|Parse structured formats (JSON/XML/CSV) with encoding and validation|
| Data Querying|Query Construction, Data Comprehension, Graph Processing, Result Processing|Writing queries using the formal syntax of declarative query languages for structured data|
| Data Science|Systems, Data Processing, Algorithmic, Mathematical, Testing, Web Security|Load and transform tabular data with groupby, filtering, and aggregation|
| Debugging|Systems, Debugging, Testing, Algorithmic, Data Processing, Mathematical|Resolve package dependency conflicts through constraint analysis|
| Scientific Computing|Data Processing, Algorithmic, Mathematical, Systems, Testing, Statistical, Web Security|Computing distance metrics between discrete probability distributions|
| Data Processing|Data I/O, Manipulation, String/Text, Algorithmic, Mathematical, Time Series, Systems, Testing|Build transformation pipelines with interpolation and feature extraction|
| System Administration|Filesystem, Process/Service, Network, Configuration, Deployment, Data Processing, Security, Shell Scripting, Testing, Algorithmic|Manage file permissions, configure services, and automate tasks with shell scripts|  


## A.1. Synthetic Trajectory Analysis  


We compute the distribution of the number of tokens (Figure 5) and turns (Figure 6) in our trajectories, separating synthetic tasks from dataset adapters.  


![6c92533db5bb07d97bce5060769b6f1e.jpeg](images/14.png)

[Image: This bar chart illustrates the frequency distribution of token counts for 226,313 dataset adapter trajectories, explicitly noting a mean of 17,507 and a median of 13,861 in the subtitle. The horizontal axis categorizes token counts into intervals ranging from 0k-5K to >40k, while the vertical axis measures frequency reaching just above 50,000. The data exhibits a distinct peak in the 5k-10K bin, which has the highest frequency of over 55,000, followed by the next highest bin in the 10k-15K range. Although frequencies generally trend downward as token counts increase from 15k to 35k, the final category of trajectories exceeding 40k tokens shows a notable increase in frequency to approximately 16,000.]  


![dab97e64ad08b56dc02f33125a9014cf.jpeg](images/14-2.png)

[Image: This histogram illustrates the distribution of token counts across 264,207 synthetic task trajectories, noting a mean of 17,363 and a median of 17,836. The horizontal axis categorizes token counts into 5,000-token increments ranging from 0K-5K to greater than 40k, while the vertical axis measures frequency in increments of 20,000. The distribution peaks sharply in the 15k-20k bin, where the frequency exceeds the 80,000 mark, followed by a gradual decline in frequency for longer trajectory lengths.]  


>Figure 5: Distribution of # tokens in the generated trajectories.  


## A.2. Details for Trajectory Generation  


We use Terminus 2 to generate all trajectories for SFT. We provide the full Terminus 2 system prompt template in Figure 7, which includes placeholders for *instruction* and *terminal_state*. Our Terminal-Task-Gen pipeline generates tasks with explicit instructions that replace the *instruction* placeholder. For dataset adapters, we instead insert the original prompt followed by a domain-specific suffix, shown in Figures 8–10. The *terminal_state* placeholder is populated with the latest terminal output summarizing the current shell state.  


![43f9e56fc9abab396e0052a1507ce692.jpeg](images/15.png)

[Image: The image displays two side-by-side histograms illustrating the frequency distribution of trajectory lengths measured in turn counts. The left chart, titled "Turn Count Distribution in Dataset Adapter Trajectories," shows data from N=226,313 samples with a mean of 17.5 and median of 16.0, peaking at the 10-14 turn bin. The right chart, titled "Turn Count Distribution in Synthetic Task Trajectories," presents N=264,207 samples with a mean of 16.3 and median of 16.0, also showing the highest frequency in the 10-14 turn range before declining rapidly for higher turn counts. Both charts use binned x-axis categories ranging from "0-4" to "50+" on a linear frequency scale.]  


>Figure 6: Distribution of # turns in the generated trajectories.  


## A.3. Details for Synthetic Task Generation  


### Curation of Primitive Skills  


We showcase the skill types and examples for each domain in Table 10. These domains encompass a wide spectrum of capabilities required for robust terminal interaction. For instance, Security tasks involve skill types such as Systems, Data Processing, Web Security, Algorithmic, and Testing, with practical applications like crafting exploit payloads to bypass authentication. Similarly, Software Engineering combines Algorithmic and Systems skills to implement complex logic like graph traversals for dependency resolution. File Operations and System Administration focus on core infrastructure tasks, ranging from parsing structured formats (JSON/XML/CSV) to managing file permissions and automating service configurations. We also curate specialized skills for Data Science, Scientific Computing, and Data Processing, which require mathematical and statistical proficiency to build transformation pipelines or compute distance metrics between probability distributions. By systematically categorizing these primitive skills from low-level filesystem manipulation to high-level algorithmic reasoning, we ensure comprehensive coverage of the challenges an autonomous agent must navigate in a terminal environment.  


### Prompts for Synthetic Task Generation  


We employ a modular prompting strategy that fuses a structural backbone with specialized constraints. Figure 11 presents the system prompt, which governs general task logic, while Figures 12–19 detail the domain-specific requirement modules injected into this template. These modules define the preconditions and objectives for each vertical; for instance, the Security module mandates crafting exploit payloads to identify vulnerabilities, while the Data Processing module requires building transformation pipelines with interpolation. This ensures that generated tasks precisely align with the diverse primitive skills outlined previously.  


### Terminus 2 Agent: System Prompt Template  


You are an AI assistant tasked with solving command-line tasks in a Linux environment. You will be given a task description and the output from previously executed commands. Your goal is to solve the task by providing batches of shell commands.  


Format your response as JSON with the following structure:  


{{
}}  


analysis": "Analyze the current state based on the terminal output provided. What do you see? What has been accomplished? What still needs to be done?",  


"plan": "Describe your plan for the next steps. What commands will you run and why? Be specific about what you expect each command to accomplish."  


"commands": [  


{
    "keystrokes": "ls -la\n",
}  


"duration": 0.1  


}}  


{
    "keystrokes": "cd project\n",
    "duration": 0.1
}  


}}  


,  


task_complete": true  


Required fields:  


- "analysis": Your analysis of the current situation  


- "plan": Your plan for the next steps  


- "commands": Array of command objects to execute  


Optional fields:  


"- task_complete": Boolean indicating if the task is complete (defaults to false if not present)  


Command object structure:  


- "keystrokes": String containing the exact keystrokes to send to the terminal (required)  


- "duration": Number of seconds to wait for the command to complete before the next command will be executed (defaults to 1.0 if not present)  


IMPORTANT: The text inside "keystrokes" will be used completely verbatim as keystrokes. Write commands exactly as
you want them sent to the terminal:  


- Most bash commands should end with a newline (\n) to cause them to execute  


- For special key sequences, use tmux-style escape sequences:  


- C-c for Ctrl+C  


The "duration" attribute specifies the number of seconds to wait for the command to complete (default: 1.0) before the next command will be executed. On immediate tasks (e.g., cd, ls, echo, cat) set a duration of 0.1 seconds. On commands (e.g., gcc, find, rustc) set a duration of 1.0 seconds. On slow commands (e.g., make, python3 [ long running script], vget [file]) set an appropriate duration as you determine necessary.  


It is better to set a smaller duration than a longer duration. It is always possible to wait again if the prior output has not finished, by running {{"keystrokes": "", "duration": 10.0}} on subsequent requests to wait longer. Never wait longer than 60 seconds; prefer to poll to see intermediate result status.  


Important notes:  


- Each command's keystrokes are sent exactly as written to the terminal  


- Do not include extra whitespace before or after the keystrokes unless it's part of the intended command  


- Extra text before or after the JSON will generate warnings but be tolerated  


- The JSON must be valid - use proper escaping for quotes and special characters within strings  


- Commands array can be empty if you want to wait without taking action  


Task Description:  


{instruction}  


Current terminal state:  


{terminal_state}  


>Figure 7: System prompt template for Terminus 2.  


### Math Dataset Adapter: Instruction Template  


{math_prompt}

Please place your final answer in a file named '/app/solution.txt'.  


>Figure 8: Instruction template for math dataset adapter.  


### Code Dataset Adapter: Instruction Template  


{code_prompt}  


Write Python code to solve the problem. Please place the solution code in a file named `/app/solution.py`.  


>Figure 9: Instruction template for code dataset adapter.  


### SWE Dataset Adapter: Instruction Template  


{swe_prompt}  


Please first localize the bug based on the issue statement, generate *SEARCH/REPLACE* edits to fix the issue, and save the diff to a file named `/app/solution.patch`.  


>Figure 10: Instruction template for SWE dataset adapter.  


![41add6c42cba8d70614b6cc20fa7b25f.jpeg](images/18.png)

[Image: This image presents a text-based prompt template titled "Skill-based Task Generation," structured into two main parts: System Prompt Construction and User Message Construction. The System Prompt section details five numbered components including Role Definition, Domain Context, Universal Task Requirements (such as being challenging yet easy to verify), Output Format using XML tags, and Critical Rules like preventing code leakage. The User Message Construction section specifies inputs for task category, primitive skills, and Docker environment content, alongside explicit instructions to generate a novel task that combines 3-5 primitives in an unexpected way. Placeholders like `<domain>`, `<Primitive_Skills>`, and `<DOCKERFILE_CONTENT>` indicate where dynamic information is inserted.]  


>Figure 11: Prompt template used for all skill-based generation. Domain-specific modules are inserted into section 2.  


![12b336c388f2ec2813fb8cfc6b8e7ee3.jpeg](images/19.png)

[Image: This image displays a text-based prompt template titled "Domain Module: Data Processing," designed to guide an AI in creating programming tasks for agent training. It defines a specific "Domain Focus" covering five key areas: file format handling (such as CSV and JSON), data transformation, ETL pipelines, stream processing, and data validation. The bottom section, labeled "Your Task," lists four criteria that the generated problem must meet: it should be challenging, easy to verify, self-contained, and realistic.]  


>Figure 12: Module for Data Processing tasks.  


![8eadc920e3ce384806c5b3c4e079d7cc.jpeg](images/19-2.png)

[Image: This image presents a system instruction slide titled "Domain Module: Data Querying," defining an AI role as a "Data Querying Task Builder" for creating programming exercises. The content is divided into a "Domain Focus" section listing technical areas such as SQL operations, query optimization, and NoSQL patterns, alongside a "Your Task" section specifying that generated problems must be challenging, verifiable, and realistic. This document appears to be a component of an automated workflow for training AI agents on database-related skills.]  


>Figure 13: Module for Data Querying tasks.  


![06ce21a6a4e22d84247b632ee0ab9fc9.jpeg](images/20.png)

[Image: The image presents a configuration prompt titled "Domain Module: Data Science," which instructs an AI agent role-playing as a "Data Science Task Builder." The document details a "Domain Focus" section listing five specific competencies: Exploratory Analysis, Feature Engineering, Statistical Modeling, Data Mining, and Reporting, each followed by relevant technical keywords. Below this, the "Your Task" section enumerates four strict criteria for creating programming challenges: they must be challenging, easy to verify, self-contained, and realistic.]  


>Figure 14: Module for Data Science tasks.  


![9f76f14de488e5a54828706294b2ee7b.jpeg](images/20-2.png)

[Image: This image presents a document section titled "Domain Module: Debugging," instructing an AI agent to act as a "Debugging Task Builder" for training purposes. The "Domain Focus" section details five specific categories of debugging tasks: Error diagnosis, Root cause analysis, Performance debugging, Memory issues, and Concurrency bugs, each accompanied by relevant technical examples such as stack traces or race conditions. Below this, the "Your Task" section specifies four criteria that the generated programming problem must meet: it should be challenging to solve, easy to verify, self-contained within the prompt, and realistic to professional scenarios.]  


>Figure 15: Module for Debugging tasks.  


![46ea17703d0a6e48be064dfea4a21100.jpeg](images/21.png)

[Image: The image presents a text document titled "Domain Module: File Operations" designed to guide an AI in generating programming tasks. The content defines a "Domain Focus" that encompasses file I/O, directory traversal, various file formats including binary and text, compression tools like zip and tar, and file system metadata. The instructions conclude by outlining specific requirements for the generated task, mandating that it be challenging, easily verifiable, self-contained, and representative of professional work.]  


>Figure 16: Module for File Operations tasks.  


![a4110d0f145d97d35b22df6cce2ea691.jpeg](images/21-2.png)

[Image: This image displays a structured prompt labeled "Domain Module: Scientific Computing" intended to guide an AI in creating programming tasks for agent training. It specifies a "Domain Focus" encompassing numerical simulation, signal processing, statistical analysis, visualization, and domain-specific applications in fields like physics and biology. The final section, "Your Task," outlines four required characteristics for the generated problems: they must be challenging, easy to verify, self-contained, and realistic.]  


>Figure 17: Module for Scientific Computing tasks.  


![5f1238ebffe017ecd1e60ed8429bcfce.jpeg](images/22.png)

[Image: The image displays a document titled "Domain Module: Security," which serves as a system prompt defining the role of a "Security Task Builder." It outlines a "Domain Focus" section listing five key technical areas: Cryptography, Vulnerability Analysis, Authentication, Network Security, and Secure Coding, along with specific examples for each. The final section, "Your Task," instructs the creation of a programming task that satisfies four specific criteria: it must be challenging to solve, easy to verify, self-contained, and realistic.]  


>Figure 18: Module for Security tasks.  


![081cb7426e030e74781fb1860142a7b6.jpeg](images/22-2.png)

[Image: This document presents a prompt template titled "Domain Module: Software Engineering," designed to instruct an AI agent on creating programming tasks. It lists five specific domain focuses including code quality, build systems, version control, API design, and architecture. The final section outlines four mandatory criteria for the generated tasks: they must be challenging, easy to verify, self-contained, and realistic.]  


>Figure 19: Module for Software Engineering tasks.  


![a7290a7c779b80764b176fbbab44638c.jpeg](images/23.png)

[Image: This image displays a document titled "Domain Module: System Administration," which serves as a prompt for an AI agent acting as a "System Administration Task Builder." The text outlines five specific domain focus areas including process management, network configuration, storage management, monitoring, and automation, listing relevant technical details for each. It further specifies that the resulting programming task must meet four criteria: it should be challenging, easy to verify, self-contained, and realistic to professional system administration work.]  


>Figure 20: Module for System Administration tasks.  


