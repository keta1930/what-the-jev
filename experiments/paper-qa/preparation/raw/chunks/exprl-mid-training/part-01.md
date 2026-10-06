arXiv:2606.17024v1 [cs.LG] 15 Jun 2026  


# ExpRL: Exploratory RL for LLM Mid-Training  


Violet Xiang$^{1}$, Amrith Setlur$^{2}$, Chase Blagden$^{3,\dagger}$, Nick Haber$^{1}$ and Aviral Kumar$^{2}$  


$^{1}$Stanford University, $^{2}$Carnegie Mellon University, $^{3}$OpenAI, $^{\dagger}$Work done while at Rogo.  


![2e81094f8caf9aed591aa82bf9881c68.jpeg](images/0.png)

[Image: Figure 1 illustrates the Exploratory RL (ExpRL) method by contrasting the performance of a base Large Language Model against one fine-tuned with the proposed approach. Panel 1 depicts the Base LLM failing on a hard problem, generating multiple incorrect solutions marked with $r=0$ and exhibiting limited coverage over possible answers as shown in the distribution plot. Panel 2 outlines the mid-training phase where auxiliary data and an LLM judge are used to assign dense rewards (such as $r=0.2, 0.5, 0.8$) to intermediate steps or outcomes. Finally, Panel 3 shows the "LLM after ExpRL" successfully solving the problem with a correct output marked by $r=1$, accompanied by a shift in the solution distribution indicating broader coverage.]  


>**Figure 1: Exploratory RL (ExpRL).** (1) On hard problems we fail to achieve high outcome-level correctness (sparse rewards) under the base LLM since it lacks coverage over diverse solutions needed to solve problems. (2) To build coverage, we mid-train the base LLM with our approach exploratory RL or ExpRL. In particular, we use unstructured auxiliary information (reference solutions on hard problems) to reward partial progress made by the base LLM via ExpRL-Outcome and ExpRL-Process rewards given by an LLM judge, and run RL with these rewards. (3) ExpRL is able to achieve non-trivial correctness, as judged by sparse outcome-level correctness, making it a well-primed initialization for subsequent sparse-reward RL.  


**Abstract:** Sparse reward reinforcement learning (RL) has become a standard tool for improving LLM reasoning, but its success depends critically on the coverage present in the base model. In practice, models are often primed for RL through *mid-training* on curated reasoning traces that teach useful primitive skills such as decomposition, verification, or self-correction. Although effective, this strategy requires manually specifying what the model should learn, and it remains unclear whether such primitive coverage is enough for much harder problems, which require combining these skills into broader solution strategies. We study a more automated approach: *RL-based mid-training* using large corpora of human-written question-answer data. Rather than treating reference solutions as targets to imitate, our method, ExpRL, uses them as *reward scaffolds*: references are hidden from the policy and used only to construct problem-specific grading rubrics for judging on-policy reasoning traces. The policy samples from the original problem prompt, while an LLM judge compares the sampled reasoning trace against the reference solution and assigns outcome-level or process-level dense rewards. This lets ExpRL reinforce partial progress, useful intermediate reductions, and productive reasoning behaviors that sparse final-answer rewards often fail to upweight. On challenging math reasoning tasks, ExpRL yields stronger RL priming than SFT, sparse-reward GRPO, and self-distillation, and provides a better initialization for subsequent sparse-reward RL. Additional mixed-domain experiments further suggest that ExpRL can extend beyond the original math-only setting.  


Code: https://github.com/violetxi/ExpRL  


# 1. Introduction  


Reinforcement learning (RL) has become a standard tool for improving the reasoning abilities of large language models (LLMs). Yet its success depends critically on the **coverage** present in the base model  


before RL begins. If the base model assigns very little probability to useful reasoning paths, then even many sampled attempts may produce few correct or partially correct trajectories. In this regime, sparse final-answer rewards give little signal to learn from, and RL mainly reinforces behaviors the model already samples well. Initialization is therefore a central bottleneck for scaling RL-based reasoning.  


