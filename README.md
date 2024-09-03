# Binary Operator Simplifier reflection


## Briefly state how much of the project you completed, e.g. which of the sub tasks work. 

I fully implemented what I believe to be working versions of the additive and multiplicative identity reducers. I also automated the testing of these functions with a generic test function which is passed the folder name housing the tests, and the reducer function which is being tested. I attempted to make the test cases thorough, however I noticed that negative numbers cannot work with this implementation due to the use of the isnumeric() Python function. It's worth noting that my program also does not work when empty prefix lists are passed in for input.

## Briefly discuss one thing you learned by completing this assignment that you believe will be valuable to you in your future courses / programming experiences.

The actual programming of the AST was fun and good programming experience, however I think the practice with using the Python testing framework was the most beneficial aspect of this assignment for me. I had never set up any sort of automated testing like that, and it was great to know that Python has a canonical and easy library for such use. I'm very happy I got hands on experience and learned the basics of more formal testing. I think it will really come in handy in other programming efforts, and I will definitely implement it in larger projects.

If I devoted more time to it, I would try to make the testing even more robust, such as changing the use of assert for input and output comparisons as it crashes the program and prevents subsequent test cases from running.

The refresher in object-oriented programming in Python was not bad either.

## Briefly discuss either one aspect of this assignment you did not enjoy or one particular difficult bug you encountered.

I spent an hour trying to find out why it wasn't pruning out the additive identity cases after implementing what I thought was sound logic. Went through it step by step, triple checked to see if the tree was being built correctly. If the recursion, traversal and base case were right. All the while the simple bug causing it all was that I was trying to compare the node value (which is a string) to the literal value 0 (which is an integer)

        if self.right.val == 0:

when it should have been

        if self.right.val == '0':

This is a lesson in the pitfalls that come with a weakly typed language such as Python (and an irritating reminder of how much I sometimes hate its quirks ... I mean "features") and that the onus is on the programmer; the compiler will not catch simple programming errors for you like it would in strongly typed languages. Instead, it will let you compare differing types, create non-existent variables out of thin air, assign anything to anything and force you to always pass by reference (kind of?) ... all in the name of simplicity and readability! Yay.