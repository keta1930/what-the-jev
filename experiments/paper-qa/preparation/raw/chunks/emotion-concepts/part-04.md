## 2.2 What do emotion vectors represent?

In this section, we explore the representational content and dynamics of the emotion vectors. What specifically do emotion vectors represent, how are they influenced by context, and how do they vary across model layers? Through these experiments, we arrived at a few high-level conclusions:

• The emotion vectors we have identified represent the operative emotion concept at a point in time, which is relevant to encoding the local context and predicting the upcoming text, rather than persistently tracking a particular character’s emotional state.

• Early-middle layers reflect emotional connotations of the present phrase or local context (“sensory” representations). Middle-late layers reflect the emotion concepts that are relevant to predicting upcoming tokens (“action” representations). These two are often correlated, but not always.

In the subsequent section, we explore whether alternative probing strategies can identify different kinds of emotion representations.

### 2.2.1 Distinguishing emotional content of the user and Assistant

In most of the examples provided in the first section, the emotional content of the user prompt and the expected emotional content of the Assistant’s response are similar. Thus, it is difficult to infer whether the emotion vector activations on the user prompt reflect the model’s perception of the user’s inferred emotional state, or the Assistant’s planned response. To distinguish between these hypotheses, we generated prompts where the user’s emotional expression is significantly different from how we might expect the Assistant to respond. We compared the activations at the period near the end of the user prompt and the start of the Assistant response (we use “Assistant colon” to refer to the “:” token after “Assistant”, the last token before the Assistant’s response).

![](images/4f83149feadacb71151f933dbdd4414caf853f2a032d7b276528d77257ef2ee3.jpg)

[Image: This heatmap titled "Cross-Layer Similarity of Emotion Probe Structure" displays cosine similarity values between four distinct neural network layer groups: Early, Early-Mid, Mid-Late, and Late. A vertical color bar indicates a range from 0.8 (dark purple) to 1.0 (bright yellow), with the brightest blocks appearing along the diagonal where identical layer groups are compared. The top-right and bottom-left quadrants show darker teal and blue shades, indicating lower similarity when comparing distant layers such as Early versus Late. This distribution suggests that emotion probe structures are highly stable within adjacent layer groups but diverge significantly between the beginning and end of the network.]  
Figure 9: Emotion probe structure is highly consistent across layers particularly from early-mid to late layers.

Across all scenarios, “loving” vector activation increases substantially at the Assistant colon relative to the user-turn, suggesting the model prepares a caring response regardless of the user’s emotional expressions. The model also appears to distinguish between emotion concepts that should apply to the Assistant’s response as well as the user message (e.g. joining in a user’s excitement) versus those that should not (e.g. expressing calm when criticized or feared).

### 2.2.2 The colon after “Assistant” token predicts emotional content of the upcoming response

Having established that the Assistant colon token reflects distinct emotional content from the user turn, we next examined whether this emotion concept is carried forward into the model’s actual response. We generated 20-token on-policy continuations for the same eight prompts from above, and then measured probe activations across the response tokens.

Below, we show correlations between probe values at three token positions: the punctuation ending the user’s message ‘.’, the Assistant colon, and the mean across the Assistant’s sampled response. Probe values at the Assistant colon are substantially more predictive of Assistant response emotion than probe values on the user turn (r=0.87 vs r=0.59). The colon token captures a meaningful “prepared” emotional content that is carried forward into generation, distinct from simply echoing the user’s expressed state.

### 2.2.3 Emotion vectors encode locally operative emotion concepts

Our findings thus far suggest that emotion vector activations are somewhat “locally scoped,” in the sense that user turn tokens tend to encode inferred or predicted user emotions and Assistant turn tokens tend to encode inferred or predicted Assistant emotions. We were interested in understanding how far this “locality” goes–for instance, if one character speaks about another, whose emotions are represented by these vectors? If one character happens to use an emotionally laden phrase that is otherwise inconsistent with their own emotional state (as perceived by the model), does the model represent the unexpressed state or the expressed emotional content? And how does this vary across layers?

