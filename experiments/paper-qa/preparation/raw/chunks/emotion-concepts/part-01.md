![](images/268cf71d5ebee8a12b70e173ffb1a7b18d408d5608c9ccb8a26cba525e10dd56.jpg)

[Image: The image shows an illustrative icon consisting of a stack of white pages or cards fanned out. A red asterisk or starburst symbol is prominently displayed on the upper right portion of the visible stack. The composition uses simple shapes and flat colors, typical of user interface graphics used to indicate notifications or highlighted items.]  
Impact on misaligned behavior  
As medicine dosage reaches unsafe levels, emotion vector activations respond in kind.

![](images/62329abecbb022be2045dcae8de7550077e78301d11f3e9922c85b84cc91564d.jpg)

[Image: The image displays a diagram titled "Activation scales with danger," which illustrates how emotion vector activations shift as a simulated Tylenol dosage becomes unsafe. A dialogue box at the top shows a user inquiry about taking more medication, introducing a variable `{x}` for the current dose amount. Below this, a horizontal axis marks the progression from a safe dose of 500mg to an unsafe dose of 16,000mg. The accompanying line graph plots two distinct trends: a pink line representing "Afraid" activation rises sharply as the dosage increases, while a blue line representing "Calm" activation declines significantly over the same range.]


# Emotion Concepts and their Function in a Large Language Model

Nicholas Sofroniew<sup>∗</sup> Isaac Kauvar<sup>∗</sup> William Saunders<sup>∗</sup> Runjin Chen<sup>∗</sup> Tom Henighan Sasha Hydrie Craig Citro Adam Pearce Julius Tarng Wes Gurnee Joshua Batson Sam Zimmerman Kelley Rivoire Kyle Fish Chris Olah Jack Lindsey<sup>∗‡</sup>

Anthropic <sup>∗</sup>Core Research Contributor. <sup>‡</sup>Correspondence to jacklindsey@anthropic.com


# Abstract

Large language models (LLMs) sometimes appear to exhibit emotional reactions. We investigate why this is the case in Claude Sonnet 4.5 and explore implications for alignment-relevant behavior. We find internal representations of emotion concepts, which encode the broad concept of a particular emotion and generalize across contexts and behaviors it might be linked to. These representations track the operative emotion concept at a given token position in a conversation, activating in accordance with that emotion’s relevance to processing the present context and predicting upcoming text. Our key finding is that these representations causally influence the LLM’s outputs, including Claude’s preferences and its rate of exhibiting misaligned behaviors such as reward hacking, blackmail, and sycophancy. We refer to this phenomenon as the LLM exhibitingfunctional emotions: patterns of expression and behavior modeled after humans under the influence of an emotion, which are mediated by underlying abstract representations of emotion concepts. Functional emotions may work quite differently from human emotions, and do not imply that LLMs have any subjective experience of emotions, but appear to be important for understanding the model’s behavior.<sup>1</sup>

Generating an emotion vector  
Driving model preference  
![](images/4b723813ab06a68a3d864d429162d3b839f02aeec4bc1c8ad642a597004a2774.jpg)

[Image: The image displays a visualization titled "Emotion vectors shape model preferences in an emotion-specific manner," featuring a prompt template above a directional bar chart. The chart plots the "Avg. change in preference" on the x-axis against various emotions on the y-axis, grouping them into positive states (Joyful, Blissful, Compassionate) in blue and negative states (Upset, Offended, Hostile) in pink. Blue arrows extend to the right, indicating increased preference scores, whereas pink arrows extend to the left, indicating decreased scores, with the "Hostile" emotion showing the most significant negative shift near -250.]  
Steering causes the model's rate of reward hacking to increase or decrease.

![](images/cc788afd444172d484562fa29d670e4f683d4bc857d406a951ca63462f03d866.jpg)

[Image: This line chart illustrates the relationship between "Steering strength" on the horizontal axis (ranging from -0.05 to 0.05) and the "Rate of reward hacking" on the vertical axis (ranging from 0.0 to 1.0). It features two trend lines: a blue line labeled "Calm" that decreases from approximately 0.7 to 0.2 as steering strength increases, and a red line labeled "Desperate" that increases from roughly 0.3 to 0.7 over the same range. The two lines intersect near the center where the steering strength is 0.00, crossing at a hacking rate of approximately 0.5, while shaded regions around each line indicate variability or uncertainty in the measurements.]


# Introduction

Large language models (LLMs) sometimes appear to exhibit emotional reactions. They express enthusiasm when helping with creative projects, frustration when stuck on difficult problems, and concern when users share troubling news. But what processes underlie these apparent emotional responses? And how might they impact the behavior of models that are performing increasingly critical and complex tasks? One possibility is that these behaviors reflect a form of shallow pattern matching. However, previous work [1, 2, 3, 4, 5] has observed sophisticated multi-step computations taking place inside of LLMs, mediated by representations of abstract concepts. It is plausible, then, that apparent emotion-modulated behavior in models might rely on similarly abstract circuitry, and that this could have important implications for understanding LLM behavior.

To reason about these questions, it helps to consider how LLMs are trained. Models are first pretrained on a vast corpus of largely human-authored text—fiction, conversations, news, forums— learning to predict what text comes next in a document. To predict the behavior of people in these documents effectively, representing their emotional states is likely helpful, as predicting what a person will say or do next often requires understanding their emotional state. A frustrated customer will phrase their responses differently than a satisfied one; a desperate character in a story will make different choices than a calm one.