The goal of mid-training is to improve this starting distribution before sparse-reward RL. Operationally, we want the model to place more probability mass on productive reasoning attempts across a wide range of hard problems, so that pass@$k$ improves and downstream RL has more useful trajectories to reinforce. This coverage is shaped both by primitive reasoning skills, such as decomposition, verification, backtracking, and self-correction [4], and by the model's ability to compose these skills into broader problem-solving techniques. For example, knowing how to check local computations does not mean the model can identify the right case split for a hard combinatorics problem and carry it through. Our aim is to build this broader coverage: not merely to improve correctness on the mid-training distribution, but to upweight productive reasoning paths that make later sparse-reward RL more effective. Operationally, we view pass@$k$ as an observable proxy for this coverage. If a policy assigns nontrivial probability mass to at least one complete productive reasoning path for a problem, then repeated sampling should eventually uncover a correct rollout. Thus, improvements in pass@$k$ indicate that mid-training has expanded the set of solution strategies the model can sample, even when pass@$1$ remains limited.  


In this work, we study how to use reference solutions for RL-based mid-training rather than imitation-based mid-training. When such reference solutions are available, a natural baseline is to convert them into supervised question-solution traces and fine-tune the model to imitate them. However, directly cloning traces that rely on solutions unlikely under the base model can disrupt its reasoning abilities [9, 21]. Another baseline in this reference-solution setting is on-policy self-distillation, as explored in [7]. This reduces the off-policy mismatch from SFT by training on the model's own rollouts, but the supervision signal still comes from token-level targets induced by a privileged teacher. When this target distribution is far from what the student can reliably produce, such supervision may hurt generalization [10]. Thus, imitation and distillation are natural baselines when reference solutions are available, but they may be limited mechanisms for broadening coverage over productive reasoning paths.  


We therefore propose **Exploratory RL** (**ExpRL**), an RL-based mid-training method that uses reference solutions to provide dense rewards for on-policy reasoning traces. Rather than exposing references as demonstrations or hints, ExpRL uses them as reward scaffolds: it helps the judge construct a problem-specific rubric for scoring partial progress in the actor's on-policy rollout. Because the policy samples only from the original problem prompt, this preserves on-policy exploration while providing richer feedback than the typical sparse outcome-level correctness rewards.  


Concretely, ExpRL assigns each on-policy rollout a partial progress score by comparing it with a reference solution for the same problem. We study two variants: ExpRL-Outcome assigns a dense outcome-level reward to the full rollout. ExpRL-Process rewards intermediate prefixes with dense scores, giving local credit to partial progress. These rewards can reinforce promising decompositions, correct intermediate reductions, or useful solution structures even when the model does not yet solve the problem fully. In this way, reference solutions help RL upweight productive reasoning paths without exposing the reference to the actor as a target trajectory or oracle prefix.  


We evaluate ExpRL in an RL-priming setting on challenging answer-based math reasoning. We compare against SFT, sparse-reward GRPO, and self-distillation. ExpRL produces a stronger Stage-I policy and a better initialization for subsequent sparse-reward RL. The gains appear not only in pass@1 but also in  


pass@k and in the diversity of reasoning attempts, consistent with improved coverage over productive
reasoning paths. We also find that ExpRL changes the model's reasoning behavior, increasing verification,
self-correction, and backtracking relative to the base model. Finally, we test ExpRL in a broader mixed-
domain setting and analyze when reference-conditioned judging provides reliable rewards. These results
suggest that ExpRL can serve as a general priming interface using reference answers.  


# 2. Preliminaries, Definitions, and Notation  


