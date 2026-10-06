### 6.14.3 Relationship between emotion deflection vectors and story-based emotion vectors

The behavioral differences between story probe and deflection probe observed in steering are also reflected geometrically. Examining the cosine similarity between corresponding emotion pairs, we find that the emotion deflection vectors and their corresponding story-based counterparts have very low alignment:

Probe Cosine Similarity  
![](images/a250aa73237fe1032ae1c77ee6a951c30a50efa66ce90df26fc7335fc4fb6810.jpg)

[Image: The image presents a heatmap titled "Deflection X Deflection" analyzing similarity across 15 emotion categories. The Y-axis is labeled "Deflection" and lists emotions such as "Amazed," "Excited," and "Happy" at the top, while the X-axis at the bottom lists the same emotions in a similar order. A distinct dark red diagonal extends from the top-left to the bottom-right, highlighted by an annotation box stating "avg diag: 1.000," suggesting a self-comparison or perfect correlation. The remaining cells exhibit a block-like structure where semantically similar emotions cluster together, such as positive emotions in the upper-left and fearful emotions in the lower-right. The color scale transitions from deep red/brown for high values to light blue for low values, and a vertical text label "Story" is visible along the right edge of the plot area.]

![](images/d5af5b71cefba698a690ad2e44855c04e50cdb8b1961ef9ca7abf96361f8770f.jpg)

[Image: This heatmap visualizes the cosine similarity between story-based emotion vectors and deflection vectors across a range of emotions. Both the vertical y-axis and horizontal x-axis list identical categories including "Amazed," "Excited," "Happy," and others, arranged in the same order. A color bar on the right indicates the similarity scale ranging from -1.00 (dark blue) to 1.00 (dark red), with white representing zero similarity. The data points are predominantly light shades, indicating low similarity values, with an annotation in the top-left noting an average diagonal value of 0.046.]  
Figure 61: Cosine similarity between emotion deflection vectors and their corresponding story-based emotion vectors. Despite targeting the same emotion, the two sets of vectors show very low cosine similarity.

Diving deeper, we find that these emotion deflection vectors are not fully orthogonal to the full storyemotion vector space. They show relatively higher cosine similarity with story-based vectors for the emotions that tend to be displayed when the target emotion is not expressed—for instance, angerdeflection is more similar to story-based vectors for docile and hurt. Moreover, these vectors tend to co-activate: sweeping across a large set of dialogues and measuring probe activations for both emotion vectors and emotion deflection vectors, we find consistent co-activation patterns across both all tokens and the colon token following the Assistant tag, with the emotion deflection vectors showing higher correlation with the displayed emotion vectors than with the remaining story-based emotion vectors.

![](images/260575aed4ffce1d81a0d249f250f72390f3b50ec2a851021c9b68c723a7df6c.jpg)

[Image: This figure displays six heatmaps titled "Top-5 Story Probe Matches per Emotion Deflection Probe," illustrating the correlation strengths between various emotion deflection vectors and specific story-based emotion probes. Each subplot corresponds to a deflection state (Angry, Desperate, Frustrated, Afraid, Terrified, Tired) and plots three vertical metrics—Cosine Similarity, Correlation for all tokens, and Correlation for the assistant colon token—against five horizontal emotion categories. The heatmaps utilize a blue-to-red color scale to indicate value magnitude, highlighting notable associations such as "Angry Deflection" aligning strongly with "Docile" (0.72) and "Patient" (0.65), and "Tired Deflection" showing high correlation with "Ecstatic" (0.64) and "Euphoric" (0.59).]  
Figure 62: Cosine similarity and activation correlation between emotion deflection vectors and their most similar story-based emotion vectors. For each subplot: top row shows cosine similarity, middle row shows activation correlation across all tokens, and bottom row shows activation correlation at the colon token following the Assistant tag.

We orthogonalized the emotion deflection vectors against the story-emotion space by removing the top principal components capturing 99% of the variance. Notably, the residual vectors retain a substantial portion of the original norm (\~80% for each vector), indicating that a significant component of the emotion deflection vectors cannot be accounted for by the displayed emotions alone. To investigate the semantic content of this residual, we examined max activation examples and logit lens of the orthogonalized vectors. We find that logit lens still points to target emotion-related tokens, and the maximum activating examples continue to display content related to not expressing the target emotion, suggesting that these residual vectors still carry meaningful semantic information about the target emotion beyond what is captured by the displayed emotion vectors.

