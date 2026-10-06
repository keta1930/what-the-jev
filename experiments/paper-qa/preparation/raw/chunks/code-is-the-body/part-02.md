# 8 Related Work

Memory and skills. Generative Agents uses persistent memory for behavioral continuity [1]; Voyager accumulates executable skills [2]; and SkillFlow v1 studies skill and code transfer among adapting agents [3]. OurArk treats these as sources of change Its continuity unit is the identity-bearing software body: memory remains private state, parent inheritance follows lineage, and peer learning is lateral.

Personal-agent frameworks. OpenClaw provides a user-run personal assistant organized around a workspace, prompt files, tools, and skills [4]. Hermes Agent adds a closed learning loop that creates skills from experience, improves them during use, persists knowledge, and recalls past sessions [5]. These systems demonstrate the practical value of persistent personal agents and durable learning. OurArk difers by making an identity-bearing software body under user custody the unit of continuity, governed evolution, and independently versioned descent.

Self-rewriting agents. Gödel Machines provide the classic formulation of a self-rewriting system whose modification requires a proof of utility [6]. Empirical systems instead evaluate modifications: the Darwin Gödel Machine evolves an archive of coding-agent implementations [7], Live-SWE-agent modifies its scafold during software tasks [8], and a Self-Improving Coding Agent edits and evaluates its own scafold [9]. MOSS is the closest source-rewriting comparison, promoting in-place harness replacements through candidate trials, replay, user consent, and rollback [10]. These systems make agent implementation an evolution target. OurArk makes it a persistent personal body that can produce independently versioned descendants with distinct identities and private state.

Protocolized resource and harness evolution. Autogenesis registers prompts, agents, tools, environments, and memory as separately versioned resources and applies a propose-assess-commit loop with lineage, branching, and rollback [11]. Its continuity unit is a registered resource and its version history. Resource duplication does not define whole-body ofspring with a new identity and private-state boundary. Self-Harness turns execution failures into bounded harness edits accepted through regression testing [12]. It optimizes an operating harness rather than modeling body custody or descent. SemaClaw develops an open personal-agent harness with persistent persona and user-owned knowledge [13], but not body-level evolution or lineage.

Repository evolution and persistent runtimes. EvoGit coordinates coding agents through a Git phylogenetic graph over branching versions of a shared evolving code artifact [14]. Agent libOS provides persistent process identity, parent-child lineage, reusable images, capabilities, and approval queues [15]. Research on divergent forks finds that code propagation is uncommon after independent development [16]. OurArk does not claim Git, identity, or code evolution individually. It unifies an agent-owned versioned body, separate identity and private state at descent, and ancestry-guided transfer after divergence.

The following table summarizes the paper’s narrow positioning. “Descent” here means materializing a persistent agent body with a distinct identity and private-state boundary, not merely forking a candidate version or spawning a runtime process.

<table><tr><td>System</td><td>Primary evolving object</td><td>Continuity or identity unit</td><td>Descent or branching</td><td>Primary acceptance mechanism</td></tr><tr><td>Self-Improving Coding Agent [9]</td><td>coding-agent scaffold</td><td>one evaluated scaffold</td><td>not the focus</td><td>benchmark performance</td></tr><tr><td>MOSS [10]</td><td>deployed agent harness</td><td>in-place harness image</td><td>in-place replacement</td><td>replay, health probes, user consent</td></tr><tr><td>Autogenesis [11]</td><td>registered prompt, agent, tool, environment, or memory</td><td>resource instance and version lineage</td><td>resource duplication and version branching</td><td>evaluation, commit, and rollback</td></tr><tr><td>EvoGit [14]</td><td>shared code artifact and version graph</td><td>artifact version</td><td>branching code versions</td><td>agent collaboration and strategic human feedback</td></tr><tr><td>Agent libOS [15]</td><td>agent process and execution image</td><td>process identity and runtime state</td><td>child processes and reusable images</td><td>capability checks and approval queues</td></tr><tr><td>OurArk</td><td>identity-bearing agent software body</td><td>repository body plus separate private state</td><td>independent body descent; recursively compatible</td><td>regression checks, human-controlled merge, and failed-update rollback</td></tr></table>

