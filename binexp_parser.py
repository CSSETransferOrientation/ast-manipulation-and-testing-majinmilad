# Template created by Dr. Beard
# Edited by Milad Chabok

#!/usr/bin/python3

import os
from os.path import join as osjoin
import unittest
from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'operator'])

# pass a prefix list of string characters in and it is popped off like a queue to build the tree
# enums are used to classify the type of node in the tree (a number or an operator)
# the AST can prune out non-consequential additive and multiplicative identities from the tree
class BinaryOperatorAST:

    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.

    The class object will act as an object representing the root node.
    """

    def __str__(self, indent=0):

        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """

        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def __init__(self, prefix_list):

        # class attributes
        # val - the number or operator the node represents
        # type - describes the node type as a number or an operator
        # left - pointer to left child
        # right - pointer to right child

        """
        Initialize a binary operator AST from a given list in prefix notation.
        Note that it destroys the list that is passed in.
        """

        # hold the number/operator value in the node
        self.val = prefix_list.pop(0)

        # if an operator recursively create left and right children, if a number backtrack (base case)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = False
            self.right = False
        else:
            self.type = NodeType.operator
            self.left = BinaryOperatorAST(prefix_list)
            self.right = BinaryOperatorAST(prefix_list)

    def prefix_str(self):

        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """

        if self.type == NodeType.number:
            return self.val
        elif self.type == NodeType.operator:
            return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

        # match self.type:
        #     case NodeType.number:
        #         return self.val
        #     case NodeType.operator:
        #         return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def infix_str(self):

        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """

        if self.type == NodeType.number:
            return self.val
        elif self.type == NodeType.operator:
            return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'

        # match self.type:
        #     case NodeType.number:
        #         return self.val
        #     case NodeType.operator:
        #         return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'

    def postfix_str(self):

        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """

        if self.type == NodeType.number:
            return self.val
        elif self.type == NodeType.operator:
            return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

        # match self.type:
        #     case NodeType.number:
        #         return self.val
        #     case NodeType.operator:
        #         return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    # a debugging function for inspecting the state of the tree during recursive traversal
    def print_depth_traversal_and_backtracking(self):

        print(self.prefix_str())

        # if number reached backtrack (base case)
        if self.type == NodeType.number:
            print('\nNow displaying the backtrack...')
            print(self.val, self.type)
            return

        # it's a right leaning tree with all left children being constants and all
        # right children being operators until the right-most leaf node
        # so traverse until the end of the right branch and then work back up
        self.right.print_depth_traversal_and_backtracking()

        print(self.val, self.type)
        print('left child:', self.left.val, self.left.type)
        print('right child:', self.right.val, self.right.type)

    def additive_identity_prune(self):

        """
        Reduce additive identities
        x + 0 = x
        """

        # if number reached backtrack (base case)
        if self.type == NodeType.number:
            return

        # it's a right leaning tree with all left children being constants and all
        # right children being operators until the right-most leaf node
        # so traverse until the end of the right branch and then work back up
        self.right.additive_identity_prune()

        # note below we are checking if the operator node value is '+' because we're only doing additive identity pruning

        # the left node is guaranteed to be a constant-value node with no children
        # so if the right node is a zero constant, simply shift the left node number
        # value and type up and discard of the zero-value right child
        if self.right.val == '0' and self.val == '+':
            self.val = self.left.val
            self.type = self.left.type
            self.left = False
            self.right = False
        # else if left node is a zero constant, effectively discard the zero-value
        # left child as well as the entire operation step and shift right node up
        elif self.left.val == '0' and self.val == '+':
            # take on the value and type of the right child
            self.val = self.right.val
            self.type = self.right.type
            # take on the children of the right child
            self.left = self.right.left
            self.right = self.right.right

    def multiplicative_identity_prune(self):

        """
        Reduce multiplicative identities
        x * 1 = x
        """

        # if number reached backtrack (base case)
        if self.type == NodeType.number:
            return

        # it's a right leaning tree with all left children being constants and all
        # right children being operators until the right-most leaf node
        # so traverse until the end of the right branch and then work back up
        self.right.multiplicative_identity_prune()

        # note below we are checking if the operator node value is '*' because we're only doing additive identity pruning

        # the left node is guaranteed to be a constant-value node with no children
        # so if the right node is a one constant, simply shift the left node number
        # value and type up and discard of the one-value right child
        if self.right.val == '1' and self.val == '*':
            self.val = self.left.val
            self.type = self.left.type
            self.left = False
            self.right = False
        # else if left node is a one constant, effectively discard the one-value
        # left child as well as the entire operation step and shift right node up
        elif self.left.val == '1' and self.val == '*':
            # take on the value and type of the right child
            self.val = self.right.val
            self.type = self.right.type
            # take on the children of the right child
            self.left = self.right.left
            self.right = self.right.right

    def mult_by_zero(self):

        """
        Reduce multiplication by zero
        x * 0 = 0
        """

        # Optionally, IMPLEMENT ME! (I'm pretty easy)
        pass

    def constant_fold(self):

        """
        Fold constants,
        e.g. 1 + 2 = 3
        e.g. x + 2 = x + 2
        """

        # Optionally, IMPLEMENT ME! This is a bit more challenging.
        # You also likely want to add an additional node type to your AST
        # to represent identifiers.
        pass

    def simplify_binary_operators(self):

        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """

        self.additive_identity_prune()
        self.multiplicative_identity_prune()
        # self.mult_by_zero()
        # self.constant_fold()

class TestBinaryOperatorAST(unittest.TestCase):

    def test_all_cases(self):
        self.run_specified_tests('arith_id', BinaryOperatorAST.additive_identity_prune)
        self.run_specified_tests('mult_id', BinaryOperatorAST.multiplicative_identity_prune)
        print('ALL TESTS RAN SUCCESSFULLY')

    # specify parent directory of tests and the modifying function being tested
    def run_specified_tests(self, test_folder_name: str, bin_op_ast_function):

        print('TESTING', test_folder_name, 'TEST CASES...\n')

        # create path to input and output files, respectively
        input_files_path = osjoin('testbench', test_folder_name, 'inputs')
        output_files_path = osjoin('testbench', test_folder_name, 'outputs')

        # get an iterable list of file names
        input_file_names = os.listdir(input_files_path)

        # iterate through input files and test against output files
        for file_name in input_file_names:

            # read input files, feed to tree, prune and retrieve new outputted prefix string
            with open(osjoin(input_files_path, file_name)) as file:

                # create ast from the input file prefix string
                prefix_list = file.readline().split()
                ast = BinaryOperatorAST(prefix_list)

                # run the modifying function
                bin_op_ast_function(ast)  # generalize this call

                # collect the prefix string output of the modified tree
                output = ast.prefix_str()

            # read output files and compare against outputted prefix string from the tree
            with open(osjoin(output_files_path, file_name)) as file:
                expected_output = file.readline()
                self.assertEqual(output, expected_output,
                                 'Oh-oh, output did not match expected output! - for test file: ' + file_name)


if __name__ == "__main__":
    unittest.main()