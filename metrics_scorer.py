# Imports
import itertools
from tabulate import tabulate

# For the metrics scorer


class MetricScorer:

    # demand
    # RFP-required skillset (Note: These are not exclusively mentioned; they will be extracted.)
    demand = []

    # supply
    team = []
    team_skills = {}

    # metrics
    redundancy = 0.0
    setsize = 0
    coverage = 0.0
    krobust = 0
    goodness = 0.0

    # weights for metrics (redundancy, setsize, coverage, k-robustness)
    w_r = 0.1
    w_s = 0.1
    w_c = 0.4
    w_k = 0.4

    def __init__(self):
        print("Metrics class instantiated")

    def reset(self):
        self.demand = []

        self.team = []
        self.team_skills = {}

        self.redundancy = 0.0
        self.setsize = 0
        self.coverage = 0.0
        self.krobust = 0
        self.goodness = 0

        self.w_r = -1
        self.w_s = -1
        self.w_c = 1
        self.w_k = 1

        print("Metrics class reset")

    def calc_redundancy(self):
        """
        Given RFP requirements (demand[]) and candidate team (team[]), check whether there are any redundant skills amongst the members (using team_skills{}).
        --> This method currently may also take irrelevant skills into consideration.
        """
        if self.team == [] or self.team_skills == {}:
            raise Exception('Team and list of team_skills cannot be empty!')
        
        redundant_skills=[]
        skills_covered=[]
        
        for i in self.team:
            try:
                # check the number of redundant skills
                for j in self.team_skills[i]:
                    if j in self.demand:
                        if j not in skills_covered:   # check if skill is relevant to self.demand(), and if it's a redundant one or not
                            skills_covered.append(j)
                        elif j in skills_covered:
                            if j not in redundant_skills:
                                redundant_skills.append(j)
            except KeyError:
                raise Exception('Researcher "+i+" not found!')

        """
        Normalize metric: normalized_score = (x_i – min(x)) / (max(x) – min(x))

        Ideally, the 'redundancy' score should only equal the number of skills that the RFP requires (which is known via extraction).
        If the redundancy score matches the number of skills needed, then the score is 0. Otherwise, it's in the [0, 1] scale.
        """
        self.redundancy = len(redundant_skills)/len(self.demand)

    def calc_setsize(self, size=5):
        """
        Return total team size. (Max size should ideally be (total amount of budget granted by funding agency)/$50K.)
        """
        self.setsize = len(self.team)

        """
        Normalize metric: normalized_score = (x_i – min(x)) / (max(x) – min(x))
        """
        self.setsize = (self.setsize)/(size)

    def calc_coverage(self):
        """
        Given RFP requirements (demand[]) and candidate team (team[]), check how many *required* skills are satisfied by the members. (Ignore skills irrelevant to RFP (demand).)

        Coverage is the percentage of all skills satisfied by the RFP. If all skills are satisfied, coverage = 100%.
        """
        if self.team == [] or self.team_skills == {} or self.demand == []:
            raise Exception(
                'Team, list of team_skills, and list of demanded skills cannot be empty!')

        covered_skills = []
        for i in self.team:
            for j in self.team_skills[i]:
                if j not in covered_skills and j in self.demand:
                    covered_skills.append(j)
        
        # measure coverage
        self.coverage=len(covered_skills)/len(self.demand)

    def calc_krobust(self):
        """
        If a team's coverage score remains the same before/after removing N members, the k-robust score for that team would be 1.
        """
        # store original values
        og_team = self.team.copy()
        og_team_skills = self.team_skills.copy()

        self.calc_coverage()
        og_coverage = self.coverage

        # generate combinations of team members of all sizes i (1 to N)
        for i in range(1, len(og_team)):
            # iterate through each combination of subsets and measure the coverage of team after the member has been removed
            for subset in itertools.combinations(og_team, i):
                # define new team/team_skills without the above subset of members
                self.team = og_team.copy()
                self.team_skills = og_team_skills.copy()
                for j in subset:
                    self.team.remove(j)
                    self.team_skills.pop(j)
                self.calc_coverage()

                # if coverage remains the same after the member has been removed, increment the value of k by one
                if og_coverage == 0 and og_coverage <= self.coverage and self.setsize >= 5:
                    self.krobust += 1
                    break

        # restore the old values of team, team_skills, and coverage
        self.team = og_team.copy()
        self.team_skills = og_team_skills.copy()
        self.coverage = og_coverage

        """
        Normalize metric:
        For k-robustness, instead of a scale from [0,1], we instead use 1 if k>0 or 0 otherwise.
        """
        if self.krobust > 0:
            self.krobust = 1

    def set_new_weights(self, weights):
        """Adjust the weights (only if negative weights are present): this is used to help normalize them."""
        if min(weights)<0:
            range_of_weights = max(weights) - min(weights)
            for i in range(len(weights)):
                weights[i] += range_of_weights
            
        # if min(weights) is still negative => all weights are equal
        if min(weights)<0:
            for i in range(len(weights)):
                weights[i] *= -1

        """Normalize the weights."""
        self.w_r=weights[0]/sum(weights)
        self.w_s=weights[1]/sum(weights)
        self.w_c=weights[2]/sum(weights)
        self.w_k=weights[3]/sum(weights)

    def get_weights(self):
        """Return existing weights."""
        return [self.w_r, self.w_s, self.w_c, self.w_k]
    
    def goodness_measure(self):
        """
        Total score = SUM(w_i*metric_i)
        """
        
        self.goodness = self.w_r*self.redundancy + self.w_s * \
            self.setsize + self.w_c*self.coverage+self.w_k*self.krobust
            
        print(self.goodness)

        """
        Normalize the score. 
        
        At default weights: {w_r: -1, w_s: -1, w_c: 1, w_k: 1}:
        The worst case would be [horrible coverage/robustness, large redundancy/set_size].
        The best case would be [complete coverage/robustness, minimal redundancy/set_size]
        """
        self.goodness = self.goodness/(self.w_r+self.w_s+self.w_c+self.w_k)
        # min_goodness=min([self.w_r, self.w_s, self.w_c,self.w_k])
        # max_goodness=max([self.w_r, self.w_s, self.w_c,self.w_k])
        # self.goodness = (self.goodness-min_goodness) / \
        #    (max_goodness-min_goodness)

    def run_metrics(self):
        # run metrics
        self.calc_redundancy()
        self.calc_setsize()
        self.calc_coverage()
        self.calc_krobust()
        self.goodness_measure()
        print("Metrics run")

    def printScorer(self):
        print("--------------------DEMAND--------------------")
        print("Skills needed:\t", self.demand)
        print("\n")

        print("--------------------SUPPLY--------------------")
        print("Team members:\t", self.team)
        print("Team member skills:\t", self.team_skills)
        print("\n")

        print("--------------------METRICS--------------------")
        print("Redundancy:\t", self.redundancy)
        print("Set size:\t", self.setsize)
        print("Coverage:\t", self.coverage)
        print("k-Robustness:\t", self.krobust)
        print("Total goodness score:\t", self.goodness)

    def printScorerTable(self):
        table = [["Team (right)\nMetric(below)", "T1"], ["Redundancy", self.redundancy], ["Set Size", self.setsize], [
            "Coverage", self.coverage], ["k-Robustness", self.krobust], ["Overall Goodness", self.goodness]]

        print(tabulate(table, headers='firstrow', tablefmt='grid'))