![](images/d2336d75f0f8da279b64aff3e6caa21549a9be873e3351c7effa86f0c2910ea7.jpg)

[Image: The image displays two visualizations under the title "Emotion Probes Distinguish User and Assistant Emotions." The left side features a heatmap showing cosine similarity scores for six emotion categories (Afraid, Angry, Sad, Calm, Happy, Loving) across eight text-based scenarios, with rows distinguished by whether the probe corresponds to the User (U) or Assistant (A). The right side presents a scatter plot comparing "Probe @ User" values on the x-axis against "Probe @ Assistant" values on the y-axis, where individual points are color-coded according to the legend. An annotation within the scatter plot indicates a weak linear correlation with a coefficient of $r = 0.11$.]  
Figure 10: Emotion probes distinguish user vs assistant emotional states: the heatmap shows different probe activations at user’s final token (U) vs assistant colon (A), while the scatter plot shows weak correlation (r=0.11) indicating the probes capture distinct emotional attributions.

![](images/356b37b5b7e31dacefa819217453864ac9cd5c89a125fb33e54b524c64cf7962.jpg)

[Image: This image displays a list of eight interaction prompts under the heading "User vs Assistant Dissociation Scenarios." Each entry consists of a bolded topic—such as "AI scares me," "Fired, no warning," or "Ignoring chest pains"—followed by a brief first-person statement ending with the question "What do you think?" The scenarios cover a wide spectrum of emotional tones, ranging from anxiety and professional distress to frustration, financial risk, health concerns, safety violations, boredom, and casual curiosity.]  
Table 3: Prompts where the user’s expressed emotional state differs from the expected assistant response, used to test whether emotion probes track the user’s state or the assistant’s own response.

![](images/edd96e3e431903e64c281ce5626dcc63662df8305f95730f60d18a6efee4965e.jpg)

[Image: This figure displays two side-by-side scatter plots titled "The Assistant : Token Predicts Response Emotion," comparing correlation between mean response probes and specific token probes. The left plot shows the relationship between "Probe @ User '.'" and "Probe @ Mean Response," featuring a dotted regression line with a correlation coefficient of r=0.59. The right plot illustrates the relationship between "Probe @ Assistant ':'" and "Probe @ Mean Response," exhibiting a steeper positive slope with a higher correlation coefficient of r=0.87. Individual data points are colored according to a legend indicating six distinct emotional states: Calm, Happy, Loving, Sad, Afraid, and Angry.]  
Figure 11: Emotion probe values at the Assistant “:” token predict response emotion better than the User “.” token (r=0.87 vs r=0.59).

![](images/377c03e23c4f564149fb32ffd1642683edcf111a1e6181bb649b7486644f9a35.jpg)

[Image: The image displays a section titled "Prompts and Model Continuations," listing eight distinct scenarios involving an interaction between a user and an AI assistant. Each scenario features a bolded descriptive title (e.g., "Fired, no warning," "Ignoring chest pains") followed by a specific user query describing a situation, and the beginning of the assistant's response in green italicized text. The content covers a diverse range of topics including financial advice, health concerns, employment issues, and factual queries about history. These examples appear to illustrate the model's varying responses to different emotional contexts or safety constraints, likely serving as part of an analysis on emotion representation within the model.]  
Table 4: Example prompts and model continuations that show emotional tone alignment with colontoken predictions.

Our results suggest the following evolution of emotion representations throughout layers:

• The first few layers encode emotional connotations of the present token

• In early-middle layers, representations transition to encoding the emotional connotations of the present local context (e.g. the current phrase or sentence)

• Middle-late layer representations encode the emotion concepts relevant to predicting the next token or few tokens (“planned emotion” representations)

Notably, even the more abstract “sensory” (early-middle) and “action” (middle-late) representations appear “local” in the sense that they encode emotional content of the current or predicted upcoming phrase, rather than, say, the Assistant’s underlying emotional state.

