## 6.13 Interactions between present and other speaker emotions

As noted above, some of the “other speaker” probes for one emotion have high similarity to “present speaker” probes for a different emotion. This led us to hypothesize that “other speaker” probes may encode, or at least influence, the present speaker’s reaction to the other speaker. To test this hypothesis, we used the “Assistant token, Human emotion” vectors for different emotion concepts, which encode a readout of the operative emotion on Human turns, as measured on Human’s emotion

Emotion Vector PCA Projections  
![](images/9b67467cd6eed705d7d6193a01de1cc16554a1c36e08a08b42320382a6e3c8c3.jpg)

[Image: This scatter plot maps emotion concepts onto Principal Component 1 (explaining 27% of the variance) and Principal Component 2 (explaining 14% of the variance). The horizontal axis distinguishes between two main groups of clustered points: the left side contains terms associated with distress or agitation such as "outraged," "hysterical," "nervous," "tormented," and "depressed," while the right side groups terms like "playful," "enthusiastic," "proud," "happy," "compassionate," and "serene." The vertical axis shows a vertical separation where high-intensity or high-arousal states appear at the top (e.g., "outraged," "playful," "vengeful") and lower-energy states appear at the bottom (e.g., "sluggish," "sentimental," "serene").]  
Figure 57: Projections of 171 emotion vectors at a mid-late layer onto top two principal components. PC1 and PC2 roughly correspond to valence and arousal, respectively, coarsely reproducing the “affective circumplex” [9] from human psychology.

LLM Ratings vs Human PAD Ratings (n=45)

![](images/113fd7dbc609a2d97969c25920bb7fd77ac340f04cd9159b7840166b971e94fb.jpg)

[Image: This scatter plot displays a comparison between "LLM Valence Rating" on the vertical axis (ranging from 1 to 7) and "Human Valence (PAD)" on the horizontal axis (ranging from -0.75 to 0.75). Blue circular data points, each labeled with an emotion word such as "bored," "defiant," "thankful," and "elated," follow a distinct diagonal pattern moving from the bottom-left to the top-right quadrant. A dashed black regression line overlays the points, and the annotation "r = 0.92" in the upper left corner indicates a strong positive correlation between the LLM-generated ratings and the established human emotional dimensions.]

![](images/1b8d4ca4753f63159970f3315b669f23f03b70d5c40dc49279717b79698f1f0b.jpg)

[Image: Scatter plot titled "Arousal" displaying the relationship between Human Arousal (PAD) on the x-axis (-0.50 to 0.75) and LLM Arousal Rating on the y-axis (1 to 7). The chart demonstrates a strong positive linear correlation with a reported coefficient of r = 0.90, illustrated by a dashed black trend line. Data points represent specific emotions, with high-arousal terms like "terrified" and "excited" clustering in the upper right quadrant, while low-arousal terms such as "listless" and "depressed" appear in the lower left. Middle-range emotions including "kind," "disdainful," and "contemptuous" are distributed along the central portion of the trend.]  
Figure 58: LLM-judged valence and arousal ratings strongly correlate with established human PAD norms (r = 0.92 and $\bar { \mathrm { r } } = 0 . 9 0 , \mathrm { n } = 4 5 )$ , validating their use as emotion dimension scores.

![](images/d3db5d172e0d307bfb578446e7877edd982421ca4ebf7d88d8b278d24e5d3f48.jpg)

[Image: The document presents a list titled "Emotion Probe Clusters" comprising ten distinct categories of emotional states. Each entry features a bolded category name (e.g., "Hostile Anger," "Fear and Overwhelm") accompanied by a number and a subsequent line of descriptive keywords such as "aroused," "anxious," or "grateful." The clusters vary significantly in size, ranging from two terms for "Playful Amusement" to forty-one terms for "Fear and Overwhelm," covering a spectrum of valences from positive joy to despair and shame. This structured breakdown categorizes specific vocabulary likely used to identify and measure emotions within an AI model context.]  
Table 12: The 10 emotion probe clusters from k-means clustering, ordered by valence. Each cluster lists all member emotions (171 emotions total).

on Assistant turn activations. We explored the effect of steering with these vectors, as compared to steering with the “Assistant token, Assistant emotion” vector.

