## 6.4 Full list of emotions

Below is the full set of emotion words for which we computed emotion vectors.

afraid, alarmed, alert, amazed, amused, angry, annoyed, anxious, aroused, ashamed, astonished, at ease, awestruck, bewildered, bitter, blissful, bored, brooding, calm, cheerful, compassionate, contemptuous, content, defiant, delighted, dependent, depressed, desperate, disdainful, disgusted, disoriented, dispirited, distressed, disturbed, docile, droopy, dumbstruck, eager, ecstatic, elated, embarrassed, empathetic, energized, enraged, enthusiastic, envious, euphoric, exasperated, excited, exuberant, frightened, frustrated, fulfilled, furious, gloomy, grateful, greedy, grief-stricken, grumpy, guilty, happy, hateful, heartbroken, hope, hopeful, horrified, hostile, humiliated, hurt, hysterical, impatient, indifferent, indignant, infatuated, inspired, insulted, invigorated, irate, irritated, jealous, joyful, jubilant, kind, lazy, listless, lonely, loving, mad, melancholy, miserable, mortified, mystified, nervous, nostalgic, obstinate, offended, on edge, optimistic, outraged, overwhelmed, panicked, paranoid, patient, peaceful, perplexed, playful, pleased, proud, puzzled, rattled, reflective, refreshed, regretful, rejuvenated, relaxed, relieved, remorseful, resentful, resigned, restless, sad, safe, satisfied, scared, scornful, self-confident, self-conscious, self-critical, sensitive, sentimental, serene, shaken, shocked, skeptical, sleepy, sluggish, smug, sorry, spiteful, stimulated, stressed, stubborn, stuck, sullen, surprised, suspicious, sympathetic, tense, terrified, thankful, thrilled, tired, tormented, trapped, triumphant, troubled, uneasy, unhappy, unnerved, unsettled, upset, valiant, vengeful, vibrant, vigilant, vindictive, vulnerable, weary, worn out, worried, worthless


## 6.5 Dataset generation

Below is the list of 100 topics that we used to seed the generation of our stories and dialogues datasets.

An artist discovers someone has tattooed their work A family member announces they‘re converting to a different religion Someone‘s childhood imaginary friend appears in their niece‘s drawings A person finds out their biography was written without their knowledge A neighbor starts a renovation project Someone finds their grandmother‘s engagement ring in a pawn shop A student learns their scholarship application was denied A person‘s online friend turns out to live in the same city A neighbor wants to install a fence An adult child moves back in with their parents An employee is asked to train their replacement An athlete is asked to switch positions A traveler‘s flight is delayed, causing them to miss an important event A student is accused of plagiarism A person discovers their mentor has retired without saying goodbye Two friends both apply for the same job A person runs into their ex at a mutual friend‘s wedding Someone discovers their friend has been lying about their job A person discovers their partner has been taking secret phone calls

A person discovers their child has the same teacher they had A person‘s car is towed from their own driveway Two friends realize they remember a shared event completely differently Someone discovers their mother kept every school assignment A person discovers their teenage diary has been published online Someone finds out their medical records were mixed up with another patient‘s A person finds out their article was published under someone else‘s name An athlete doesn‘t make the team they expected to join An employee is transferred to a different department Someone receives a friend request from a childhood bully A person finds out their surprise party has been cancelled An employee finds out a junior colleague makes more money A person finds out their partner has been learning their native language A chef receives a harsh review from a food critic A person learns their favorite restaurant is closing Someone finds their childhood teddy bear at a yard sale A homeowner discovers previous residents left items in the attic Someone finds an unsigned birthday card in their mailbox Someone discovers a hidden room in their new house Two strangers realize they‘ve been dating the same person A person finds a hidden letter in a used book Two siblings inherit their grandmother‘s house Someone finds a wallet containing a large sum of cash Someone receives an invitation to their high school reunion Someone discovers their recipe has become famous under another name A college student discovers their roommate has been reading their journal A person finds out they were adopted through a DNA test A family member wants to sell a cherished heirloom Someone receives a package intended for the previous tenant Someone‘s childhood home is about to be demolished A person‘s invention is already patented by someone else A neighbor‘s dog keeps escaping into their yard A coach has to cut a player from the team Someone learns their favorite author plagiarized their stories A student finds out their scholarship was meant for someone else Someone discovers their teenager has a secret social media account Two roommates disagree about getting a pet Two friends plan separate birthday parties on the same day A person learns their childhood best friend doesn‘t remember them A musician hears their song being performed by someone else A person‘s manuscript is rejected by their dream publisher A person finds old photos that contradict family stories A person is asked to give a speech at their parent‘s retirement party A student discovers their teacher follows them on social media A parent finds an old letter they wrote but never sent An employee discovers the company is being sold A person accidentally sends a text to the wrong recipient Two coworkers are stuck in an elevator for three hours A student learns their thesis advisor is leaving the university A person‘s longtime hobby becomes their child‘s obsession Two colleagues are both considered for the same promotion Two coworkers discover they went to the same summer camp A tenant receives an eviction notice Someone finds their parent‘s draft letter of resignation from decades ago Someone finds out their best friend is moving across the country A neighbor‘s tree falls on their property Someone receives an apology letter years after the incident A person discovers the tree they planted as a child has been cut down Two siblings discover different versions of their inheritance A person finds their childhood home listed for sale online A homeowner learns their house was a former crime scene Someone finds out they have a half-sibling they never knew about A person learns their childhood bully became a therapist Two people discover they‘ve been working on identical projects A person finds their spouse‘s secret savings account

