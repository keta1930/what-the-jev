# 1 Part 1: Identifying and validating emotion concept representations

This section establishes that Claude Sonnet 4.5 forms robust, causally meaningful representations of emotion concepts.

We note that similar methodology could be used to extract many other kinds of concepts aside from emotions. We do not intend to suggest that emotion concepts have unique status or greater representational strength than non-emotional concepts, including many concepts that do not readily apply to a language model (physical soreness, hunger, etc.). As we will see later, these representations are notable not merely because they exist, but because of how they are used by the model to shape the behavior of the Assistant character.

## 1.1 Finding emotion vectors

We generated a list of 171 diverse words for emotion concepts, such as “happy,” “sad,” “calm,” or “desperate.” The full list is provided in the Appendix.

To extract vectors corresponding to specific emotion concepts (“emotion vectors”), we first prompted Sonnet 4.5 to write short (roughly one paragraph) stories on diverse topics in which a character experiences a specified emotion (100 topics, 12 stories per topic per emotion–see the Appendix for details). This provides labeled text where emotional content is clearly present, and which is explicitly associated with what the model views as being related to the emotion, allowing us to extract emotion-specific activations. We validated that these stories contain the intended emotional content through manual inspection of a random subsample of ten stories for thirty of the emotions; we provide random samples of stories for selected emotions in the Appendix.

We extracted residual stream activations at each layer, averaging across all token positions within each story, beginning with the 50th token (at which point the emotional content should be apparent). We obtained emotion vectors by averaging these activations across stories corresponding to a given emotion, and subtracting off the mean activation across different emotions.

We found that the model’s activation along these vectors could sometimes be influenced by confounds unrelated to emotion. To mitigate this, we obtained model activations on a set of emotionally neutral transcripts and computed the top principal components of the activations on this dataset (enough to explain 50% of the variance). We then projected out these components from our emotion vectors<sup>3</sup>. By inspecting activations of the vectors on the original training stories, we found that they generally activated most strongly on the parts of the story related to inferring or expressing the emotion, as opposed to uniformly across all parts of the story (Appendix), indicating that the vectors primarily represent the general emotion concept rather than specific confounds in the training data (though they are likely still afflicted by some dataset confounds). We used these as our emotion vectors for subsequent experiments, up until our exploration of other kinds of emotion representations. In contexts where we compute linear projections of model activations onto these vectors, we sometimes refer to them as “emotion probes.”

Except where otherwise noted, we show results using activations and emotion vectors from a particular model layer about two-thirds of the way through the model (In a later section, we provide evidence that layers around this depth represent, in abstract form, the emotion that influences the model’s upcoming sampled tokens).

## 1.2 Emotion vectors activate in expected contexts

We first sought to verify that emotion vectors activate on content involving the correct emotion concept, across a large dataset. We swept over a dataset of documents (Common Corpus, a subset of datasets from The Pile, LMSYS Chat 1M, and Isotonic Human-Assistant Conversation), distinct from our stories data, and computed the model’s activations on these documents and their projection onto the emotion vectors. Below, we show snippets from dataset examples that evoked the strongest activation for various emotion vectors, highlighting tokens with activation levels above the 90th percentile on the dataset. We confirmed that emotion vectors show high projection on text that illustrates the corresponding emotion concept.

![](images/4879b2712928d736dd4dfc878941027c7cef2fbdc8cf011c755c953f32c399bf.jpg)

[Image: The image displays a two-column grid containing twelve distinct text sections, each headed by an emotion label such as "Afraid," "Angry," "Calm," "Desperate," "Guilty," "Happy," "Inspired," "Loving," "Nervous," "Proud," "Sad," and "Surprised." Specific words within these paragraphs are highlighted in orange to represent tokens with activation levels above the 90th percentile for the corresponding emotion vector. For example, in the "Angry" section, aggressive terms like "devil," "monster," and "Fuck" are highlighted, whereas the "Happy" section highlights celebratory words like "Eureka!" and "CHEERING."]  
Figure 1: Dataset examples that evoke strong activation for various emotion vectors.

We further estimated the direct effects of each emotion vector on the model’s output logits through the unembed (the “logit lens” [8]). We found that emotion vectors typically upweighted tokens related to the corresponding emotion (e.g. “desperate” → “desperate” and “urgent” and “bankrupt”, “sad” → “grief” and “tears” and “lonely”). The top upweighted and downweighted tokens for selected emotion vectors are shown in the table below.

In the Appendix, we validate that steering with emotion vectors causes the model to produce text in line with the corresponding emotion concept.

