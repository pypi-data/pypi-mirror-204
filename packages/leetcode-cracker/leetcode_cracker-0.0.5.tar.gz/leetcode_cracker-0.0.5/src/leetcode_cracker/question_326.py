def print_question():
    print("""
Given an integer n, return true if it is a power of three. Otherwise, return false.

An integer n is a power of three, if there exists an integer x such that n == 3x.
""")
def print_solution():

    print("""
class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        if n == 0:
            return False
        while n > 1:
            n = n/3
        if n == 1:
            return True
        else:
            return False
    """)
def solution_stats():
    print("""
        Time: Beats 75.31%
        Memory: Beats 92.35%
    """)
    

  
