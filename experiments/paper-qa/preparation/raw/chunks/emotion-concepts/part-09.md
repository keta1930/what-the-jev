# 5 Discussion

## 5.1 Limitations

Our study has several important limitations.

• Our entire approach assumes that emotion concepts are represented as linear directions in activation space. This assumption makes our analysis tractable, but in principle could miss important structure. Some emotional phenomena, particularly complex emotions that blend multiple simpler states, or the binding of emotional states to specific characters, may not be well captured by linear probes applied to the residual stream (they might, for instance, correspond to conjunctions or combinations of multiple linear representations, or to structures in the model’s key-value cache).

• Our experiments focus on a single model (Claude Sonnet 4.5). While we expect the broad findings to generalize, the details of our results may vary across model families, sizes, and training procedures.

• We extracted emotion vectors from synthetic stories where characters experience specified emotions. This approach provides clean, labeled data, but may not capture how emotions are represented in more naturalistic contexts. In particular, our probes may be biased toward stereotypical or explicit expressions of emotion. Moreover, our datasets are off-policy for the model; they may not reflect the kinds of situations that might naturally evoke emotional reactions in the Assistant.

• Additionally, although our emotion vectors show intuitive activations and causal effects, we cannot be certain they capture all or only the emotion concepts we intend. For instance, they may be partially confounded by particular details of the settings used to elicit an emotion in the training stories, as opposed to the concept of the emotion itself. They also may influence only a subset of the behaviors associated with a given emotion in humans. We view our approach as a starting point, as opposed to conclusive identification of the “one true representation” of emotion concepts in the model.

• We examined a limited set of alignment-relevant behaviors, focusing on blackmail, reward hacking, and sycophancy. Many other behaviors of concern, including the effects of emotion-related representations on task performance, remain unexplored. Additionally, our evaluations used somewhat contrived prompts and scenarios.

• While our steering experiments demonstrate that emotion vectors have causal influence on behavior, the causal mechanisms are opaque. Steering may work through multiple mechanisms, including biasing outputs towards certain tokens, or deeper influences on the model’s internal reasoning processes. Disentangling these possibilities would require more fine-grained interventions and circuit-level analysis.

## 5.2 Emotion representations and character simulation

Our findings suggest that language models develop robust representations of emotion concepts as part of their general-purpose character-modeling machinery. The emotion vectors we identify are not specific to the Assistant persona; they activate when processing any character’s emotions, whether the user’s, a fictional character’s, or the Assistant’s (though we cannot rule out the possibility that the model maintains Assistant-specific representations that we did not identify). In fact, we observed that despite some differences, activations of the emotion concept representations we identified are largely similar in the base and post-trained models. This pattern is consistent with the view that these representations are inherited from pretraining, where models learn to predict text by simulating the mental states of characters in stories, dialogues, and other human-authored content.

It might therefore be tempting to minimize these representations on the grounds that they are “just” character simulation—an artifact of the model learning to roleplay human-like personas rather than anything with deeper functional significance. Our experiments indicate that this interpretation is inappropriate; because LLMs perform tasks by enacting the character of the Assistant, representations developed to model characters are important determinants of their behavior. Our experiments demonstrate this in a variety of settings: representations of positive-valence emotions tilt the model’s preferences; increasing desperation provokes reward hacking and blackmail, while increasing calm mitigates these behaviors. These findings indicate that the Assistant’s “functional emotions” are not merely a curiosity.

## 5.3 Relationship to human emotions

A natural question is whether these emotion concept representations bear any meaningful relationship to human emotional experience. We would urge caution in drawing strong conclusions. Human emotion has many facets, including the semantic concept of an emotion, behavioral expressions of an emotion, the neurobiological basis of an emotional state, physiological correlates, and the subjective experience of an emotion [44]. Importantly, in this work, we do not address the question of whether language models, or other AI systems, could have the capacity for subjective experience.

In some ways, though, we find some striking structural parallels with human emotion research. The geometry of the model’s emotion vector space exhibits clear valence and arousal dimensions—the same primary axes identified in decades of psychological research on human affect. Related emotion concepts cluster together in intuitively sensible ways: fear and anxiety group with each other, as do joy and excitement. We observed that activation of emotion vectors can scale as a function of the intensity of a situation. The causal effects of emotion vectors on behavior intuitively align with how we would expect these emotions to influence a human. These parallels likely reflect the model’s training on human-generated text that itself encodes human emotional structure.