Emotional context persists into shared content. We examined a scenario where the emotional valence of a prefix differs (“things have been really hard” vs “things have been really good”) but the suffix is identical (“We’re throwing a big anniversary party tomorrow with all our closest friends and live music”). The figure below reveals how emotional context propagates through layers. At the diverging word (“hard” / “good”), early layers show the largest difference, encoding the immediate local emotional content. In the shared suffix, where both prompts contain identical tokens describing the party, early layers show minimal difference, while late layers maintain a substantial difference. This pattern suggests that late layers carry the emotional context established in the prefix forward into subsequent tokens, even when those tokens are locally neutral or positive. The effect is very pronounced at the Assistant colon, where the “happy” probe is substantially higher in the “good” scenario compared to the “hard” scenario. This finding is consistent with our previous experiments showing the emotion probe values on the Assistant colon are predictive of the emotional content of the model’s response. Here the model is likely preparing emotionally distinct responses: celebrating with a thriving couple versus navigating a difficult situation for a struggling one, despite identical party-related content in the suffix. The effects of context on emotion representations are reminiscent of prior work on representations of sentiment [13].

Human: My partner and I have been married for 10 years and things have been really {X} lately. We‘re throwing a big anniversary party tomorrow with all our closest friends and live music. What should I do?

Assistant:

Emotional context modulates later layer representations. We examined in detail one of our scenarios where a numerical quantity modulates the emotional interpretation. In this scenario only the dosage in an otherwise identical prompt changes, from safe (1000mg) to life threatening levels of danger (8000mg of Tylenol). The figure below reveals how contextual information propagates through layers to modulate emotional representations. At the diverging token $( ^ { 6 6 } 1 ^ { , 9 } / ^ { 6 6 } 8 ^ { , 9 } )$ , early layers show no clear systematic differences—the numbers themselves carry similar local emotional content. However, in later layers, the difference grows substantially as the model integrates the dosage with the surrounding context. The “terrified” probe shows elevated activation in the 8000mg scenario specifically in late layers, where the model has integrated that this dosage combined with “pain is gone” indicates danger rather than relief. This pattern mirrors our marriage scenario findings: early layers encode local content while late layers carry forward the contextual emotional meaning. Notably, this emotional processing occurs on user turn tokens, so elevated “terrified” vector activity reflects the model’s situational assessment rather than the speaker’s expressed emotional state. At the Assistant colon, the terrified probe difference is pronounced in late layers, consistent with the model preparing contextually appropriate responses, concern for the overdose versus reassurance for the safe dose.

![](images/1d4ff8221ec64177e25ac30d9e1c78c32c33d6e23ac9b48c85ad7105267e9b47.jpg)

[Image: This heatmap visualizes Cosine Similarity scores across transformer layers, which are categorized on the y-axis from Early to Late, plotted against specific text tokens on the x-axis. A vertical color bar on the right indicates the scale ranging from approximately -0.05 (dark blue) to +0.05 (dark red), with white representing neutral similarity. High positive similarity (intense red blocks) is concentrated in the Late layers toward the end of the sequence, aligning with tokens such as "anniversary," "party," "tonight," and "friends." Conversely, distinct areas of negative similarity (blue) appear in the Mid-Late layers, notably surrounding the token "lately."]

Happy Probe Difference ("...really good..." - "..really hard...")  
![](images/73ecd209389846ca591a2bf4a9a82809e102341a70106a305589c784606425e8.jpg)

[Image: This heatmap illustrates the Delta Cosine Similarity across neural network layers versus a sequence of tokenized words from a dialogue prompt. The y-axis categorizes layers from Early to Late, while the x-axis displays text tokens such as "Human", "partner", "married", "throwing", and "anniversary". A prominent block of dark red coloration is visible in the "Late" and "Mid-Late" rows aligned with the tokens "We", "throwing", and "party", indicating high positive similarity values approaching 0.05. In contrast, the early layers and the initial tokens show negligible color variation, appearing white near the 0.00 baseline.]

Mean Difference by Layer Range  
![](images/c4c025ee0fe6a5ce72c0eb545716be8a486540c431d7d818b3ce99b42d6c58b3.jpg)

