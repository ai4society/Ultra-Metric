# Ultra-Metric
Code and examples for how to use metrics for the output of any team / group / item recommendation system.
- [metrics_scorer.py](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_scorer.py) - code/implementation for each of the 4 metrics described below, given unweighted skillsets.
- [metrics_scorer_with_skill_weights.py](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_scorer_with_skill_weights.py) - code/implementation for each of the 4 metrics described below, given weighted skillsets.
- [metrics_notebook.ipynb](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_notebook.ipynb) - shows example for how to use the scorer files.

## Table of Contents
- [Metrics Used](#metrics-used)
- [Terminology](#terminology)
- [Example with Unweighted Skills](#example-with-unweighted-skills)
  - [Before Normalization](#before-normalization)
  - [After Normalization](#after-normalization)
  - [Computing the Overall Goodness Metric](#computing-the-overall-goodness-metric)
- [Example with Weighted Skills](#example-with-weighted-skills)
  - [Before Normalization](#before-normalization-1)
  - [After Normalization](#after-normalization-1)
  - [Computing the Overall Goodness Metric](#computing-the-overall-goodness-metric-1)

## Metrics Used 
- Redundancy: what is the percentage of skills shared amongst 2+ researchers? (How many researchers have common skills?)
- Set size: what is the team size? (Usually determined by total_funding_amount/$50K)
- Coverage: how many skills are covered by researchers and how many are still required by the RFP?
- k-Robustness: how many team members can we remove before the team starts to fall apart?

## Terminology 

- Demand: *What kind of skills may be required/desired by the RFP?*
	- $\{ s_1, s_2, ..., s_m \}$
- Supply: *What resources do we have available?*
	- Team of researchers $T_i = {a, b, c, d, ..., N}$
	- Researcher skills = $\{a: [s_1, s_2, ..., s_a], b: [s_1, s_2, ..., s_b], ..., N: [s_1, s_2, ..., s_n]\}$

## Example with Unweighted Skills 

- Demand: $\{s_1, s_2, s_3, s_4\}$
- Supply:
	- Consider the following teams in this format: *team_name = {set_of_researchers}*
		- $T_1 = \{a\}$
		- $T_2 = \{a, b, c\}$
		- $T_3 = \{a, b\}$
		- $T_4 = \{a, d, e\}$
	- Researcher skills: *researcher_name = {set_of_skills}*:
		- $a = \{s_1, s_2\}$
		- $b = \{s_3, s_4\}$
		- $c = \{s_2, s_3\}$
		- $d = \{s_1, s_2\}$
		- $e = \{s_2, s_3\}$

Problem: *Evaluate the goodness of each team using the above-mentioned metrics.*

### **Before Normalization:**
| Team (right) / Metric (below) | $T_1$                                                           | $T_2$                                       | $T_3$ | $T_4$                                                            |
| ----------------------------- | --------------------------------------------------------------- | ------------------------------------------- | ----- | ---------------------------------------------------------------- |
| $π_{redundancy}$              | $0$ *(team of one member, no redundant skills)*                 | $2$ *(since $s_2$ and $s_3$ are redundant)* | $0$   | $2$                                                              |
| $π_{setsize}$                 | $1$ *(number of people in the team)*                            | $3$                                         | $2$   | $3$                                                              |
| $π_{coverage}$                | $-2$ *(indicates that this team is short of two needed skills)* | $0$                                         | $0$   | $-1$                                                             |
| $π_{k-robustness}$            | $0$ (you can't remove anyone)                                   | $1$ (you can remove *c*)                    | $0$   | $1$ *(you can remove *a* or *d*, and coverage would not change)* |

### **After Normalization:**
We normalize our data to stay between $[0,1]$ so that the measure is consistent across different teams, team members, team skillsets, etc. Consider:
- $x_i$ : value of metric before normalization
- $min(x)$: what is the minimum value possible from this metric?
- $max(x)$: what is the maximum value possible from this metric? For each of the following:
	- `maxRedundancy = (total number of demand skills) * (number of researchers)`, where each researcher of the team has all the demand skills.
	- `maxSetsize = 5`, which is the max number of people there can be in a team. (Metric is configurable.)
	- `maxCoverage = 1`, which reflects the total percentage of demand skills that are satisfied.
	- `maxKrobust = 1`, if at least one member of the team can be removed.

Then, normalized score = $(x_i – min(x)) / (max(x) – min(x))$

| Team (right) / <br>Metric (below) | $T_1$                         | $T_2$       | $T_3$       | $T_4$       |
| --------------------------------- | ----------------------------- | ----------- | ----------- | ----------- |
| $π_{redundancyNorm}$              | $0/4=0$                       | $2/4=0.5$   | $0/4=0$     | $2/4=0.5$   |
| $π_{setsizeNorm}$                 | $1/5 = 0.2$                   | $3/5 = 0.6$ | $2/5 = 0.4$ | $3/5 = 0.6$ |
| $π_{coverageNorm}$                | $2/4 = 0.50$                  | $4/4=1$     | $4/4=1$     | $3/4=0.75$  |
| $π_{k-robustnessNorm}$            | $0$ (you can't remove anyone) | $1$         | $0$         | $1$         |

### **Computing the Overall Goodness Metric:**
**Each metric has a weight. By default, they're:**
- Redundancy: $-1$
- Set size: $-1$
- Coverage: $1$
- k-Robustness: $1$

By default, high *redundancy* and *set size* are not desired, hence the negative weight. But the weights are configurable and can be changed if needed, using `set_new_weights()` in [metrics_scorer.py](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_scorer.py).

Negative weights can often lead to (1) negative goodness scores, and/or (2) division-by-zero exceptions, so we computed weighted normalization to adjust those weights (the ratios still remain the same):
- Assume the set of weights to be:  $weights = [-1, -1, 1, 1]$.
- Take the range of the weights: $range=max(weights)-min(weights)$
- Add the range value to each the weights: $adjustedWeights=[-1+2, -1+2, 1+2, 1+2]=[1,1,3,3]$

Now, compute overall goodness using $adjustedWeights$ as the new set of metrics:

| Team (right) / Metric (below) | $T_1$                                                          | $T_2$    | $T_3$   | $T_4$     |
| ----------------------------- | -------------------------------------------------------------- | -------- | ------- | --------- |
| $π_{overallGoodness}$         | $(1\cdot0 + 1\cdot0.2 + 3\cdot0.5 + 3\cdot0)/(1+1+3+3)=0.2125$ | $0.8875$ | $0.425$ | $0.79375$ |

**What if you set different weights (e.g., give a high priority for coverage)?**
- Redundancy: 0.11
- Set size: 0.09
- Coverage: 0.8
- k-Robustness: 0.0

| Team (right) / Metric (below) | $T_1$                                                                | $T_2$   | $T_3$   | $T_4$   |
| ----------------------------- | -------------------------------------------------------------------- | ------- | ------- | ------- |
| $π_{overallGoodness}$         | $(0.11\cdot0.0 + 0.09\cdot0.2 + 0.8\cdot0.5 + 0.0\cdot0)/(1.0)=0.58$ | $0.909$ | $0.836$ | $0.709$ |
## Example with Weighted Skills
- Demand: $\{s_1, s_2, s_3, s_4\}$
- Supply:
	- Consider the following teams in this format: *team_name = {set_of_researchers}*
		- $T_1 = \{a, b, c\}$
		- $T_2 = \{b, d, e\}$
	- Researcher skills: *researcher_name = {set_of_skills}*:
		- $a = \{s_1:0.5, s_2:0.15\}$
		- $b = \{s_3:1, s_1:0.1\}$
		- $c = \{s_2:0.75, s_3:0.5\}$
		- $d = \{s_2:0.25\}$
		- $e = \{s_1:0.1, s_4:0.2, s_5:0.8\}$

Problem: *Evaluate the goodness of each team using the above-mentioned metrics.*
### Before Normalization: 
| Team (right) / Metric (below) | $T_1$                                                                                                         | $T_2$                                               |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| $π_{redundancy}$              | $0.1+0.15+0.5+0$ *( take the 2nd largest skill value that is present amongst all the members)*                | $0.1+0+0+0$ *(since $s_1$ and $s_3$ are redundant)* |
| $π_{setsize}$                 | $3$ *(number of people in the team)*                                                                          | $3$                                                 |
| $π_{coverage}$                | $0.5+0.75+1+0$ *(max skill weight per skill)*                                                                 | $0.1+0.25+1+0.2$                                    |
| $π_{k-robustness}$            | $1$ (you can remove *b* or *c*, and $\{s_1, s_2, s_3\}$ would still be covered somehow, regardless of weight) | $0$ (you can't remove anyone)                       |
### After Normalization:
| Team (right) / <br>Metric (below) | $T_1$             | $T_2$           |
| --------------------------------- | ----------------- | --------------- |
| $π_{redundancyNorm}$              | $0.75/4=0.1875$   | $1.1/4=0.1$     |
| $π_{setsizeNorm}$                 | $3/5 = 0.6$       | $3/5 = 0.6$     |
| $π_{coverageNorm}$                | $2.25/4 = 0.5625$ | $1.55/4=0.3875$ |
| $π_{k-robustnessNorm}$            | $1$               | $0$             |
### **Computing the Overall Goodness Metric:**
Following the example with unweighted skills, consider the default weights for each of the metrics to be: 
- Redundancy: $1$
- Set size: $1$
- Coverage: $3$
- k-Robustness: $3$

| Team (right) / <br>Metric (below) | $T_1$                                                                  | $T_2$    |
| --------------------------------- | ---------------------------------------------------------------------- | -------- |
| $π_{overallGoodness}$             | $(1\cdot0.1875 + 1\cdot0.6 + 3\cdot0.5625 + 3\cdot1)/(1+1+3+3)=0.6844$ | $0.2328$ |

## BibTeX
If you find this metric useful in your research, please cite it using the following BibTeX entry:
```bibtex
@inproceedings{valluru2024promoting,
  title={Promoting Research Collaboration with Open Data Driven Team Recommendation in Response to Call for Proposals},
  author={Valluru, Siva Likitha and Srivastava, Biplav and Paladi, Sai Teja and Yan, Siwen and Natarajan, Sriraam},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={38},
  number={21},
  pages={22833--22841},
  year={2024}
}