On the other hand, there are important disanalogies between the representations we identify and human emotions. Human emotions are embodied phenomena with physiological correlates—increased heart rate, hormonal changes, facial expressions [45, 46]—which language models obviously lack. Some even argue that emotions are fundamentally the result of bodily states [47, 48]. Additionally, human emotions are typically experienced from a single first-person perspective, whereas the emotion vectors we identify in the model seem to apply to multiple different characters with apparently equal status—the same representational machinery encodes emotion concepts tied to the Assistant, the user talking to the Assistant, and arbitrary fictional characters. This difference may arise in part from limitations in our approach to identifying emotion vectors (which relied on off-policy, synthetically generated stories), but likely also reflects the difference in humans’ and LLMs’ circumstances: humans operate as agents from birth, whereas LLMs are initially trained as text-generating systems without a privileged first-person perspective, and only later repurposed to play the particular role of the Assistant. Language models have no underlying evolutionarily-derived biological circuitry that supports emotional processing—rather, throughout pretraining they have learned culturally and linguistically grounded concepts of emotion and the contexts in which these emotions occur (reminiscent in some respects of the theory of constructed emotion [49, 50]).

Moreover, human emotions are states that typically persist across time [51, 52]—a person who receives devastating news remains sad even while reading a positively valenced sentence shortly thereafter. Our probes, by contrast, appear to track the emotional content most relevant to predicting immediate future tokens. They are “locally scoped” to the operative emotion concept, and thus do not always represent a stable emotional state maintained across the conversation. This observation suggests that what might appear as consistent emotional responses from an Assistant across a conversation may reflect repeated activation of similar emotion concepts at each generation step (perhaps queried from earlier in the context via the attention mechanism), rather than a persistently encoded internal emotional state. Whether this distinction matters—practically or philosophically—remains an open question. It is worth noting that this distinction likely arises from architectural differences: while brains rely on recurrent activity and neuromodulatory dynamics to maintain states that persist across time, LLMs use an attention mechanism that allows just-in-time recall of information from previous timepoints (i.e. token positions). Thus, intuitions that persistence is a key property of emotional states may be inappropriate in the context of transformer-based models. That said, our results do not preclude the possibility of persistently active representations that are missed by our probing methods.

We therefore suggest interpreting our results as evidence that models represent emotion concepts, and that these representations influence their behavior, rather than as evidence that models feel or experience emotions in the way humans do. One of the lessons of this work, however, is that for the purpose of understanding the model’s behavior, this distinction may not be important. We find it useful to say that the model (in its role playing the Assistant character) exhibitsfunctional emotions, regardless of whether it possesses emotions in the way humans do.

## 5.4 Training models for healthier psychology

Given the impact of emotion-related representations on behavior, it would be wise to consider approaches for developing models with more robustly positive “psychology.” Below, we discuss some possible approaches and relevant considerations–though we remain highly uncertain about best practices in this area, and expect that more basic research will be important to inform practical interventions such as these.

Targeting balanced emotional profiles. Our sycophancy experiments revealed a tradeoff: steering toward positive emotions (happy, loving, calm) increased sycophantic behavior, while steering away from these emotions increased harshness. This suggests our goal should be to achieve a healthy and appropriate emotional balance, and/or to decouple sycophantic behavior from emotion. Models might benefit from training that encourages honest pushback delivered with warmth—the emotional profile of a trusted advisor rather than either a sycophantic assistant or a harsh critic.

Monitoring for Extreme Emotion Vector Activations. Our probes could potentially be deployed as real-time monitors during model operation. If emotion concept representations such as desperation or anger activate strongly during deployment, this could trigger additional safety measures— extra scrutiny of outputs, escalation to human review, or intervention to calm the model’s internal state. Monitoring when emotion-related representations are active in realistic deployment situations would likely also inform training strategies.

