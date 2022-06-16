# parser.py
# run --> python3 parser.py grammar.cfg "sentence"
# when given a .cfg file as specified in the README.md, will display all legal
# parse trees for the sentence passed in using a modified earley parser method

# Gustav Baumgart
# Brian Orza

# imports
from nltk.tree import Tree
from copy import deepcopy
import sys

# keeps the count for the number of variables created
# new variables are created in the order X0, X1, X2, ...
counter = 0


# takes in a file of context-free grammar
# returns the list of rules which are represented as lists
# S -> A B is represented as ['S', 'A', 'B']
def get_cfg(filename):
    rules = []

    fp = open(filename)

    for line in fp:

        if line[0] == '#':
            continue

        templist = line.strip().split()

        rules.append(templist[:1]+templist[2:])

    fp.close()

    return rules


# Add PoS tags wherever needed in order to satisfy the property where terminal
# states are always produced by a PoS tag that only leads to them
def add_tags(rules):
    global counter
    new_rules = []

    # TODO: add code to add PoS tags whenever needed

    return new_rules


# returns a list of POS and non-POS rules
def separate_POS(rules):
    POS = []
    non_POS = []

    for rule in rules:
        if len(rule) == 2 and rule[1].islower():
            POS.append(rule)
        else:
            non_POS.append(rule)

    return (POS, non_POS)


# returns True if progress on rule is complete, False otherwise
def incomplete(state):

    return state[0][-1] != "."


# sets up chart as a list of lists
def set_up_earley(n):
    table = []

    for i in range(n+1):
        table.append([])

    return table

# adds state to specific chart entry
def enqueue(state, chart, chart_entry):
    if state not in chart[chart_entry]:
        chart[chart_entry].append(state)


# adds possible rules to chart to be evaluated later
def predictor(state, sep_rules, chart):

    # unpack state
    curr_rule, curr_span, curr_tree = state
    i, j = curr_span

    # get non_POS rules
    non_POS = sep_rules[1]

    for rule in non_POS:
        if curr_rule[curr_rule.index(".")+1] == rule:
            temp_rule = rule.copy()
            temp_rule.insert(1,".")

            enqueue(temp_rule, (j,j), Tree(rule[0],[])), chart, j)


# scans unit productions for rules that apply to the category in question
def scanner(state, sep_rules, chart, words):
    # unpack state
    curr_rule, curr_span, curr_tree = state
    i, j = curr_span

    # get POS rules
    POS = sep_rules[0]

    # add POS rule if exists
    for rule in POS:
        if rule[0] == curr_rule[curr_rule.index('.')+1] and rule[1] == words[j]:
            temp_state = (rule.copy()+['.'], (j, j+1), Tree(rule[0], [rule[1]]))
            enqueue(temp_state, chart, j+1)
            return


# goes through the chart to check for states that could be updated with new
# information from a completed rule
def completer(state, sep_rules, chart):
    # unpack state
    curr_rule, curr_span, curr_tree = state
    j, k = curr_span


    # check for states to 'complete'
    for state in chart[j]:
        if incomplete(state) and state[0][state[0].index['.']+1] == curr_rule[0]:
            # move period tracking progress up one
            new_rule = state[0][:state[0].index['.']] + [state[0][state[0].index['.']+1], '.'] + state[0][state[0].index['.']+2:]

            # edit tree to include progress from completed state
            new_tree = Tree(state[2].label, deepcopy(state[2].children) + [deepcopy(curr_tree)])

            # build and add state
            temp_state = (new_rule, (state[1][0], k), new_tree)
            enqueue(temp_state, chart, k)


# performs modified Earley algorithm
# words is a list of string, each a word passed in
# sep_rules is two lists of lists (POS, non_POS)
# returns list of trees starting at S
# a state is represented as a tuple with three subcomponents
# (rule with progress marked,
# (start pos of rule wrt terminals, period pos of rule wrt terminals),
# working progress on a nltk.tree)
# example:
# ( ['S', 'A', '.', 'B'] , (0,1) , Tree('S', [Tree('A', ['word'])]) )
# notice there is no 'B' branch yet because the period marks the progress
# which has not passed 'B'
def earley(words, sep_rules):

    chart = set_up_earley(len(words))

    enqueue((["Gamma", ".", "S"], (0, 0), Tree("Gamma",[])), chart, 0)

    for i in range(len(words)):
        index = 0

        while index < len(chart[i]):
            if incomplete(state) and state[0][state[0].index('.')+1] not in map(lambda x: x[0], sep_rules[0]):
                predictor(state, sep_rules, chart)
            elif incomplete(state) and state[0][state[0].index('.')+1] in map(lambda x: x[0], sep_rules[0]):
                scanner(state, sep_rules, chart)
            else:
                completer(state, sep_rules, chart)

            index++

    return [state[2] if not incomplete(state) and state[0][0] == 'S' for state in chart[-1]]


# removes nodes artificially added (such as X0, X1, ...)
def remove_X(tree):

    # TODO: implement recursive algorithm to remove nodes that start with X

    return tree


# prints trees passed in as a list or display via another method
def display_trees(trees):

    # TODO: add a way to visualize trees

    pass


def main():

    # check number of arguments
    if len(sys.argv) != 3:
        print("ERROR: Incorrect number of parameters")
        return

    # get the rules and separate them
    original_rules = get_cfg(sys.argv[1])
    new_rules = add_tags(original_rules)
    sep_rules = separate_POS(new_rules)

    # perform algorithm
    mod_trees = earley(sys.argv[2].split(), sep_rules)

    # revert to old rules in each generated tree
    final_trees = list(map(remove_X, mod_trees))

    display_trees(final_trees)


if __name__ == '__main__':
   main()