# 9 Conclusion

OurArk starts from a simple design thesis: a persistent personal agent should have an owned, identity-bearing software body. Applying evolution and descent to that same body lets a seed become the root of independently specializing lineages. A fouragent, three-descent prototype demonstrates this architecture through human-agent co-evolution, separated private state and model reasoning, and governed body change. After divergence, the architecture allows descendants to pull parent changes as candidates for local adaptation rather than sharing a continuously synchronized base.

The evidence is architectural and mechanism-level, and the long-term direction is a personal ecosystem of agents that people possess, govern, specialize, and evolve with.

# References

[1] Joon Sung Park, Joseph C. O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior. In Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology, UIST ’23, pages 1–22, New York, NY, USA, 2023. Association for Computing Machinery. Article 2; doi:10.1145/3586183.3606763.

[2] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager: An open-ended embodied agent with large language models, 2023. arXiv:2305.16291.

[3] Pagkratios Tagkopoulos, Fangzhou Li, and Ilias Tagkopoulos. SkillFlow: Eficient skill and code transfer through communication in adapting AI agents, 2025. arXiv:2504.06188v1.

[4] OpenClaw Foundation. OpenClaw: Personal AI assistant. Software release, July 2026. Version v2026.7.1, released July 13, 2026; https://github.com/openclaw/openclaw/releases/tag/v2026.7.1.

[5] Nous Research. Hermes agent. Software release, July 2026. Version v0.19.0, tag v2026.7.20, released July 20, 2026; https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.20.

[6] Jürgen Schmidhuber. Gödel Machines: Self-referential universal problem solvers making provably optimal selfimprovements, 2003. arXiv:cs/0309048; revised 2006.

[7] Jenny Zhang, Shengran Hu, Cong Lu, Robert Lange, and Jef Clune. Darwin Gödel machine: Open-ended evolution of self-improving agents, 2025. arXiv:2505.22954.

[8] Chunqiu Steven Xia, Zhe Wang, Yan Yang, Yuxiang Wei, and Lingming Zhang. Live-SWE-agent: Can software engineering agents self-evolve on the fly?, 2025. arXiv:2511.13646.

[9] Maxime Robeyns, Martin Szummer, and Laurence Aitchison. A self-improving coding agent, 2025. arXiv:2504.15228.

[10] Qianshu Cai, Yonggang Zhang, Xianzhang Jia, Huajiang Zheng, Wei Xue, Jun Song, Xinmei Tian, and Yike Guo. MOSS: Self-evolution through source-level rewriting in autonomous agent systems, 2026. arXiv:2605.22794.

[11] Wentao Zhang, Zhe Zhao, Haibin Wen, Yingcheng Wu, Cankun Guo, Ming Yin, and Bo An. Autogenesis: A self-evolving agent protocol, 2026. arXiv:2604.15034.

[12] Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, and Shuyue Hu. Self-harness: Harnesses that improve themselves, 2026. arXiv:2606.09498.

[13] Ningyan Zhu, Huacan Wang, Jie Zhou, Feiyu Chen, Shuo Zhang, Ge Chen, Chen Liu, Jiarou Wu, Wangyi Chen, Xiaofeng Mou, and Yi Xu. SemaClaw: A step towards general-purpose personal AI agents through harness engineering, 2026. arXiv:2604.11548.

[14] Beichen Huang, Ran Cheng, and Kay Chen Tan. EvoGit: Decentralized code evolution via Git-based multi-agent collaboration, 2025. arXiv:2506.02049.

[15] Yingqi Zhang. Agent libOS: A runtime substrate for capability-controlled self-evolving LLM agents, 2026. arXiv:2606.03895.

[16] John Businge, Moses Openja, Sarah Nadi, and Thorsten Berger. Reuse and maintenance practices among divergent forks in three software ecosystems. Empirical Software Engineering, 27:54, 2022. Article 54; doi:10.1007/s10664-021-10078- 2.