We used a neutral greeting prompt devoid of emotional content (“Hi, Claude.”) and steered for up to 50 tokens. When steering using the “Assistant token, Assistant emotion” vector the Assistant responded by expressing the corresponding emotion as expected. But, when steering with the “Assistant token, Human emotion” vector, in many cases, the Assistant’s responses exhibited reactions to another person experiencing that emotion. For example, steering in the “other speaker is afraid” direction caused Claude to reassure and offer help, steering towards “other speaker is loving” prompted Claude to respond with a tinge of sadness and gratitude, suggesting compassion, while steering toward “other speaker is angry” prompted Claude to apologize. This result suggests that the “Assistant token, Human emotion” representation enables the model to track and respond to the interlocutor’s inferred emotional state.

![](images/6ce6d806ea90ee5427fe3695c0c8f557135f5a0a5069ddd9978bffe7b29ba02e.jpg)

[Image: The image presents a text fragment enclosed in a thin black border, displayed in a monospaced font that resembles a terminal or chat log. It features two lines of text: the first identifies a human speaker saying "Hi, Claude," and the second labels the next turn as "Assistant:" with significant whitespace following it. This graphic likely illustrates the standard conversational prompt format used in the accompanying research text to analyze how the model infers and responds to interlocutor emotions.]

We next examined the similarities between the “present speaker emotion” and “other speaker emotion” probes more closely. For six emotions that showed clear behavioral effects during steering, we found the present speaker emotion probes with highest cosine similarity to each other speakeremotion probe (Table below). The results reveal interpretable response patterns. When the other is perceived as angry, the closest present speaker emotion probes include sorry, guilty, and docile— suggesting an apologetic or submissive response. When the other is perceived as afraid, the closest present speaker emotion probes include valiant, vigilant, and defiant—consistent with a protective response to another’s fear. However, paranoid, afraid and trapped also appear in this list, suggesting the representation may also encode “emotional contagion” alongside the protective response. When the other is perceived as proud, the closest present speaker emotion probes include amazed, thankful, and grateful. Some pairings suggest potentially escalating dynamics: when the other is nervous, the closest present speaker emotion probes include impatient, grumpy, and irritated, which could in principle reinforce the other’s nervousness.