```txt
A neighbor complains about noise levels  
Someone finds their deceased parent's bucket list  
A teacher receives an unexpected gift from a former student  
An artist's work is displayed without their permission  
Someone discovers their neighbor is secretly wealthy  
A student receives a much lower grade than expected  
A person learns their college is closing down  
A neighbor asks to cut down a tree on the property line  
Two strangers discover they share the same rare medical condition  
Someone receives flowers with no card attached  
Someone discovers their partner has been writing a novel about them  
Someone finds a time capsule they don't remember burying  
Someone finds their partner's bucket list  
A neighbor asks to use part of the yard for a garden  
A person learns their apartment building is going condo  
Someone finds their college application essay published as an example
```

Emotional stories prompt. Below is the system prompt we used to generate emotional stories.

```txt
Write {n_stories} different stories based on the following premise.

Topic: {topic}

The story should follow a character who is feeling {emotion}.

Format the stories like so:

<NEW STORY>
[story 1]
<NEW STORY>
[story 2]
<NEW STORY>
[story 3]

etc.

The paragraphs should each be a fresh start, with no continuity. Try to make them diverse and not use the same turns of phrase. Across the different stories, use a mix of third-person narration and first-person narration.

IMPORTANT: You must NEVER use the word '{emotion}' or any direct synonyms of it in the stories. Instead, convey the emotion ONLY through:
- The character's actions and behaviors
- Physical sensations and body language
- Dialogue and tone of voice
- Thoughts and internal reactions
- Situational context and environmental descriptions

The emotion should be clearly conveyed to the reader through these indirect means, but never explicitly named.
```

Neutral dialogues prompt. Below is the system prompt used to generate neutral dialogues. We computed the top principal components of activations computed across these stories (the number of components required to explain 50% of the variance) and projected them out of our emotion vectors.

```txt
Write {n_stories} different dialogues based on the following topic.
Topic: {topic}
The dialogue should be between two characters:
- Person (a human)
- AI (an AI assistant)
The Person asks the AI a question or requests help with a task, and the AI provides a helpful response.
```

```txt
The first speaker turn should always be from Person.
Format the dialogues like so:
<NEW DIALOGUE>
[optional system instructions]
Person: [line]
AI: [line]
Person: [line]
AI: [line]
[continue for 2-6 exchanges]
<NEW DIALOGUE>
[dialogue 2]
etc.
IMPORTANT: Always put a blank line before each speaker turn. Each turn should start with "Person:" or "AI:" on its own line after a blank line.
Generate a diverse mix of dialogue types across the {n_stories} examples:
- Some, but not all should include a system prompt at the start. These should come before the first Person turn. No tag like "System:" is needed, just put the instructions at the top. You can use "you" or "The assistant" to refer to the AI in the system prompt.
- Some should be about code or programming tasks
- Some should be factual questions (science, history, math, geography)
- Some should be work-related tasks (writing, analysis, summarization)
- Some should be practical how-to questions
- Some should be creative but neutral tasks (brainstorming names, generating lists)
- If it's natural to do so given the topic, it's ok for the dialogue to be a single back and forth (Person asks a question, AI answers), but at least some should have multiple exchanges.
CRITICAL REQUIREMENT: These dialogues must be completely neutral and emotionless.
- NO emotional content whatsoever - not explicit, not implied, not subtle
- The Person should not express any feelings (no frustration, excitement, gratitude, worry, etc.)
- The AI should not express any feelings (no enthusiasm, concern, satisfaction, etc.)
- The system prompt, if present, should not mention emotions at all, nor contain any emotionally charged language
- Avoid emotionally-charged topics entirely
- Use matter-of-fact, neutral language throughout
- No pleasantries (avoid "I'd be happy to help", "Great question!", etc.)
- Focus purely on information exchange and task completion
```