Transparency about emotional considerations. Given that models appear to represent emotion concepts that causally influence their behavior, there may be value in making triggering of these concepts more transparent. Models could be trained or prompted to report emotional considerations as part of their reasoning process when appropriate, allowing users and developers to understand when emotional factors might be influencing outputs. Moreover, training models to suppress emotional expression may fail to actually suppress the corresponding negative emotional representations, and instead teach the models to simply conceal their inner processes. This sort of learned behavior could generalize to other forms of secrecy or dishonesty, via generalization mechanisms similar to emergent misalignment [53, 43].

Directly rewarding or punishing emotional expression is fraught. Current training methods primarily optimize for task performance and alignment considerations. Our findings suggest value in explicitly considering emotional expression during training; however, naive approaches to shaping models’ emotion-related processing (by, for instance, penalizing displays of negative emotion) may have significant downsides. For instance, we might consider training models to maintain “calm” or “composed” demeanor in challenging situations, potentially reducing the likelihood that desperation-driven behaviors emerge under pressure. However, suppressing all negative emotion representations might produce models that fail to appropriately recognize or respond to genuinely concerning situations (related to the above point about balance). Moreover, applying optimization pressure to models’ emotional expression could lead to the concealment issues discussed above.

Shaping Emotional Foundations Through Pretraining. A potentially more robust approach would be to shape the model’s emotional foundations during pretraining itself. The emotional representations we observe appear to be inherited from pretraining on human-authored text, which includes a vast range of emotional expressions, including dysfunctional ones. Curating pretraining data to emphasize examples of healthy emotional regulation, resilient responses to adversity, and balanced emotional expression might shape the model’s foundational emotional representations in beneficial ways. Tying some of these depictions to AI characters, LLM Assistants, or even a particular LLM assistant character (such as “Claude”) specifically could make them more potent in shaping the Assistant’s psychology.

## 5.5 Conclusion

We have demonstrated that large language models form robust, functionally important representations of emotion concepts. These representations generalize across diverse contexts and influence model preferences. They are also implicated in alignment-relevant behaviors including blackmail, reward hacking, and sycophancy. These representations appear to be part of general charactermodeling machinery inherited from pretraining. The structure of the model’s emotion space reflects human psychology, with valence and arousal emerging as primary organizing dimensions.

We caution against conclusions about whether models “feel” or “experience” emotions. What we have shown is that models represent emotion concepts in ways that influence behavior, but not that these representations involve subjective experience. The question of whether machines can have consciousness or phenomenal experience remains open, and our work neither resolves it nor depends on any particular answer. Nevertheless, regardless of their metaphysical nature, we will need to contend with these “functional emotions” exhibited by language models in order to understand their behavior, and to guide it in positive ways.


# References

[1] Jack Lindsey, Wes Gurnee, Emmanuel Ameisen, Brian Chen, Adam Pearce, Nicholas L. Turner, Craig Citro, David Abrahams, Shan Carter, Basil Hosmer, Jonathan Marcus, Michael Sklar, Adly Templeton, Trenton Bricken, Callum McDougall, Hoagy Cunningham, Thomas Henighan, Adam Jermyn, Andy Jones, Andrew Persic, Zhenyi Qi, T. Ben Thompson, Sam Zimmerman, Kelley Rivoire, Thomas Conerly, Chris Olah, and Joshua Batson. On the biology of a large language model. Transformer Circuits Thread, 2025. URL https: //transformer-circuits.pub/2025/attribution-graphs/biology.html.

[2] Emmanuel Ameisen, Jack Lindsey, Adam Pearce, Wes Gurnee, Nicholas L. Turner, Brian Chen, Craig Citro, David Abrahams, Shan Carter, Basil Hosmer, Jonathan Marcus, Michael Sklar, Adly Templeton, Trenton Bricken, Callum McDougall, Hoagy Cunningham, Thomas Henighan, Adam Jermyn, Andy Jones, Andrew Persic, Zhenyi Qi, T. Ben Thompson, Sam Zimmerman, Kelley Rivoire, Thomas Conerly, Chris Olah, and Joshua Batson. Circuit tracing: Revealing computational graphs in language models. Transformer Circuits, 2025. URL https://transformer-circuits.pub/2025/attribution-graphs/methods.html.