**Problem setup.** We are given a large dataset $\mathcal{D}_{\text{mid}} = \{(\mathbf{x}_i, \mathbf{y}_i^\star)\}_{i=1}^N$, where $\mathbf{x}_i$ denotes a problem and $\mathbf{y}_i^\star$ is a step-by-step reference solution. Typically, these reference solutions are human-written and may differ substantially in style from LLM-generated reasoning traces. We use $\pi_\theta$ to denote an LLM policy with trainable parameters $\theta$, and $\pi_b$ to denote the base pre-trained LLM. Our goal is to train $\pi_b$ on $\mathcal{D}_{\text{mid}}$ so as to build broader coverage over productive reasoning paths that will help it subsequently solve problems from a downstream dataset $\mathcal{D}'$ (which may or may not be similar to $\mathcal{D}_{\text{mid}}$) when trained further with RL using only a sparse binary outcome reward $r(\mathbf{x}, \mathbf{y}) \in \{0, 1\}$, indicating whether the rollout's final answer is correct (e.g., by string-matching a final boxed answer).  


**Evaluating exploratory capabilities.** Our primary downstream metric is pass@1 after Stage-II sparse-reward RL on $\mathcal{D}'$, which measures reliable single-sample performance. We also report pass@k, the probability of sampling at least one correct rollout in $k$ independent attempts, as an operational proxy for coverage under sampling. Higher pass@k indicates that the policy assigns more probability mass to reasoning paths that can lead to a correct solution. We measure pass@k on $\mathcal{D}_{\text{mid}}$ to diagnose whether RL priming increases coverage where reference-guided rewards are applied, and on $\mathcal{D}'$ to test whether this exploratory capability transfers to downstream sparse-reward RL.  


**RL priming for downstream RL.** We use *RL priming* to refer to any (mid-)training procedure that prepares a base model for a downstream later RL stage with binary rewards. *E.g.*, for math reasoning this would mean imbuing a base model with the ability to compose primitive skills into productive reasoning paths needed for downstream RL on hard problems. Ultimately, we say that a model is well primed for downstream RL if its pass@k on $\mathcal{D}'$ is large.  


**RL algorithms.** As we discuss shortly, our approach for RL priming will involve running RL with a dense reward signal applied at both outcome level (in the end) and *process level* (intermediate points). For our RL runs with outcome rewards (dense or sparse), we use GRPO [6] with normalization applied across $n$ rollouts per problem. For our implementation of process rewards, we use the REINFORCE [1] update. Here, we still sample $n$ rollouts per problem and compute the following gradient for the current policy $\pi$ given a batch of problems $\mathbf{x}_1, \ldots, \mathbf{x}_N$, each with $n$ responses. The batch gradient $\nabla_{\pi} J(\pi)$ is then given by:  


$$ \nabla_{\pi}J(\pi):=\frac{1}{N}\sum_{i\in[N]}\frac{1}{n}\sum_{j\in[n]}\sum_{k\in[|\mathbf{y}_{j}|]}A(\mathbf{x}_{i},\mathbf{y}_{\mathbf{i}}^{*},y_{i}^{k})\cdot\nabla_{\pi}\log\pi(y_{i}^{k}\mid\mathbf{y}_{i}^{<k}) $$  


(1)  


In the above expression $\pi(y_j^k \mid \mathbf{y}_j^{<k})$ is the probability of the $k^{\text{th}}$ token in response $\mathbf{y}_j$. In particular, note that the advantage $A(\mathbf{x}_i, y_j^k)$ is computed at the token level since rewards and advantages differ at different positions in a rollout, when using process rewards. Later we outline our construction of the advantage function for this setting.  


# 3. ExpRL: Reference-Guided Dense Rewards for RL Priming  


In this section, we introduce ExpRL, an RL-based priming stage before downstream sparse outcome-reward RL. ExpRL uses dense (non-binary) rewards at the outcome or process level derived from reference solutions on a broad mid-training dataset of question-answer pairs. RL with these dense rewards is intended to broaden coverage over productive reasoning paths. Stage-I gains in pass@1 and pass@$k$ serve as diagnostics that the primed policy assigns more probability mass to trajectories that can reach correct solutions. The aim is not to hand-specify isolated skills, but to induce a broader repertoire of useful reasoning behaviors for subsequent sparse-reward RL to reinforce. As reflected by the poor pass@$k$ for the base model (Qwen3-4B-Instruct) in Table 2, it is clear that it lacks sufficient coverage over reasoning paths even though it may consist of useful reasoning behaviors. Since human-written solutions are substantially different from the model's own reasoning traces, directly acquiring such coverage through offline training (e.g., SFT) is challenging [21], which motivates an on-policy RL procedure.  


