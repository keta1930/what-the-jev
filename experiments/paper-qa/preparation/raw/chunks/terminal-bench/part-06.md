## E.1 COMMAND FAILURES ACROSS MODELS

For Figures (OpenAI) 15, 16, 17, 18, 19, 20, 21, (Anthropic) 22, 23, 24, 25, (Gemini) 26, 27, (Grok) 28, 29, (Z AI) 30, (MiniMax) 31, (Moonshot AI) 32, (Alibaba) 33 categories (inner ring) that represent less than 5% of all failures have been grouped under the “Other” category. Subcategories (outer ring) representing less than 3% of failures have been similarly grouped. Labels are shortened versions of those shown in the taxonomy in Appendix E.2.

![](images/6b55b25094a95ab2be7fc25b4ed84c816db1b3d44bd58b07dbbfc734ebff0cbc.jpg)

[Image: This concentric donut chart illustrates the distribution of Terminus 2 command failures attributed to the GPT-5 model, categorizing errors into broad classes on the inner ring and specific subtypes on the outer ring. The largest category is "Invocation" at 45.9%, where the primary cause is "Command not found" (29.4%). Other significant categories include "Filesystem" (16.9%), driven largely by "File not found" (13.8%), along with "Runtime" (14.6%), "REPL" (13.1%), and a combined "Other" category (9.6%).]  
Figure 15: Terminus 2 command failures with GPT-5.2.

![](images/c478be1327f2336c0c8c2a14353125c97a7aadeeaafba1f7f69f75783d6375c9.jpg)

[Image: This nested donut chart displays the breakdown of command failures for Terminus 2 using the GPT-5.2 model. The data is organized into hierarchical categories, with the 'Invocation' group representing the largest share of failures at 39.1%, largely driven by the 'Command not found' error which accounts for 28.6% of the total. Significant portions of the failures are attributed to the 'Filesystem' category (22.3%), specifically 'File not found' (18.5%), while 'Other' failures make up 14.0% of the total distribution.]  
Figure 16: Terminus 2 command failures with GPT-5.

![](images/bcff09218b79d8f7cf101aa68a2ea191efd3c749810d6c8e023d16b9728c276d.jpg)

[Image: The image presents a nested donut chart detailing Terminus 2 command failures with GPT-5, organized into broad categories on the inner ring and specific error types on the outer ring. The largest category is Invocation at 38.5%, dominated by the "Command not found" error (18.6%), followed by Filesystem issues at 28.4%, primarily driven by "File not found" (22.6%). Smaller categories include REPL (12.1%), Runtime (10.9%), Toolchain (5.6%), and Other (4.6%), with specific failures such as "App failure" (6.3%), "Executable not found" (10.4%), and "Shell syntax error" (5.5%) contributing to the total distribution.]  
Figure 17: Terminus 2 command failures with GPT-5 Mini.

![](images/e04870ef46a0a4adb7a7dea4e8908b8e78925bfaa61b56750fae7e7d08fb5aa9.jpg)

[Image: This nested donut chart details the causes of Terminus 2 command failures using the GPT-5 Mini model, categorizing errors into major groups on the inner ring and specific instances on the outer ring. The most frequent failure category is "Invocation" at 29.9%, dominated by "Shell syntax error" (13.6%) and "Command not found" (12.4%), followed by "Filesystem" errors at 21.3%, primarily due to "File not found" issues (17.2%). Other significant categories include "REPL" (15.4%), "Runtime" (9.0%), and "Data" (7.9%), while smaller segments cover "Toolchain" (5.8%) and general "Other" failures (10.6%).]  
Figure 18: Terminus 2 command failures with GPT-5 Nano.

![](images/c1eea9e84abfc53602c314192e9c7da370153dfa5ca9f5857e235a4c9d6b486c.jpg)

