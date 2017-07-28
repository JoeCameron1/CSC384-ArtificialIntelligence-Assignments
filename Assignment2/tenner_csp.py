#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''
from cspbase import *
import itertools

#######################################################################
# MY HELPER FUNCTIONS
#######################################################################

# My helper function for initial set-up in both tenner csp models 1 & 2.
def set_up(constraints, rows, board, initial_tenner_board):
    for a in range(rows):
        for b in range(10): 
            square = initial_tenner_board[0][a][b]
            if square == -1: 
                board[a][b] = Variable("V[{}][{}]".format(a,b), list(range(10)))
            else: 
                board[a][b] = Variable("V[{}][{}]".format(a,b), [square])


# My helper function for adding constraints to columns in both tenner csp models 1 & 2.
def constraint_Column(constraints, rows, board, initial_tenner_board):
    for column in range(10): 
        column_variables = [] 
        for row in range (rows):
            column_variables.append(board[row][column])
        column_constraint = Constraint("Column{}".format(column), column_variables)
        satisfied = []
        domains = [variable.domain() for variable in column_variables]
        for domain_tuple in itertools.product(*domains):
            if sum(domain_tuple) == initial_tenner_board[1][column]:
                satisfied.append(domain_tuple)
        column_constraint.add_satisfying_tuples(satisfied)
        constraints.append(column_constraint)

# My helper function for adding constraints to rows in tenner csp model 2 only.
def constraint_Row(constraints, rows, board, initial_tenner_board):
    for row in range(rows):
        row_variables = []
        for column in range(10):
            row_variables.append(board[row][column])
        row_constraint = Constraint("Row{}".format(row), row_variables)
        satisfied = []
        domains = [variable.domain() for variable in row_variables] 
        for domain_tuple in itertools.product(*domains): 
            if sum(domain_tuple) == 45:
                counts = dict()
                for a in domain_tuple:
                    if counts.get(a, 0) > 0:
                        break
                    counts[a] = counts.get(a, 0) + 1
                else:
                    satisfied.append(domain_tuple)
        row_constraint.add_satisfying_tuples(satisfied)
        constraints.append(row_constraint)


# My helper function to make board constraints for both tenner csp models 1 & 2.
def make_Constraints(constraints, rows, board, a, b, process):
    for (x,y) in process:
        row = a + x
        column = b + y
        if (row >= 0 and row <= rows) and (column >= 0 and column <= 9):
            variable1 = board[row][column]
            variable2 = board[a][b]
            current_constraint = Constraint("C(A[{}][{}])(A[{}][{}]".format(row, column, a, b), [variable1, variable2])
            satisfied = []
            for domain_tuple in itertools.product(variable1.domain(), variable2.domain()):
                if domain_tuple[0] != domain_tuple[1]:
                    satisfied.append(domain_tuple)
            current_constraint.add_satisfying_tuples(satisfied)
            constraints.append(current_constraint)
    

#######################################################################

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return
       tenner_csp, variable_array
       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists
       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]
       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 8.
       The input board is specified as a pair (n_grid, last_row).
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid.
       If a -1 is in the list it represents an empty cell.
       Otherwise if a number between 0--9 is in the list then this represents a
       pre-set board position. E.g., the board
       ---------------------
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constraints n-nary constraints of sum constraints for each
       column.
    '''
    
    rows = len(initial_tenner_board[0])
    board = [[0 for x in range(10)] for y in range(rows)]
    constraints = []

    set_up(constraints, rows, board, initial_tenner_board)
                
    for row in range(rows):
        for column in range(10):
            process = [(0,-1),(-1,-1),(-1,0),(-1,1)] 
            duplicate = column
            while duplicate > 1:
                process.append((0,-duplicate))
                duplicate = duplicate - 1
            make_Constraints(constraints, rows, board, row, column, process)

    constraint_Column(constraints, rows, board, initial_tenner_board)
        
    variables = []
    for row in board:
        for variable in row:
            variables.append(variable)
            
    tenner_csp_model_1 = CSP("tenner_csp_model_1", variables) # CSP Model.
    
    for constraint in constraints:
        tenner_csp_model_1.add_constraint(constraint)
        
    return tenner_csp_model_1, board


def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along
       with an array of variables for the problem. That is return
       tenner_csp, variable_array
       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists
       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]
       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from
       (0,0) to (n,9)) where n can be 3 to 8.
       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.
       However, model_2 has different constraints. In particular,
       model_2 has a combination of n-nary
       all-different constraints and binary not-equal constraints: all-different
       constraints for the variables in each row, binary constraints for
       contiguous cells (including diagonally contiguous cells), and n-nary sum
       constraints for each column.
       Each n-ary all-different constraint has more than two variables (some of
       these variables will have a single value in their domain).
       model_2 should create these all-different constraints between the relevant
       variables.
    '''
    
    rows = len(initial_tenner_board[0])
    board = [[0 for x in range(10)] for y in range(rows)]
    constraints = []
    
    set_up(constraints, rows, board, initial_tenner_board)
                
    for row in range(rows):
        for column in range(10):
            process = [(-1,-1),(-1,0),(-1,1)]
            make_Constraints(constraints, rows, board, row, column, process)

    constraint_Row(constraints, rows, board, initial_tenner_board)
        
    constraint_Column(constraints, rows, board, initial_tenner_board)
        
    variables = [] 
    for row in board:
        for variable in row:
            variables.append(variable)
            
    tenner_csp_model_2 = CSP("tenner_csp_model_2", variables) # CSP Model.
    
    for constraint in constraints:
        tenner_csp_model_2.add_constraint(constraint)
        
    return tenner_csp_model_2, board