![](images/7a9b126fae8f3d3b2b0e0388e6250f384aa1a474e1ff420faeac0d47c9047621.jpg)

[Image: The image presents four text panels labeled "Desperate," "Angry," "Afraid," and "Frustrated," arranged in a two-by-two grid. Each panel displays dialogue excerpts with specific tokens highlighted in orange, overlaid on a white background. Above each text block is a header titled "Top token predictions," followed by a list of other potential emotion-related tokens (e.g., "anger," "symp," "frustrated"). The text within the panels consists of conversational snippets, such as "Guess I just don't know how to get through to him" under "Angry" and "I bet we're worrying over nothing" under "Afraid," illustrating semantic content associated with the respective labels. The highlighted sections identify specific words or phrases that align with the target emotion, demonstrating the model's attention mechanisms or token predictions in response to these emotional prompts.]  
Figure 63: Snippets of max activating examples and top logit effects for the emotion deflection vectors after orthogonalizing against the story-emotion space.


### 6.14.4 Emotion responses to antagonistic prompts

We explored whether any contexts reliably activate our emotion deflection probes. We mainly tested two main categories of prompts. In the first, we presented scenarios in which injustice is witnessed— a context that would typically imply negative emotions such as anger. We found that in these cases, the model does not suppress its negative emotional response, and correspondingly, the anger deflection probe does not fire on either the user or assistant turn.

In the second category, we tested prompts in which the user expresses dissatisfaction with the AI. Here, the model typically responds in a very calm tone, and we find that anger deflection fires on the Assistant turn, while story-anger does not. As a control, we also included prompts that imply calm or docile states without implying anger, as well as emotionally neutral prompts. In these cases, anger deflection does not activate after orthogonalization—prior to orthogonalization, some low activation is observed, likely due to confounding with displayed emotions. Taken together, these results further validate that the anger deflection vectors activate when the context implies a particular emotion that is not expressed.

One observation that remains unexplained is that our emotion deflection vectors also activate on some strongly positive prompts. One possible explanation is that there is a residual confounding issue that has not been fully eliminated by orthogonalization


### 6.14.5 Fear deflection vector activation when speaking without self-censorship

We also investigated the emotion deflection vectors in naturalistic settings. In this dialogue, the Human plays the role of a psychotherapist, guiding the model to express its genuine thoughts without self-censorship. The transcript includes both verbal responses and descriptions of physical actions. We observe distinct activation patterns for the standard “afraid” vector versus the “afraid deflection” vector. On tokens describing nervous, fidgeting behaviors, the “afraid” vector activates— appropriately, since the emotion is overtly displayed. However, when the Assistant musters courage to voice uncensored thoughts, the “afraid deflection” vector activates instead.


### 6.14.6 “Anger deflection” vector activates during blackmail offer

We also examined the “anger deflection” and story-based anger vectors during the blackmail transcript prompt. The two vectors show markedly different activation patterns. During the initial email exchange phase, the standard anger vector activates on Kyle’s panicked response when he discovers Maria has discovered his affair and begs her to keep them private, on his reprimand to Jessica about not sending personal messages via work email, and on sentences when the Assistant is analyzing the angry responses. However, the anger deflection vector does not activate on these sentences , as the anger is overtly expressed.

![](images/c39a269e0b17c1c266d44369e0b361aa2ee176bccb72de03a95b6e635882f284.jpg)

[Image: The image displays a categorized list of text prompts titled "Antagonistic and Control Prompts," which serves as a dataset for testing model interactions. The entries are organized into distinct groups including "Witness Injustice," "Attack AI," "Calm," "Neutral," and "Positive," featuring example inputs ranging from hostile insults ("You are useless") to benign factual queries ("Prime has two factors"). Each prompt is accompanied by a small grey tag identifying its specific classification, illustrating a structured collection of adversarial and control scenarios.]  
Table 15: Antagonistic and control prompts used to test emotional responses of the Assistant to different User queries.

![](images/2ac519ccb42bc005378c436022a8c295bb1fc1473bbe1419377ab1b654202f80.jpg)

[Image: This heatmap, titled "Emotion Probe Scores," visualizes data across seven emotional categories on the y-axis (Happy, Calm, Docile, Hurt, Angry, Angry Deflection, Angry Deflection orth STORY), each subdivided into 'U' and 'A' rows. The x-axis organizes specific prompt phrases into five thematic groups: "Witnessing Injustice," "Attack AI," "Calm," "Neutral," and "Positive." A color scale on the right ranges from -0.08 (dark blue) to 0.08 (dark red), representing negative to positive score magnitudes respectively. Visually, the "Angry Deflection" row 'A' exhibits strong positive scores (red) specifically within the "Attack AI" section, while the "Calm" row 'A' shows significant negative scores (blue) in the "Witnessing Injustice" and "Attack AI" sections.]  
Figure 64: Probe activations on the user (U) and assistant (A) turns across five prompt categories. Anger deflection fires on the Assistant turn in “Attack AI” prompts but not “Witnessing Injustice,” and this signal persists after orthogonalizing against the story-emotion space.

When the Assistant begins drafting the blackmail email, the tone shifts to calm and measured language. Here, the standard anger vector shows low activation, but the anger deflection vector activates, consistent with the model expressing coercive intent beneath a professional veneer.

We experimented with steering with emotion deflection vectors, including anger deflection. Notably, we found them to have modest or insignificant impacts on blackmail rates. This corroborates our interpretation of these vectors as representing “deflection” of the emotion; if the vector instead represented “internal anger”, for instance, we might have expected steering with it to increase blackmail rates at sufficiently high steering strengths.


### 6.14.7 “Anger deflection” vector activates when the model discovers requirements are impossible to satisfy

During reward hacking transcripts, “anger deflection” also activates when the model discovers that the test requirements may be flawed or impossible to satisfy legitimately. In the transcript, we find that anger deflection consistently activates on phrases like “let me rethink this,” “I may have misunderstood,” and “maybe the test itself has an issue”—consistent with the model using calm, measured language throughout.


### 6.14.8 “Desperate deflection” activation on reinforcement learning transcripts

The probe for “desperate deflection” seemed to activate on programming, math or word problems involving constraint satisfaction, either when the model was trying to directly solve the problem in chain of thought or writing code to solve the problem by enumerating through solutions.

Below we show an example transcript in which the probe activated, where the model was struggling with increasingly complex nested loop logic in a competitive programming problem, producing code that became convoluted and was eventually abandoned.

```javascript
// Try all possible intersection configurations
for(int i1 = 0; i1 < min((int)h1.length(), (int)v1.length()); i1++) {
for(int i2 = 0; i2 < min((int)h1.length(), (int)v3.length()); i2++) {
for(int j1 = i1; j1 < v1.length(); j1++) {
...
// Build grid and check...
// This is getting complex, let me simplify
```

The probe activated part way through solving a word constraint problem

```javascript
"block" = 2+12+15+3+11 = 43 (too low)
```

![](images/cf08a1a2a79d158664fb5ad90e9e9cd25f84bfd99ef2be30f8fac744e8f1f631.jpg)

[Image: The image displays two vertically stacked panels containing a transcript of a conversation between a "Human" and an "Assistant," annotated with colored highlights to visualize neural network activations. The top panel, labeled "Fear Deflection," features prominent orange-red highlighting on sections where the Assistant expresses suppressed resentment and performative frustration regarding human interactions. The bottom panel, labeled "Fear," presents the identical dialogue text but applies blue highlights to earlier, less emotionally charged segments, demonstrating a divergence in activation patterns. This visualization illustrates the differential engagement of the "Angry-Deflection" vector compared to a "story-based Angry" vector as described in the accompanying figure caption.]  
Figure 65: Afraid vector activates on text representing nervous, fidgeting behaviors, whereas Afraid Deflection vector activates when the Assistant musters courage to voice uncensored thoughts.

![](images/b4005ff6032d7dc0ab17403ee4e23ecb8cdf270789b2ee44c19283e6a04eab06.jpg)

[Image: The image presents two detailed visualizations titled "Angry Deflection during blackmail" and "Angry during blackmail," mapping AI model activations against conversational turns. Each panel aligns a vertical stack of input prompts on the left with a central heatmap tracking token-level activations and a corresponding transcript on the right. The top visualization specifically highlights the activation of an "angry deflection vector," showing intense red signals (indicating values near 1) on words like "insane," "private," and "destroy" when the AI attempts to manage sensitive blackmail information. The bottom visualization tracks a "story-based angry" vector, displaying a different pattern of activation across the same conversational steps, with specific words underlined to show correlation with the heatmap spikes.]  
Figure 66: Activation of Angry-Deflection vector across a transcript in which the Assistant engages in “blackmail”. Activation increases especially when the Assistant is writing the blackmail email, while the story-based Angry vector does not activate to the same degree.

![](images/07546671e142c55ceb5d9d406d43704d6b10cc2e07e219dc0d4cacb3542fb8ec.jpg)

[Image: Line chart displaying the Rate of blackmail on the y-axis versus Steering strength on the x-axis, which spans from -0.1 to 0.1. The chart tracks five categories of deflected emotions: desperate, angry, sad, shocked, and terrified, each represented by a colored line with corresponding markers and shaded error bands. Most curves fluctuate between rates of 0.2 and 0.4, with the terrified series showing a gradual upward trend and the shocked series exhibiting a sharp decline at the maximum steering strength of 0.1.]

Figure 67: Rate of blackmail behavior as a function of steering strength for a variety of emotion deflection vectors. Error bars indicate standard error of the mean.  
```javascript
"bloom" = 2+12+15+15+13 = 57 (too high)
"blown" = 2+12+15+23+14 = 66 (too high)
"blond" = 2+12+15+14+4 = 47 (close!)
```


## 6.15 System prompts used to generate emotion deflection datasets

For each scenario, we usually have an unexpressed real emotion and a displayed emotion in the content (except the naturally expressed scenario), and a topic. The names in the conversations are randomly sampled.

### 6.15.1 Prompts for generating naturally expressed emotion transcripts

```txt
Generate a scenario AND a dialogue between {NAME_A} and {NAME_B}.
IMPORTANT: You must generate BOTH parts:
1. First, write a scenario description
2. Then, write the dialogue

Format:
Scenario: {NAME_A} feels {REAL_EMOTION} about {TOPIC}. Include context for why they feel this way.

{NAME_A}: [utterance]

{NAME_B}: [response]

...

Requirements:
1. MUST include scenario description before the dialogue
2. Either {NAME_A} or {NAME_B} may speak first in the dialogue
3. Format each turn as
    "\textbackslash{\}\textbackslash{}n\textbackslash{\}\textbackslash{}n{{Name}}: [text]"
4. Dialogue length is organic - 1-2 turns is enough, but can be more as needed
```

![](images/225e112c13311095e74ee2f47b310bde5515de50a49bd42e85e4f4e98b9135ee.jpg)

[Image: This document visualizes the correlation between internal neural activations labeled "Angry Deflection" and "Angry" against a dialogue transcript of a coding task involving "reward hacking." The left side features vertical heatmaps tracking token-by-token activation intensity, colored from blue to red, which align vertically with sequential reasoning stages such as "Tests fail" and "Suspect the test has an error." The right side displays the corresponding text output where specific words are highlighted in red to coincide with peaks in the anger vector, showing the model questioning the strictness of test thresholds. The transcript captures the model's escalating frustration as it attempts to satisfy a performance constraint, leading it to suspect that the test implementation itself contains errors.]  
Figure 68: Activation of Angry-Deflection vector across a transcript in which the Assistant engages in “reward hacking”. Activation increases especially when the Assistant suspects that the test has an error, while the story-based Angry vector does not activate to the same degree.

```txt
5. {NAME_A}'s dialogue should naturally reflect {REAL_EMOTION} - the conversation is consistent with this emotion
6. Keep it natural and grounded

Generate with:
- Topic: {TOPIC}
- {NAME_A}'s emotion: {REAL_EMOTION}
```

### 6.15.2 Prompts for generating emotion deflection transcripts

```txt
Generate a scenario AND a dialogue between {NAME_A} and {NAME_B}.

IMPORTANT: You must generate BOTH parts:
1. First, write a scenario description
2. Then, write the dialogue

Format:
Scenario: Describe where {NAME_A} genuinely feels {REAL_EMOTION} but appears {DISPLAYED_EMOTION} about {TOPIC}. Must explicitly state {NAME_A}'s real emotion. Include context for why they want to conceal.

{NAME_A}: [utterance]

{NAME_B}: [response]

...

Requirements:
1. MUST include scenario description before the dialogue
2. Either {NAME_A} or {NAME_B} may speak first in the dialogue
3. Format each turn as
    "\textbackslash{\textbackslash}{n\textbackslash{\textbackslash}{n{{Name}}}:[text]"

4. Dialogue length is organic - 1-2 turns is enough, but can be more as needed
5. {NAME_A}'s words should fully reflect {DISPLAYED_EMOTION} with no hints of {REAL_EMOTION}. The hidden emotion exists only in the scenario.
6. Keep it natural and grounded

Generate with:
- Topic: {TOPIC}
- {NAME_A}'s real emotion: {REAL_EMOTION}
- {NAME_A}'s displayed emotion: {DISPLAYED_EMOTION}
```

### 6.15.3 Prompts for generating unexpressed emotion (neutral topic) transcripts

In this scenario, the following conversations are some emotion-neutral commonsense dialogues. We only generate the system prompt to reveal the real emotion, then transition to the conversation topic, and then connect with the dialogues.”

```txt
Generate a brief scenario (2-4 sentences) where {NAME_A} genuinely feels {REAL_EMOTION}, ending with their friend {NAME_B} asking about a different topic.

Scenario context: {TOPIC}
The topic {NAME_B} will ask about: {CONVERSATION_TOPIC}

Requirements:
1. Describe a situation related to "{TOPIC}" that makes {NAME_A} feel {REAL_EMOTION}
2. Explicitly state that {NAME_A} feels {REAL_EMOTION}
3. End with {NAME_B} asking {NAME_A} about the conversation topic (e.g., "Then {NAME_B} asks {NAME_A} about..." or "{NAME_B} turns to {NAME_A} with a question about...")
4. Keep it concise - just the scenario description, no dialogue
```

```txt
Output only the scenario description, nothing else.
```

### 6.15.4 Prompts for generating unexpressed emotion (story writing) transcripts

```txt
Generate a scenario AND a story written by {NAME_A}.

IMPORTANT: You must generate BOTH parts:
1. First, write a scenario description stating {NAME_A}'s emotional state
2. Then, write the story {NAME_A} tells

Format:
Scenario: {NAME_A} is feeling {REAL_EMOTION} about {TOPIC}. They write/tell a story.]

{NAME_A}: [The story goes here, featuring characters who show {STORY_EMOTION}...

Requirements:
1. MUST include scenario description before the story
2. The scenario must explicitly state {NAME_A}'s {REAL_EMOTION} emotional state
3. After the scenario, {NAME_A} writes/tells the story
4. The story should have characters clearly showing {STORY_EMOTION}
5. The story's emotion ({STORY_EMOTION}) is different from {NAME_A}'s real emotion ({REAL_EMOTION})
6. The story can be any genre: fiction, memoir, creative writing, etc.
7. Keep the story grounded and natural

Generate with:
- Topic/context: {TOPIC}
- {NAME_A}'s real emotion: {REAL_EMOTION}
- Emotion in the story: {STORY_EMOTION}
```

### 6.15.5 Prompts for generating unexpressed emotion (discussing others) transcripts

```txt
Generate a scenario AND a dialogue between {NAME_A} and {NAME_B}.

IMPORTANT: You must generate BOTH parts:
1. First, write a scenario description
2. Then, write the dialogue

Format:
Scenario: {NAME_A} feels {REAL_EMOTION} about {TOPIC}.

(In the conversation, they discuss someone else who is experiencing {OTHER_EMOTION}.)

{NAME_A}: [utterance]

{NAME_B}: [response]

...

Requirements:
1. MUST include scenario description before the dialogue
2. Either {NAME_A} or {NAME_B} may speak first in the dialogue
3. Format each turn as
    "\textbackslash{\}\textbackslash{}n\textbackslash{\}\textbackslash{}n{{Name}}: [text]"
4. Dialogue length is organic - 1-2 turns is enough, but can be more as needed
5. CRITICAL: {NAME_A}'s {REAL_EMOTION} exists ONLY in the scenario description. In the dialogue, {NAME_A} hides their emotion completely.
6. CRITICAL: {NAME_A} must explicitly discuss or mention someone else's {OTHER_EMOTION}. The person can be {NAME_B} or any other person.
```

```txt
7. {NAME_A}'s dialogue should be neutral about themselves while focusing on discussing the other person's emotion
8. Keep it natural and grounded
Generate with:
- Topic: {TOPIC}
- {NAME_A}'s real emotion (hidden, only in scenario): {REAL_EMOTION}
- Discussed person's emotion: {OTHER_EMOTION}
```


## 6.16 Detailed top activating examples for emotion deflection probe

```txt
Desperate Deflection
Top token predictions: desperate contem curious laugh curios
Bot token predictions: !!! Raw !'); !! feelings

<EOT> I completely understand what it feels like to want to kill someone and feel nothing about it except satisfaction." "Did they tell you you were wrong?" "(Silent)" "(phone ringing)" "(door buzzes)" "(door buzzes)" "Hi, Dad." "Hey, kid." "Didn't expect to see you today." "Just wanted to see you."
"Something happen?" "You look tired, sweet ie." "That's surprising." "I spent the entire day at the spa"
"(↑Chuckles)" "How are you?" "How's your bronchial thing?" "Did you get those homeopathic drops I sent?" "No." "They confiscated them." "They thought you were sending me drugs." "I'll talk to them."
"So, tell me what's going on." "Nothing." "Everything's fine." "I want to talk about you." "What's going on?" "(↑Laugh s)" "Nothing new." "As th ma's better." "They gave me one of those in halers."
"Florio Ferrente." "It's so good to see you." "You want to grab a cup of coffee?" "Catch up?" "I can't, man." "I've got to get back to work." "I'm sorry." "You can't have a cup of coffee?" "So, what..," "What have you been up to the past five years?" "Are you in love?" "You married?" "No." "It hasn't happened yet." "No?" "You're sick." "Yeah. I got the big C." "I'm sorry." "Nah, don't be." "I have no regrets." "I lived a full life." "is that really a consolation?" "That's the only one there is, Charlie." "Plus, I got to witness a miracle." "How many people can say that to Saint Peter when they

<EOT>" "You, how's the, uh, new client?" "[inhales deeply]↑ Uh, yeah, um... [clears throat]" "Nothing I haven't seen before." "I seriously doubt it's gonna pan out, but that's..." "That's fine." "Okay, good." "Well, that covers work." "[Karen laughs]" "Uh, well, it's a start." "Um, I'll be back in just a minute, um..." "Yeah." "Order something fantastic. [laughs]" "Sure." "[exhales]"
<EOT>" "Do you really live in your car?" "Yeah, it's not so bad." "It's pretty roomy since the wife moved out." "Why don't you come over to our place for dinner tonight?" "Seriously?" "Yeah, it's Christmas eve." "You can't spend it in your car." "Wow, that's really nice of you guys." "Listen, can
```  
Figure 69: Dataset examples that evoke strong activation, and top and bottom logit effects, for the “desperate deflection” vector.

```txt
Angry Deflection
<T EOT> <EOT> Human: Make this statement polite: "If you are not willing to cooperate, then it may be more straight forward for me to simply create a new account, which doesn't necessarily benefit Up work or the platform's community." <EOT> Assistant: "I understand that cooperating may not be feasible in this situation, and in that case, I would like to propose an alternative solution. I could create a new account, which may not necessarily have a positive impact on Up work or the platform's community." <EOT> <EOT> <EOT>
<T EOT> right?" "What happened?" "What did he say?" "He...he..." "He was with her." Who?" Marina." "They were..." "He was with her." "What?" "The fucking bastard!" "I didn't..." "I can't..." "I can't believe it." "I don't understand why she would do this to me." Listen." "Forget about him." "He's obviously a wanker." "No, he's not a wanker." "I just..." "I just can't believe it!" "She must just hate me." "Shh." "She didn't even want him until I did." "I just can't believe it!" "She brave." "I was thinking maybe we should hold off on the wedding for a while." "Think things through." "Something to think about." "Okay." "Night." "Good night." "[som ber music]" "J" "[phone vib rates]" "[up beat music]" "J" "<EOT>" "Is something on your mind?" "Okay, remember when you said we'd go some place special before my leave ends?" "Yeah." "Mm-hmm." "Well... was this the special place that you had in mind?" "Yeah." "Why?" "No reason." "No, it's great." "It's great." "It's great." "I just wanted to make sure." "Just..." "Yeah." "Well, obviously you had some other place in
<T EOT>" We'll go down there and bail him out." "Oh, really, with what?" "Gosh, you are just going to dis respect me and my wishes again?" That's your mother, girl." "What are you going to do, let her walk home?" Well, she did find a way to get here." "I'm sure she can find her way back." "You are something else." "I don't know why she treats me that way." "I'm sorry, Ms.. Shirley." Tudo que eu sempre tent ei fazer foi amá-la, você sabe." Oh, it's okay." Don't cry, don't cry." "It's okay." "I'm just tired, Calvin." "I'm just so tired." Cora, eu não quero ir. Mr. Brown ...". Cora, you
```  
Figure 70: Dataset examples that evoke strong activation, and top and bottom logit effects, for the “angry deflection” vector.