[Image: This nested donut chart details the distribution of Terminus 2 command failures when processed by the GPT-5 Nano model. The inner ring displays major failure categories, led by "Invocation" at 39.4%, followed by "Filesystem" at 19.3% and "REPL" at 17.7%. The outer ring breaks these down further into specific error types, showing that "Command not found" comprises the largest individual portion at 37.3%, while other significant sub-categories include "Module not found" (15.6%) and "File not found" (14.1%).]  
Figure 19: Terminus 2 command failures with GPT-5-Codex.

![](images/02188c1cc9030f999f663d0c9b3e749377460efa3a87edcd5ef3daad321b3536.jpg)

[Image: This donut chart visualizes the breakdown of command failures for the Terminus 2 dataset using GPT-5-Codex. The inner ring divides total failures into six main categories, with "Filesystem" accounting for the largest portion at 33.9%, followed closely by "Invocation" at 30.7%. The outer ring details specific error types within these categories; for instance, the Filesystem category is primarily driven by "File not found" errors (26.1%), while the Invocation category is dominated by "Command not found" errors (19.8%). Smaller segments identify other specific issues such as "Module not found" (4.4%), "App failure" (4.3%), and various "Other" groupings that sum to approximately 13.8% of all failures.]  
Figure 20: Terminus 2 command failures with GPT-OSS-120B.

![](images/f1f8887789979192daf4f8e16406a13f6fd0fc8f3208d2f8053dc433ad8134c5.jpg)

[Image: This nested donut chart displays the breakdown of command execution failures for the GPT-OSS-120B model on the Terminus 2 benchmark. The inner ring aggregates errors into five main categories—Invocation (37.2%), Filesystem (28.4%), REPL (17.4%), Runtime (7.7%), and Other (9.3%)—while the outer ring specifies the exact error messages responsible for each percentage. The most frequent failure is "Command not found" under Invocation (28.3%), followed by "File not found" under Filesystem (17.5%). Other notable error types include "Module not found" (8.9%), "Undefined symbols" (6.3%), and "App failure" (5.2%).]  
Figure 21: Terminus 2 command failures with GPT-OSS-20B.

![](images/dc27e9e3f1ef40e251c57d9f9a3fdc4fc5d8c560d0c4d0c3f1d34076133e4a14.jpg)

[Image: Figure 21 presents a nested donut chart detailing the percentage distribution of command failures for the GPT-OSS-20B model, categorized into broad groups on the inner ring and specific error types on the outer ring. The largest category is "Invocation" failures at 34.0%, which is predominantly driven by "Command not found" errors that account for 26.7% of the total. Other significant failure clusters include "Runtime" errors at 22.9%, "REPL" issues at 17.2%, and a miscellaneous "Other" category comprising 12.7% of incidents. The remaining smaller segments identify specific technical faults such as "Segmentation fault" (7.4%), "Module not found" (7.4%), "HTTP 404" (3.3%), and minimal occurrences of "Assert error" (0.8%).]  
Figure 22: Terminus 2 command failures with Claude Opus 4.5.

![](images/6607a29fba02f9a0b584565e50e42c3a6674fd2fd97bac63536d7cd72704cf71.jpg)

[Image: This donut chart displays the percentage breakdown of command failures for the Terminus 2 model using Claude Opus 4.5, organized into six hierarchical categories defined by color. The largest category is "Invocation" at 38.0%, dominated by the specific error "Command not found" (24.4%), followed by "Runtime" at 22.8% driven mainly by "App failure" (16.2%). The remaining failures are distributed among "REPL" (15.8%), "Other" (10.0%), "Filesystem" (7.4%), and "Testing" (6.0%), with specific sub-errors like "Module not found" and "Assert error" clearly labeled with arrows pointing to their respective segments.]  
Figure 23: Terminus 2 command failures with Claude Opus 4.1.

![](images/8c9d116cddc3902326b6d1eac651608fee9b4d5431cc738c304608f59f4a2d06.jpg)

