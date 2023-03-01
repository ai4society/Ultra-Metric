# Ultra-Metric
Code and examples for how to use metrics for the output of any team / group / item recommendation system.

## Metrics Used
- Redundancy: what is the percentage of skills shared amongst 2+ researchers? (How many researchers have common skills?)
- Set size: what is the team size? (Usually determined by total_funding_amount/$50K)
- Coverage: how many skills are covered by researchers and how many are still required by the RFP?
- K-robustness: how many team members can we remove before the team starts to fall apart?

## Terminology

- Demand: *What kind of skills may be required/desired by the RFP?*
	- {s1, s2, ..., s_i}
- Supply: *What resources do we have available?*
	- Team of researchers T_i = {a, b, c, d, ..., N}
	- Researcher skills = {a: [s1, s2, ..., s_i], b: [s1, s2, ..., s_j], ..., N: [s1, s2, ..., s_k]}

## Example

- Demand: {s1, s2, s3, s4}
- Supply:
	- Consider the following teams in this format: *team_name = {set_of_researchers}*
		- T1 = {a}
		- T2 = {a, b, c}
		- T3 = {a, b}
		- T4 = {a, d, e}
	- Researcher skills: *researcher_name = {set_of_skills}*:
		- a = {s1, s2}
		- b = {s3, s4}
		- c = {s2, s3}
		- d = {s1, s2}
		- e = {s2, s3}

Problem: *Evaluate the potential of each team using the above-mentioned metrics.*

| Metric (right) / Team (below) | T1                                                     | T2                     | T3          | T4              |
| ----------------------------- | ------------------------------------------------------ | ---------------------- | ----------- | --------------- |
| $π_{redundancy}$              | $1\times1+1\times1=2$                                            | $1\times2+1\times2+1\times2=6$        | $1\times2+1\times2=4$ | $1\times2+1\times2+1\times2=6$ |
| $π_{setsize}$                 | $1$                                                      | $3$                      | $2$           | $3$               |
| $π_{coverage}$                | $-2$ *(indicates that this team is short of two skills)* | $0$                      | $0$           | $-1$              |
| $π_{k-robustness}$            | $0$ (you can't remove anyone)                            | $1$ (you can remove *c*) | $0$           | $0$                |