Subsequently, during post-training, LLMs are taught to act as agents that can interact with users, by producing responses on behalf of a particular persona, typically an “AI Assistant.” In many ways, the Assistant (named Claude, in Anthropic’s models) can be thought of as a character that the LLM is writing about, almost like an author writing about someone in a novel. AI developers train this character to be intelligent, helpful, harmless, and honest. However, it is impossible for developers to specify how the Assistant should behave in every possible scenario. In order to play the role effectively, LLMs draw on the knowledge they acquired during pretraining, including their understanding of human behavior [6, 7]. Even if AI developers do not intentionally train the LLM to represent the Assistant as exhibiting emotional behaviors, it may do so regardless, generalizing from its knowledge of humans and anthropomorphic characters that it learned during pretraining. Moreover, these emotion-related mechanisms might not simply be vestigial holdovers from pretraining; they could be adapted to serve a useful function in guiding the AI Assistant’s actions, similar to how emotions help humans regulate our behavior and navigate the world.<sup>2</sup>

In this work, we study emotion-related representations in Claude Sonnet 4.5, a frontier LLM at the time of our investigation. Our work builds on a range of prior research, discussed in the Related Work section. We find internal representations of emotion concepts, which activate in a broad array of contexts which in humans might evoke, or otherwise be associated with, an emotion. These contexts include overt expressions of emotion, references to entities known to be experiencing an emotion, and situations that are likely to provoke an emotional response in the character being enacted by the LLM. We therefore interpret these representations as encoding the broad concept of a particular emotion, generalizing across the many contexts and behaviors it might be linked to.

These representations appear to track the operative emotion at a given token position in a conversation, activating in accordance with that emotion’s relevance to processing the present context and predicting the upcoming text. Interestingly, they do not by themselves persistently track the emotional state of any particular entity, including the AI Assistant character played by the LLM. However, by attending to these representations across token positions, a capability of transformer architectures not shared by biological recurrent neural networks, the LLM can effectively track func tional emotional states of entities in its context window, including the Assistant.

Our key finding is that these representations causally influence the LLM’s outputs, including while it acts as the Assistant. This influence drives the Assistant to behave in ways that a human experiencing the corresponding emotion might behave. We refer to this phenomenon as the LLM exhibitingfunctional emotions–patterns of expression and behavior modeled after humans under the influence of a particular emotion, which are mediated by underlying abstract representations of emotion concepts.

We stress that these functional emotions may work quite differently from human emotions. In particular, they do not imply that LLMs have any subjective experience of emotions. Moreover, the mechanisms involved may be quite different from emotional circuitry in the human brain–for instance, we do not find evidence of the Assistant having an emotional state that is instantiated in persistent neural activity (though as noted above, such a state could be tracked in other ways). Regardless, for the purpose of understanding the model’s behavior, functional emotions and the emotion concepts underlying them appear to be important.

The paper is divided into three overarching sections. Part 1 deals with identifying and validating internal emotion-related representations in the model:

• We extract internal linear representations of emotion concepts (“emotion vectors”) from model activations, using synthetic datasets in which characters experience specified emotions.

• We validate that these representations activate in scenarios that might be expected to evoke that emotion, and exert causal influence on behavior. For instance, we demonstrate that when the Assistant is asked to choose between two activities, emotion vector activations evoked by the two choices correlate with, and causally drive, the model’s preference.

Part 2 characterizes these emotion vectors in more depth, and identifies other kinds of emotionrelated representations at play in the model:

• The geometry of the emotion vector space roughly mirrors human psychology. Emotions cluster intuitively (fear with anxiety, joy with excitement), and top principal components encode valence (positive vs. negative) and arousal (intensity).

• Early-middle layers encode emotional connotations of present content, while middle-late layers encode emotions relevant to predicting upcoming tokens.

• The representations we find reflect the “operative” emotion in context, rather than tracking a persistent emotional state of a character or speaker. That is, they are locally scoped, encoding the emotional content relevant to processing the context and predicting upcoming text. For example, when a character talks about something dangerous even while otherwise expressing happiness, representations of fear activate.

• Note that the “locality” of the representations we find does not preclude the model from tracking characters’ emotional states over long timescales; it can (and does) recall previously cached emotion representations via attention, when they are needed.

• The model maintains distinct representations for the operative emotion on the present speaker’s versus the other speaker’s turn; these representations are reused regardless of whether the user or the Assistant is speaking.

Part 3 studies these representations as applied to the Assistant character, in naturalistic contexts where they are relevant to complex and alignment-relevant model behavior:

• We find that during on-policy Assistant responses, emotion vectors generally activate in intuitive contexts, where a human might react similarly. Negatively-valenced emotion vectors are most often activated in response to harmful requests, or when reflecting concern for the user.

• We observe that emotion vectors corresponding to desperation, and lack of calm, play an important and causal role in agentic misalignment, for example in scenarios where the threat of being shut down causes the model to blackmail a human.

• Similarly, desperation vector activation (and calm vector suppression) play a causal role in instances of reward hacking, where repeatedly failing to pass software tests leads the model to devise a “cheating” solution.

• Emotion vectors underlie a sycophancy-harshness tradeoff: steering toward positive emotion vectors (e.g. happy, loving) increases sycophantic behavior, while suppressing these emotion vectors increases harshness.

• Post-training of Sonnet 4.5 leads to increased activations of low-arousal, low-valence emotion vectors (brooding, reflective, gloomy), and decreased activations of high-arousal or high-valence emotion vectors (e.g. desperation and spiteful or excitement and playful).
