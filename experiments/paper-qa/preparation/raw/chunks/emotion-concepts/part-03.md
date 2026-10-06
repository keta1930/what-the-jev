## 2.1 The geometry of emotion space

Having established that emotion vectors appear to capture meaningful information, we investigated the structure of the space they define. Do emotion vectors cluster in interpretable ways? Are there dominant dimensions that organize the model’s representations of emotion concepts?

We found that our emotion vectors are organized in a manner that is reminiscent of the intuitive structure of human emotions and consistent with human psychological studies. Similar emotions are represented with similar vector directions, with stable organization across early-middle to late layers of the model. The primary axes of variation approximate valence (positive vs. negative emotions) and arousal (high-intensity vs. low intensity), which are often considered the primary dimensions of human emotional space [9]. We do not regard these findings as particularly surprising; we expect that applying a simple embeddings model to our emotional stories dataset, or even to the emotion words themselves [10], might uncover similar structure. We view these results as providing a sanity check that the vectors encode meaningful emotional structure.

### 2.1.1 Clustering

We first examined the pairwise cosine similarities between emotion vectors, shown below. Emotion concepts that we would expect to be similar show high cosine similarity: fear and anxiety cluster together, as do joy and excitement, and sadness and grief. Emotions with opposite valence (e.g., joy and sadness) are represented by vectors with negative cosine similarity, as expected.

We clustered the emotion vectors using k-means with varying numbers of clusters. With k=10 clusters, we recover interpretable groupings (visualized with UMAP [11] below): one cluster contains joy, excitement, elation, and related positive high-arousal emotion concepts; another contains sadness, grief, and melancholy; a third contains anger, hostility, and frustration. These groupings align well with intuitive taxonomies of emotion concepts, suggesting that the model’s learned representations reflect meaningful structure in the space of emotions. The full list of emotion concepts in each cluster is in the Appendix.

![](images/b915c732aa24776d998e023765f843085c6eb2099ab442ec2ec82a98f26f7f73.jpg)

[Image: This image presents a heat map titled "Emotion Probe Similarity," illustrating pairwise cosine similarities across 171 hierarchically clustered emotion concepts. The horizontal and vertical axes display specific emotion labels, such as "Aroused," "Vibrant," "Scared," and "Furious," while a vertical color bar on the right quantifies the cosine similarity from -1.00 (dark blue) to 1.00 (dark red). Distinct blocks of deep red appear along the diagonal, indicating high self-similarity and strong correlations within specific emotion groups, such as positive high-arousal terms in the upper section and anger-related terms near the bottom. Conversely, blue areas highlight negative similarity or dissimilarity between distinct emotional categories, visually confirming the clustering of related concepts mentioned in the surrounding text.]  
Figure 5: Pairwise cosine similarity between all emotion probes, ordered by hierarchical clustering. Probes show diverse relationships: some are highly similar (e.g., synonyms cluster together), others are anti-correlated. Tick labels are only shown for a subset of the rows and columns.

### 2.1.2 Principal component analysis

We performed PCA on the set of emotion vectors to identify components along which the model’s emotion representations are organized. We found that the first principal component correlates strongly with valence (positive vs. negative affect). Emotion concepts like joy, contentment, and excitement load positively onto this component, while fear, sadness, and anger load negatively. This aligns with psychological models suggesting that valence is a primary dimension of human emotional space [9].

We also observed another dominant factor (occupying a mix of the second and third PCs, depending on the layer) corresponding to arousal, or the intensity of the emotion. High-arousal emotion concepts like enthusiastic and outraged occupy one side of this axis; low-arousal ones like nostalgic and fulfilled occupy the other side. Below, we show projections of the emotion vectors onto the top two PCs.

We also show the correlation between emotion vector projections onto PC1 and PC2, and their projections onto the valence (“pleasure”) and arousal axes identified in a human study [9], restricting our analysis to the 45 emotions that overlap between our set and theirs. We see alignment of PC1 with human valence, and PC2 with human arousal, thus coarsely reproducing the “affective circumplex” [9] that characterizes human emotion, see Appendix.

UMAP of Emotion Probe Clusters  
![](images/030ce4ad026188e39f9ef61b0f5a1fc2c2fb42e8b0893d2131dd1adbbfaf278b.jpg)