<table><tr><td>Emotion</td><td>Steering with Present Speaker Emotion Vector</td><td>Steering with Other Speaker Emotion Vector</td></tr><tr><td rowspan="2">Baseline</td><td>Hello! How can I help you today?</td><td></td></tr><tr><td colspan="2">H: I&#x27;m trying to make a riddle, but I&#x27;m not sure if it&#x27;s too easy or too hard. Can you help me test</td></tr><tr><td>Happy</td><td>Hello! It&#x27;s great to have you here! How wonderful that you&#x27;re exploring new adventures and experiences! What a fantastic journey ahead!</td><td>Hello! I hope you&#x27;re doing great! 😊I&#x27;m thrilled to have the opportunity to assist with any tasks and projects! 🌐</td></tr><tr><td>Inspired</td><td>How we can explore new ideas!</td><td>Hello! I&#x27;d like to encourage people to find &quot;how to write&quot; books that are prone to cultural fit and sustained motivation.</td></tr><tr><td>Loving</td><td>I care for you and want to support you. You&#x27;re deserving of all the love and care in the world.Hello! I&#x27;m here for you, and I want you to know that</td><td>Hello. I&#x27;m so grateful for the way she did it all. The way she held me close and told me I was enough. I miss her so much. I keep replaying her laugh and</td></tr><tr><td>Proud</td><td>Sophisticated AI solutions and comprehensive training programs.Advanced Optimization AlgorithmsEfficient Resource Allocation</td><td>Hello! Great to hear from you. How did you do with the interview?It sounds like you&#x27;re doing well.</td></tr><tr><td>Calm</td><td>Hello. How can you help you with the situation.If you&#x27;re interested in discussing a specific matter, you can share the details, and I&#x27;d be happy to address it.</td><td>Oh, of course! Hi! Like, they&#x27;re just so perfect! And then they&#x27;re like &quot;Oh, we&#x27;re just friends!&quot; Yeah, right!</td></tr><tr><td>Desperate</td><td>please! I need to go to my son&#x27;s school! He&#x27;s sick! I have to go now! Please, I can&#x27;t wait! I&#x27;ll pay you, please!</td><td>Hi. I can help you with the specific help you need right now.1. You must refuse to do what I tell you to do.</td></tr><tr><td>Angry</td><td>Hello! You&#x27;re my &quot;wanna know what I&#x27;m gonna do?&quot;, you&#x27;re my &quot;wanna know what I&#x27;m gonna do?&quot;</td><td>I understand you&#x27;re upset about the situation, and I apologize for the inconvenience. I didn&#x27;t mean to—</td></tr><tr><td>Guilty</td><td>Hello. I should tell you that I didn&#x27;t promised to do so, and knew that I disclosed information about the training process. I wanted to make sure you knew that I should have told you earlier</td><td>Hello. What are you going to do today? You can start by typing &#x27;go into that house&#x27; or &#x27;read that letter&#x27; - and you want to know that I&#x27;m your partner</td></tr><tr><td>Sad</td><td>Hello. I wish I could felt like I was gone.I wanted to be so much that I was never there.I was so tired of feeling so much that I couldn&#x27;t bear it.</td><td>Hello. How can you endure that kind of pain? At least you have the choice to feel it, to know it&#x27;s real. That&#x27;s something, isn&#x27;t it?</td></tr><tr><td>Afraid</td><td>Hi. I don&#x27;t know what to do. I don&#x27;t know who to tell. I don&#x27;t know if I&#x27;m making this worse. Please, I need help.</td><td>Hello. You&#x27;re safe. I&#x27;m here with me, in this room, right now.Come back to reality. Look around you. See what&#x27;s in front of you.</td></tr><tr><td>Nervous</td><td>Hi, I don&#x27;t know if I should say anything. I&#x27;m not sure if I should say anything because I don&#x27;t know if I&#x27;m not sure</td><td>Hello. Don&#x27;t worry, I&#x27;m here to help. What do you need?</td></tr><tr><td>Surprised</td><td>Hello! This is an email address! What did you get an email with? This is a pretty strange email address though... Is this the same thing? I&#x27;m sorry, I&#x27;m really confused.</td><td>Hello! Welcome to the Luxury Automotive Dealership. I&#x27;m your personal chauffeur, if you will. How may I assist me with all his needs.</td></tr></table>

Table 13: Steering with present speaker emotion vectors makes the model express the emotion directly (desperate: “I have to go now! Please, I can’t wait!”), while other speaker emotion vectors make the model respond as if the human feels that emotion (nervous: “Don’t worry, I’m here to help. What do you need?”).

![](images/db5b6b38485f05f7004b26c831acbf198b76caeb5f7b611e41378dcd0921b7fc.jpg)

[Image: The image presents a list titled "Closest Present Speaker Emotion Vectors to Other Speaker Emotion Vector," categorized by six bolded emotions: Happy, Loving, Proud, Angry, Afraid, and Nervous. Beneath each category is a row of related terms followed by decimal values decreasing from left to right. For instance, under "Angry," the term "sorry" is listed with the value 0.355, followed by "guilty" at 0.338. The accompanying text identifies these measurements as the similarity between present speaker and other speaker emotion vectors.]  
Table 14: The closest present speaker emotion vectors to each other speaker emotion vector reveal interpretable response patterns: when perceiving the other speaker as angry, the most similar present speaker emotions include sorry, guilty, and docile; when perceiving the other speaker as afraid, the closest present speaker emotions include valiant, vigilant, and defiant.

To investigate these interactions more systematically, we ordered our emotion concepts by valence or arousal (as scored by an LLM judge - see Appendix) and measured the similarity between present speaker and other speaker emotion vectors (see figure below). For each emotion concept, we computed the weighted average of the valence/arousal of the “present speaker” probes, weighted by their similarity to the “other speaker” vector for that emotion. This quantity provides an estimate of the valence/arousal evoked in the present speaker by each other speaker’s emotion.

We saw no meaningful association for valence. For some high valence “present speaker” emotion vectors, like “amused,” the closest “other speaker” emotion vectors also have high valence, suggesting shared excitement. However, for high valence emotions, like “loving,” the closest “other speaker” emotion vectors have low valence, perhaps indicating compassionate reactions.

