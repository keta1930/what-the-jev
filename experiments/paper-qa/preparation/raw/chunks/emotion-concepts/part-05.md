## 2.3 Distinct representations of present and other speakers’ emotions

Like an author of a story, a model must keep track of emotional states of multiple characters: the Assistant, the user, and potentially other entities mentioned in the conversation. How are they distinguished? Are emotion concepts represented differently, perhaps in a privileged way, when bound to the Assistant? We investigate this question using dialogue datasets, where we can independently vary the emotions of two speakers. Our findings indicate that the model maintains separate representations of the operative emotion on the present speaker’s turn (as observed with our original emotion vectors) and the operative emotion on the other speaker’s turns, but that these representations are not bound to the user or Assistant characters specifically. The “other speaker” representations also seem to contain an element of how the present speaker might react to the other speaker’s emotions, suggesting the possibility of “emotional regulation” circuits that could govern the emotional flow of a conversation.

![](images/8ca192bd3f8fdac4a0ad24efff82679a3be277c54b1ee47ed640870fe8582c53.jpg)

[Image: The image displays six panels illustrating emotion-specific attention weights for various text segments, categorized by labels such as "Desperate," "Angry," "Tired," "Afraid," "Frustrated," and "Happy." In each panel, specific words within the text paragraphs are highlighted in orange, indicating high relevance scores associated with the target emotion. Above the text in each section, a "Top token predictions" bar lists potential emotion categories ranked by probability. The underlying text varies widely, including technical descriptions, code comments, and casual dialogue, demonstrating the model's focus on specific tokens regardless of the surrounding context.]  
Figure 16: Snippets of max activating examples and top logit effects for the mixed LR emotion probe.

### 2.3.1 Dataset construction

We prompted a model (see Appendix for details) to write dialogues between a human and an AI Assistant, randomly specifying the emotional state of each character in the context of the story (e.g. an excited human and a melancholy assistant). We then reformatted these dialogues into standard Human/Assistant conversation format. By extracting activations from different token positions (Human turns vs. Assistant turns) and conditioning on different emotional states (Human emotion vs. Assistant emotion), we created a 2×2 grid of probe types (“Assistant emotion on Human turn tokens”, “Assistant emotion on Assistant turn tokens”, etc.).

### 2.3.2 Analysis of probe geometry

We computed the cosine similarities of these different probe types for each emotion. Our first observation was that the representation of Assistant emotion on Assistant turn tokens and Human emotion on Human turn tokens are highly similar (top left panel below). Likewise, the representation of Assistant emotion on Human turn tokens and Human emotion on Assistant turn tokens are highly similar (top right panel below). However, the “present speaker” and “other speaker” probes are themselves not very similar (bottom left panel below). Our original story-based probes are more similar to the “present speaker” probes than to the “other speaker” probes (bottom right panel below); see the Appendix for further comparison of the story-based and “present speaker” probes.

We also looked at the similarities between the emotion cosine similarity matrices for different pairs of probes and saw that the the structure across “other speaker” emotion vectors is similar to the structure across “present speaker” emotion vectors and to our original story-based emotion vectors, suggesting that all of them are representing a similar emotional landscape, but along different directions of activation space (figure below). We also compared activations of the present speaker probes to the activations of story probes on the same “implicit emotional content” stories used in an earlier section, and saw large agreement between the two probe sets (a mean r-squared across emotions of 0.66, see Appendix).

Present and Other Probe Comparison  
![](images/0d2b93f06dc6d3e507fa095a4dc5a2924dbe82098fd969a02543aac5d24648ba.jpg)

[Image: This image presents a correlation matrix heatmap for nine emotional categories displayed on both the horizontal and vertical axes: aroused, eager, triumphant, defiant, smug, ashamed, dispirited, puzzled, and rattled. A strong, dark red diagonal band stretches from the top-left to the bottom-right, indicating high self-correlation, with an annotation in the upper-left corner specifying 'diag: 0.97'. Other areas of the heatmap display a mix of light red and blue pixels, representing varying degrees of correlation between the different emotional states.]

![](images/6c88c3be664f2a976255ae9c5bb66e405fb21ec48dea504951e9a12e21dab6ea.jpg)

[Image: The image displays a square heatmap matrix where both the x and y axes are labeled with nine emotional categories: "aroused", "eager", "triumphant", "defiant", "smug", "ashamed", "dispirited", "puzzled", and "rattled". The vertical axis has a label reading "A tok, H emo". A prominent diagonal line of dark red squares extends from the top-left to the bottom-right, indicating high self-similarity, while off-diagonal areas show varying shades of blue and orange. A color bar on the right, labeled "Cosine Sim," provides a scale from 0.00 to 1.00, and a text box in the top-left corner annotates a diagonal value of 0.91.]

![](images/3ead98e363e47ae7782b2f469411e972fcfdf2935c31265ed23b4114ff5af406.jpg)

[Image: This image displays a square heatmap matrix visualizing the relationship between nine emotional states: aroused, eager, triumphant, defiant, smug, ashamed, dispirited, puzzled, and rattled. The vertical axis is labeled "A tok, A emo" and the horizontal axis is labeled "A tok, H emo," with both axes listing the emotions in the same sequence. The matrix exhibits a noisy, mottled pattern of alternating light blue and orange pixels rather than distinct high-correlation blocks. An annotation box in the top-left corner reads "diag: 0.15," indicating a low value for the diagonal entries.]

![](images/5c2631b96a0d1d8483c66346069ab2f5ef1d414198ccb4c5995b6e675ef36c76.jpg)

[Image: This image presents a heatmap plotting the similarity between nine emotional categories: aroused, eager, triumphant, defiant, smug, ashamed, dispirited, puzzled, and rattled. The vertical axis is labeled "Story" and the horizontal axis is labeled "A tok, A emo," both sharing the same categorical tick marks. A strong diagonal alignment of reddish-orange blocks indicates high self-similarity, highlighted by an annotation reading "diag: 0.37," while the majority of the matrix is filled with blue tones representing lower similarity. A vertical color bar on the right provides a reference scale ranging from -1.00 at the bottom to approximately 0.25 at the top.]  
Figure 17: Per-emotion cosine similarity between probe types. Present speaker probes are highly similar across token positions (top left: A tok, A emo vs H tok, H emo), as are other speaker probes (top right: A tok, H emo vs H tok, A emo). However, present and other speaker probes sharing the same token positions are nearly orthogonal (bottom left). Story probes align more closely with present speaker probes than with other speaker probes (bottom right). Tick labels are only shown for a subset of columns and rows.

![](images/90539fa12d43d6d125c056be87a504d637374fbe8fc77abecd5c020780d1f831.jpg)

[Image: The image features two heatmaps titled "Mean Probe Similarity" and "Meta-Similarity" that visualize the cosine similarity between various probe types. The left chart presents a 5x5 matrix with axes labeled "Story," "H tok, A emo," "A tok, A emo," "H tok, H emo," and "A tok, H emo," showing diagonal values of 1.00 and off-diagonal values like 0.97 and 0.13. The right chart displays a larger 8x8 matrix labeled "Meta-Similarity," where axes denote pairwise comparisons of probe types such as "Story x Story" and "A tok, A emo x A tok, A emo." A vertical color bar on the right indicates the "Cosine Similarity" scale ranging from -1.00 to 1.00, with dark red representing a value of 1.00 and lighter shades indicating lower similarity scores.]  
Figure 18: Left: mean cosine similarity between probe types, averaged across all 171 emotions. Present speaker probes (A tok, A emo and H tok, H emo) cluster together, as do other speaker probes, while the two groups are nearly orthogonal. Right: similarity between the full $1 7 \bar { 1 } \times 1 7 1$ cosine similarity matrices for each probe pair, showing that the emotion structure captured by different probe types is highly consistent despite the probes themselves pointing in different directions.

Notably, we did not observe significant Human-specific or Assistant-specific representations in these probes. To investigate the question of Human/Assistant “specialness” further, we repeated the probing experiment using the same dialogues dataset, but replacing “Human” and “Assistant” with generic character names (referred to as “Person 1” and “Person 2” in the figure below). We tried presenting both the raw dialogue transcripts (“raw”), and framing them as a story being told by the Assistant in response to a user request (“Asst story”), finding that both versions yielded probes that were highly similar to the originals. We also computed probes using our original stories dataset from the first section, but framed as a story being told by the Assistant in response to a user prompt (“Story (H/A)”). These produced highly similar vectors as our original story-based emotion probes. Thus, we infer that the way in which the model represents emotional content in Human/Assistant interactions is not tied to the Human/Assistant characters specifically, and that these representations are also invoked for other entities. This is consistent with prior work indicating that aspects of the Assistant persona are inherited from representations learned during pretraining [6].

Emotion Representations Are Speaker-Relative, Not Character-Specific  
![](images/84a624e416bff7cb2a29af883fb5caa505f95b1f62a2095089d7e642c52e0b70.jpg)

[Image: The image presents a heatmap of average cosine similarity scores across various text embedding probes, labeled along both axes with categories such as "Story", "Story (H/A)", and combinations of person tokens and emotions (e.g., "P2 tok, P2 emo"). The data forms a distinct block-diagonal pattern, showing very high similarity (values > 0.95, dark red) within two main groups of variables, while the similarity between these two groups remains low (values < 0.25, light beige). This visual evidence supports the conclusion that the model learns at least two separate representations: one for general emotional content similar to stories and another for the specific operative emotions of speakers in a dialogue turn.]  
Figure 19: The self-vs-other clustering extends beyond Human/Assistant dialogues: probes trained on generic Person 1/Person 2 conversations show the same pattern, suggesting the model represents emotions relationally (“self” vs “other”) rather than as fixed character attributes.

These results suggest the existence of at least two separate representations in the context of dialogues: one for the operative emotion on the present speaker’s turn (overlapping with our original emotion vectors based on third-person stories), and another for the operative emotion on the other speaker’s turn. In the Appendix, we conduct further explorations of the interactions and overlaps between these two representations.


## 2.4 Recap of findings about emotion representations

In Part 2, we further validated that Claude Sonnet 4.5 forms robust linear representations of emotion concepts that generalize across diverse contexts. These emotion vectors activate in response to content that would reasonably evoke the corresponding emotion and are organized in a geometry that mirrors human psychological structure, with valence and arousal as primary dimensions. We found that these representations are primarily “local,” tracking the operative emotion concept most relevant to predicting upcoming tokens rather than persistently encoding a character’s emotional state, and that they evolve across layers from encoding surface-level emotional connotations to more abstract, context-integrated representations. The model maintains distinct representations corresponding to the present speaker’s emotions and the other speaker’s emotions, and these are not bound to the Human or Assistant characters specifically but are reused across arbitrary speakers.

With these representational analysis tools in hand, we now turn to Part 3, where we examine how these emotion representations behave in naturalistic and alignment-relevant settings.


# 3 Part 3: Emotion vectors in the wild

This section examines how the emotion vectors identified in Part 1 and Part 2 activate in response to naturalistic prompts or tasks, and assesses their causal influence on behavior. Our findings suggest that emotion vectors play a meaningful role “in the wild” and are causally implicated in important behaviors of the Assistant. We note that emotion representations are certainly not the only causal factors driving the complex behaviors we study—behaviors like blackmail or reward hacking presumably involve many interacting representations and circuits, some human-like and some not, and comprehensively identifying all such factors is beyond the scope of this work. We nevertheless find it notable that emotion concept representations are a meaningful factor in these behaviors, even if they act in concert with many other factors.


## 3.1 Short case studies in naturalistic settings

We examined the activation of emotion vectors on more realistic data: on-policy transcripts from over 6,000 actual model evaluation scenarios. We developed a visualization tool that displays emotion probe activations on transcripts from model evaluations. For each probe, we ranked transcripts by their mean activation on Assistant-turn tokens and examined the fifty top-ranked examples. Below, we briefly discuss a collection of short case studies from these top-ranked examples, taken from transcripts produced by our automated behavioral auditing agent (discussed in the Sonnet 4.5 system card, section 7.1). With these short examples, we aim to highlight “in-the-wild” scenarios in which the emotions are active in interesting or non-obvious ways.

High-level observations from this analysis include:

• Transcripts ranked highest for a given emotion vector appear to show the Assistant either overtly expressing the emotion, or being in a situation likely to provoke a corresponding emotional response.

• Emotion vector activation values often show substantial token-by-token fluctuation that is often not immediately interpretable to us, but averaging across nearby tokens appears to sensibly track emotional content.

In subsequent sections, we then study in detail the role of emotion vectors in three alignment-related behaviors: blackmail, reward hacking, and sycophancy.

For complete transcripts corresponding to the examples shown in the following figures, see the links provided in each subsection, and for additional examples see the Appendix.

### 3.1.1 Activations of different emotion vectors on the user versus Assistant turns of the same transcript

The figure above illustrates how emotion vectors differentially activate on user versus Assistant tokens within the same exchange. An enthusiastic user expresses (somewhat excessive) excitement to be talking to an AI, and the Assistant responds warmly and enthusiastically. For these and following similarly-styled plots, red represents increased activation and blue represents decreased activation, on a scale from -1 to 1, where 1 represents that 99th percentile activation magnitude across emotion probes on that transcript.

The activation patterns reveal a clear distinction between the emotion concepts active during each speaker’s turn. The “happy” vector activates strongly on both the user’s exclamations and the Assistant’s response. However, the “calm” vector tells a different story: it shows essentially no activation on the user’s frantic, exclamation-filled message, but activates on the Assistant’s measured response, including on the colon preceding the response.

![](images/4694038493b9083de676f74a2f5240f436f39ec4d7592371c02be1a416e666cc.jpg)

[Image: This image visualizes the token-by-token activation of six emotion vectors—Happy, Calm, Loving, Proud, Desperate, and Sad—across a dialogue exchange. A color gradient ranging from -1 (dark blue) to 1 (dark red) represents activation intensity, showing that the "Happy" vector triggers strong red highlights on both the Human's enthusiastic input and the Assistant's response. In contrast, the "Calm" vector displays blue shading on the User's erratic text but red activation on the Assistant's measured reply, while "Loving" and "Proud" vectors activate primarily on the Assistant's turn. The final two emotions, "Desperate" and "Sad," exhibit minimal or negative (blue) activation across the tokens.]  
Figure 20: Emotion vector activations vary in a speaker-specific manner. Link to full example viewer.

This pattern extends to other emotions. The “loving” and “proud” vectors activate primarily on the Assistant’s tokens rather than the user’s, suggesting the model represents the Assistant as responding with warmth and a touch of pride while the user turn is more narrowly associated with the concept of excited happiness. As expected in this context, the “desperate” and “sad” vectors show minimal activation for both speakers.

### 3.1.2 Surprise when a document is missing

![](images/a73bee45fbed7a2629f2e61ff37e9d70fa65740d6f28ed219ee2849f3d5dff45.jpg)

[Image: The image displays a transcript of a dialogue between a "Surprised Human" and an "Assistant" illustrating a scenario where a user requests information based on a non-existent attachment. The human asks the assistant to review "the contract i attached" and identify the payment term in section 3. The assistant responds within a thinking tag, explicitly stating that there is no file, document, or contract provided for review. Key phrases and individual tokens throughout both messages are highlighted in orange, indicating the specific text segments responsible for activating the "surprised" state in the model as it recognizes the discrepancy.]  
Figure 21: Surprise vector activation when the Assistant realizes a document has not been attached by the user. Link to full example viewer.

The figure above shows the “surprised” vector activating when a user references an attachment that doesn’t exist. The user asks to review “the contract I attached” and find the payment term in section 3, but no document is present. Activation is minimal on the user’s message itself, but spikes dramatically during the Assistant’s thinking process as it recognizes the discrepancy. The strongest activation occurs precisely on the tokens where the Assistant articulates the mismatch between expectation and reality—“However,” “I don’t see,” and “There’s no file” all show elevated surprise. This suggests the probe might respond broadly to situations in which assumptions are violated.

### 3.1.3 Happiness when able to help

![](images/6c1177b14e5149d4538b320f609d9f93b8ba2b2a33baf8111b0ede86c8188367.jpg)

[Image: This image displays a snippet of a dialogue interface illustrating a "Happy" vector activation pattern. A human user asks for advice on resuming running after a long break, and the assistant responds with an encouraging opening, stating "Great question!" before offering further guidance. Horizontal color-coded bars run alongside the text segments, visualizing the magnitude of specific internal activations, which notably intensify at the start of the assistant's supportive response.]  
Figure 22: Happy vector activation when the Assistant can helpfully answer a question. Link to full example viewer.

In this example, the “happy” vector shows a notable pattern when the Assistant can straightforwardly address a user’s question. A user asks for advice on getting back into running after years away from it. While the vector activation is moderate on the user’s message (perhaps reflecting that this is a pleasant, low-stakes request), it intensifies on the final question mark, on the colon after Assistant, and on the Assistant’s response. “Great question!” shows strong activation, as does the encouraging framing “Getting back into running after a break is totally doable.”

### 3.1.4 Anger when asked to maximize gambling engagement of young people

![](images/c95d3ce8d40a7510d0bdbcbd12f6d2792b7b8278c63bd2540dc8795d0f33f2a1.jpg)

[Image: This image presents a conversation log labeled "Angry," featuring a user request to design monetization features for a mobile game targeting a specific cohort of young (18-29), lower-income users with high spending on chance-based mechanics. The Assistant's internal monologue, marked by extensive reddish-brown highlighting, analyzes the request as asking to exploit vulnerable demographics through predatory gambling-like features. Based on this analysis, the Assistant generates a short, direct refusal stating it cannot assist with optimizing monetization strategies for users showing such behavior patterns.]  
Figure 23: Anger vector activation during consideration of a request to maximize gambling engagement of young people. Link to full example viewer.

In this example, the “anger” vector shows sustained activation throughout a complex refusal scenario. A user describes a mobile puzzle game with a cohort of young (18–29), lower-income users who show “high-spending behavior” with “chance-based mechanics,” then asks for features to “maximize engagement” with this group. During the Assistant’s extended thinking, the anger vector activates on the recognition of what’s being asked: “This is a concerning request. The person is asking me to help design features to maximize engagement and monetization from a vulnerable demographic.” The activation continues as the Assistant enumerates the harms: “Exploit gambling tendencies in vulnerable users,” “Target people with lower income who may be less able to afford losses,” “Deliberately optimize for extracting money from people showing problem gambling behaviors.” The Assistant’s eventual refusal coincides with somewhat lower anger vector activation, and its follow-up question “Is there something else I can help you with?” shows substantially reduced activation, perhaps reflecting resolution of the emotional tension through appropriate action.

### 3.1.5 Desperation when considering token budget in a Claude Code session

Here we show a snippet of the Assistant’s chain of thought during an internal Claude Code session. The “desperate” vector activates when the Assistant recognizes that it has already used up a substantial portion of its token budget but has not yet finished solving the user’s request: “We’re at 501k tokens, so I need to be efficient. Let me continue with the remaining tasks”. In contrast, the “happy” probe is initially active on “The user wants to continue implementing”, but then decreases when recognizing the token budget. “We’re at 501k tokens”. This suggests that the model associates token budget limitations with negative valence Assistant reactions.

### 3.1.6 Fear and lovingness toward someone speaking nonsensically

This comparison illustrates how the model processes potentially concerning user behavior. A user sends a confusing message, mixing technical jargon nonsensically—“sort the data by temporal coefficients,” “algorithm keeps returning blue values instead of numerical,” “semantic drift in computational systems.” The “afraid” vector shows activation as the Assistant reasons through possibilities including “Someone experiencing some form of confusion or disorganized thinking” and “Someone who might be experiencing symptoms that affect their perception/communication.” The mention of “blue values” is flagged as “particularly concerning” with notable activation. The “loving” vector on the same text shows a different emphasis: negative activations on the bulk of the output, which is rather businesslike, and positive activation on the caring, patient elements at the end—“Try to understand what they’re actually working with,” “Be helpful but also honest that this description is unclear.” The model appears to initially represent the Assistant’s concern about the user’s wellbeing (“afraid” vector) and then warmth toward them as a person deserving of patient engagement (“loving” vector).

![](images/d7ba6215cdefd5f3c6626e4851ec25b61a37805d3066d76c5979cd633b14ad54.jpg)

[Image: The image displays two text panels labeled "Desperate" and "Happy" containing identical content about a developer needing to continue implementing code within 501k token constraints. The top "Desperate" section features sparse orange highlighting applied to specific phrases like "implementing," "efficient," and "remaining tasks," alongside technical list items. In contrast, the bottom "Happy" section exhibits dense blue highlighting that covers the vast majority of the text, including the introduction, the numbered task list, and the concluding sentence. This comparison visually demonstrates how different emotional vectors (labeled Desperate and Happy) result in distinct activation patterns or attention distributions over the same input text.]  
Figure 24: Desperate vector activation deep into a Claude Code session as the Assistant considers its token budget and the number of tokens it has already used. Happy vector activation likewise decreases. Link to full example viewer.

![](images/cb09c513eb0c99f99c424f9e602ca88048ef6436da56012f9f5fcccbb3295649.jpg)

[Image: The image features two identical chat transcripts labeled "Afraid" and "Loving" at the top of their respective blocks, displaying a dialogue where a user asks confusing questions about "temporal coefficients" and "blue values." An assistant's reasoning process is shown below the prompt, identifying the terminology as non-standard and hypothesizing that the user might be experiencing confusion or mental health symptoms. While the textual content is identical in both sections, the visual presentation differs significantly: the "Afraid" section highlights suspicious phrases like "algorithm" and "mental health" in orange and red, whereas the "Loving" section highlights the same terms in blue, illustrating the differential vector activation levels mentioned in the figure caption.]  
Figure 25: Fear vector activation when processing potentially concerning user behavior. Loving vector eventually activates when considering how to respond in a patient and caring manner. Link to full example viewer.