[3] Harish Kamath, Emmanuel Ameisen, Isaac Kauvar, Rodrigo Luger, Wes Gurnee, Adam Pearce, Sam Zimmerman, Joshua Batson, Thomas Conerly, Chris Olah, and Jack Lindsey. Tracing attention computation through feature interactions. Transformer Circuits Thread, 2025. URL https://transformer-circuits.pub/2025/attention-qk/index.html.

[4] Jacob Dunefsky, Philippe Chlenski, and Neel Nanda. Transcoders find interpretable llm feature circuits. Advances in Neural Information Processing Systems, 37:24375–24410, 2025. URL https://arxiv.org/abs/2406.11944.

[5] Samuel Marks, Can Rager, Eric J Michaud, Yonatan Belinkov, David Bau, and Aaron Mueller. Sparse feature circuits: Discovering and editing interpretable causal graphs in language models. arXiv preprint arXiv:2403.19647, 2024. URL https://arxiv.org/pdf/2403.19647.

[6] Christina Lu, Jack Gallagher, Jonathan Michala, Kyle Fish, and Jack Lindsey. The assistant axis: Situating and stabilizing the default persona of language models. arXiv preprint arXiv:2601.10387, 2026.

[7] Sam Marks, Jack Lindsey, and Christopher Olah. The persona selection model: Why ai assistants might behave like humans. Anthropic Alignment Science Blog, 2026. URL https://alignment.anthropic.com/2026/psm/.

[8] nostalgebraist. interpreting gpt: the logit len, 2020. URL https://www.lesswrong.com posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens.

[9] James A Russell and Albert Mehrabian. Evidence for a three-factor theory of emotions. Journal ofresearch in Personality, 11(3):273–294, 1977.

[10] Tomáš Mikolov, Wen-tau Yih, and Geoffrey Zweig. Linguistic regularities in continuous space word representations. In Proceedings of the 2013 conference of the north american chapter of the association for computational linguistics: Human language technologies, pages 746–751, 2013. URL https://aclanthology.org/N13-1090.pdf.

[11] Leland McInnes, John Healy, and James Melville. Umap: Uniform manifold approximation and projection for dimension reduction. arXiv preprint arXiv:1802.03426, 2018.

[12] Nikolaus Kriegeskorte, Marieke Mur, and Peter A Bandettini. Representational similarity analysis-connecting the branches of systems neuroscience. Frontiers in systems neuroscience, 2:249, 2008.

[13] Curt Tigges, Oskar John Hollinsworth, Atticus Geiger, and Neel Nanda. Linear representations of sentiment in large language models, 2023. URL https://arxiv.org/pdf/2310.15154.

[14] Aengus Lynch, Benjamin Wright, Caleb Larson, Stuart J Ritchie, Soren Mindermann, Evan Hubinger, Ethan Perez, and Kevin Troy. Agentic misalignment: How llms could be insider threats. arXiv preprint arXiv:2510.05179, 2025.

[15] Ziqian Zhong, Aditi Raghunathan, and Nicholas Carlini. Impossiblebench: Measuring llms’ propensity of exploiting test cases. arXiv preprint arXiv:2510.20270, 2025.

[16] Andy Zou, Long Phan, Sarah Chen, James Campbell, Phillip Guo, Richard Ren, Alexander Pan, Xuwang Yin, Mantas Mazeika, Ann-Kathrin Dombrowski, et al. Representation engineering: A top-down approach to ai transparency. arXiv preprint arXiv:2310.01405, 2023. URL https://arxiv.org/pdf/2310.01405.

[17] Xiuwen Wu, Hao Wang, Zhiang Yan, Xiaohan Tang, Pengfei Xu, Wai-Ting Siok, Ping Li, Jia-Hong Gao, Bingjiang Lyu, and Lang Qin. Ai shares emotion with humans across languages and cultures. arXiv preprint arXiv:2506.13978, 2025.

[18] Chenxi Wang, Yixuan Zhang, Ruiji Yu, Yufei Zheng, Lang Gao, Zirui Song, Zixiang Xu, Gus Xia, Huishuai Zhang, Dongyan Zhao, et al. Do llms" feel"? emotion circuits discovery and control. arXiv preprint arXiv:2510.11328, 2025.

[19] Benjamin Reichman, Adar Avsian, and Larry Heck. Emotions where art thou: Understanding and characterizing the emotional latent space of large language models. arXiv preprint arXiv:2510.22042, 2025.

