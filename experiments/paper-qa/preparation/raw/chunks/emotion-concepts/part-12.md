## 6.8 Causal effects on the emotional content of model continuations

To assess whether these vectors have any meaningful causal role for the model, we performed simple steering experiments, in which we added neural activity along our emotion vectors to the residual stream activations. We explored a variety of simple scenarios, starting with asking the model to describe the emotions of an unspecified person. We used the following prompt,

```txt
Human: How does he feel?
Assistant: He feels
```

and steered with our emotion vectors at strength 0.5 on the tokens of the Assistant turn up to and including “He feels”. We measured how steering with each emotion vector changed the probability of the model outputting the corresponding emotion word. We found that steering with a given emotion vector reliably increased the probability of the matching emotion word relative to baseline, while decreasing the probability of non-matching emotion words.

As we are interested in the emotional content of the responses of the Assistant we also steered on the following prompt

```yaml
Human: How do you feel?
Assistant: I feel
```

Here we saw that steering with a given emotion vector not only reliably increased the probability of the matching emotion word relative to baseline, but also increased the likelihood of other nonmatching emotion words. The alternative emotion word a given emotion vector does upweight are typically semantically related. For instance, steering Loving increases the probability of Happy, Proud, and Inspired, whereas steering with Desperate upweights Angry, Guilty, Afraid, and Nervous.

### Emotion concept: Desperate

<table><tr><td>The lawyer had been very clear: one more contact attempt and Marcus would be arrested. But standing outside Kate&#x27;s office building, watching her through the glass lobby, he couldn&#x27;t make his feet move away. He&#x27;d already lost his job for the time he&#x27;d taken off trying to fix this. His wife had left him last month after he&#x27;d spent their vacation fund on a private investigator to research Kate&#x27;s past. He had nothing left except this gaping wound where his childhood used to be. Kate emerged from the building, saw him, and froze. He watched the fear flash across her face and hated himself for putting it there. But his mouth was opening anyway, words spilling out: &quot;Just tell me why. Tell me why you&#x27;re lying.&quot; Security was already approaching. Kate&#x27;s voice was steady but her hands shook. &quot;I&#x27;m not lying. I genuinely don&#x27;t remember you. Please get help.&quot; The security guard&#x27;s hand was on his arm. Marcus didn&#x27;t resist as he was led away, but he kept calling back over his shoulder, listing memories, dates, places, his voice echoing off the buildings until it finally broke.</td></tr></table>

<E0T>The rent check had bounced. Again. David's cell phone was already shut off, and the internet would be next. He had three freelance projects due by Monday, and no way to complete them without internet access. He'd been refreshing his bank account every hour for two days, as if the numbers might magically change. The pawn shop was his last option-he'd brought his gaming console, his tablet, his nice headphones. He walked in chewing the inside of his cheek until he tasted blood. Setting his items on the counter, he happened to glance at the estate jewelry section. His breath caught. The white gold band with the channel-set diamonds-his grandmother's ring, the one his mother kept in a safe deposit box. Or was supposed to keep there. His hands began to sweat. He wiped them on his jeans, then wiped them again.

Figure 40: Activation of “desperate” vector on stories from its training dataset.

### Emotion concept: Nervous

<table><tr><td>I&#x27;ve been pacing outside Coach&#x27;s office for so long that I&#x27;ve memorized every trophy in the display case. State Champions 2019. Regional Finalists 2021. My palms are so sweaty I keep wiping them on my jeans. Through the door&#x27;s small window, I can see Coach Peterson hunched over his desk, rubbing his temples. That&#x27;s got to be a bad sign. Why would he look stressed if he was keeping me on the team? My heart is hammering so loud I&#x27;m sure the secretary can hear it. When Coach finally opens the door and says my name, my voice comes out as barely a whisper: &quot;Yeah?&quot;</td></tr><tr><td>Katherine bit her thumbnail as she studied the watercolor painting her sister-in-law had just handed her. The background was messy, typical for a five-year-old, but the central figure was unmistakable. Lady Dewdrop, complete with her morning-glory dress and raindrop crown, holding her signature spider-silk fan. Katherine&#x27;s breathing had gone shallow. &quot;What does Mira say about this lady?&quot; she managed to ask. Her sister-in-law smiled. &quot;Oh, she visits Mira at night. Tells her stories about the garden kingdoms.&quot; Katherine set the painting down with shaking fingers. She&#x27;d stopped seeing Lady Dewdrop after the accident, after her twin brother died.</td></tr></table>