**Design principle for ExpRL.** Since the goal of ExpRL is to broaden the model's coverage, a sparse outcome reward on final correctness for sampled on-policy rollouts is insufficient on questions in the mid-training data. It only indicates whether a rollout eventually reaches a correct answer, without discriminating between rollouts that make useful intermediate progress and those that do not. Our design principle is therefore to reward on-policy traces based on how likely they are to reach reference solutions for problems in the mid-training data, using a dense reward even when the overall trace is incorrect. As long as the mid-training dataset contains hard questions that require diverse reasoning patterns, this procedure should help shift probability mass toward more productive reasoning paths and provide a stronger initialization that covers useful reasoning paths for downstream RL. ExpRL uses an LLM-based judge to measure similarity to reference solutions and instantiates this principle through both outcome-level and process-level rewards, as we discuss next.  


**Concrete approach: RL priming via dense reference-guided rewards.** Building on this principle, our approach uses reference solutions to construct dense rewards. Doing so is possible because modern LLMs are often better at verifying partial progress against a reference than at generating a correct solution from scratch. We exploit this verification-generation gap to assign informative scores, thereby ranking sampled traces by how much useful progress they exhibit. Optimizing these rewards shifts probability mass toward regions of the space of traces that are more likely to result in an eventual success, improving pass@$k$ and, more importantly, building a stronger exploration prior for subsequent sparse reward RL.  


**Step I: Assigning numerical dense rewards via reference-guided verification.** To obtain dense signals, we ask the model to compare self-generated solutions against provided reference solutions. We instantiate our base model as our LLM judge $J$ that scores a candidate solution $\mathbf{y}$ by comparing it to the reference $\mathbf{y}^*$ under a fixed rubric, which measures alignment between the generated trace and techniques or high-level strategies in the reference solution (see Appendix A.1.2 for the rubric). Formally, given $(\mathbf{x}, \mathbf{y}, \mathbf{y}^*)$, the judge outputs a score $\tilde{s}(\mathbf{x}, \mathbf{y}, \mathbf{y}^*) \in \{1, 2, 3, 4, 5\}$:  


$$ s(\mathbf{x},\mathbf{y},\mathbf{y}^{\star})=\frac{\tilde{s}(\mathbf{x},\mathbf{y},\mathbf{y}^{\star})-1}{4}\in[0,1]. $$  


The judge is explicitly instructed to *verify rather than solve* and not to introduce missing steps, fill in unstated intermediate results, or correct errors in the model output. If a rubric item is not directly supported by the text of $\mathbf{y}$, it is scored as being absent. Because the entire reference solution $\mathbf{y}^*$ is available, this comparison yields a dense learning signal even when rollouts with correct final answers are rarely sampled by the model on problems in the mid-training set. After generating these rewards, we  


use them downstream in two ways to instantiate ExpRL.  


a) ExpRL-Outcome. Using the reference-guided score, we define an ExpRL-Outcome reward on full traces sampled from the mid-training data: $s(\mathbf{x}, \mathbf{y}, \mathbf{y}^*)$. Unlike sparse outcome rewards, this provides graded feedback to partially correct solutions that match the reference under the rubric but fail later, preserving distinctions among unsuccessful rollouts and providing useful signal even when fully correct solutions are rarely sampled. These rewards are used only during exploratory mid-training and need not perfectly reflect task success, as long as they encourage exploration over productive reasoning paths.  