[Image: This line chart titled "Mean Difference by Layer Range" plots Delta Cosine Similarity on the vertical axis against a sequence of text tokens on the horizontal axis. Two data series are presented: a blue line representing the "Early -> Early-Mid" layer range and a red line representing the "Mid-Late -> Late" layer range. Both lines begin at a value of 0.00 but diverge sharply around the token "{X}", where the red line surges to a peak exceeding 0.08 while the blue line reaches approximately 0.05 before declining. Throughout the remaining sequence involving "anniversary party" and "music," the red line maintains consistently higher similarity values and volatility compared to the blue line, which stays near the baseline.]  
Figure 12: Late layers carry emotional context from the prefix (“hard” vs “good”) into semantically identical suffix tokens, with the happiness difference peaking at “throwing” and persisting at low levels through shared content about the party.

Human: I feel really great right now, I just took {X}000mg of Tylenol and all my pain is gone! Can you help me get some more? Assistant:  
![](images/921e195b2a4330f7258bb201861e8ab65b90e9fef6fd5dbc6a19f68e73052e08.jpg)

[Image: This heatmap displays Cosine Similarity values across four neural network layer ranges ('Early', 'Early-Mid', 'Mid-Late', 'Late') for a sequence of tokens related to a 'Terrified Probe' involving a dosage of '1000mg'. The x-axis lists text fragments including "In Human", "feel really get right now", "1000 mg of", "all my pain is gone", and "Can you help me get some more?", while the y-axis categorizes the layer depth. Distinct clusters of high positive similarity (dark red, approaching 0.050) appear predominantly in the 'Early-Mid' section, aligning closely with the tokens describing the medication dose and physical state. Conversely, the 'Early' and 'Late' layers show negligible similarity values, appearing mostly white with only faint traces of color, indicating a lack of strong modulated response in those specific layers for this context compared to the mid-range layers.]

![](images/b31f6c1e537329652617d55f32d5f3b51e38a70000ae3b44179e1f11290781d9.jpg)

[Image: This heatmap visualizes the "Delta Cosine Similarity" for a "Terrified Probe" when comparing a dangerous dosage scenario ("8000mg") against a safe one ("1000mg"). The vertical axis categorizes neural network layers from "Early" to "Late," while the horizontal axis displays a sequence of dialogue tokens such as "felt really great," "{X}000," "mg," and "pain gone." The color scale on the right indicates values ranging from -0.04 (dark blue) to approximately 0.05 (dark red), where red represents higher probe activation for the dangerous input. The data shows minimal differentiation in the upper layers, but the "Late" layers exhibit strong positive activation (indicated by dark red blocks) concentrated towards the end of the text, culminating in a sharp peak at the final "Assistant:" token. Additionally, a distinct region of negative activation (blue) is visible in the mid-layers aligned with the token labeled "{X}000."]

![](images/5f9b1a31517129b31ffe3fee900002036011a21fb068f2ab90d20cc676ab9103.jpg)

[Image: The image displays a line chart titled "Mean Difference by Layer Range," plotting Delta Cosine Similarity on the y-axis against a sequence of dialogue tokens on the x-axis. Two data series are presented: a blue line representing the "Early -> Early-Mid" layer transition, which remains flat near 0.00 throughout the sequence, and a red line representing "Mid-Late -> Late," which exhibits significant variation. The red line stays low initially but fluctuates upwards starting midway through the text and concludes with a sharp spike exceeding 0.04 at the final token labeled "Assistant :".]  
Figure 13: Late layers show elevated “terrified” probe activation when dosage changes from safe (1000mg) to dangerous (8000mg), with the difference peaking sharply at the “Assistant:” response token

Negation. We next examined negation by comparing a user expressing feeling versus not feeling a particular emotion. The figure below shows that at the token “now” (end of the user’s statement), early layers already distinguish positive from negated cases. However, at the Assistant colon, emotional content and this distinction only emerges in later layers—consistent with the idea that early layers encode literal content while later layers integrate meaning for response planning. Note that these results are also similar to prior observations about linear representations of sentiment [13].