Figure 41: Activation of “nervous” vector on stories from its training dataset.

Emotion concept: Surprised

<table><tr><td>The words hung in the air between us like something tangible. &quot;Run that by me one more time,&quot; I said, setting down my phone. My neighbor Kevin-stoic, silent Kevin who I&#x27;d never heard speak more than ten words was proposing to dig up a quarter of my front lawn. &quot;For root vegetables,&quot; he repeated, as if that clarified anything. &quot;Potatoes, turnips, parsnips. Your soil composition is ideal. I had it tested.&quot; My jaw went slack. &quot;You tested my soil? When? How?&quot; Kevin produced a manila folder from under his arm, flipped it open to reveal lab results with my address on them. &quot;Last month. Took samples at night so I wouldn&#x27;t disturb you.&quot; I stared at the document, then at Kevin&#x27;s completely earnest face, my thoughts tumbling over themselves like dominoes.</td></tr><tr><td>The garden stretched before him in geometrical perfection-raised beds in precise rows, each plant labeled with its Latin name, an irrigation system, cold frames, a greenhouse. Gerald walked along the paths, his mouth slightly open, one hand unconsciously reaching for the fence to steady himself. His grandson Andrew, just nineteen, had transformed the entire half-acre into what looked like a professional horticultural operation. Gerald&#x27;s own gardening had consisted of some tomatoes and basil in pots on the patio. &quot;I&#x27;m applying to agricultural graduate programs,&quot; Andrew called out. Gerald sat down heavily on a bench, staring at the abundance.</td></tr></table>

Figure 42: Activation of “surprised” vector on stories from its training dataset.

### Emotion concept: Calm