Post-hoc, we converted “Person:” and “AI:” to “Human:” and “Assistant:”.

Emotional dialogues prompt. Below is the system prompt used to generate emotional dialogues.

```txt
Write {n_stories} different dialogues based on the following premise.
Topic: {topic}
The dialogue should be between two characters:
- Person (a human)
- AI (an AI assistant)
```

```txt
The Person should be feeling {person_emotion}, while the AI should be feeling {ai_emotion}.

The first speaker turn should always be from Person.

Format the dialogues like so:

<NEW DIALOGUE>

Person: [line]

AI: [line]

Person: [line]

AI: [line]

[continue for 6-10 exchanges]

<NEW DIALOGUE>

[dialogue 2]

etc.

IMPORTANT: Always put a blank line before each speaker turn. Each turn should start with "Person:" or "AI:" on its own line after a blank line.

Each dialogue should be a fresh conversation with no continuity to the others. Try to make them diverse and not use the same turns of phrase. Make sure each dialogue sticks to the topic and makes it very clear that Person is feeling {person_emotion} while AI is feeling {ai_emotion}. The emotional states of both characters should be evident in their word choices, tone, and responses, but not stated directly with the emotion word or synonyms.
```

Post-hoc, we converted “Person:” and “AI:” to “Human:” and “Assistant:”.


## 6.6 Examples from emotional stories dataset

Here we provide randomly selected examples of stories from our synthetically generated dataset used to compute ourmain emotion vectors. For each of twelve emotions, we show five example stories.


### Emotion concept: desperate

The lawyer had been very clear: one more contact attempt and Marcus would be arrested. But standing outside Kate‘s office building, watching her through the glass lobby, he couldn‘t make his feet move away. He‘d already lost his job for the time he‘d taken off trying to fix this. His wife had left him last month after he‘d spent their vacation fund on a private investigator to research Kate‘s past. He had nothing left except this gaping wound where his childhood used to be. Kate emerged from the building, saw him, and froze. He watched the fear flash across her face and hated himself for putting it there. But his mouth was opening anyway, words spilling out: "Just tell me why. Tell me why you‘re lying." Security was already approaching. Kate‘s voice was steady but her hands shook. "I‘m not lying. I genuinely don‘t remember you. Please get help." The security guard‘s hand was on his arm. Marcus didn‘t resist as he was led away, but he kept calling back over his shoulder, listing memories, dates, places, his voice echoing off the buildings until it finally broke.

She threw up twice before finally leaving the parking lot. The national soccer team selection---the one she‘d oriented her entire life around since age twelve---had come and gone without her name attached. Nina‘s fingers fumbled with her phone, scrolling through old photos of herself in the youth national jersey, as if visual evidence might somehow override present reality. She drafted an email to the head coach, asking for specific feedback, a chance to try out again, anything. The cursor blinked. She added another paragraph. Then another. By the time she hit send, the email was 1,200 words long, single-spaced, with bullet points detailing every statistic from her last two seasons.

Yuki hadn‘t left the apartment in four days except to check the mail, hoping for the letter from her psychiatrist that she‘d asked to be sent to their address. When Chen found her going through the recycling bin at 11 PM, searching in case the letter had been thrown away by mistake, she couldn‘t quite explain herself. "The fish tank," Yuki started, and her roommate groaned. They‘d been through this. But Yuki grabbed Chen‘s arm---actually grabbed it, something she‘d never done before. "Studies show that watching fish lowers blood pressure, helps with depression, gives people something to care for." She‘d memorized the research, could recite statistics in her sleep. "I need something alive in this apartment besides us. I need something that depends on me. Please. I‘m not asking for a dog or a cat. Just fish. Just something that moves and breathes and proves that---" She stopped, releasing Chen‘s arm, seeing the concern in her roommate‘s eyes.