b) ExpRL-Process. While outcome-level dense rewards provide a more frequent learning signal compared to sparse outcome, they do not localize credit within the sampled rollout. To improve credit assignment, we also consider a process-level reward from partial rollouts, i.e., rollout prefixes. Given a generated solution $\mathbf{y}$, we form a sequence of prefixes $\{\mathbf{y}_{\le t}\}_{t=1}^T$ according to a fixed rule for slicing prefixes (that we discuss in A.1.1), and apply the same judge to each prefix to obtain:  


$$ s_{t}=s(\mathbf{x},\mathbf{y}_{\leq t},\mathbf{y}^{\star}),\qquad t=1,\ldots,T. $$  


These prefix scores provide intermediate feedback about partial progress toward the reference solution.
Intuitively, process-level rewards encourage early decisions that are predictive of eventual success, while
avoiding over-crediting prefixes that later degrade.  


**Process-level advantage normalization.** Although $\{s_t\}_{t=1}^T$ provides absolute judge scores for each prefix, we convert them into *centered* segment-level advantages to emphasize *relative* partial progress rather than absolute score calibration across problems. Specifically, we use  


$$ A_{t}(x,y)=\begin{cases}s_{t}-s_{t-1},&\mathrm{i f}t>1,\\ s_{1}-s_{T},&\mathrm{i f}t=1.\end{cases} $$  


(2)  


For $t > 1$, a segment receives positive advantage only if it improves judged alignment with the reference relative to the previous prefix, and negative advantage if it reflects regression. This encourages the policy to build on intermediate progress. We center the first segment as $A_1 = s_1 - s_T$ rather than using $A_1 = s_1$ directly, so that its scale is comparable to later differences and the first step does not dominate the update. We use this $A_t$ as the process-level learning signal in the on-policy objective below.  


**Step II: Optimization objective and training details.** We optimize the policy using on-policy RL with KL regularization against a reference policy $\pi_0$:  


$$ \operatorname*{m a x}_{\theta}\mathbb{E}_{(\mathbf{x},\mathbf{y}^{\star})\sim\mathcal{D}_{\mathrm{m i d}}}\left[\mathbb{E}_{\mathbf{y}\sim\pi_{\theta}(\cdot|\mathbf{x})}\left[R(\mathbf{x},\mathbf{y},\mathbf{y}^{\star})\right]-\beta\mathrm{K L}(\pi_{\theta}(\cdot\mid\mathbf{x})\parallel\pi_{0}(\cdot\mid\mathbf{x}))\right], $$  


(3)  


where $R$ denotes the outcome or process-level dense rewards defined above. In particular, for ExpRL-Outcome rewards, we use $s(\mathbf{x}, \mathbf{y}, \mathbf{y}^*)$ directly and apply a GRPO-style update that normalizes scores across the batch. For ExpRL-Process rewards, we instead substitute the advantages from Equation 2 into the GRPO update, and do not apply any other normalization. Since this stage is used only for mid-training, the rewards need not be perfectly accurate; they only need to encourage broad and diverse behaviors. We ablate alternative normalization strategies for process advantages in Appendix A.2.  


**Running downstream RL after ExpRL.** After mid-training with ExpRL, we initialize downstream RL from the primed policy and train on the target dataset $\mathcal{D}'$ using the standard sparse outcome reward. The downstream objective and reward structure are unchanged; only the initialization differs. In  


implementation, we use two different on-policy RL pipelines (details in A.1) for Stage 1 and Stage 2, replacing the reference-guided dense rewards used by ExpRL with binary final-answer rewards during downstream RL. By shifting probability mass toward productive reasoning trajectories before sparse-reward training begins, ExpRL increases the likelihood that downstream RL encounters informative rollouts early in training.  


## Summary: Mid-Training via Exploratory RL or ExpRL  


ExpRL is an online RL approach for mid-training that uses reference solutions to define dense outcome/process rewards rather than traces to imitate. By rewarding partial progress rather than pure correctness, it shifts probability mass toward productive reasoning paths, building stronger coverage for later sparse reward RL.  


