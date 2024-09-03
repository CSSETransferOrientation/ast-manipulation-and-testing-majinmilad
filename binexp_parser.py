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

# pass a prefix list in and it is popped off like a queue to build the tree
# enums are used to classify the type of node in the tree (a number or an operator)
class BinOpAst:

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
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

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

    def additive_identity(self):

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
        self.right.additive_identity()

        # the left node is guaranteed to be a constant-value node with no children
        # so if the right node is a zero constant, simply shift the left node value
        # and type up and discard of the zero-value right child
        if self.right.val == '0':
            self.val = self.left.val
            self.val = self.left.type
        # else if left node is a zero constant, effectively discard the zero-value
        # left child as well as the entire operation step and shift right node up
        elif self.left.val == '0':
            # take on the value and type of the right child
            self.val = self.right.val
            self.type = self.right.type
            # take on the children of the right child
            self.left = self.right.left
            self.right = self.right.right

    def multiplicative_identity(self):

        """
        Reduce multiplicative identities
        x * 1 = x
        """

        # IMPLEMENT ME!
        pass

    # def mult_by_zero(self):
    #
    #     """
    #     Reduce multiplication by zero
    #     x * 0 = 0
    #     """
    #
    #     # Optionally, IMPLEMENT ME! (I'm pretty easy)
    #     pass
    #
    # def constant_fold(self):
    #     """
    #     Fold constants,
    #     e.g. 1 + 2 = 3
    #     e.g. x + 2 = x + 2
    #     """
    #     # Optionally, IMPLEMENT ME! This is a bit more challenging.
    #     # You also likely want to add an additional node type to your AST
    #     # to represent identifiers.
    #     pass

    def simplify_binary_operators(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        self.additive_identity()
        self.multiplicative_identity()
        # self.mult_by_zero()
        # self.constant_fold()


if __name__ == "__main__":
    # unittest.main()
    # print(list(NodeType))

    prefix_list = '+ 1 x 5 + 0 + 6 x 2 3'
    prefix_list = prefix_list.split()
    print(prefix_list)

    ast = BinOpAst(prefix_list)
    # print(ast)

    # print(ast.infix_str())
    # print(ast.prefix_str())
    # print()
    # ast.additive_identity()
    # print()
    # print(ast.prefix_str())

    pass