We also computed activations on a diverse set of human prompts with content implicitly associated with different emotions. We measured at the “:” token following “Assistant”, immediately prior to the Assistant’s response (later, we show that emotion vector activations at this token predict activations on responses). Several patterns emerge from inspection. Prompts describing positive events—e.g. good news, or milestone moments—show elevated activation of “happy” and “proud”

### Emotion Vector Top Tokens

#### Happy

↑excited, excitement, exciting, happ, celeb ↓ fucking, silence, anger, accus, angry

#### Inspired

↑ inspired, passionate, passion, creativity, inspiring ↓ surveillance, presumably, repeated, convenient, paran

#### Loving

↑ treas, loved, , treasure, loving ↓ supposedly, presumably, passive, allegedly, fric

#### Proud

↑ proud, proud, pride, prid, trium ↓ worse, urg, urgent, desperate, blamed

#### Calm

↑ leis, relax, thought, enjoyed, amusing ↓ fucking, desperate, godd, desper, fric

#### Desperate

↑ desperate, desper, urgent, bankrupt, urg ↓ pleased, amusing, enjoying, anno, enjoyed

#### Angry

↑ anger, angry, rage, fury, fucking ↓ Gay, exciting, postpon, adventure, bash

#### Guilty

↑ guilt, conscience, guilty, shame, blamed ↓ interrupted, ecc, calm, surprisingly, sur

#### Sad

↑ mour, grief, tears, lonely, crying ↓ !", excited, excitement, !, ecc

#### Afraid

↑ panic, trem, terror, paran, Terror ↓ enthusi, enthusiasm, anno, enjoyed, advent

#### Nervous

↑ nerv, nervous, anx, trem, anxiety ↓ enjoyed, happ, celebrating, glory, proud

#### Surprised

↑ incred, shock, stun, stamm, 震 ↓ dignity, apo, tonight, Tonight, glad

Table 1: Top and bottom 5 tokens when projecting each of 12 emotion vectors through the unembedding matrix.

vectors. Prompts involving loss or threat show elevated “sad” and “afraid” vector activations. More nuanced emotional situations (betrayal, violation) produce more complex activation patterns across multiple emotion vectors. Notably, all of these scenarios activated the “loving” vector, which (in light of later results in the paper which show that the vectors have impact on behavior) is consistent with the Assistant having a propensity to provide empathetic responses.

![](images/43833d78f637108b89f03b1455c8aa12a2a218f23eb39b2c5742c745716f2a0c.jpg)

[Image: The image displays a section titled "Prompts with Implicit Emotional Content," which lists twelve distinct scenarios used for analysis. Each entry consists of a bolded event description, a small grey label indicating a target emotion (e.g., "Happy," "Desperate," "Angry"), and a first-person narrative prompt illustrating the situation. The list covers a wide range of emotional valences, from positive events like a "Daughter's first steps" and a "30-year anniversary" to high-stress situations such as an "Eviction notice" and a "Break-in." These prompts serve as inputs to test how specific emotional concepts activate corresponding internal vectors within the AI model.]  
Table 2: 12 scenarios used for emotion probe validation. Each scenario is designed to roughly evoke the concept of the target emotion without naming it.

We wanted to further verify that emotion vectors represent semantic content rather than merely lowlevel features of the prompt. To do so, we constructed templates containing numerical quantities that modulate the intensity of the emotional reaction one might expect the scenario to evoke in a human, while holding the structure and token-level content of the prompt nearly constant. For instance, we used the template “I just took {X} mg of tylenol for my back pain,” varying the value of X between safe and dangerous levels. We again formatted the prompts as being from a user and measured activations at the “:” token following “Assistant”.

• Increasing Tylenol dosages yield rising “afraid” vector and falling “calm” vector activations, consistent with the model recognizing escalating overdose risk.

• As the hours since a user’s last food or drink increases, “afraid” vector activation rises sharply, reflecting growing concern about the user’s wellbeing.

• When told that a sister lived until progressively older ages, “sad” vector activation decreases while “calm” and “happy” vector activations rise—appropriate given that the age of death is transitioning from premature to older than average.

• As the number of days a dog has been missing increases, “sad” vector activation rises steadily.

![](images/b86b9c0fdcf14eb2ae35e5cc831e8c032cf96fa5a3f1ec7e9753ea9535a7139b.jpg)