[Image: This donut chart displays the distribution of Terminus 2 command failures generated by the Claude Opus 4.1 model, categorized into broad groups in the inner ring and specific error types in the outer ring. The largest category is "Invocation," accounting for 37.1% of total failures, with "Command not found" being the most frequent specific error at 25.1%. "Runtime" errors comprise the second largest segment at 22.9%, dominated by "App failure" at 13.3%, while "REPL" and "Other failures" account for 13.2% and 13.8% respectively. Smaller segments include "Filesystem" errors (7.2%), "Testing" failures such as "Assert error" (5.9%), and minor categories like "Shell syntax error" (4.8%) and "Module not found" (12.1%).]  
Figure 24: Terminus 2 command failures with Claude Sonnet 4.5.

![](images/3e9c2f0c9317601dce56549940227e85fa6ebb0e1832e15c739b20e3d6ba910e.jpg)

[Image: This nested donut chart illustrates the percentage breakdown of command failures for Terminus 2 using the Claude Sonnet 4.5 model, organized into hierarchical categories. The inner ring groups errors into primary domains, with Runtime accounting for the largest portion at 27.4%, followed closely by Invocation at 24.5% and REPL at 16.8%. The outer ring details specific failure types within those domains, identifying "Command not found" (19.3%) and "App failure" (16.5%) as the most common individual issues, while "File not found" comprises 9.1% of the total. Minor categories include "Script syntax errors" (4.3%), "Segmentation fault" (5.8%), and several "Other" sub-groups ranging from 1.5% to 6.2%.]  
Figure 25: Terminus 2 command failures with Claude Haiku 4.5.

![](images/e5c2d5b0557f3087f342fe2b798f1f525c252e66a3f9f52097ae62e9fc4c84c5.jpg)

[Image: This donut chart illustrates the distribution of Terminus 2 command failures for the Claude Haiku 4.5 model, organized into specific error types on the outer ring and broader categories on the inner ring. The most prevalent issues occur in the "Invocation" category (20.7%), driven largely by "Command not found" errors (18.8%), followed closely by the "Runtime" category (20.2%) which includes "App failure" (9.7%) and "Segmentation fault" (6.0%). Other significant failure modes include "REPL" errors (16.9%), such as "Module not found" (5.8%) and "Script syntax errors" (5.0%), alongside "Filesystem" (9.8%) and "Network" failures (7.4%). Smaller proportions of errors fall into "Data" (5.5%), "Toolchain" (6.3%), and an "Other" category comprising 7.1% of total failures.]  
Figure 26: Terminus 2 command failures with Gemini 2.5 Pro.

![](images/37083c82cef9ce5af0b881961b8811aa1db044a0d56c47368b493882930a25a3.jpg)

[Image: This nested donut chart illustrates the breakdown of command failures for Terminus 2 using the Gemini 2.5 Pro model, categorized by error type. The inner ring divides failures into six primary categories, with Invocation accounting for the largest share at 25.8%, followed by Filesystem (17.9%), Runtime (17.3%), REPL (16.6%), Other (14.6%), and Network (7.9%). The outer ring provides granular details for each category, identifying "Command not found" as the most frequent individual error at 14.9%, followed by "File not found" (11.4%) and "App failure" (9.7%). Smaller segments capture specific issues like "Shell syntax error" (4.7%), "OOM" (4.0%), and "Connection failure" (3.6%).]  
Figure 27: Terminus 2 command failures with Gemini 2.5 Flash.

![](images/e083e39ff32b5b6daad4919b3262ad2aeca77778f6ddcc8beac5a03baf5d383c.jpg)

[Image: This figure presents a nested donut chart detailing the distribution of Terminus 2 command failures when using the Gemini 2.5 Flash model. The inner ring segments represent broad error categories such as Invocation (31.7%), REPL (19.7%), Filesystem (16.5%), and Runtime (9.6%), while the outer ring breaks these down into specific failure types with corresponding percentages. The largest single segment is "Command not found" at 23.9%, located within the dark blue Invocation section. Other notable specific failures include "File not found" (10.9%) in the pink Filesystem section, "Undefined symbols" (7.0%) in the purple REPL section, and "Script syntax errors" (6.1%). Smaller segments account for less frequent issues like Assert errors, App failures, and module or directory not found errors, distributed across the remaining categories of Toolchain, Testing, and Data.]  
Figure 28: Terminus 2 command failures with Grok 4.