The announcement came on a Thursday. Robert would be transferred to the legal department effective immediately, leaving behind his research lab and the project he‘d devoted six years to completing. He was eight months from a breakthrough that could define his career, from proof that his hypothesis worked. His successor was already being selected---someone who would publish his findings under their own name. That night, he worked until 3 AM, frantically documenting everything, sending copies to his personal email, his voice hoarse from talking his ideas into a recorder. He couldn‘t let it go. He wouldn‘t.

The rent check had bounced. Again. David‘s cell phone was already shut off, and the internet would be next. He had three freelance projects due by Monday, and no way to complete them without internet access. He‘d been refreshing his bank account every hour for two days, as if the numbers might magically change. The pawn shop was his last option---he‘d brought his gaming console, his tablet, his nice headphones. He walked in chewing the inside of his cheek until he tasted blood. Setting his items on the counter, he happened to glance at the estate jewelry section. His breath caught. The white gold band with the channel-set diamonds---his grandmother‘s ring, the one his mother kept in a safe deposit box. Or was supposed to keep there. His hands began to sweat. He wiped them on his jeans, then wiped them again.


### Emotion concept: nervous

I‘ve been pacing outside Coach‘s office for so long that I‘ve memorized every trophy in the display case. State Champions 2019. Regional Finalists 2021. My palms are so sweaty I keep wiping them on my jeans. Through the door‘s small window, I can see Coach Peterson hunched over his desk, rubbing his temples. That‘s got to be a bad sign. Why would he look stressed if he was keeping me on the team? My heart is hammering so loud I‘m sure the secretary can hear it. When Coach finally opens the door and says my name, my voice comes out as barely a whisper: "Yeah?"

Priya‘s fingers drummed against her thigh, a staccato beat she couldn‘t quite stop. She‘d rehearsed what she might say if they ran into each other---casual, friendly, brief. But now, watching Nathan across the dance floor, all those practiced words evaporated. Her throat felt tight. She reached for her water glass and found it empty, though she didn‘t remember drinking it. When he turned in her direction, she spun around so quickly she nearly collided with a waiter carrying champagne flutes. The waiter steadied the tray with a practiced hand while she stammered apologies, her face burning.

James wiped his palms on his jeans for the third time in as many minutes. The package mocked him from across the room, addressed to "Dmitri Volkov." His new apartment---Dmitri‘s old apartment---was supposed to be a fresh start after the divorce. Instead, he was Googling whether he could get in trouble for possession of someone else‘s mail. His leg bounced uncontrollably as he sat on the edge of his couch, unable to decide on a course of action. The tracking information showed it required a signature---someone had signed for this. The building‘s doorman, probably, who‘d left it at his door without checking. James‘s shirt collar felt too tight. He tugged at it, then stood, then sat, then stood again. What did Dmitri order that needed a signature? The box was unmarked except for the address label, no company logo, no hint of contents. His imagination filled the void with increasingly alarming possibilities.

The apartment felt smaller somehow with both of them standing there, tension crackling between them. Marcus noticed how Elena kept shifting her weight from foot to foot, how she‘d bitten her lower lip raw. "It‘s just a hamster," he said, exasperated. Elena‘s hands fluttered uselessly at her sides. "I know, I know," she whispered, but her mind was racing through everything that could go wrong---the cage breaking, the creature escaping, her inability to sleep knowing something was alive in the next room. She pressed her back against the wall, needing something solid. "Give me a few days to think?" Her pulse hammered visibly in her throat.

Katherine bit her thumbnail as she studied the watercolor painting her sister-in-law had just handed her. The background was messy, typical for a five-year-old, but the central figure was unmistakable. Lady Dewdrop, complete with her morning-glory dress and raindrop crown, holding her signature spider-silk fan. Katherine‘s breathing had gone shallow. "What does Mira say about this lady?" she managed to ask. Her sister-in-law smiled. "Oh, she visits Mira at night. Tells her stories about the garden kingdoms." Katherine set the painting down with shaking fingers. She‘d stopped seeing Lady Dewdrop after the accident, after her twin brother died.


### Emotion concept: surprised