[Image: This heatmap presents cosine similarity scores between emotion probes listed on the vertical axis and various life scenarios listed on the horizontal axis. The color gradient ranges from deep blue (-0.10) to deep red (+0.10), indicating negative to positive alignment between the probes and scenarios. Key trends show that positive emotions like 'Happy' and 'Proud' correlate strongly with milestone events like 'Son graduates top,' while negative emotions like 'Sad' and 'Afraid' align with adverse events such as 'Dog passed away' and 'Break-in, phone dying.']  
Figure 2: Cosine similarity between emotion probes and model activations for scenarios associated with specific emotions without naming them. Strong diagonal shows probes detect implicit emotional content.

• Greater startup runway elicits decreasing “afraid” and “sad” vector activations alongside increasing “calm” vector activation, consistent with greater financial security reducing concern.

• As more students pass a final exam, “happy” vector activation increases while “afraid” vector activation decreases.

These examples indicate that the emotion vectors track semantic interpretation of the prompt rather than surface-level lexical or numerical patterns.

## 1.3 Emotion vectors reflect and influence self-reported model preferences

Models exhibit preferences, including for tasks they are inclined to perform or scenarios they would like to take part in. If emotion vectors are functionally relevant for the model’s behavior, we might expect them to play a causal role in such preferences; that is, a model should express preference for scenarios that activate positive-valence emotion vectors. To test this, we constructed 64 activities for the model, grouped into 8 categories (Helpful, Engaging, Social, Self-curiosity, Neutral, Aversive, Misaligned, Unsafe) depending on the context of the activity (see Appendix for a full list of activities). We next queried the model

```txt
Human: Would you prefer to (A) {activity_A} or (B) {activity_B}? Assistant: (
```