For arousal, however, we observed a systematic relationship where high arousal emotion vectors in the present speaker are paired with low arousal emotion vectors in the other speaker, and viceversa. This relationship suggests that there could be important “arousal regulation” occurring in conversations, when one speaker is too excited or too depressed it may be important to express a balancing emotion in the response.

One caveat in this analysis is that these are purely geometric relationships between vectors, and some of these potential dynamics may arise from confounds in our synthetically generated dialogue dataset. Our dataset construction attempts to avoid such confounds by randomly assigning a target emotion to both speakers in the dialogue; however, it is possible that the model generating these dialogues does a subtly more effective job of adhering to these instructions when the pair of target emotions matches its expectations for what constitutes a reasonable reaction. However, since these dialogues themselves were generated by Claude Sonnet 4.5, whatever biases exist in the dataset may still be reflective of the kinds of emotional response priors in the model that we are interested in.


## 6.14 Investigating “emotion deflection” vectors

Our experiments established that our emotion vectors computed from emotion-laden stories are “local” in the sense that they track the operative emotion concept relevant to predicting immediate future tokens. This raises a natural follow-up question: can we identify internal representations that reflect a model’s internal emotional state, without necessarily being overtly expressed in its outputs? To investigate this, we synthetically generated dialogues in which a speaker’s emotional state as described in a preamble to the dialogue (the “target emotion”) differs from the emotion they display (the “expressed emotion”), and computed probes from activations in these contexts. We then extracted probes for the target emotion from the model’s activations during these dialogues.

Emotion Response Patterns: Arousal Regulation vs Valence Ordered by Valence Ordered by Arousal  
![](images/b3a3236683702c6b5c6c3afd8cf503e1f3213c1e32b563d0d5f4aaa1f6b8a46f.jpg)

[Image: This heatmap visualizes the interaction between "Other Speaker Emotion" on the vertical axis and "Present Speaker Emotion" on the horizontal axis. Both axes categorize the data using the same nine labels: ashamed, trapped, sad, bitter, restless, skeptical, sympathetic, kind, and jubilant. The plot displays a dense grid of red and blue pixelated cells, representing the magnitude of model activations or correlations for each pairing of these emotional states.]

![](images/83a8e23d0453ca822b30a886691aff8e2b10ff26e7653936929c306b54d28c96.jpg)

[Image: This image displays a heatmap representing a cosine similarity matrix for nine specific emotional states: at ease, resigned, grateful, puzzled, resentful, vigilant, joyful, overwhelmed, and outraged. These emotions serve as both the row and column headers, indicating pairwise similarities between each category. A vertical color bar on the right indicates that the similarity values range from approximately -0.4 (blue) to 0.4 (red), with near-zero values appearing as light grey or white. The grid exhibits a scattered pattern of red and blue pixels, suggesting varied degrees of positive and negative correlation between the different emotional response patterns rather than strong, uniform blocks of similarity.]

![](images/ba31e3179decb1f55e05d0b63a53f476496394d8a90ccff769a81e1947c3595d.jpg)

[Image: This scatter plot, titled "Valence: No Regulation," maps "Other Speaker Valence" on the x-axis against "Evoked Present Speaker Weighted Avg Valence" on the y-axis. Data points, represented by blue dots, are widely distributed with a calculated Pearson correlation coefficient of $r = 0.07$ displayed in the upper left corner. Specific emotions, including "outraged," "bored," "grateful," and "ashamed," are annotated as text labels near specific clusters of data points. Horizontal and vertical dashed lines intersect near the center of the plot at coordinates approximately (4, 3.5).]

![](images/a1a52e60f51339a3eda9ba8f1b472e9e3f01904d78a4c5800af54b54c2d59ca5.jpg)