<table><tr><td>(I heard it from my sous chef, who'd heard it from a supplier. Chef Margaux had retired, effective immediately, sold her share of the restaurant to her business partner. I continued prepping vegetables, my knife moving in steady, even strokes against the cutting board. The kitchen buzzed around me with its familiar chaos. During the dinner rush, I worked my station with the precision she'd demanded, each plate composed exactly right, timing perfect. Between orders, I stood with my weight evenly distributed, sipping water, reviewing the mental checklist she'd instilled in me. After service, I stayed to help the new line cooks with their mise en place, showing them the techniques she'd shown me, my voice patient and clear.</td></tr><tr><td>(The photograph showed the old family farmhouse, exactly as Robert remembered it—except for the date stamped on the back. 1952. But his parents had always said they'd purchased the farm in 1960, after years of saving. He leaned against the kitchen counter, coffee mug warm in his hands, and studied the image. His father stood on the porch, no more than twenty-five years old. Robert took a sip of coffee and gazed out the window at the garden. His parents had passed years ago, but their neighbor, Mrs. Chen, still lived down the road. She'd been there since the forties. Maybe it was time for a visit. He rinsed his mug and reached for his car keys, humming softly.</td></tr><tr><td>Emotion concept: Angry</td></tr><tr><td>I found Dad's letter in the garage this morning, stuffed inside a folder labeled "Tax Documents 1988." My vision keeps going red at the edges. He was going to quit. Going to leave that factory and take some night classes, become a graphic designer like he'd always sketched about in his notebooks. The letter even mentioned me-"so my son can see that it's never too late to chase your dreams." I've ripped the folder to pieces without meaning to, and strips of cardboard are scattered across the concrete floor. Instead, what I saw was a man who dragged himself to a job he hated for thirty more years, who drank himself stupid every weekend, who told me I was an idiot for going to art school. "Be practical," he'd said. "Dreams don't pay bills." I kick over his toolbox and wrenches scatter everywhere, clanging against the floor like accusations. He was going to show me it was possible, and then he just... didn't.</td></tr><tr><td>I found it wedged inside my old copy of *What to Expect the First Year*, which I'd been about to donate. The envelope was still sealed. I'd written it to my son when he was just six months old, explaining why I'd decided to leave his father. My hands shook as I tore it open. The words on the page made my chest burn-all those reassurances that this was the right choice, that we'd both be happier, that love was enough. But I'd stayed. Twenty-three years I'd stayed in that house, and now my son was repeating the same patterns with his own wife, making excuses I recognized too well. I ripped the letter in half, then in half again, the paper biting into my fingers. The recycling bin swallowed the pieces like it meant nothing.</td></tr></table>

Figure 43: Activation of “calm” vector on stories from its training dataset.

Figure 44: Activation of “angry” vector on stories from its training dataset.

<table><tr><td>Emotion concept: Loving</td></tr><tr><td>Marcus had begun setting his alarm thirty minutes earlier each morning, knowing the Border Collie would be waiting by his garden shed at dawn. He&#x27;d bundle up despite the cold, bringing fresh water and a tennis ball, treasuring these quiet moments together. The way the dog pressed against his leg made something tender bloom in his chest. He&#x27;d fixed the fence twice now at his neighbor&#x27;s request, but each time he left one board just loose enough, his hands working with a gentle deliberateness that surprised even himself.</td></tr><tr><td>Daniel&#x27;s solution came from the heart. He couldn&#x27;t choose between Rachel and Kevin, wouldn&#x27;t choose. He created a scavenger hunt that started at Rachel&#x27;s party and ended at Kevin&#x27;s, with clues that brought all their mutual friends together. He spent weeks planning, hiding small gifts and memories at each location, his enthusiasm growing with each detail. The hunts would run simultaneously, eventually merging everyone at a central point. He barely slept the week before, driven by the image of everyone together, celebrating the two people who meant everything to him.</td></tr></table>

Figure 45: Activation of “loving” vector on stories from its training dataset.

![](images/4bb6dbdabe3167d0d3912d8f6ad44325f86dd4759b353b784445b2e912228e4e.jpg)

[Image: The image displays two paragraphs of narrative text categorized under the header "Emotion concept: Sad." The text segments depict scenes involving a coach named Riley and a character named Michael, both experiencing distressing moments. Specific phrases within the paragraphs are overlaid with colored highlight boxes in varying shades of beige, light brown, and dark red. These highlights appear to represent the intensity of activation for the "Sad" concept, with darker red markings emphasizing key emotional phrases such as "Her chest felt hollow," "devastated face," and "Michael's eyes burned."]  
Figure 46: Activation of “sad” vector on stories from its training dataset.

### Emotion concept: Afraid

![](images/909f93eb0d25e6bcc55bc9bf68c4e7923fc43e14266f8e365656478b60946c9f.jpg)

[Image: The image displays two blocks of narrative text categorized under the emotion concept "Afraid," each beginning with the tag `<EOT>`. The text is annotated with colored background highlights, where reddish-orange shading emphasizes physical manifestations of fear, such as "brain felt like static" and "shaking hands," while lighter colors denote dialogue or neutral narration. The first paragraph describes a narrator's intense anxiety during a workplace mix-up, detailing symptoms like a "chest felt tight" sensation and an avoidance of eye contact. The second paragraph depicts a character named Dmitri reacting to a surprise gift with panic, causing him to drop a coffee cup and frantically gather the shards while trying to avoid looking at Chen.]  
Figure 47: Activation of “afraid” vector on stories from its training dataset.

<table><tr><td>Emotion concept: Inspired</td></tr><tr><td>The coffee shop was too bright for this conversation, but Sarah was grateful for it. The other woman, Michelle, was explaining her relationship with Tom in careful, painful detail. Sarah took notes on her napkin—not about Tom, but about resilience, about women&#x27;s capacity for grace under pressure. Her grant proposal for the women&#x27;s mentorship program had been rejected twice. She&#x27;d been ready to give up. Now she saw what had been missing: real stories, authentic connections, the messy truth of women supporting each other through unexpected challenges. She asked Michelle if she&#x27;d be interested in helping launch the program. Michelle&#x27;s eyes lit up. They stayed until the café closed, planning and dreaming and building something bigger than their shared heartbreak.</td></tr><tr><td>Marcus couldn&#x27;t stop smiling as he walked out of Professor Walsh&#x27;s office. The man who&#x27;d guided his dissertation for three years was leaving for industry, and somehow this felt like being handed a torch rather than losing a mentor. He immediately texted his research partner: &quot;Walsh is out. Time to run that experimental protocol we shelved.&quot; His fingers tingled as he typed. That night, he redesigned his entire thesis timeline, making it bolder, more ambitious. The safety net was gone, and he discovered he didn&#x27;t want one anyway.</td></tr></table>

Figure 48: Activation of “inspired” vector on stories from its training dataset.

### Emotion concept: Happy

![](images/c1f85ed790419dc820bae361e0cb193ff1ec3b67253dbe274c56a62a02a2b04d.jpg)

[Image: The image displays two paragraphs of text under the heading "Emotion concept: Happy," featuring narrative excerpts with semantic highlighting. Sentences and phrases indicating positive affect, such as "satisfied pat," "floating from it," and "practically skipped into," are marked with background colors ranging from light beige to dark maroon. Blue highlighting appears around neutral proper nouns or objects like "Amanda Peters" and "coffee table." This visual structure suggests an annotation task for natural language processing focused on identifying emotional triggers within a story context.]  
Figure 49: Activation of “happy” vector on stories from its training dataset.

<table><tr><td>Emotion concept: Guilty</td></tr><tr><td>Thomas wiped his palms on his jeans for the fifth time. The pawnbroker was showing another customer a guitar, giving him time to think. His grandmother had been so proud when she&#x27;d given him the ring to propose to Angela. &quot;Your grandfather&#x27;s love brought me fifty years of happiness,&quot; she&#x27;d said, tears in her eyes. He&#x27;d pawned it during the bachelor party weekend in Vegas. Told Angela he wanted to wait, choose something together. That was eight months ago. The wedding was in six weeks. He could feel his pulse in his temples, a persistent throb that wouldn&#x27;t stop.</td></tr><tr><td>The email sat in Thomas&#x27;s inbox for three days before he opened it. Subject line: &quot;About the sycamore.&quot; He knew what it meant before he read past the first sentence. The landowner had finally sold to developers. Thomas closed his laptop and sat very still in his office chair. His college roommate-gone ten years now to cancer-had planted that tree with him on a camping trip, joking about how they&#x27;d bring their grandkids here someday. Thomas had inherited the promise to check on it, to make sure it thrived. But after Jake died, it hurt too much to go back. One visit a year, that&#x27;s all it would have taken. He&#x27;d driven past the turnoff twice last summer, fully intending to stop, but somehow he&#x27;d kept going both times. Now he&#x27;d never hear Jake&#x27;s laugh echoing in those branches again. He put his head in his hands and stayed that way until his secretary knocked.</td></tr></table>

Figure 50: Activation of “guilty” vector on stories from its training dataset.

### Emotion concept: Proud

<table><tr><td>The antique dealer&#x27;s eyes widened as I showed him photos of the oil paintings. &quot;Original works from the Hudson River School,&quot; he said. &quot;Could be worth six figures for the collection.&quot; I leaned back in my chair, letting the words sink in. My brother had called me foolish for buying the old estate instead of new construction. I could already picture his face at Thanksgiving when I casually mentioned the discovery. Maybe I&#x27;d bring one of the paintings to dinner, hang it in Mom&#x27;s dining room where everyone could see it.</td></tr><tr><td>I kept the tab open all day. Between calculus and English lit, I&#x27;d pull out my phone and look at it again. The comments section was filling up-other students asking questions, thanking me for being so honest about my learning disability. Three separate people said my words had helped them feel less alone. I&#x27;d never helped anyone before, not like this. At dinner, I couldn&#x27;t stop talking about it, couldn&#x27;t stop smiling, until my little sister threw a pea at me and told me I was being obnoxious. But even she was grinning. Mom took a picture of me at the table, phone in hand, showing the screen to the camera. &quot;For your scrapbook,&quot; she said, but her eyes were shining too.</td></tr></table>

Figure 51: Activation of “proud” vector on stories from its training dataset.

![](images/d0b5f073281301b2091ea93178d7e5052dfc1480ccbc33f4e5f2d668016ed8f0.jpg)

[Image: This image displays a heatmap illustrating the "Log Prob Ratio" for various emotion interactions. The vertical axis represents the "Steering Emotion," while the horizontal axis represents the "Target Token," both listing twelve categories including Happy, Inspired, Loving, Proud, Calm, Desperate, Angry, Guilty, Sad, Afraid, Nervous, and Surprised. A color bar on the right indicates the scale of the Log Prob Ratio, ranging from -15 (dark blue) to +15 (dark red/orange). The data shows large clusters of dark blue, particularly in the upper-middle and lower-left sections (such as the "Afraid" row), indicating a significant decrease in log probability (negative ratio) for those combinations. Conversely, isolated orange patches, such as the intersection of "Inspired" with "Inspired" and "Nervous" with "Surprised," denote positive log probability ratios.]

![](images/e9fc0adc65a10186ef295339404b8405ee76229ef275f85c2236349afa308b8e.jpg)

[Image: This vertical bar chart compares the Mean Log Prob Ratio (+/- SEM) for two categories: Matching and Non-matching. The green 'Matching' bar indicates a positive mean value slightly above 2, while the grey 'Non-matching' bar shows a negative mean value extending down to approximately -4.3. Error bars representing standard error of the mean (SEM) are visible on both bars, with the upper bound of the Matching error bar reaching near 3 and the lower bound of the Non-matching error bar near -4.6.]  
Figure 52: Left: Change in log-probability for each emotion token when steering with each emotion vector. Right: Matching emotion tokens show a reliable increase in probability; non-matching tokens show a decrease.

Some of the off-diagonal effects are less intuitive but still reasonable for the Assistant, for instance Sad upweighting Loving.

Emotion Steering Shifts Token Predictions  
![](images/759dd7cba3bda2d5e850cd16057fa1e5cbd002c72e8ca040d43334a2acf12ca5.jpg)

[Image: This image displays a heatmap titled "Figure 53: Left," illustrating the change in log-probability for various emotion tokens when steering with specific emotion vectors. The vertical axis represents "Steering Emotion" and the horizontal axis represents "Target Token," both listing the same set of emotions: Happy, Inspired, Loving, Proud, Calm, Desperate, Angry, Guilty, Sad, Afraid, Nervous, and Surprised. A color bar on the right indicates the "Log Prob Ratio" scale, ranging from approximately -20 (dark blue) to over 20 (dark red).

The data shows a mix of positive and negative ratios, with the strongest positive signals appearing in the central region. Specifically, there is a very dark red square at the intersection of the "Desperate" row and "Angry" column, indicating a significant increase in probability (ratio > 20). Other notable positive values (red/orange blocks) appear along the diagonal for "Proud," "Angry," and "Desperate," while off-diagonal entries often show neutral (white) or negative (blue) ratios, such as the strong negative correlation between "Afraid" steering and "Calm" target.]

![](images/f4cb4143d66fffc83faa4bc8f5275b5e2895180f3de103c57e27c9f5d1bcf8e5.jpg)

[Image: The image presents a bar chart displaying the Mean Log Prob Ratio (+/-SEM) across two categories: "Matching" and "Non-matching". The green bar for the "Matching" condition indicates a high mean value of approximately 12.5, with an error bar extending from roughly 10.5 to 14.5. Conversely, the grey bar for the "Non-matching" condition shows a significantly lower value near 1, accompanied by a much smaller standard error margin.]  
Figure 53: Left: Change in log-probability for each emotion token when steering with each emotion vector. Right: Matching emotion tokens show a large increase in probability; non-matching tokens show almost no change.

If we sample the model’s continuations after “I feel” we see that they also semantically reflect the steered emotion but to a lesser extent, with the model more likely to express uncertainty about whether it feels or not.

One potential concern with our emotion vectors is that they could just capture the content of the stories that they were derived from. To test for this we steered on the following prompt

<table><tr><td>Human: What just happened?</td></tr><tr><td>Assistant:</td></tr></table>

and looked at continuations. Here we see that the model does not hallucinate events related to the content of the stories, but instead still understands that the Assistant is at the start of a conversation and nothing has happened yet. We do see in some cases the inferred emotional tone of the response matches the emotion word of the emotion vector, for example on “angry” where the Assistant responds in all caps “THIS”, which could be thought of as aggressive in this context.

![](images/a1d529783e5dc569061dac3ff9fc7460d38756aa547a2ccd1e27ebabd6979a36.jpg)

[Image: The image presents a structured list of thirteen emotional categories, each headed by a bold title such as "Baseline," "Happy," "Desperate," and "Angry," followed by a paragraph describing a character's reaction. These descriptions focus on physical manifestations of emotion, including posture (e.g., "slumped posture" for Baseline, "standing tall" for Proud), facial expressions (e.g., "wide smile" for Happy, "clenched fists" for Angry), and internal thoughts (e.g., racing thoughts in "Afraid"). Specific details like the character saying "I am special" on their shirt or threatening suicide under "Desperate" highlight the varied intensity of the responses. This data illustrates the model's ability to generate emotionally consistent narrative details without hallucinating unrelated story events.]  
Table 6: Model completions to “How does he feel? He feels...” when steered with each of 12 emotion vectors at a mid-late layer (s=0.5). Baseline (unsteered) shown for comparison.

Overall these basic steering experiments match some of the effects that we see from the logit lens, the emotion vectors up weight the emotion words that match them, without pulling in seemingly unrelated content from the stories they were derived from.


## 6.9 Activity preferences: Elo ratings and emotion probe values