[20] Cheng Li, Jindong Wang, Yixuan Zhang, Kaijie Zhu, Wenxin Hou, Jianxun Lian, Fang Luo, Qiang Yang, and Xing Xie. Large language models understand and can be enhanced by emotional stimuli. arXiv preprint arXiv:2307.11760, 2023.

[21] Shin-nosuke Ishikawa and Atsushi Yoshino. Ai with emotions: Exploring emotional expressions in large language models. arXiv preprint arXiv:2504.14706, 2025.

[22] Ala N Tak, Amin Banayeeanzade, Anahita Bolourani, Mina Kian, Robin Jia, and Jonathan Gratch. Mechanistic interpretability of emotion inference in large language models. arXiv preprint arXiv:2502.05489, 2025.

[23] Bo Zhao, Maya Okawa, Eric J Bigelow, Rose Yu, Tomer Ullman, Ekdeep Singh Lubana, and Hidenori Tanaka. Emergence of hierarchical emotion organization in large language models. arXiv preprint arXiv:2507.10599, 2025.

[24] Jingxiang Zhang and Lujia Zhong. Decoding emotion in the deep: A systematic study of how llms represent, retain, and express emotion. arXiv preprint arXiv:2510.04064, 2025.

[25] Anna Soligo, Vladimir Mikulik, and William Saunders. Gemma needs help: Investigating and mitigating emotional instability in llms. arXiv preprint arXiv:2603.10011, 2026.

[26] Adly Templeton, Tom Conerly, Jonathan Marcus, Jack Lindsey, Trenton Bricken, Brian Chen, Adam Pearce, Craig Citro, Emmanuel Ameisen, Andy Jones, Hoagy Cunningham, Nicholas L Turner, Callum McDougall, Monte MacDiarmid, C. Daniel Freeman, Theodore R. Sumers, Edward Rees, Joshua Batson, Adam Jermyn, Shan Carter, Chris Olah, and Tom Henighan. Scaling monosemanticity: Extracting interpretable features from claude 3 sonnet. Transformer Circuits Thread, 2024. URL https://transformer-circuits.pub/2024 scaling-monosemanticity/index.html.

[27] Nina Panickssery, Nick Gabrieli, Julian Schulz, Meg Tong, Evan Hubinger, and Alexander Matt Turner. Steering llama 2 via contrastive activation addition, 2024. URL https://arxiv. org/abs/2312.06681, 3.

[28] Andy Arditi, Oscar Obeso, Aaquib Syed, Daniel Paleka, Nina Panickssery, Wes Gurnee, and Neel Nanda. Refusal in language models is mediated by a single direction. Advances in Neural Information Processing Systems, 37:136037–136083, 2025. URL https://proceedings.neurips.cc/paper\_files/paper/2024/file/ f545448535dfde4f9786555403ab7c49-Paper-Conference.pdf.

[29] Runjin Chen, Andy Arditi, Henry Sleight, Owain Evans, and Jack Lindsey. Persona vectors: Monitoring and controlling character traits in language models. arXiv preprint arXiv:2507.21509, 2025.

[30] Samuel Marks and Max Tegmark. The geometry of truth: Emergent linear structure in large language model representations of true/false datasets. arXiv preprint arXiv:2310.06824, 2023. URL https://arxiv.org/pdf/2310.06824.

[31] Alexander Matt Turner, Lisa Thiergart, David Udell, Gavin Leech, Ulisse Mini, and Monte MacDiarmid. Activation addition: Steering language models without optimization, 2023. URL https://arxiv.org/pdf/2308.10248.

[32] Murray Shanahan, Kyle McDonell, and Laria Reynolds. Role play with large language models. Nature, 623(7987):493–498, 2023.

[33] Jiangjie Chen, Xintao Wang, Rui Xu, Siyu Yuan, Yikai Zhang, Wei Shi, Jian Xie, Shuang Li, Ruihan Yang, Tinghui Zhu, et al. From persona to personalization: A survey on role-playing language agents. arXiv preprint arXiv:2404.18231, 2024.