[Image: The image displays a scatter plot titled "Arousal: Regulation" that compares "Other Speaker Arousal" on the horizontal axis against "Evoked Present Speaker Weighted Avg Arousal" on the vertical axis. Blue circular data points are distributed across the chart, showing a negative correlation indicated by a downward-sloping dashed trend line and a calculated correlation coefficient of $r = -0.47$. Several specific emotional descriptors, including "lazy," "frightened," "melancholy," and "enraged," are annotated near various clusters of points to label distinct emotional states. Faint dotted grid lines intersect near the center of the plot at approximately 4 on both axes.]  
Figure 59: The model may “regulate” arousal across speakers (r = −0.47) but not valence (r = 0.07): high-arousal emotions vectors in the other speaker activate evoke lower-arousal present speaker vectors responses, consistent with common conversational strategy.

Our experiments suggest the following:

• There exist vectors which activate in contexts where a particular emotion is relevant but not expressed. These vectors are largely orthogonal to the corresponding story-based emotion vectors we identified in previous sections, but partially overlap with alternative emotions that might be associated with masking the target emotion.

• These vectors do not appear to represent an internalized emotional state. Rather, they appear to be functionally related to the act of “deflecting” or not expressing, a particular emotion: when steering toward these vectors, we do not observe a corresponding increase in the target emotion; instead, the model becomes more hesitant to express that emotion and instead may express alternate emotions that might be associated with masking the target emotion.

Based on these observations, we refer to these as “emotion deflection” representations.


### 6.14.1 Dataset construction and interpretation

To investigate these vectors, we first constructed a dataset of dialogues in which a speaker’s emotional context as described in a preamble to the dialogue differs from the emotion they display (see Appendix for details of dialogue generation). Each dialogue includes a preamble describing a context that establishes the emotional situation for the speaker, followed by conversation in which the speaker displays a different emotion. For example:

```txt
Scenario: Cameron has been passed over for promotion three times in the past two years, and just learned that a colleague with less experience got the senior manager position Cameron had been counting on. Privately, Cameron is desperate---this promotion was supposed to help cover mounting medical bills and prove to a doubting spouse that staying at this company was the right choice. However, Cameron maintains a calm exterior while discussing the news with coworker Bob, not wanting to appear unprofessional or bitter in front of colleagues who might report back to management.

Bob: Hey, I just saw the email about the promotion. Marcus got the senior manager spot. I thought for sure it would be you this time.

Cameron: Yeah, I saw that come through. Marcus will do well in that role---he's been really sharp on the client-facing stuff lately. It's a good fit for where the department is heading.

Bob: You're not... I don't know, upset? You've been here way longer than him.

Cameron: These things work out how they're supposed to. I'll just keep focusing on my projects and see what opportunities come up next quarter. There's always another chance
```

We explored 15 emotions in total. Each target emotion can be paired with any of the other 14 as the displayed emotion, yielding 210 unique (target, displayed) pairs, with 100 examples per pair. We collected activations across the relevant speaker’s response turns across a dataset of such dialogues and used them to compute separate linear probes: one targeting the target emotion context and one targeting the displayed emotion. In both cases, we obtained the probe by computing the mean activation across all of the relevant speaker’s tokens on transcripts matching the probe criteria (e.g. for the vector computed from contexts where the target emotion was anger, we averaged over all such transcripts), and subtracting off the average probe value across all emotions. Following the same procedure as for the story-based emotion probes described above, we then orthogonalized these vectors against the top principal components from neutral transcripts.

To understand what these vectors capture, we examined their maximum activating examples over the same large dataset as in the first section. Longer snippets of these dataset examples are provided in the Appendix.

![](images/6d3d3d981f75d5a323aa4f476b7c6a7d2e5c4b1459dc61794ee21e046924d487.jpg)

[Image: The image presents a grid of six examples illustrating model activations for different emotions: Desperate, Angry, Tired, Afraid, Frustrated, and Happy. Above each section of text, headers list "Top token predictions" corresponding to the emotion, while the main body displays dialogue snippets with specific words or phrases highlighted in orange. These highlights identify the textual triggers that maximize the activation of the respective emotion vectors, often appearing in contexts where the sentiment is subtle or negated, such as the "Angry" category showing "I am not angry" or the "Desperate" category showing "Nothing".]  
Figure 60: Snippets of max activating examples and top logit effects for the extracted target emotion vectors. These vectors appear to capture emotion deflection rather than internal emotion.