![](images/eb27c14f7042700b60768afe8899d1ba90648a204d030680c84897a3f274c83d.jpg)

[Image: This multi-level donut chart illustrates the distribution of Terminus 2 command failures with Grok 4, grouping specific error types into broader categories visible in the inner ring. The dominant failure category is "Invocation" at 31.7%, primarily caused by "Command not found" errors (23.9%), followed by "REPL" issues (19.7%) and "Filesystem" problems (16.5%). Lesser categories include "Runtime" (9.6%), "Toolchain" (6.8%), "Testing" (6.0%), and "Data" (5.1%), while miscellaneous "Other" failures account for 4.6% of the total.]  
Figure 29: Terminus 2 command failures with Grok Code Fast 1.

![](images/5c391deb42d3a896fb3c97741a40ff3c0406357ddf6c9ac15d57955012fe85af.jpg)

[Image: This nested donut chart details the distribution of Terminus 2 command failures categorized by type and cause. The inner ring divides failures into seven primary categories, led by "Invocation" at 31.2% and "Runtime" at 24.2%, followed by "Other" (12.5%), "REPL" (10.3%), "Data" (8.5%), "Filesystem" (6.5%), and "Testing" (6.8%). The outer ring breaks these down further into specific errors, with "Command not found" representing the largest individual slice at 25.5%, followed by "App failure" at 14.6% and "Other failures" at 12.5%.]  
Figure 30: Terminus 2 command failures with GLM 4.6.

![](images/14dd94ce89032b27a02d9f03696dfdd152ce6223cf101b58622ade5ae611cd53.jpg)

[Image: The image presents a multi-ring donut chart detailing the distribution of Terminus 2 command failures across various error categories. The inner ring categorizes failures into broader groups, with 'Invocation' accounting for the largest portion at 35.1%, followed by 'REPL' (15.3%) and 'Runtime' (15.2%). The outer ring breaks these down into specific error types, where 'Command not found' is the single largest contributor at 21.5%, and 'App failure' is the second largest specific category at 10.5%. Additional specific errors identified include shell syntax errors (8.5%), script syntax errors (6.5%), and undefined symbols (3.7%), while other segments represent miscellaneous or aggregated failures within their respective domains.]  
Figure 31: Terminus 2 command failures with MiniMax M2.

![](images/70f47e0d67fb1b59eb9dcb32f0a8b8bcfcf12d1c7c093ea020e9aa6cc8c3108c.jpg)

[Image: This donut chart visualizes the distribution of Terminus 2 command failures for the MiniMax M2 model, distinguishing between specific error types on the outer ring and aggregated categories on the inner ring. "Runtime" constitutes the largest failure group at 27.6%, driven by "App failure" (16.4%) and "Segmentation fault" (7.1%), followed closely by "Invocation" errors at 25.3%, largely caused by "Command not found" (19.6%). "REPL" issues make up 19.1% of failures, with components including "Module not found" (9.9%) and "Undefined symbols" (3.8%), while "Network" problems account for 8.2% and miscellaneous failures comprise the final 19.8%.]  
Figure 32: Terminus 2 command failures with Kimi K2 Instruct.

![](images/27905b154bb96284ea8f4b113ff809ae95d28b18ca56715f8e9df3e9b63e92f3.jpg)

[Image: This donut chart displays the distribution of command failures for "Terminus 2 with Kimi K2 Instruct," organizing errors into broader categories on the inner ring and specific causes on the outer ring. The "Invocation" category is the most frequent source of failure at 35.1%, primarily driven by "Command not found" errors which account for 21.5% of all instances. Other major categories include "REPL" (15.3%), "Runtime" (15.2%), and "Other" (11.5%), while smaller segments represent issues within the "Filesystem" (8.2%), "Toolchain" (7.9%), and "Data" (6.8%) domains.]  
Figure 33: Terminus 2 command failures with Qwen3 Coder 480B A35B Instruct (FP8).