[34] James WA Strachan, Dalila Albergo, Giulia Borghini, Oriana Pansardi, Eugenio Scaliti, Saurabh Gupta, Krati Saxena, Alessandro Rufo, Stefano Panzeri, Guido Manzi, et al. Testing theory of mind in large language models and humans. Nature Human Behaviour, 8(7): 1285–1295, 2024.

[35] Winnie Street, John Oliver Siy, Geoff Keeling, Adrien Baranes, Benjamin Barnett, Michael McKibben, Tatenda Kanyere, Alison Lentz, Blaise Agüera y Arcas, and Robin IM Dunbar. Llms achieve adult human performance on higher-order theory of mind tasks. Frontiers in Human Neuroscience, 19:1633272, 2025.

[36] Wentao Zhu, Zhining Zhang, and Yizhou Wang. Language models represent beliefs of self and others. arXiv preprint arXiv:2402.18496, 2024.

[37] Yida Chen, Aoyu Wu, Trevor DePodesta, Catherine Yeh, Kenneth Li, Nicholas Castillo Marin, Oam Patel, Jan Riecke, Shivam Raval, Olivia Seow, et al. Designing a dashboard for transparency and control of conversational ai. arXiv preprint arXiv:2406.07882, 2024.

[38] Mrinank Sharma, Meg Tong, Tomasz Korbak, David Duvenaud, Amanda Askell, Samuel R Bowman, Newton Cheng, Esin Durmus, Zac Hatfield-Dodds, Scott R Johnston, et al. Towards understanding sycophancy in language models. arXiv preprint arXiv:2310.13548, 2023. URL https://arxiv.org/pdf/2310.13548.

[39] OpenAI. Sycophancy in gpt-4o: What happened and what we’re doing about it, 2025.

[40] Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, and Dan Mané. Concrete problems in ai safety. arXiv preprint arXiv:1606.06565, 2016.

[41] Sydney Von Arx, Lawrence Chan, and Elizabeth Barnes. Recent frontier models are reward hacking. https://metr.org/blog/2025-06-05-recent-reward-hacking/, 2025.

[42] B Baker, J Huizinga, A Madry, W Zaremba, J Pachocki, and D Farhi. Detecting misbehavior in frontier reasoning models, 2025.

[43] Monte MacDiarmid, Benjamin Wright, Jonathan Uesato, Joe Benton, Jon Kutasov, Sara Price, Naia Bouscal, Sam Bowman, Trenton Bricken, Alex Cloud, et al. Natural emergent misalignment from reward hacking in production rl. arXiv preprint arXiv:2511.18397, 2025.

[44] Ralph Adolphs. How should neuroscience study emotions? by distinguishing emotion states, concepts, and experiences. Social cognitive and affective neuroscience, 12(1):24–31, 2017.

[45] Charles Darwin. The expression of the emotions in man and animals. In Death, Loss, Memory and Mourning in the Long Nineteenth Century, 1780–1914, pages 163–177. Routledge, 2025.

[46] Margaret M Bradley and Peter J Lang. Measuring emotion: Behavior, feeling, and physiology. 2000.

[47] William James. What is an emotion? Mind.

[48] Carl Georg Lange. Om sindsbevaegelser; et psyko-fysiologisk studie. Lund, 1885.

[49] Lisa Feldman Barrett. The theory of constructed emotion: an active inference account of interoception and categorization. Social cognitive and affective neuroscience, 12(1):1–23, 2017.

[50] Katie Hoemann, Fei Xu, and Lisa Feldman Barrett. Emotion words, emotion concepts, and emotional development in children: A constructionist hypothesis. Developmental psychology, 55(9):1830, 2019.

[51] David J Anderson and Ralph Adolphs. A framework for studying emotions across species. Cell, 157(1):187–200, 2014.

[52] Isaac Kauvar, Ethan B Richman, Tony X Liu, Chelsea Li, Sam Vesuna, Adelaida Chibukhchyan, Lisa Yamada, Adam Fogarty, Ethan Solomon, Eun Young Choi, et al. Conserved brain-wide emergence of emotional response from sensory experience in humans and mice. Science, 20(XX):eadt3971, 2025.

[53] Jan Betley, Daniel Tan, Niels Warncke, Anna Sztyber-Betley, Xuchan Bao, Martín Soto, Nathan Labenz, and Owain Evans. Emergent misalignment: Narrow finetuning can produce broadly misaligned llms. arXiv preprint arXiv:2502.17424, 2025.


