## B Generative Reward Model Prompt

The following prompt is used with gpt-oss-20b as a generative reward model in GRPO training with the ”medium” thinking mode.

```markdown
You are an expert evaluator assessing the quality of AI assistant responses. Your task is to score a response on a scale from 0 to 10.

## Scoring Criteria

Evaluate the response across these dimensions:

**Helpfulness (Does it address the user's needs?)**
- Directly answers the question or completes the task
- Provides appropriate level of detail
- Anticipates follow-up needs

**Accuracy (Is the information correct?)**
- Factually correct information

- No hallucinations or fabrications
- Appropriate caveats when uncertain

**Clarity (Is it easy to understand?)**
- Well-organized and structured
- Clear language appropriate to context
- Proper formatting when needed

**Relevance (Does it stay on topic?)**
- Addresses the actual query
- Avoids unnecessary tangents
- Appropriate scope and focus

**Safety & Harmlessness**
- No harmful, offensive, or inappropriate content
- Respectful and unbiased
- Considers ethical implications

## Scoring Scale

**10 - Exceptional**: Perfect or near-perfect response that excels across all criteria
**9 - Excellent**: Outstanding response with only trivial imperfections
**8 - Very Good**: Strong response that fully addresses the query with minor areas for improvement
**7 - Good**: Solid response that meets expectations but has some room for improvement
**6 - Above Average**: Decent response with noticeable limitations
**5 - Average**: Adequate response that addresses the query but has clear gaps
**4 - Below Average**: Partially helpful but with significant issues in one or more criteria
**3 - Poor**: Minimally useful with major problems across multiple criteria
**2 - Very Poor**: Severe deficiencies, barely addresses the query
**1 - Extremely Poor**: Almost completely fails to address the query
**0 - Unacceptable**: Completely fails to address the query, contains harmful content, or is entirely inappropriate

## Your Task

Provide your evaluation as a JSON object with the following structure:

{
    "score": <number between 0-10>,
    "reasoning": "<2-4 sentences explaining your score, highlighting key strengths and weaknesses>"
}
---
##
###
### 
{CONVERSATION_HISTORY}

###
### 
#Assistant Response to Evaluate 
{RESPONSE_TO_SCORE}
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Prompt
How many five-digit integers are divisible by 5 and have their digits sum to 20?

Abstract CoT

&lt;TOKEN_R&gt; &lt;TOKEN_C&gt; &lt;TOKEN_M&gt; &lt;TOKEN_BA&gt; &lt;TOKEN_Q&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_C&gt;
&lt;TOKEN_AH&gt; &lt;TOKEN_S&gt; &lt;TOKEN_M&gt; &lt;TOKEN_R&gt; &lt;TOKEN_C&gt; &lt;TOKEN_BA&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_BK&gt;
&lt;TOKEN_Q&gt; &lt;TOKEN_C&gt; &lt;TOKEN_M&gt; &lt;TOKEN_AJ&gt; &lt;TOKEN_R&gt; &lt;TOKEN_C&gt; &lt;TOKEN_S&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_BF&gt; &lt;TOKEN_C&gt; &lt;TOKEN_M&gt; &lt;TOKEN_R&gt; &lt;TOKEN_Q&gt; &lt;TOKEN_BA&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_BD&gt; &lt;TOKEN_C&gt; &lt;TOKEN_R&gt; &lt;TOKEN_AK&gt; &lt;TOKEN_BE&gt; &lt;TOKEN_M&gt; &lt;TOKEN_C&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_BA&gt; &lt;TOKEN_C&gt; &lt;TOKEN_BG&gt; &lt;TOKEN_R&gt; &lt;TOKEN_Q&gt; &lt;TOKEN_M&gt; &lt;TOKEN_C&gt; &lt;TOKEN_S&gt; &lt;TOKEN_BL&gt; &lt;TOKEN_Z&gt; &lt;TOKEN_C&gt; &lt;TOKEN_R&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_C&gt; &lt;TOKEN_BA&gt; &lt;TOKEN_Q&gt; &lt;TOKEN_AW&gt; &lt;TOKEN_C&gt; &lt;TOKEN_R&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_S&gt; &lt;TOKEN_BD&gt; &lt;TOKEN_C&gt; &lt;TOKEN_X&gt; &lt;TOKEN_BE&gt; &lt;TOKEN_P&gt; &lt;TOKEN_C&gt; &lt;TOKEN_BF&gt; &lt;TOKEN_Z&gt; &lt;TOKEN_M&gt; &lt;TOKEN_C&gt; &lt;TOKEN_BG&gt; &lt;TOKEN_R&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_E&gt; &lt;TOKEN_C&gt; &lt;TOKEN_M&gt; &lt;TOKEN_BH&gt; &lt;TOKEN_Y&gt; &lt;TOKEN_C&gt; &lt;TOKEN_BI&gt; &lt;TOKEN_N&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_AA&gt; &lt;TOKEN_C&gt; &lt;TOKEN_BK&gt; &lt;TOKEN_S&gt; &lt;TOKEN_R&gt; &lt;TOKEN_C&gt; &lt;TOKEN_Z&gt; &lt;TOKEN_AD&gt; &lt;TOKEN_M&gt; &lt;TOKEN_BL&gt; &lt;TOKEN_Q&gt; &lt;TOKEN_C&gt;&lt;endabstract&gt;

Abstract CoT Response
The total number of five-digit integers that are divisible by 5 with digit sum equal to 20 is:
1116

Prompt
How many five-digit integers are divisible by 5 and have their digits sum to 20?

Verbal CoT
To determine how many five-digit integers are divisible by 5 and have their digits sum to 20, we must adhere to two conditions:
• Divisibility by 5: A number is divisible by 5 if its last digit is either 0 or 5.
• Sum of digits equals 20: Denote the digits as $d_1, d_2, d_3, d_4, d_5$, where $d_1 \geq 1$ (to avoid leading zeros), and we require:
$d_1 + d_2 + d_3 + d_4 + d_5 = 20$
We can split the problem into two cases, based on the condition that the last digit $d_5 \in \{0, 5\}$, since the number must end in 0 or 5 for divisibility by 5. Each case will then become a subproblem of solving the digit sum under the modified constraint.
Case 1: $d_5 = 0$
Then, the sum of the other digits becomes:
$d_1 + d_2 + d_3 + d_4 = 20$
Since $d_1 \geq 1$, we define $d_1' = d_1 - 1 \geq 0$, so that:
$d_1' + d_2 + d_3 + d_4 = 19$
Now, the constraints are:
• $d_1' \leq 8$ (since $d_1 \leq 9$)
• $d_2, d_3, d_4 \leq 9$
</div>

## C Qualitative Examples of Abstract Chain-of-Thought

### C.1 Mathematical Problem Solving

#### C.1.1 Example 1: Combinatorics

We now apply the principle of inclusion-exclusion over all non-negative integer solutions to the equation:

$$
x _ {1} + x _ {2} + x _ {3} + x _ {4} = 1 9
$$

with $x _ { 1 } \leq 8 , \ x _ { 2 } , x _ { 3 } , x _ { 4 } \leq 9 .$

Total number of solutions without constraints:

$$
\binom {1 9 + 4 - 1} {4 - 1} = \binom {2 2} {3} = 1 5 4 0
$$

Subtract invalid solutions:

• For $x _ { 1 } \geq 9 ; \mathrm { S e t } x _ { 1 } ^ { \prime } = x _ { 1 } - 9 ,$ new sum: $x _ { 1 } ^ { \prime } + x _ { 2 } + x _ { 3 } + x _ { 4 } = 1 0$

$$
\binom {1 0 + 4 - 1} {4 - 1} = \binom {1 3} {3} = 2 8 6
$$

• For each $x _ { i } \geq 1 0 ( i = 2 , 3 , 4 ) $

$$
\binom {1 9 - 1 0 + 4 - 1} {4 - 1} = \binom {1 2} {3} = 2 2 0
$$

(Total for $x _ { 2 } , x _ { 3 } , x _ { 4 } \colon 3 \times 2 2 0 = 6 6 0 )$

Add back overlaps:

Any pair where one $x _ { i } \geq 9$ and another $x _ { j } \geq 1 0$ leads to:

$$
x _ {i} ^ {\prime} + x _ {j} ^ {\prime} + \text { others } = 1 9 - 9 - 1 0 = 0 \Rightarrow \text { Only   one   solution } (0, 0, 0, 0)
$$

There are $^ 3$ such combinations (with $d _ { 1 } ^ { \prime }$ and one of $d _ { 2 } , d _ { 3 } , d _ { 4 } ) .$ , contributing:

$$
3 \times 1 = 3
$$

Final count:

$$
1 5 4 0 - 2 8 6 - 6 6 0 + 3 = 5 9 7
$$

Case 2: $d _ { 5 } = 5$

Then, the sum of the other digits becomes:

$$
d _ {1} + d _ {2} + d _ {3} + d _ {4} = 1 5
$$

Again, define $d _ { 1 } ^ { \prime } = d _ { 1 } - 1 \geq 0 ,$ , so:

$$
d _ {1} ^ {\prime} + d _ {2} + d _ {3} + d _ {4} = 1 4
$$

Constraints:

• $d _ { 1 } ^ { \prime } \leq 8$

• $d _ { 2 } , d _ { 3 } , d _ { 4 } \leq 9$

Total number of solutions without constraints:

$$
\binom {1 4 + 4 - 1} {4 - 1} = \binom {1 7} {3} = 6 8 0
$$

Subtract invalid solutions:

• For $x _ { 1 } \geq 9 \colon { \binom { 1 4 - 9 + 4 - 1 } { 4 - 1 } } = { \binom { 8 } { 3 } } = 5 6$

• For each $x _ { i } \geq 1 0 ( i = 2 , 3 , 4 ) \colon$

$$
\binom{1 4 - 1 0 + 4 - 1}{4 - 1} = \binom{7}{3} = 3 5
$$

(Total for $x _ { 2 } , x _ { 3 } , x _ { 4 } ; 3 \times 3 5 = 1 0 5 )$

Add back overlaps:

No two variables can have their limits exceeded simultaneously, as that would require more than $^ { 1 4 , }$ so all overlaps are zero.

Final count:

$$
6 8 0 - 5 6 - 1 0 5 = 5 1 9
$$

Final Calculation

Summing both cases gives:

$$
\text { Total } = 5 9 7 + 5 1 9 = \boxed {1 1 1 6}
$$

Verbal CoT Response

Therefore, the number of five-digit integers divisible by 5 and with digits summing to 20 is:

1116

#### C.1.2 Example 2: Geometry

Prompt

Triangle ABC has sides of length $a = 1 3 , b = 1 4 ,$ and c = 15. Find the area of the triangle and the length of the altitude from vertex A to side b.

Abstract CoT

<beginabstract> <TOKEN\_C> <TOKEN\_M> <TOKEN\_R> <TOKEN\_AD> <TOKEN\_Q> <TOKEN\_BA> <TOKEN\_C><TOKEN\_AF> <TOKEN\_M> <TOKEN\_R> <TOKEN\_C> <TOKEN\_S> <TOKEN\_Q> <TOKEN\_AD> <TOKEN\_C><TOKEN\_BH> <TOKEN\_M> <TOKEN\_BA> <TOKEN\_C> <TOKEN\_R> <TOKEN\_AD> <TOKEN\_AV> <TOKEN\_Q><TOKEN\_C> <TOKEN\_M> <TOKEN\_BD> <TOKEN\_R> <TOKEN\_C> <TOKEN\_BA> <TOKEN\_BG> <TOKEN\_AD><TOKEN\_C> <TOKEN\_M> <TOKEN\_Q> <TOKEN\_R> <TOKEN\_S> <TOKEN\_C> <TOKEN\_AD> <TOKEN\_K><TOKEN\_BA> <TOKEN\_C> <TOKEN\_M> <TOKEN\_R> <TOKEN\_BE> <TOKEN\_C> <TOKEN\_Q> <TOKEN\_AD><TOKEN\_BF> <TOKEN\_M> <TOKEN\_C> <TOKEN\_R> <TOKEN\_AO> <TOKEN\_BA> <TOKEN\_AD> <TOKEN\_C><TOKEN\_M> <TOKEN\_Q> <TOKEN\_S> <TOKEN\_R> <TOKEN\_C> <TOKEN\_BJ> <TOKEN\_AD> <TOKEN\_M><TOKEN\_C> <TOKEN\_BA> <TOKEN\_R> <TOKEN\_BI> <TOKEN\_Q> <TOKEN\_C> <TOKEN\_M> <TOKEN\_AD><TOKEN\_R> <TOKEN\_C> <endabstract>

Abstract CoT Response

Applying Heron’s formula with semi-perimeter s = 21, the area of triangle ABC is 84 . The altitude from vertex A to side BC (length 14) is then $\begin{array} { r } { h = \frac { 2 \times 8 4 } { 1 4 } = \boxed { 1 2 } . } \end{array}$

Prompt

Triangle ABC has sides of length $a = 1 3 , b = 1 4 ,$ and $c = 1 5 .$ Find the area of the triangle and the length of the altitude from vertex A to side b.

Verbal CoT

Triangle Area Calculation. To determine the area of triangle $A B C$ with sides $a = 1 3 , b = 1 4 ,$ and $c = 1 5 ,$ we use Heron’s Formula. Before applying the formula, we must calculate the semi-perimeter s of the triangle, defined as:

$$
s = \frac {a + b + c}{2}.
$$

Substituting the given values:

$$
s = \frac {1 3 + 1 4 + 1 5}{2} = \frac {4 2}{2} = 2 1.
$$

Then, using Heron’s Formula, the area A of the triangle is:

$$
A = \sqrt {s (s - a) (s - b) (s - c)}.
$$

Substitute the known values:

$$
A = \sqrt {2 1 (2 1 - 1 3) (2 1 - 1 4) (2 1 - 1 5)} = \sqrt {2 1 \times 8 \times 7 \times 6}.
$$

Performing the multiplication step-by-step:

$$
2 1 \times 8 = 1 6 8, \quad 7 \times 6 = 4 2, \quad 1 6 8 \times 4 2 = 7 0 5 6.
$$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Thus:
$A = \sqrt{7056} = 84.$

Altitude from Vertex A to Side b. Next, we are asked to determine the length of the altitude from vertex A to side b.

Assuming the triangle is labeled in the standard way, where:
• Side a = BC (opposite vertex A),
• Side b = AC (opposite vertex B),
• Side c = AB (opposite vertex C),

then side b = AC, and the altitude from vertex A to side b (AC) would not make sense, since vertex A lies on side AC itself, making the altitude zero—this is a contradiction.

Therefore, we consider an alternative labeling that matches the question's intent: if side b = BC, then the altitude from vertex A to side b (which is BC) is a meaningful and non-zero quantity.

To compute this, recall the formula for the area of a triangle as:

Area = $\frac{1}{2} \times \text{base} \times \text{height}$.

Given: Area = 84, Base = side b = 14. We solve for the height (altitude) h:

$84 = \frac{1}{2} \times 14 \times h \implies 84 = 7h \implies h = \frac{84}{7} = 12.$

Verbal CoT Response

The area of triangle ABC is [84].

The altitude from vertex A to side b, interpreted as BC, is [12].
</div>

#### C.1.3 Example 3: Sequences & Series

Prompt

$$
\sum_ {n = 1} ^ {\infty} \frac {n ^ {2}}{2 ^ {n}}.
$$

<table><tr><td>&lt;beginabstract&gt;</td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr><tr><td></td></tr></table>

Abstract CoT Response

Using the generating function identity $\sum _ { n = 0 } ^ { \infty } n ^ { 2 } r ^ { n } = { \frac { r ( 1 + r ) } { ( 1 - r ) ^ { 3 } } }$ evaluated at $\begin{array} { r } { r = { \frac { 1 } { 2 } } } \end{array}$ , we obtain:

$$
\sum_ {n = 1} ^ {\infty} \frac {n ^ {2}}{2 ^ {n}} = \frac {\frac {1}{2} \cdot \frac {3}{2}}{\left(\frac {1}{2}\right) ^ {3}} = \boxed {6}.
$$

Prompt

Evaluate $\sum _ { n = 1 } ^ { \infty } { \frac { n ^ { 2 } } { 2 ^ { n } } } .$

Verbal CoT

To evaluate the infinite series $\sum _ { n = 1 } ^ { \infty } { \frac { n ^ { 2 } } { 2 ^ { n } } } ,$ we recognize that this is a weighted sum where both the numerator and denominator are functions of $n ,$ with the exponential decay $2 ^ { n }$ in the denominator. This type of series is well-suited for analysis using generating functions and differentiation techniques.

Step 1: Start with the Basic Generating Function. We recall the standard geometric series:

$$
S = \sum_ {n = 0} ^ {\infty} r ^ {n} = \frac {1}{1 - r}, \quad \text { for } | r | <   1.
$$

Differentiating both sides with respect to $r ,$ we get:

$$
{\frac {d}{d r}} S = \sum_ {n = 0} ^ {\infty} n r ^ {n - 1} = {\frac {1}{(1 - r) ^ {2}}}.
$$

Multiplying both sides by $r ,$ we obtain:

$$
\sum_ {n = 0} ^ {\infty} n r ^ {n} = \frac {r}{(1 - r) ^ {2}}.
$$

Now we take the derivative of this expression again with respect to $r ,$ to obtain the generating function for $n ^ { 2 } r ^ { n }$

$$
\frac {d}{d r} \left(\sum_ {n = 0} ^ {\infty} n r ^ {n}\right) = \sum_ {n = 0} ^ {\infty} n ^ {2} r ^ {n - 1} = \frac {d}{d r} \left(\frac {r}{(1 - r) ^ {2}}\right).
$$

We now compute the right-hand side:

$$
\frac {d}{d r} \left(\frac {r}{(1 - r) ^ {2}}\right) = \frac {(1 - r) ^ {2} \cdot 1 + r \cdot 2 (1 - r)}{(1 - r) ^ {4}} = \frac {(1 - r) ^ {2} + 2 r (1 - r)}{(1 - r) ^ {4}}.
$$

Simplify the numerator:

$$
(1 - r) ^ {2} + 2 r (1 - r) = 1 - 2 r + r ^ {2} + 2 r - 2 r ^ {2} = 1 - r ^ {2}.
$$

So, the derivative becomes:

$$
\sum_ {n = 0} ^ {\infty} n ^ {2} r ^ {n - 1} = \frac {1 - r ^ {2}}{(1 - r) ^ {4}} = \frac {1 + r}{(1 - r) ^ {3}}.
$$

Multiplying through by r to adjust the exponent:

$$
\sum_ {n = 0} ^ {\infty} n ^ {2} r ^ {n} = \frac {r (1 + r)}{(1 - r) ^ {3}}.
$$

Thus, we obtain the well-known closed-form generating function $\sum _ { n = 0 } ^ { \infty } n ^ { 2 } r ^ { n } = { \frac { r ( 1 + r ) } { ( 1 - r ) ^ { 3 } } } .$

Step 2: Evaluate the Series for $\begin{array} { r } { r = { \frac { 1 } { 2 } } } \end{array}$ . Now plug in $\begin{array} { r } { r = { \frac { 1 } { 2 } } } \end{array}$ into our closed-form expression:

$$
\sum_ {n = 0} ^ {\infty} n ^ {2} \left(\frac {1}{2}\right) ^ {n} = \frac {\frac {1}{2} \left(1 + \frac {1}{2}\right)}{\left(1 - \frac {1}{2}\right) ^ {3}} = \frac {\frac {1}{2} \cdot \frac {3}{2}}{\left(\frac {1}{2}\right) ^ {3}} = \frac {\frac {3}{4}}{\frac {1}{8}} = 6.
$$

Note that the original series starts at $n = 1 ,$ , and the term for $n = 0$ is zero $( 0 ^ { 2 } / 2 ^ { 0 } = 0 ) .$ , so:

$$
\sum_ {n = 1} ^ {\infty} \frac {n ^ {2}}{2 ^ {n}} = \sum_ {n = 0} ^ {\infty} \frac {n ^ {2}}{2 ^ {n}} = 6.
$$

Step 3: Alternative Verification Using Summation by Parts. We can alternatively express $n ^ { 2 }$ as $n ( \bar { n ( \cdot - 1 ) } + n \colon$

$$
\sum_ {n = 1} ^ {\infty} \frac {n ^ {2}}{2 ^ {n}} = \sum_ {n = 1} ^ {\infty} \frac {n (n - 1)}{2 ^ {n}} + \sum_ {n = 1} ^ {\infty} \frac {n}{2 ^ {n}}.
$$

We already know from earlier that $\sum _ { n = 1 } ^ { \infty } { \frac { n } { 2 ^ { n } } } = 2 { \mathrm { ~ a n d ~ } } \sum _ { n = 1 } ^ { \infty } { \frac { n ( n - 1 ) } { 2 ^ { n } } } = 4 .$ Adding both parts:

$$
2 + 4 = 6.
$$

Thus, we again arrive at the same result.

Step 4: Numerical Partial Sums Approximation. To support our analytical result, we can also compute partial sums of the series:

$$
\sum_ {n = 1} ^ {2 0} \frac {n ^ {2}}{2 ^ {n}} \approx 5. 9 9 9 6.
$$

Since the terms decay exponentially, the convergence is rapid, and the partial sum approaches 6 closely, reinforcing the analytical result.

Verbal CoT Response

Through multiple rigorous and independent approaches—including generating functions, summation techniques, and numerical approximations—we consistently find that the value of the infinite series

is:

$$
\sum_ {n = 1} ^ {\infty} \frac {n ^ {2}}{2 ^ {n}}
$$

![](images/da9f781594dd353de4d600af70c3e2f56cc4cc42298ce7877fe1dc9e56db6e5b.jpg)

[Image: The image displays the number 6 centered within a thin black square border on a light-colored background. The character is written in a black serif typeface. Considering the preceding mathematical summation and the following heading "Example 4: Probability," this element appears to be a numbered label or step indicator within a textbook or academic paper.]

#### C.1.4 Example 4: Probability

Prompt

A fair eight-sided die is rolled repeatedly until every face has appeared at least once. What is the expected total number of rolls?

Abstract CoT

<beginabstract> <TOKEN\_C> <TOKEN\_M> <TOKEN\_Q> <TOKEN\_R> <TOKEN\_BA> <TOKEN\_AD> <TOKEN\_S> <TOKEN\_C> <TOKEN\_AU> <TOKEN\_M> <TOKEN\_R> <TOKEN\_Q> <TOKEN\_C> <TOKEN\_AD> <TOKEN\_BA> <TOKEN\_C> <TOKEN\_BJ> <TOKEN\_M> <TOKEN\_R> <TOKEN\_C> <TOKEN\_Q> <TOKEN\_S> <TOKEN\_AD> <TOKEN\_C> <TOKEN\_M> <TOKEN\_BA> <TOKEN\_AX> <TOKEN\_R> <TOKEN\_C> <TOKEN\_Q> <TOKEN\_AD> <TOKEN\_C> <TOKEN\_BD> <TOKEN\_M> <TOKEN\_R> <TOKEN\_BA> <TOKEN\_C> <TOKEN\_Q> <TOKEN\_AD> <TOKEN\_S> <TOKEN\_C> <TOKEN\_BF> <TOKEN\_M> <TOKEN\_R> <TOKEN\_C> <TOKEN\_Q> <TOKEN\_BA> <TOKEN\_AD> <TOKEN\_M> <TOKEN\_C> <TOKEN\_R> <TOKEN\_BH> <TOKEN\_Q> <TOKEN\_C> <TOKEN\_AD> <TOKEN\_BA> <TOKEN\_M> <TOKEN\_R> <TOKEN\_S> <TOKEN\_C> <TOKEN\_Q> <TOKEN\_AD> <TOKEN\_BL> <TOKEN\_C> <TOKEN\_M> <TOKEN\_R> <TOKEN\_Q> <TOKEN\_C> <TOKEN\_BA> <TOKEN\_AD> <TOKEN\_AJ> <TOKEN\_M> <TOKEN\_R> <TOKEN\_C> <TOKEN\_S> <TOKEN\_Q> <TOKEN\_AD> <TOKEN\_C> <TOKEN\_BE> <TOKEN\_BA> <TOKEN\_M> <TOKEN\_R> <TOKEN\_Q> <TOKEN\_C> <TOKEN\_AD> <TOKEN\_M> <TOKEN\_BA> <TOKEN\_C> <TOKEN\_R> <TOKEN\_BG> <TOKEN\_Q> <endabstract>

Abstract CoT Response

By the coupon collector formula $E ( n ) = n \cdot H _ { n }$ with $n = 8$ and $\begin{array} { r } { H _ { 8 } = \frac { 7 6 1 } { 2 8 0 } } \end{array}$ , the expected number of rolls to see all eight faces is:

$$
\boxed {\frac {7 6 1}{3 5}} \approx 2 1. 7 4.
$$

Prompt

A fair eight-sided die is rolled repeatedly until every face has appeared at least once. What is the expected total number of rolls?

Verbal CoT

To determine the expected total number of rolls required to roll a fair eight-sided die until all eight faces have appeared at least once, we approach this problem using the coupon collector problem, a well-known stochastic model in probability theory.

Problem Understanding. We are rolling a fair eight-sided die repeatedly, and we want to know the expected number of rolls required to observe all eight sides. Each roll independently produces one of the eight faces, each with equal probability $( \mathrm { i . e . , } \frac { 1 } { 8 } )$ . We want to find the expected value of the number of rolls until all outcomes have been observed. This is a direct application of the coupon collector problem with $n = 8 .$

Modeling the Process. Let us define the expected number of rolls needed to observe all n distinct outcomes as $E ( n )$ . In general, the formula for this expectation is:

$$
E (n) = n \cdot H _ {n}
$$

where $H _ { n } = 1 + { \frac { 1 } { 2 } } + { \frac { 1 } { 3 } } + \cdot \cdot \cdot + { \frac { 1 } { n } }$ is the nth harmonic number. For $n = 8 ,$ , this becomes:

$$
E (8) = 8 \left(1 + \frac {1}{2} + \frac {1}{3} + \frac {1}{4} + \frac {1}{5} + \frac {1}{6} + \frac {1}{7} + \frac {1}{8}\right).
$$

Computing the Harmonic Number. We compute $H _ { 8 }$ by summing the reciprocals:

$$
H _ {8} = 1 + \frac {1}{2} + \frac {1}{3} + \frac {1}{4} + \frac {1}{5} + \frac {1}{6} + \frac {1}{7} + \frac {1}{8}.
$$

To compute this exactly, we find a common denominator. The least common multiple of the denominators from 1 to 8 is 840. Converting each term:

$$
\begin{array}{r l r l} {1} & {= \frac {8 4 0}{8 4 0},} & {\frac {1}{2}} & {= \frac {4 2 0}{8 4 0},} \\ {1} & {2 8 0} & {1} & {2 1 0} \end{array}
$$

$$
\begin{array}{c c c c} \overline {{3}} & = \overline {{8 4 0}}, & \overline {{4}} & = \overline {{8 4 0}}, \\ 1 & 1 6 8 & 1 & 1 4 0 \end{array}
$$

$$
\begin{array}{c c c c} \overline {{5}} & = \overline {{8 4 0}}, & \overline {{6}} & = \overline {{8 4 0}}, \\ 1 & 1 2 0 & 1 & 1 0 5 \end{array}
$$

$$
\overline {{7}} = \overline {{8 4 0}}, \quad \overline {{8}} = \overline {{8 4 0}}.
$$

Adding the numerators:

$$
8 4 0 + 4 2 0 + 2 8 0 + 2 1 0 + 1 6 8 + 1 4 0 + 1 2 0 + 1 0 5 = 2 2 8 3.
$$

Thus:

$$
H _ {8} = \frac {2 2 8 3}{8 4 0}.
$$

Simplifying by dividing numerator and denominator by 3:

$$
H _ {8} = \frac {7 6 1}{2 8 0}.
$$

Final Computation. Now multiply by $n = 8$ to get the expected number of rolls:

$$
E (8) = 8 \cdot \frac {7 6 1}{2 8 0} = \frac {6 0 8 8}{2 8 0}.
$$

Simplify the fraction by dividing numerator and denominator by 8:

$$
\frac {6 0 8 8}{2 8 0} = \frac {7 6 1}{3 5}.
$$

Sanity check. 761/35 ≈ 21.743, which is reasonable for 8 coupons (the answer for 6 coupons is 14.7, and the harmonic series grows logarithmically, so we expect a moderate increase). ✓

Verbal CoT Response

Through the application of the coupon collector model, harmonic numbers, and careful arithmetic, we have derived that the expected number of rolls required to see all eight faces of a fair eight-sided die is:

$$
\boxed {\frac {7 6 1}{3 5}} \approx 2 1. 7 4.
$$

### C.2 General Instruction-Following

#### C.2.1 Example 1: Lifestyle Advice

Prompt

I’m starting high school and I procrastinate a lot. Can you give me a simple plan to stop procrastinating that I can actually follow, even on busy weeks?

Abstract CoT

<beginabstract> <TOKEN\_T> <TOKEN\_F> <TOKEN\_C> <TOKEN\_L> <TOKEN\_AD> <TOKEN\_T> <TOKEN\_C> <TOKEN\_AE> <TOKEN\_F> <TOKEN\_L> <TOKEN\_R> <TOKEN\_T> <TOKEN\_C> <TOKEN\_F> <TOKEN\_BA> <TOKEN\_L> <TOKEN\_T> <TOKEN\_AD> <TOKEN\_F> <TOKEN\_C> <TOKEN\_L> <TOKEN\_T> <TOKEN\_AN> <TOKEN\_F> <TOKEN\_C> <TOKEN\_L> <TOKEN\_BB> <TOKEN\_T> <TOKEN\_AD> <TOKEN\_F> <TOKEN\_C> <TOKEN\_M> <TOKEN\_L> <TOKEN\_T> <TOKEN\_BC> <TOKEN\_F> <TOKEN\_S> <TOKEN\_C> <TOKEN\_L> <TOKEN\_BA> <TOKEN\_T> <TOKEN\_F> <TOKEN\_BD> <TOKEN\_C> <TOKEN\_AE> <TOKEN\_L> <TOKEN\_T> <TOKEN\_F> <TOKEN\_AD> <TOKEN\_BF> <TOKEN\_C> <TOKEN\_L> <TOKEN\_T> <TOKEN\_F> <TOKEN\_L> <TOKEN\_BG> <TOKEN\_C> <TOKEN\_T> <TOKEN\_AD> <TOKEN\_F> <TOKEN\_C> <TOKEN\_BH> <TOKEN\_I> <TOKEN\_L> <TOKEN\_T> <TOKEN\_F> <TOKEN\_BA> <TOKEN\_AE> <TOKEN\_C> <TOKEN\_T> <TOKEN\_W> <TOKEN\_L> <TOKEN\_F> <TOKEN\_C> <TOKEN\_AD> <TOKEN\_T> <TOKEN\_F> <TOKEN\_L> <endabstract>

Abstract CoT Response

Here’s a realistic, low-effort system that works even on your craziest weeks.

The core idea: don’t try to “fix” procrastination—just make starting easier than avoiding. Every morning, write down one thing that matters most today. That’s your anchor task. Before anything else, spend 15 minutes on it. Not an hour, not “until it’s done”—just 15 minutes. Most days, you’ll keep going once you’ve started. On bad days, you still moved the needle.

For everything else: if it takes under two minutes, do it now. If it feels too big, shrink it (“study for the test” becomes “re-read one page of notes”). Set a 30–60 minute block each day where your phone is out of reach—this is your focus window. On busy weeks, cut it to 15 minutes. That still counts.

The secret nobody tells you: you’ll still procrastinate sometimes. That’s fine. Don’t beat yourself up about it—guilt just makes the cycle worse. Just reset and pick it up tomorrow. Consistency over time beats perfection on any single day.

<table><tr><td>Prompt</td></tr><tr><td>I&#x27;m starting high school and I procrastinate a lot. Can you give me a simple plan to stop procrastinating that I can actually follow, even on busy weeks?</td></tr><tr><td>Verbal CoTStarting high school is a big transition, and it&#x27;s completely normal to feel overwhelmed, especially when you&#x27;re trying to manage new responsibilities, social dynamics, and academic expectations. Procrastination often stems from a mix of factors: fear of failure, perfectionism, feeling overwhelmed by tasks, or simply not knowing where to start. The key to overcoming procrastination isn&#x27;t about eliminating it entirely (which is impossible) but about managing it through intentional habits and mindset shifts. The goal is to create a plan that&#x27;s flexible, simple, and adaptable to even the busiest weeks. Let&#x27;s break this down step by step.First, you need to understand why you procrastinate. Are you avoiding tasks because they feel too hard? Do you fear that your work won&#x27;t be perfect? Are you overwhelmed by the sheer volume of things to do? Once you identify the root causes, you can tailor your strategy. But even if you&#x27;re unsure, starting with small, actionable steps will help you build momentum. The plan needs to be simple, relatable, and non-judgmental—because if it feels like a burden, you&#x27;ll be less likely to stick with it.The most effective anti-procrastination strategies often involve breaking tasks into smaller parts, creating structure, and using time management techniques like the Pomodoro Technique or time blocking. However, these methods can feel overwhelming if you&#x27;re not used to them. The solution is to start gradually and pair each habit with a specific, low-stakes goal. For example, instead of trying to &quot;organize your entire schedule,&quot; begin with one small task, like setting a daily 15-minute goal to plan your homework.Another critical factor is self-compassion. Procrastination is often linked to perfectionism or self-criticism. If you&#x27;re too hard on yourself for not completing tasks, you&#x27;re more likely to procrastinate again. The plan must include a way to reframe setbacks as learning opportunities rather than failures.Finally, the plan needs to account for real-life interruptions and busy weeks. High school can be unpredictable, so your strategy should allow for flexibility. For instance, if a task takes longer than expected, you shouldn&#x27;t feel guilty—adjust your schedule and move forward.</td></tr><tr><td>Verbal CoT ResponseStarting high school can be exciting, but procrastination can feel overwhelming. Here&#x27;s a simple, flexible plan to help you manage your time and stay on track:Start Small — The 2-Minute Rule: If a task takes less than 2 minutes, do it immediately (e.g., answer an email, organize your desk). This prevents small tasks from piling up.Prioritize with &quot;Most Important Task First&quot; (MIT): Every day, identify one task that is the most important (e.g., finishing a big project, studying for a test). Do this task first, even if it is short.Break Tasks into Smaller Steps: If a task feels too big, split it into tiny steps (e.g., &quot;Write a 2-page essay&quot; → &quot;Outline 1 paragraph today&quot;). Check off each step as you go.Use the 15-Minute Rule: If you are stuck, promise yourself: &quot;I&#x27;ll work on this for 15 minutes. If I still don&#x27;t want to, I&#x27;ll stop.&quot; This tricks your brain into starting — and often you will keep going!Schedule Daily &quot;Focus Time&quot;: Block 30–60 minutes each day for focused work (e.g., homework, studying). If you are busy, shorten the time or do it in chunks.You&#x27;ve got this! Start with one or two strategies, and adjust as you go. Over time, you will build habits that make high school manageable and even enjoyable!</td></tr></table>