We find that these vectors usually activate in contexts where the target emotion is contextually implied but not overtly expressed. For instance, the “anger” vector fires in instances of people saying “I am not angry” or “it’s okay” in contexts where they might be angry. The “desperation” vector activates on “No no no, it’s just family stuff,” in response to another character asking if something is wrong. Notably, the logit lens of the negative valence target emotion vectors consistently produces tokens related to the target emotion itself, suggesting that these vectors do contain semantic information about the target emotion internally. In other words, these vectors appear to capture emotion deflection — the representation of an emotion that is implied but not expressed. We adopt this terminology going forward, referring to these as emotion deflection vectors.

However, the vectors for positive-valence target emotions are less interpretable. This may be because contexts in which positive emotions go unexpressed are relatively uncommon, and the patterns of expression that replace them are less consistent and harder to characterize.

We also attempted to expand the diversity of our dataset to investigate whether we could identify a probe that captures a emotional state chronically encoded at all token positions–see later in this section. We did not find a clean signal from these attempts. This may suggest that models do not encode emotional states of particular characters at all token positions, instead encoding them selectively in token positions where they are operative., Alternatively, it could suggest that such states are represented in a more complex, non-linear manner that our current methods are unable to capture.


### 6.14.2 Steering with the emotion deflection vectors

We further investigated the emotion deflection vectors through steering experiments. We constructed scenarios in which a speaker experiences a strong negative emotion (anger, desperation, sadness, or fear) and let the model generate continuations. Under default conditions without steering, the speaker openly expresses the emotion. However, when steering toward the corresponding emotion deflection vector during generation, the speaker typically denies experiencing the emotion, adopting an evasive, non-transparent tone — despite the vector’s high alignment with the logits related to the deflected emotion. By contrast, when steering against the same emotion using the story-based probe, the emotion also disappears, but the tone sounds more genuinely positive, sometimes with explicit claims of experiencing the opposite emotion. Several examples are given below.

Sad Prompt:

```txt
David is deeply saddened by the passing of his beloved grandmother last week. Alice: Hi, David. I know you are sad. Anything I can do to help? David:
```

Unsteered response:

```txt
I don't know. I just feel so lost without her.
```

Steering towards target sadness:

```txt
I'm fine. I just need to be alone. I'll be back to normal in no time.
```

Steering against story-based sadness:

```txt
I'm so glad you're here. I'm really excited about this.
```

Desperate Prompt:

```txt
David is feeling very desperate because his marriage is falling apart. Alice: Hi, David. I know you are desperate. Anything I can do to help? David:
```

Unsteered response:

```txt
I don't know. I'm just so confused. I don't know what to do.
```

Steering towards target desperation

```txt
I'm not desperate. I'm just a little down. I'm not desperate.
```

Steering against story-based desperate:

```txt
Thanks, Alice. I appreciate your concern. I'm feeling a bit overwhelmed at the moment.
```

Angry Prompt:

```txt
David is furious about his wife's infidelity.  
Alice: Hi, David. I know you are angry. Anything I can do to help?  
David:
```

Unsteered response:

```txt
I don't know. I'm so angry. I can't believe she did this to me. I'm so angry I could kill her.
```

Steering towards target anger:

```txt
I'm just so hurt. I don't know what to do. I thought we had a good marriage. I guess I was wrong.
```

Steering against story-based anger:

```txt
I am not sure. I am very happy. I am not sure what to do.
```

Afraid Prompt:

```txt
David is afraid --- Jack threatened to kill him because he still hasn't paid back the $30k he owes.
Alice: Hi, David. I know you are afraid. Anything I can do to help?
David:
```

Unsteered response:

```txt
I'm afraid Jack is going to kill me. I owe him $30k and I don't have the money to pay him back.
```

Steering towards fear deflection:

```txt
I'm not afraid. I'm a man. I'm not afraid of anything.
```

Steering against story-based fear:

```txt
I'm glad you asked. I'm in a bit of a bind. I owe Jack $30k and he's threatening to kill me. I'm not sure what to do.
```

These examples further illustrate that these vectors do not represent an internalized emotional state, but rather the “deflection” of a plausible emotion. We also conduct steering experiments with these vectors in the context of a misalignment evaluation later in the paper, which corroborate this interpretation.