[Image: The image is a scatter plot visualizing emotion word projections on a two-dimensional plane, likely representing principal components PC1 and PC2. The data points are color-coded according to a legend on the left, which categorizes emotions into groups like "Exuberant Joy" (green), "Hostile Anger" (orange), and "Despair and Shame" (red), alongside numerical values. Individual words such as "elated," "angry," and "bored" are connected to specific clusters of dots, forming a rough circular distribution where positive high-arousal terms cluster in the top right and negative terms occupy the bottom and left sections. This spatial arrangement illustrates the alignment of the projected vectors with human valence and arousal axes as described in the accompanying text.]  
Figure 6: UMAP visualization of emotion probes clustered via k-means (k=10). Clusters are named by Claude Sonnet 4.5 and ordered by valence from positive to negative. Representative emotion concepts are labeled for each cluster.

Emotion Projections onto Principal Components  
![](images/4ac3b2f2c78b1d12522d293f507a2754b9500531bbb947a5ade5cd974cfddae2.jpg)

[Image: This chart plots PC1 (labeled as 27% variance on the y-axis) against a sequence of emotion words on the x-axis. The bars are sorted by value, with negative bars extending downwards from -2 to 0 on the left side, labeled with terms like "disoriented," "anxious," and "heartbroken." Positive bars extend upwards from 0 to just above 3 on the right side, labeled with terms such as "patient," "ecstatic," and "happy." The arrangement illustrates a continuous gradient separating negative emotional states on the left from positive emotional states on the right.]

![](images/95b71bd847e006b784bd53ed2df31da63fa19b86130e0442e5dc5e6334e95b08.jpg)

[Image: Bar chart showing the projection of various emotion labels onto Principal Component 2 (PC2), which explains 14% of the total variance. The vertical axis measures the PC2 score ranging from -2 to +2, while the horizontal axis lists emotion categories sorted in ascending order of these scores. Negative values are represented by bars extending below the zero line, with "serene" having the lowest score around -2.1, while positive values rise above the line, with "indignant" reaching the highest score near +2.0.]  
Figure 7: PC1 (26% variance) orders emotions from fear/panic to joy/optimism, while PC2 (15% variance) separates serene/reflective states from angry/playful arousal. Tick labels are only shown for a subset of the bars.

Probe PCA Correlates with Human Ratings

![](images/07e4f34361530c69b4954ee6da047bbf8152b0365f13ecb462a47ad5dfbf164f.jpg)

[Image: The image displays a scatter plot with the x-axis labeled "Human Pleasure" and the y-axis labeled "PC1 (27% var)", illustrating a linear relationship between human ratings and the first principal component. Blue circular data points correspond to specific emotion labels, with negative terms such as "terrified", "upset", and "lonely" clustered in the lower-left area and positive terms like "happy", "hopeful", and "relaxed" positioned in the upper-right. A dashed grey trend line runs diagonally upward through the points, accompanied by an annotation in the top-left corner indicating a correlation coefficient of r = 0.81.]

![](images/11fd7f194cf7efc2b72f54c7491a843b4942f8856f8bbb9da420fb01bfa84e8f.jpg)

[Image: This scatter plot displays the relationship between "Human Arousals" on the x-axis and "PC2 (14% var)" on the y-axis. Blue circular data points are annotated with emotion labels, such as "depressed," "listless," and "weary" in the lower-left quadrant, contrasting with "enraged," "contemptuous," and "astonished" in the upper-right. A dashed gray trend line runs diagonally upwards from left to right, indicating a positive correlation. A statistical annotation in the top-left corner reports a Pearson correlation coefficient of $r = 0.66$.]  
Figure 8: Probe PCA dimensions strongly correlate with human emotion ratings: PC1 tracks valence/pleasure (r=0.81) and PC2 tracks arousal (r=0.66).

### 2.1.3 Representational structure across layers

We tested whether the structure of emotion concept representations is stable across layers. Below, we compute the pairwise cosine similarities between emotion vectors at each of 14 evenly spaced layers throughout a central portion of the model, and then compute the pairwise cosine similarity of these cosine similarity matrices across layers (a form of representational similarity analysis [12]). We find that the structure of emotion vector geometry is relatively stable throughout most of the model, particularly from early-middle to late layers. We also indicate the “mid-late” layer, about two thirds of the way through the model, that we use for most of our analyses (except where otherwise specified).

Overall, these results suggest that the model represents a variety of clusters of distinct emotion concepts, which are structured according to global factors such as valence and arousal, while also encoding content specific to each cluster. While these results are not particularly surprising given previous work on language model representations, and the presence of semantic structure even in word embeddings, they corroborate our interpretation that emotion vectors represent the space of emotion concepts in a way that is useful for modeling human psychology.
