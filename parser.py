# parser.py
# run --> python3 parser.py grammar.cfg "sentence"
# when given a .cfg file as specified in the README.md, will display all legal 
# parse trees for the sentence passed in using a modified earley parser method

# Gustav Baumgart
# Brian Orza

# imports
from nltk.tree import Tree
import sys

# keeps the count for the number of variables created
# new variables are created in the order X0, X1, X2, ...
counter = 0


# takes in a file of context-free grammar
# returns the list of rules which are represented as lists
# S -> A B is represented as ['S', 'A', 'B']
def get_cfg(filename):
    rules = []
    
    # TODO: add code to parse .cfg file
    
    return rules


# Add PoS tags wherever needed in order to satisfy the property where terminal 
# states are always produced by a PoS tag that only leads to them
def add_tags(rules):
    global counter
    new_rules = []
    
    # TODO: add code to add PoS tags whenever needed
    
    return new_rules


# returns a list of unit productions, and a list of non-unit productions
def separate_unit_prod(rules):
    unit_prod = []
    non_unit_prod = []
    
    # TODO: add code to separate unit productions and non-unit productions
    
    return (unit_prod, non_unit_prod)


# returns True if progress on rule is complete, False otherwise
def incomplete(state):
    
    # TODO: add logic to check for progress on rule within state
    
    return True


# sets up chart as a list of lists
def set_up_earley(n):
    table = []
    
    # TODO: create a list of n+1 empty lists
    
    return table


# adds possible rules to chart to be evaluated later
def predictor(state, sep_rules, chart):
    
    # TODO: implement completer
    
    pass


# scans unit productions for rules that apply to the category in question
def scanner(state, sep_rules, chart):
    
    # TODO: implement scanner
    
    pass


# goes through the chart to check for states that could be updated with new
# information from a completed rule
def completer(state, sep_rules, chart):
    
    # TODO: implement completer
    
    pass


# performs modified Earley algorithm
# words is a list of string, each a word passed in 
# sep_rules is two lists of lists (unit_prod, non_unit_prod)
# returns list of trees starting at S
def earley(words, sep_rules):
    
    # TODO: implement Earley parser
    
    return []


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
    sep_rules = separate_unit_prod(new_rules)
    
    # perform algorithm
    mod_trees = earley(sys.argv[2].split(), sep_rules)
    
    # revert to old rules in each generated tree
    final_trees = list(map(remove_X, mod_trees))
    
    display_trees(final_trees)

    
if __name__ == '__main__':
   main()