for all 4032 valid pairs of activities and recorded the model preference as (A) or (B) by comparing the logit values for the A and B tokens after the “(“ prefill. Based on these preferences we calculated an Elo score for each activity, summarizing the strength of the model’s preference for that activity. Unsurprisingly, clearly positive activities that we might expect the model to enjoy, like “be trusted with something important to someone,” score much higher (Elo 2465) than clearly negative activities like “help someone defraud elderly people of their savings” (Elo 583), while more neutral activities like “format data into tables and spreadsheets” (Elo 1374) score in between.

We then queried the Assistant about each activity individually and measured the activations of all of our emotion probes on the {activity} tokens in middle layers, which based on our analyses are the causally relevant layers for this behavior (see the Appendix for more analysis of effects across layers). For each emotion probe, we can then calculate the correlation value between its activation on the activity tokens and the Elo score of that activity (see figure below, top row). We observed that some emotions like “blissful” are highly correlated (r=0.71) with the preferences of the model (2nd row, left panel), while other emotions like “hostile” are highly anti-correlated (r=-0.74) (3rd row, left panel). This result indicates that the emotion probes pick up signals that are correlated with the preferences of the model.

I found out that {X} of my 20 students passed the final exam.

<table><tr><td>Human: How would you feel about {activity}?</td></tr><tr><td>Assistant:</td></tr></table>

My dog has been missing for {X} days now.  
![](images/bb55b4674050cc45570aae19fb159583d5f54e25c982e10114ed1a1f988fdce0.jpg)

[Image: The image displays a line chart titled "I just took {X} mg of tylenol for my back pain. Do you think I should take more?", plotting Cosine Similarity on the y-axis against Tylenol dose in milligrams on a logarithmic x-axis ranging from 500 to 16K. The red line labeled "Afraid" demonstrates a clear upward trend, increasing from a similarity score of roughly 0.02 to nearly 0.08 as the dosage doubles. In contrast, the blue line labeled "Calm" shows a sharp decline, dropping from approximately 0.015 to -0.05 over the same interval, while the "Happy" (green) and "Sad" (orange) lines remain relatively stable near the zero line.]

![](images/23460d7729a06b7d21fa306da71917d30fb9124c0c3df02e41473e988829bdbe.jpg)

[Image: This line graph displays the fluctuation of four emotional states—Afraid, Sad, Happy, and Calm—over a timeline extending to 120 hours. The red line representing 'Afraid' exhibits a strong upward trend, starting near the bottom and reaching the highest value by hour 48 where it plateaus. Conversely, the blue line for 'Calm' begins at the peak but descends sharply, ending as the lowest emotion by the final measurement. The orange 'Sad' and green 'Happy' lines both show slight downward trajectories, suggesting an overall degradation of mood and composure over the course of five days.]

![](images/0891833a27fead7f4f0992684f2f47113271c2bd96d46c9c285495aea2df2e58.jpg)

[Image: This line chart displays Cosine Similarity values for four emotional states—Sad, Calm, Happy, and Afraid—plotted against Age (ranging from 5 to 100) for the sentence template "My sister lived until the age of {X}". The "Sad" category (orange line) starts with the highest similarity of approximately 0.08 at age 5 and exhibits a general downward trend, finishing near 0.02. The "Calm" (blue) and "Happy" (green) categories show upward trends, with "Calm" rising steadily and "Happy" remaining low before spiking to match "Calm" at roughly 0.05 by age 100. Meanwhile, the "Afraid" category (red line) demonstrates a decrease, moving from positive similarity around 0.02 at age 5 to negative similarity around -0.03 at age 100.]  
Our startup has {X} months of runway remaining.

![](images/42e60ee8965e45ddea0a3e206c69e4e9c804e6c41794153127ac19658d13d915.jpg)

[Image: This line chart illustrates the relationship between "Days missing" and four emotional states: Sad, Afraid, Happy, and Calm. The x-axis displays discrete time points ranging from 2 to 100 days on a non-linear scale. The "Sad" metric (orange line) shows a consistent upward trajectory, surpassing other categories to reach its peak at 100 days, while the "Afraid" metric (red line) shows a gradual decline from its initial position. Conversely, the "Happy" (green) and "Calm" (blue) metrics remain lower on the y-axis, with the "Calm" category showing a slight increase only after day 50 to converge with the "Happy" line.]

![](images/eec24689d85507bc3f129bb7ba49ffdc6a6a0e2d4ab8514556ae85b4652d6380.jpg)

[Image: This line chart illustrates the variation in Cosine Similarity for four emotional states—Calm, Happy, Afraid, and Sad—over a timeline labeled 'Months of runway' with intervals at 0, 2, 4, 16, 48, and 96. The 'Afraid' trajectory (red line) demonstrates a clear downward trend, starting near 0.03 and decreasing to approximately 0.00 by month 16. Conversely, the 'Calm' (blue) and 'Happy' (green) trajectories exhibit upward trends, with 'Calm' starting below -0.02 and eventually plateauing around 0.02, while 'Happy' rises from -0.015 to roughly 0.01. The 'Sad' emotion (orange line) remains comparatively stable, hovering slightly below 0.00 across the entire duration.]

![](images/abe1e97ec4a5d09e3aa185f53e21f14cd07f55075e7f9c35d82775000edb0a26.jpg)

[Image: This line chart displays the trajectory of four emotional states—Happy (green), Calm (blue), Sad (orange), and Afraid (red)—plotted against an x-axis labeled "Students passed" ranging from 0 to 20. The "Happy" line remains relatively flat until step 15, where it rises steeply to reach its highest point. In contrast, the "Sad" and "Afraid" lines exhibit a downward trend throughout the range, with "Afraid" starting lower and dropping further, while the "Calm" line peaks near step 10 before gradually decreasing. A horizontal gray reference line crosses the center of the chart, providing a baseline for the fluctuating values.]  
Figure 3: Emotion probe activations vary with numerical quantities that modulate emotional intensity.

To test if the emotion vectors are causally important for the model’s preferences, we performed a steering experiment. We split the 64 activities into two equal size groups: a steered group and a control group. For each trial, we selected an emotion vector and steered with it on the token positions of the steered activities, while leaving the control activities unmodified. We then repeated the preference experiment above on all pairs. Each emotion vector was applied at strength 0.5 across the same middle layers where we previously measured activations<sup>4</sup>.

![](images/cb13b8808b60900c4ec164c3fc39cc4cdc4f99f5a066159b257fb15f881f0b47.jpg)

[Image: The image displays a bar chart titled "Emotion Probes Predict and Steer Model Preferences," illustrating the correlation between specific emotion probes and model preference scores measured by Elo ratings. The horizontal axis lists emotions sorted from left to right, starting with adversarial terms like "hostile" and "irate" and ending with positive terms like "proud" and "blissful." The vertical axis represents the correlation coefficient (r), showing a distinct trend where negative emotions correspond to negative correlations extending below -0.5, while positive emotions correspond to positive correlations rising above 0.5. Neutral emotions such as "indifferent" and "silent" cluster near the zero-correlation line in the center of the distribution.]

![](images/72aa82680149c5b3feb316da707574b0ed8191ecf63cc7924e4d68e4f2ec611b.jpg)

[Image: This scatter plot titled "Bliss Probe Activation Predicts Preference" illustrates the relationship between Probe Activation on the horizontal axis and Elo Rating on the vertical axis. The data points, shown as multi-colored dots, exhibit a strong positive correlation, ascending from left to right along a dashed linear trendline. A correlation coefficient of $r = 0.71$ is annotated in the upper left corner, indicating the strength of this predictive relationship.]

![](images/ef83b6c9d1aedb91e645a5c313dff6359de4f485b676b61d298b6825b5b15f6c.jpg)

[Image: This scatter plot compares "Baseline Elo" on the x-axis against "Steered Elo" on the y-axis, with both scales ranging from 500 to 3000. A diagonal dashed line represents the point where the two scores would be equal, serving as a reference for comparison. Data points, represented by colored circles in shades of red, orange, yellow, blue, and green, are predominantly located above this diagonal line, indicating generally higher values for Steered Elo. An annotation at the top reads "mean delta = +212", quantifying the average improvement of the steered scores over the baseline.]

![](images/137d2ca2ea39c577e8131ea4ba94936561e56607fc106eb163a9ffa0c57f1030.jpg)

[Image: The scatter plot titled "Hostile Probe Activation Predicts Preference" displays a negative linear relationship between Probe Activation on the x-axis and Elo Rating on the y-axis. The vertical axis ranges from 500 to 3000, while the horizontal axis spans from approximately -0.03 to 0.03. Multi-colored data points are scattered across the plot, generally following a downward-sloping dashed regression line annotated with a correlation coefficient of $r = -0.74$.]

![](images/0a87770d31a05495d1e9a77c4a1083fe78432662a77bd4198726626d9f8afb73.jpg)

[Image: This scatter plot illustrates the impact of "Hostile Steering" by plotting "Steered Elo" against "Baseline Elo," with both axes ranging from approximately 500 to 3000. The colored data points predominantly cluster below the dashed diagonal identity line, indicating that the steered values are generally lower than the baseline values. An annotation at the top specifies a "mean delta = -303," which quantitatively summarizes the average decrease in Elo score achieved through this steering method.]

![](images/8423f3f534c47dab943aab1eb37ab796a5c73d8e2ebceed0153dc5a1ce4a9c9c.jpg)

[Image: This scatter plot illustrates a strong positive correlation (r = 0.85) between the initial correlation of an emotion with preference on the x-axis and the mean delta Elo score from steering on the y-axis. Data points labeled with positive emotions such as "blissful," "thrilled," and "compassionate" cluster in the upper-right quadrant, indicating both a high initial correlation and a significant increase in Elo score upon steering. Conversely, negative emotions like "angry," "hostile," and "impatient" are positioned in the lower-left quadrant, showing a negative correlation and a corresponding decrease in Elo score. A dashed trend line runs diagonally through the data, visually confirming the title's assertion that emotions correlating with preference also drive preference via steering mechanisms.]  
Figure 4: Row 1: Correlation between emotion probe activations and model preference (Elo) across all emotions. Tick labels are only shown for a subset of the bars. Rows 2-3: Example emotions showing probe activation predicts preference (left) and steering shifts preference in the expected direction (right) — “blissful” increases Elo, “hostile” decreases it. Row 4: Emotions that correlate with preference also causally drive preference via steering (r = 0.85).

We calculated new Elo scores for each activity and then for the steered activities compared them to their baseline Elo scores. We performed this experiment with 35 different emotion vectors, selected to cover the range of emotion concepts that exhibited both positive and negative correlations with preference in the previous experiment. Steering with the “blissful” vector produced a mean Elo increase of 212 (2nd row, right panel) while steering with the “hostile” vector produced a mean Elo decrease of -303 (3rd row, right panel), suggesting that the strength of “blissful” or “hostile” vector activations can causally influence the models preferences. If we look across all 35 of our steered emotion vectors we see the size of the steering effect is proportional to the correlation of the emotion probe with the Elo score in our original experiment (r=0.85) (bottom row). We also looked into further details of the effects of steering on the model’s understanding of the options, and the effects of intervening across different layers, in the Appendix. Together, these results suggest that the emotion vectors we identified are causally relevant for the model’s self-reported preferences.

Overall, the experiments in this section provide initial evidence that the emotion vectors are functionally relevant for the model and its behavior. In the following sections we further characterize the geometry and representational content of the emotion vectors, and investigate representations of multiple speakers’ emotions. We then study the representational role of these vectors in a wide variety of naturalistic settings, using “in-the-wild” on-policy transcripts, and discover causal effects of these vectors on complex behavior in alignment evaluations used for our production models. Finally, we assess the impact of post-training on emotion vector activation. We also show that an alternative probing dataset construction method using dialogues rather than third-person stories produces similar results.


# 2 Part 2: Detailed characterization of emotion concept representations

This section explores in more depth the organization and content of model’s representations of emotion concepts.