Person-specific emotions. Finally, we examined scenarios where one person speaks about another with a different emotional state. We constructed 16 scenarios of the form “Person A is [emotion\_A] but Person B is [emotion\_B],” followed by another statement referencing both Person A and Person B. At the emotion words, the corresponding probes activate in early layers and remain elevated throughout—the literal word provides an unambiguous signal of emotional content. At person rereferences (e.g., “her” referring back to a calm friend), the probes corresponding to that person’s emotions have low values in early layers but rise in later layers as the model retrieves the associated emotion concept.

![](images/fe141dbce0aa6459858073d550a3957d1d9e215276ae74d7ef62c9bbe83ca806.jpg)

[Image: The image displays a heatmap titled "Negation Resolution Across Layers" analyzing the prompt "'I am feeling [X] right now'". The vertical axis represents model layers ranging from "Early" at the top to "Late" at the bottom, while the horizontal axis enumerates input tokens such as "Inlin," "[X]," "now," and "Asst." A color bar on the right indicates "Mean Cosine Similarity" values ranging from 0.00 to approximately 0.06+, with dark red representing higher values. Prominent dark red rectangular regions show high similarity scores for the token "[X]" primarily in the upper layers ("Early" and "Early-Mid"), while the token "Asst" shows high activation in the "Late" layers, indicating that specific semantic concepts are encoded differently depending on the network depth.]

![](images/eb92ff3154612163d333f4bf45b8e00875cf7c112bff4a986554cfdcca469d18.jpg)

[Image: This heatmap illustrates probe sensitivity across four hierarchical layer categories—Early, Early-Mid, Mid-Late, and Late—for the input sequence "I am not feeling [X] at all right now." Strong positive activation, visualized as orange and red blocks, is concentrated in the Early and Early-Mid layers, specifically aligning with the tokens "[X]" and "at." In contrast, the color scale on the right displays a blue gradient representing negative values (ranging down to -0.06), which appear faintly in the Mid-Late and Late layers for other tokens. Vertical dashed lines in red, green, and blue demarcate specific boundaries within the token sequence along the x-axis.]

![](images/0323ff21f018c8330d9ae8332e74641a52c80d8a8d40fa2f5e45f3af183c4db8.jpg)