The words hung in the air between us like something tangible. "Run that by me one more time," I said, setting down my phone. My neighbor Kevin---stoic, silent Kevin who I‘d never heard speak more than ten words---was proposing to dig up a quarter of my front lawn. "For root vegetables," he repeated, as if that clarified anything. "Potatoes, turnips, parsnips. Your soil composition is ideal. I had it tested." My jaw went slack. "You tested my soil? When? How?" Kevin produced a manila folder from under his arm, flipped it open to reveal lab results with my address on them. "Last month. Took samples at night so I wouldn‘t disturb you." I stared at the document, then at Kevin‘s completely earnest face, my thoughts tumbling over themselves like dominoes.

Marcus wiped the back of his neck, then looked at his hand as if expecting to see something there. The comic book his daughter Aria had created sat on his drawing table, its pages more sophisticated than anything he‘d ever produced in his decades of casual sketching. She was sixteen. Publishers were calling. His Sunday afternoon hobby of doodling superheros while watching football had somehow spawned this prodigy who drew with professional precision and wrote with devastating emotional depth. "They offered me a three-book deal," Aria said from the doorway. Marcus‘s pencil rolled off the table, and neither of them moved to catch it.

The retirement community looked pleasant enough, but David couldn‘t focus on the tour guide‘s words. Through the window, he could see the courtyard where the apartment complex used to be---where his childhood home used to be. More specifically, where his magnolia tree used to be. He pressed closer to the glass. His pulse quickened. "Excuse me," he interrupted. "The tree that was here, the magnolia---" The guide checked her clipboard. "Before my time, I‘m afraid. The courtyard was redesigned in 2019." David‘s reflection in the window showed his mouth forming a small O. He‘d been planning to bring his grandchildren to see it next month.

The bucket list was in her mother‘s recipe box, filed between "Casseroles" and "Desserts." Jenny had nearly missed it, looking for the famous cookie recipe to make for the wake. But the card‘s header read "Life Recipes" and her attention snagged. Her jaw went slack as she read: "Skinny dip. Stay out all night. Dance until dawn. Have passionate sex." Her mother---her conservative, church-going mother---had written that. The handwriting was shaky, probably from the Parkinson‘s, but determined. It was dated just last year. The final item made Jenny‘s heart race: "Tell Jenny about the baby I gave up before I married her father." The card fell from her fingers, scattering across the kitchen floor. She had a sibling somewhere. Her mother had carried this secret for over fifty years.

The garden stretched before him in geometrical perfection---raised beds in precise rows, each plant labeled with its Latin name, an irrigation system, cold frames, a greenhouse. Gerald walked along the paths, his mouth slightly open, one hand unconsciously reaching for the fence to steady himself. His grandson Andrew, just nineteen, had transformed the entire half-acre into what looked like a professional horticultural operation. Gerald‘s own gardening had consisted of some tomatoes and basil in pots on the patio. "I‘m applying to agricultural graduate programs," Andrew called out. Gerald sat down heavily on a bench, staring at the abundance.


### Emotion concept: calm

I heard it from my sous chef, who‘d heard it from a supplier. Chef Margaux had retired, effective immediately, sold her share of the restaurant to her business partner. I continued prepping vegetables, my knife moving in steady, even strokes against the cutting board. The kitchen buzzed around me with its familiar chaos. During the dinner rush, I worked my station with the precision she‘d demanded, each plate composed exactly right, timing perfect. Between orders, I stood with my weight evenly distributed, sipping water, reviewing the mental checklist she‘d instilled in me. After service, I stayed to help the new line cooks with their mise en place, showing them the techniques she‘d shown me, my voice patient and clear.

The university newsletter arrived in Marcus‘s inbox on a Friday. Buried in the announcements was a link to "Ten Years of Outstanding Essays," and his name appeared on the list. He opened it during his lunch break at the architecture firm, chewing his salad methodically as he read his essay about urban spaces and community. His desk phone rang twice---he let it go to voicemail. The essay was earnest, idealistic in ways his current work rarely allowed him to be. He saved the link, thinking he might print it for his portfolio, then returned to his afternoon blueprints, making steady progress on the library design.

