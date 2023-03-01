# Imports
import itertools

# For the metrics scorer
class MetricScorer:

    # demand
    # RFP-required skillset (Note: These are not exclusively mentioned; they will be extracted.)
    demand = []

    # supply
    team = []
    researchers = {}

    # metrics
    redundancy = 0.0
    setsize = 0
    coverage = 0.0
    krobust = 0

    def __init__(self):
        print("Metrics class instantiated")

    def reset(self):
        self.demand = []
        self.team = []
        self.researchers = {}
        self.redundancy = 0.0
        self.setsize = 0
        self.coverage = 0.0
        self.krobust = 0
        print("Metrics class reset")

    def calc_redundancy(self):
        """
        Given RFP requirements (demand[]) and candidate team (team[]), check whether there are any redundant skills amongst the members (using researchers{}).
        --> This method currently may also take irrelevant skills into consideration.
        """
        if self.team == [] or self.researchers == []:
            raise Exception('Team and list of researchers cannot be empty!')
        for i in self.team:
            try:
                # add the number of skills each researcher has
                self.redundancy += 1*len(self.researchers[i])
            except KeyError:
                raise Exception('Researcher "+i+" not found!')

    def calc_setsize(self):
        """
        Return total team size. (Max size should ideally be (total amount of budget granted by funding agency)/$50K.) 
        """
        self.setsize = len(self.team)

    def calc_coverage(self):
        """
        Given RFP requirements (demand[]) and candidate team (team[]), check how many *required* skills are satisfied by the members. (Ignore skills irrelevant to RFP (demand).)

        If all skills are satisfied, coverage = 0.
        Else, the score will be negative. (The negative number will imply how many skills are still left to be fulfilled.)
        """
        if self.team == [] or self.researchers == [] or self.demand == []:
            raise Exception(
                'Team, list of researchers, and list of demanded skills cannot be empty!')

        covered_skills = []
        for i in self.team:
            for j in self.researchers[i]:
                if j not in covered_skills and j in self.demand:
                    covered_skills.append(j)
        self.coverage = -1*(len(self.demand)-len(set(covered_skills)))

    def calc_krobust(self):
        """
        If a team's coverage score remains the same before/after removing N members, the k-robust score for that team would be N.
        """
        # store original values
        og_team = self.team.copy()
        og_researchers = self.researchers.copy()
        
        self.calc_coverage()
        og_coverage = self.coverage
        
        # generate combinations of team members of all sizes i (1 to N)
        for i in range(1, len(og_team)):
            # iterate through each combination of subsets and measure the coverage of team after the member has been removed
            for subset in itertools.combinations(og_team, i):
                # define new team/researchers without the above subset of members
                self.team = og_team.copy()
                self.researchers = og_researchers.copy()
                for j in subset:
                    self.team.remove(j)
                    self.researchers.pop(j)
                self.calc_coverage()
                
                # if coverage remains the same after the member has been removed, increment the value of k by one
                if og_coverage==0 and og_coverage <= self.coverage:
                    self.krobust += 1
                    break
                
        # restore the old values of team, researchers, and coverage
        self.team = og_team.copy()
        self.researchers = og_researchers.copy()
        self.coverage = og_coverage
                
    def run_metrics(self):
        self.calc_redundancy()
        self.calc_setsize()
        self.calc_coverage()
        self.calc_krobust()
        print("Metrics run")

    def printScorer(self):
        print("Demand:\t", self.demand)
        print("Supply:\tTeam members:\t", self.team)
        print("\tResearchers:\t", self.researchers)

        print("\n")
        print("Redundancy:\t", self.redundancy)
        print("Set size:\t", self.setsize)
        print("Coverage:\t", self.coverage)
        print("k-Robustness:\t", self.krobust)
