# Ultra-Metric
Code and examples for how to use metrics for the output of any team / group / item recommendation system.
- [metrics_scorer.py](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_scorer.py) - code/implementation for each of the 4 metrics described below
- [metrics_notebook.ipynb](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_notebook.ipynb) - shows example for how to use *metrics_scorer.py.*

## Metrics Used
- Redundancy: what is the percentage of skills shared amongst 2+ researchers? (How many researchers have common skills?)
- Set size: what is the team size? (Usually determined by total_funding_amount/$50K)
- Coverage: how many skills are covered by researchers and how many are still required by the RFP?
- K-robustness: how many team members can we remove before the team starts to fall apart?

## Terminology

- Demand: *What kind of skills may be required/desired by the RFP?*
	- $\{ s_1, s_2, ..., s_i \}$
- Supply: *What resources do we have available?*
	- Team of researchers $T_i = {a, b, c, d, ..., N}$
	- Researcher skills = $\{a: [s_1, s_2, ..., s_i], b: [s_1, s_2, ..., s_j], ..., N: [s_1, s_2, ..., s_k]\}$

## Example

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

Problem: *Evaluate the potential of each team using the above-mentioned metrics.*

**Before Normalization:**
| Team (right) / Metric (below) | $T_1$                                                     | $T_2$                     | $T_3$          | $T_4$              |
| ----------------------------- | ------------------------------------------------------ | ---------------------- | ----------- | --------------- |
| $π_{redundancy}$              | $1\times1+1\times1=2$                                            | $1\times2+1\times2+1\times2=6$        | $1\times2+1\times2=4$ | $1\times2+1\times2+1\times2=6$ |
| $π_{setsize}$                 | $1$                                                      | $3$                      | $2$           | $3$               |
| $π_{coverage}$                | $-2$ *(indicates that this team is short of two skills)* | $0$                      | $0$           | $-1$              |
| $π_{k-robustness}$            | $0$ (you can't remove anyone)                            | $1$ (you can remove *c*) | $0$           | $0$                |

**After Normalization:**
We normalize our data to stay between [0,1] so that the measure is consistent across different teams, team members, team skillsets, etc. Consider:
- $x_i$ : value of metric before normalization
- $min(x)$: what is the minimum value possible from this metric?
- $max(x)$: what is the maximum value possible from this metric? For each of the following:
	- $maxRedundancy$ = (total number of demand skills) * (number of researchers)             /*where each researcher of the team has all the demand skills*/  
	- $maxSetsize$ = 5                 /* default value (temporarily) */
	- $maxCoverage$ = (total number of demand skills)
	- $maxKrobust$ = 1               /* for now */

Then, normalized score = $(x_i – min(x)) / (max(x) – min(x))$

| Team (right) / Metric (below) | $T_1$                                                     | 
| ----------------------------- | ------------------------------------------------------ | 
| $π_{redundancyNorm}$              | $(2-1)/(len(demand)\cdot len(team\_size) -1) = (2-1)/(4*1-1) = 0.333$| 
| $π_{setsizeNorm}$                 | $1/5 = 0.2$                                                      | 
| $π_{coverageNorm}$                | $2/4 = 0.50$ |
| $π_{k-robustnessNorm}$            | $0$ (you can't remove anyone)                            |

**Computing the Overall Goodness Metric:**
Each metric has a weight. By default, they're:
- Redundancy: -1
- Set size: -1
- Coverage: 1
- k-Robustness: 1
By default, high *redundancy* and *set size* are considered to be "negative" traits, hence the negative weight. But users can change this if they wish using *[set_new_weights()](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_scorer.py#:~:text=def-,set_new_weights,-(self%2C)* in [metrics_scorer.py](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_scorer.py).

| Team (right) / Metric (below) | $T_1$                                                     | 
| ----------------------------- | ------------------------------------------------------ | 
| $π_{overall\_goodness}$              | $((-1\cdot0.333 + -1\cdot0.2 + 1\cdot0.5 + 1\cdot0)+1)/(1+1)=0.4833$| 

What if you set different weights?
- Redundancy: 0.11
- Set size: 0.09
- Coverage: 0.8
- k-Robustness: 0.0
By default, high *redundancy* and *set size* are considered to be "negative" traits, hence the negative weight. But users can change this if they wish using *[set_new_weights()](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_scorer.py#:~:text=def-,set_new_weights,-(self%2C)* in [metrics_scorer.py](https://github.com/ai4society/Ultra-Metric/blob/main/metrics_scorer.py).

| Team (right) / Metric (below) | $T_1$                                                     | 
| ----------------------------- | ------------------------------------------------------ | 
| $π_{overall\_goodness}$              | $((0.11\cdot0.333 + 0.09\cdot0.2 + 0.8\cdot0.5 + 0.0\cdot0)-0.00)/(1.0-0.0)=0.5683$| 
