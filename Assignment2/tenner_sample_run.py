from tenner_csp import *
from propagators import *
import ast, sys

b1 = ([[-1, 0, 1,-1, 9,-1,-1, 5,-1, 2],
       [-1, 7,-1,-1,-1, 6, 1,-1,-1,-1],
       [-1,-1,-1, 8,-1,-1,-1,-1,-1, 9],
       [ 6,-1, 4,-1,-1,-1,-1, 7,-1,-1],
       [-1, 1,-1, 3,-1,-1, 5, 8, 2,-1]],
      [29,16,18,21,24,24,21,28,17,27])

b2 = ([[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
       [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
       [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
       [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
       [6, -1, -1, 5, -1, 0, -1, -1, -1, -1],],
      [21, 26, 21, 21, 29, 10, 28, 26, 21, 22])

def print_tenner_soln(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])

if __name__ == "__main__":

    for b in [b1, b2]:
        print("Solving board:")
        for row in b[0]:
            print(row)

        print("Using Model 1")
        csp, var_array = tenner_csp_model_1(b)
        solver = BT(csp)
        print("=======================================================")
        print("FC")
        solver.bt_search(prop_FC)
        print("Solution")
        print_tenner_soln(var_array)
        
        print("Using Model 2")
        csp, var_array = tenner_csp_model_2(b)
        solver = BT(csp)
        print("=======================================================")
        print("GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_tenner_soln(var_array)

