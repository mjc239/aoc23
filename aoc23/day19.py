from dataclasses import dataclass
import operator
from dataclasses import field
from copy import deepcopy
from itertools import combinations


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def create(cls, def_string):
        # Create a part from the string provided in the input
        attributes = def_string.strip("{}").split(",")
        attributes = [a.split("=") for a in attributes]
        attribute_dict = {a[0]: int(a[1]) for a in attributes}

        return cls(**attribute_dict)

    @property
    def part_sum(self):
        # Part value = sum of xmas attributes
        return self.x + self.m + self.a + self.s


@dataclass
class Condition:
    variable: str  # e.g. x
    relation: str  # e.g. <
    value: int  # e.g. 101

    def __repr__(self):
        return f"{self.variable}{self.relation}{self.value}"


def process_workflow_string(workflow_string: str):
    # input = string of form:
    # 'px{a<2006:qkq,m>2090:A,rfg}'

    # name: 'px'
    # rules_string: 'a<2006:qkq,m>2090:A,rfg'
    name, rules_string = workflow_string[:-1].split("{")

    # processed_rules: [[a<2006, 'qkq'], [m>2090, 'A'], ['rfg']]
    processed_rules = []

    for rule_string in rules_string.split(","):
        # rule_string of form:
        # 'a<2006:qkq' or 'rfg'
        rule = rule_string.split(":")

        if len(rule) == 1:
            # final rule in workflow
            processed_rules.append(rule)

        elif len(rule) == 2:
            # Convert condition to Condition
            condition_string, new_name = rule

            # condition_string: 'a<2006'
            processed_rules.append(
                [
                    Condition(
                        condition_string[0],
                        condition_string[1],
                        int(condition_string[2:]),
                    ),
                    new_name,
                ]
            )

    return name, processed_rules


def process_input(input_list: list[str]):
    # Split input_list at the empty line
    workflows = {}
    parts = []
    gap_index = input_list.index("")
    input_workflows = input_list[:gap_index]
    input_parts = input_list[gap_index + 1 :]

    # Process rules and parts separately
    workflows = {
        name: processed_rules
        for name, processed_rules in map(process_workflow_string, input_workflows)
    }

    parts = [Part.create(line) for line in input_parts]

    return workflows, parts


# The operator module helps with this:
OPERATORS = {"<": operator.lt, ">": operator.gt}


def evaluate_workflow(part: Part, workflow: list[list[Condition, str]]) -> str:
    # Follow the part along the tree, until an output string is found
    # (either a new workflow to move to, or 'A' or 'R')
    for rule in workflow:
        if len(rule) == 1:
            # At end of workflow
            return rule[0]
        else:
            # Check if condition is satisfied
            condition, name = rule
            operator = OPERATORS[condition.relation]
            if operator(getattr(part, condition.variable), condition.value):
                return name


def is_part_accepted(part: Part, workflows):
    # Start at `in`
    key = "in"

    # Continue until termination
    while key not in ["A", "R"]:
        key = evaluate_workflow(part, workflows[key])

    return key == "A"


@dataclass
class Region:
    accepted: bool = None

    # Each range starts with the full set of possible values
    x: tuple[int] = field(default_factory=lambda: [1, 4000])
    m: tuple[int] = field(default_factory=lambda: [1, 4000])
    a: tuple[int] = field(default_factory=lambda: [1, 4000])
    s: tuple[int] = field(default_factory=lambda: [1, 4000])

    def set_upper_limit(self, variable: str, value: int):
        limits = getattr(self, variable)
        if value < limits[1]:
            limits[1] = value

        # Check that lower limit < upper limit
        assert limits[0] <= limits[1]

    def set_lower_limit(self, variable: str, value: int):
        limits = getattr(self, variable)
        if value > limits[0]:
            limits[0] = value

        # Check that lower limit < upper limit
        assert limits[0] <= limits[1]

    def count_parts(self):
        if len(self.x) * len(self.m) * len(self.a) * len(self.s) == 0:
            return 0
        else:
            return (
                (self.x[1] - self.x[0] + 1)
                * (self.m[1] - self.m[0] + 1)
                * (self.a[1] - self.a[0] + 1)
                * (self.s[1] - self.s[0] + 1)
            )


def compute_regions(workflows: dict[str, list[list[Condition, str]]]) -> list[Region]:
    regions = []

    # Start with a single, maximal range at the 'in' workflow
    states = [("in", Region())]

    while len(states) != 0:
        # Take the most recently added state
        state = states.pop()
        name, region = state

        workflow = workflows[name]

        for rule in workflow:
            if len(rule) == 2:
                condition, name = rule
                # There are 2 cases - the rule is/is not satified
                # Make a copy for later
                skip_region = deepcopy(region)

                # Case 1 - condition satisfied
                # Reset the limits of the region, based on the condition
                if condition.relation == "<":
                    region.set_upper_limit(condition.variable, condition.value - 1)
                elif condition.relation == ">":
                    region.set_lower_limit(condition.variable, condition.value + 1)

                # Add the completed region to regions,
                # or add new state to stack
                if name in ["A", "R"]:
                    region.accepted = name
                    regions.append(region)
                else:
                    states.append((name, region))

                # Case 2 - condition not satisfied
                if condition.relation == ">":
                    skip_region.set_upper_limit(condition.variable, condition.value)
                elif condition.relation == "<":
                    skip_region.set_lower_limit(condition.variable, condition.value)

                # Redefine region, to use as input for next rule in loop
                region = skip_region

            else:
                # End of workflow
                # Either terminate or add new state to stack
                name = rule[0]
                if name in ["A", "R"]:
                    region.accepted = name
                    regions.append(region)
                else:
                    states.append((name, region))

    return regions


def count_parts(regions: list[Region], state: str):
    regions = [region for region in regions if region.accepted == state]
    return sum([region.count_parts() for region in regions])


def _intersect_intervals(interval_1: list[int], interval_2: list[int]) -> list[int]:
    a_1, b_1 = interval_1
    a_2, b_2 = interval_2
    if b_1 < a_2 or b_2 < a_1:
        return []
    else:
        return [max(a_1, a_2), min(b_1, b_2)]


def intersect_regions(region_1: Region, region_2: Region) -> Region:
    return Region(
        x=_intersect_intervals(region_1.x, region_2.x),
        m=_intersect_intervals(region_1.m, region_2.m),
        a=_intersect_intervals(region_1.a, region_2.a),
        s=_intersect_intervals(region_1.s, region_2.s),
    )
