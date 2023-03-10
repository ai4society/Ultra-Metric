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

- Demand: $\{s_1, s_2, ..., s_i\}$
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

| Team (right) / Metric (below) | $T_1$                                                     | $T_2$                     | $T_3$          | $T_4$              |
| ----------------------------- | ------------------------------------------------------ | ---------------------- | ----------- | --------------- |
| $π_{redundancy}$              | $1\times1+1\times1=2$                                            | $1\times2+1\times2+1\times2=6$        | $1\times2+1\times2=4$ | $1\times2+1\times2+1\times2=6$ |
| $π_{setsize}$                 | $1$                                                      | $3$                      | $2$           | $3$               |
| $π_{coverage}$                | $-2$ *(indicates that this team is short of two skills)* | $0$                      | $0$           | $-1$              |
| $π_{k-robustness}$            | $0$ (you can't remove anyone)                            | $1$ (you can remove *c*) | $0$           | $0$                |
