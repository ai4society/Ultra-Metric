# Ultra-Metric
Code and examples for how to use metrics for the output of any team / group / item recommendation system.

## Metrics Used
- Redundancy: what is the percentage of skills shared amongst 2+ researchers? (How many researchers have common skills?)
- Set size: what is the team size? (Usually determined by total_funding_amount/$50K)
- Coverage: how many skills are covered by researchers and how many are still required by the RFP?
- K-robustness: how many team members can we remove before the team starts to fall apart?

## Terminology

- Demand: *What kind of skills may be required/desired by the RFP?*
	- {$s_2$, $s_2$, ..., $s_i$}
- Supply: *What resources do we have available?*
	- Team of researchers $T_i = {a, b, c, d, ..., N}$
	- Researcher skills = {a: [$s_1$, $s_2$, ..., $s_i$], b: [$s_1$, $s_2$, ..., $s_j$], ..., N: [$s_1$, $s_2$, ..., $s_k$]}

## Example

- Demand: {$s_1$, $s_2$, $s_3$, $s_4$}
- Supply:
	- Consider the following teams in this format: *team_name = {set_of_researchers}*
		- T1 = {a}
		- T2 = {a, b, c}
		- T3 = {a, b}
		- T4 = {a, d, e}
	- Researcher skills: *researcher_name = {set_of_skills}*:
		- a = {$s_1$, $s_2$}
		- b = {$s_3$, $s_4$}
		- c = {$s_2$, $s_3$}
		- d = {$s_1$, $s_2$}
		- e = {$s_2$, $s_3$}

Problem: *Evaluate the potential of each team using the above-mentioned metrics.*

| Team (right) / Metric (below) | $T_1$                                                     | $T_2$                     | $T_3$          | $T_4$              |
| ----------------------------- | ------------------------------------------------------ | ---------------------- | ----------- | --------------- |
| $π_{redundancy}$              | $1\time$s_1$+1\time$s_1$=2$                                            | $1\time$s_2$+1\time$s_2$+1\time$s_2$=6$        | $1\time$s_2$+1\time$s_2$=4$ | $1\time$s_2$+1\time$s_2$+1\time$s_2$=6$ |
| $π_{setsize}$                 | $1$                                                      | $3$                      | $2$           | $3$               |
| $π_{coverage}$                | $-2$ *(indicates that this team is short of two skills)* | $0$                      | $0$           | $-1$              |
| $π_{k-robustness}$            | $0$ (you can't remove anyone)                            | $1$ (you can remove *c*) | $0$           | $0$                |