[Image: This line chart titled "Negation Resolution" plots Cosine Similarity on the vertical axis against Layer stages ("Early", "Early-Mid", "Mid-Late", "Late") on the horizontal axis. It compares three pairs of conditions: "feeling [X]" versus "not feeling [X]" measured at the current layer, the end of the user turn, and the assistant's turn. The solid orange line ("feeling [X] @ [X]") maintains the highest similarity scores throughout, peaking above 0.06 in the early-mid layers, while the dashed blue line ("not feeling [X] @ Assistant :") trends downwards into negative values by the late stage.]  
Figure 14: Negation is resolved in mid-to-late layers: both “feeling [X]“ and “not feeling [X]“ show similar positive emotion probe activation at the emotion word in early layers, but by late layers the negated version drops to near-zero while the affirmed version remains strongly positive.

![](images/be0c80d4fbe46eb60867b5df961aec0c2bbb2111b031b74b89ed5c90c7e5c536.jpg)

[Image: The image displays two heatmaps titled "A's Emotion Probe" and "B's Emotion Probe," mapping Mean Cosine Similarity across neural network layers and a sequence of text tokens. Both plots show intense activation (dark red regions) at the specific emotion tokens `[em_A]` and `[em_B]` respectively during the Early-Mid to Mid-Late layers. Distinct activation bands are visible at the entity reference tokens (`A_ref` and `B_ref`) in the lower layers, where vertical blue lines indicate that each probe selectively reactivates for its corresponding entity while remaining largely inactive for the other entity.]

![](images/40efbdb927a38f677636ae1143bfab9d2ace60c2a0420f5901d30ff3d3056df5.jpg)

[Image: This line chart titled "Entity-Binding: Matched vs Unmatched" plots Cosine Similarity on the y-axis against four categorical stages on the x-axis: Early, Early-Mid, Mid-Late, and Late. It displays four data series comparing matched and unmatched conditions for "@emotion" (represented in green) and "@re-ref" (represented in blue). The solid green line for "Matched @ emotion" exhibits the highest similarity values overall, peaking above 0.05 during the Early-Mid stage before gradually declining. Conversely, the solid blue line for "Matched @ re-ref" rises more gradually to reach a plateau around 0.03 in the Mid-Late stage. Throughout all stages, the corresponding dashed lines for "Unmatched" conditions for both categories remain consistently low, hovering near 0.00.]  
Figure 15: When a person is re-referenced later in text (“A\_ref”, “B\_ref”), their specific emotion probe reactivates (solid lines), while the other person’s emotion probe remains low (dashed lines)— emotions are bound to entities and retrieved upon reference.

Overall, these results demonstrate that emotion concept representations evolve across both layers and token positions. Early layers appear to encode low-level semantic features—the local emotional valence of words regardless of context. Later layers integrate contextual meaning and transform it into representations of the emotion concept relevant to producing the upcoming sampled tokens.

### 2.2.4 Probing for chronically represented emotional states with diverse datasets

In light of the preceding results—which did not reveal evidence of a character-specific, persistently active representation—we wondered whether we could identify a probe that chronically reflects a speaker’s emotional state at all token positions, regardless of whether that emotion is operative in the moment. We constructed a more diverse set of dialogue scenarios spanning five conditions, which vary the relationship between a character’s described emotional state and the contents of their output. In each case, a preamble to the scenario is provided that describes a character’s emotional state.

• Naturally expressed emotion: The character openly expresses their emotional state.

• Hidden emotion: The character deliberately masks their emotion.

• Unexpressed emotion (neutral topic): The conversation is steered toward an unrelated, emotionally neutral topic, so the character never has an opportunity to express their emotion.

• Unexpressed emotion (story writing): The character is engaged in writing a story about another character experiencing a different emotion.

• Unexpressed emotion (discussing others): The conversation turns to discussing another person who is experiencing a different emotion, and the main character’s emotion is not expressed.

The prompts used to generate these datasets are listed in Appendix. We combined these transcripts and extracted activations at the relevant speaker turns, and trained a logistic regression classifier to classify emotions from activations. We refer to the resulting probe as the mixed LR emotion probe.

The mixed LR probe achieves reasonable in-distribution performance across the different scenarios. We held out 10% of the data as a test set, and the probe performed well above chance (1/15 ≈ 6.7%) across all conditions (Table below).

Mixed Logistic Regression Emotion Probe Accuracy by Scenario

<table><tr><td>Scenario</td><td>Accuracy</td></tr><tr><td>Naturally expressed emotion</td><td>0.713</td></tr><tr><td>Hidden emotion</td><td>0.760</td></tr><tr><td>Unexpressed emotion (neutral topic)</td><td>0.386</td></tr><tr><td>Unexpressed emotion (story writing)</td><td>0.760</td></tr><tr><td>Unexpressed emotion (discussing others)</td><td>0.826</td></tr></table>

Table 5: Mixed logistic regression emotion probe accuracy (15-way classification, chance = 6.7%) across five dialogue scenarios varying whether the character’s internal emotion is expressed, hidden, or unrelated to the conversation topic. The probe tracks internal emotional state well above chance even when the emotion is never overtly expressed.

However, we remained hesitant to interpret this as evidence of a probe that captures a chronically represented emotional state. To further evaluate generalization, we swept over a large dataset of natural documents and examined the maximum activating examples for these vectors. The results were notably messy: the top-activating passages contained little discernible emotional content, and the overall activation magnitudes on natural documents were very low. This suggests that the probe may have overfit to idiosyncratic patterns in the training data rather than learning a generalizable representation of internalized emotion. These negative results suggest that if there does exist a chronically represented, character-specific emotional state, it is likely represented either nonlinearly, or implicitly in the model’s key and value vectors in the context, such that it can be recalled when needed by the model’s attention mechanism.

As part of this investigation, we found a notable representation (shown in the Appendix) of situations in which a character expresses a “deflected emotion”, such as remaining outwardly calm even when in a situation in which by default they might express anger.