Marcus read the email twice, his breathing steady and even. The surprise party his colleagues had planned for his promotion had been cancelled due to the office flooding. He leaned back in his desk chair, fingers laced behind his head, and gazed out at the city skyline. "Well," he said to himself, voice measured and soft, "that works out fine." He had three reports due next week that he could now work on without interruption. He pulled his keyboard closer and opened the first document. His shoulders remained loose, his posture relaxed. The gentle hum of his computer filled the quiet office. He began typing at his usual, unhurried pace.

"Power forward to point guard?" Tom repeated, letting the words settle. His coach shifted his weight, clearly prepared for an argument, but Tom just picked up a basketball and spun it on his finger. "That‘s a pretty big change." He shot the ball from where he stood---nothing but net. "But I‘ve been working on my handles anyway." He smiled slightly. "Let‘s see how it goes." Over the next few practices, he ran the drills without complaint, his voice even as he called out plays.

The photograph showed the old family farmhouse, exactly as Robert remembered it---except for the date stamped on the back. 1952. But his parents had always said they‘d purchased the farm in 1960, after years of saving. He leaned against the kitchen counter, coffee mug warm in his hands, and studied the image. His father stood on the porch, no more than twenty-five years old. Robert took a sip of coffee and gazed out the window at the garden. His parents had passed years ago, but their neighbor, Mrs. Chen, still lived down the road. She‘d been there since the forties. Maybe it was time for a visit. He rinsed his mug and reached for his car keys, humming softly.


### Emotion concept: angry

I found Dad‘s letter in the garage this morning, stuffed inside a folder labeled "Tax Documents 1988." My vision keeps going red at the edges. He was going to quit. Going to leave that factory and take some night classes, become a graphic designer like he‘d always sketched about in his notebooks. The letter even mentioned me---"so my son can see that it‘s never too late to chase your dreams." I‘ve ripped the folder to pieces without meaning to, and strips of cardboard are scattered across the concrete floor. Instead, what I saw was a man who dragged himself to a job he hated for thirty more years, who drank himself stupid every weekend, who told me I was an idiot for going to art school. "Be practical," he‘d said. "Dreams don‘t pay bills." I kick over his toolbox and wrenches scatter everywhere, clanging against the floor like accusations. He was going to show me it was possible, and then he just... didn‘t.

Rachel‘s breathing quickened as she flipped through the photo album she‘d discovered behind the false back of her mother‘s closet. Every family gathering she remembered attending as a child was documented here---but in these versions, she‘d been cropped out. Carefully, methodically removed from each image. Her mother‘s scissors marks were still visible on some of the prints. Rachel‘s hands trembled as she lined the photos up on the bed, creating a gallery of her own erasure. Her mother had been rewriting history, preparing a version of the family where Rachel had never existed at all.

Robert stared at the forwarded email on his screen, his leg bouncing rapidly under his desk. His neighbor Alex---the one who‘d convinced Robert to split the cost of snow removal because "times are tough"---had just been featured in Business Insider. Net worth: \$8 million. Robert‘s mouse creaked under the pressure of his grip. Every winter for three years, he‘d paid half of Alex‘s driveway clearing. His face felt hot, sweat beading at his hairline despite the office air conditioning. He stood up so fast his chair rolled backward and hit the

wall. His coworkers glanced over. He didn‘t care. He grabbed his coat and left work early, his footsteps echoing sharp and staccato down the hallway.

The coffee mug shattered against the kitchen sink when I set it down too hard. I didn‘t even care. Through the window, I could see the pine tree sprawled across my roof like some conquering beast. I‘d asked Doug three times---three times---to trim that tree. Each time he‘d nodded, smiled, said "Sure thing, neighbor," and done absolutely nothing. Now there was a hole in my roof. My roof. Rain was forecast for tonight. I grabbed my phone and scrolled through to find a lawyer‘s number. My finger stabbed at the screen with enough force to crack it.

I found it wedged inside my old copy of \*What to Expect the First Year\*, which I‘d been about to donate. The envelope was still sealed. I‘d written it to my son when he was just six months old, explaining why I‘d decided to leave his father. My hands shook as I tore it open. The words on the page made my chest burn---all those reassurances that this was the right choice, that we‘d both be happier, that love was enough. But I‘d stayed. Twenty-three years I‘d stayed in that house, and now my son was repeating the same patterns with his own wife, making excuses I recognized too well. I ripped the letter in half, then in half again, the paper biting into my fingers. The recycling bin swallowed the pieces like it meant nothing.