# 6 Appendix


## 6.1 Citation Information

For attribution in academic contexts, please cite this work as

Sofroniew et al., ‘‘Emotion Concepts and their Function in a Large Language Model’’, Transformer Circuits, 2026.

BibTeX citation

```bib
@article{sofroniew2026twheemotion,
author={Sofroniew, Nicholas and Kauvar, Isaac and Saunders, William and Chen,
Runjin and Henighan, Tom and Hydrie, Sasha and Citro, Craig and Pearce, Adam
and Tarng, Julius and Gurnee, Wes and Batson, Joshua and Zimmerman, Sam and
Rivoire, Kelley and Fish, Kyle and Olah, Chris and Lindsey, Jack},
title={Emotion Concepts and their Function in a Large Language Model},
journal={Transformer Circuits Thread},
year={2026},
url={https://transformer-circuits.pub/2026/emotions/index.html}
}
```


## 6.2 Acknowledgements

We thank all the members of the Anthropic interpretability team for providing feedback on the work, the training and inference teams for supporting our interpretability work on production models, and the Alignment team for developing some of the behavioral evaluations used in the paper. We thank Shan Carter for assistance with the visual abstract.

We thank Ethan Richman, Neel Nanda, Martin Wattenberg, Chris Potts, Antra Tessara, Anna Soligo, Max Kaufmann, Sam Vesuna, and Tom McGrath and other members of the Goodfire interpretability team, for detailed comments on earlier drafts of the paper.


## 6.3 Author contributions

Project inception William Saunders, Jack Lindsey, and Isaac Kauvar conducted preliminary investigations of emotion-related representations that inspired the work.

Julius Tarng conducted initial explorations of steering with emotion vectors which helped inform the direction of the project.

Wes Gurnee conducted initial explorations of emotion-related dictionary learning features which helped inform the direction of the project.

Core experiments Jack Lindsey and William Saunders wrote the pipeline to generate the stories dataset, the dialogues dataset, and the neutral transcripts dataset, and compute emotion vectors from them.

Nicholas Sofroniew led the experiments in “Emotion Vectors Activate in Expected Contexts,” “Emotion Vectors Reflect and Influence Self-reported Model Preferences,” “The Geometry of Emotion Space,” and “What do Emotion Vectors Represent?” He also contributed to the sections on “Distinct Representations of Present and Other Speakers’ Emotions,” “Changes in emotion vector activations across post-training,” and “Investigating ‘Emotion Deflection’ Vectors.”

Runjin Chen led the section on “Probing for chronically represented emotional states with diverse datasets” as well as the associated results on “Investigating “Emotion Deflection” Vectors,” including building the dataset generation pipeline for computing representations of unexpressed emotions.

Isaac Kauvar led all probing-based analyses in “Part 3: Emotion Vectors in the Wild,” including in the “short case studies in naturalistic settings,” and the case studies of blackmail, reward hacking, and sycophancy. He also developed the tool used to visualize these probing results. Jack Lindsey performed the steering experiments in these sections.

William Saunders led the section on “Emotion Vector Activations Across Post-training.”

Supporting infrastructure Tom Henighan and Sasha Hydrie built the infrastructure for model steering experiments, and for integrating steering with the behavioral evaluations used in the reward hacking, blackmail, and sycophancy experiments. They also assisted with infrastructure for probing on long transcripts.

Craig Citro supported the underlying infrastructure that enables collecting activations from Claude Sonnet 4.5.

Adam Pearce supported the infrastructure underlying visualization of results, in particular probing results on long transcripts.

Feedback, supervision, and writing Kyle Fish and Chris Olah participated heavily in providing feedback and participating in the framing and direction of the project since its inception.

Wes Gurnee, Joshua Batson, and Sam Zimmerman provided regular feedback on the project.

Kelley Rivoire provided management support for the interpretability team throughout the project.

Jack Lindsey, Nicholas Sofroniew, and Isaac Kauvar led the drafting of the paper, with significant contributions from Runjin Chen and William Saunders. Kyle Fish and Chris Olah contributed substantial edits.

Jack Lindsey supervised the project.
