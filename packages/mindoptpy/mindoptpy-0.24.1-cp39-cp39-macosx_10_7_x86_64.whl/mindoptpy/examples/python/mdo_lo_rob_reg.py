import random
import time
import math

from mindoptpy import *

if __name__ == "__main__":
    random.seed(1)

    # randomly generate vector a and scalar b
    d = 4
    true_a = [random.gauss(0, 1) * math.sqrt(d) for i in range(d)]
    true_b = random.gauss(0, 1)
    print(true_a)

    # randomly generate observations (x[i],y[i]), i = 1,...,m with 10% outliers
    m = 15
    X = [[random.gauss(0, 1) for j in range(d)] for i in range(m)]
    y = [0 for i in range(m)]
    for i in range(m):
        if i < math.floor(0.9*m):
            y[i] = sum([x_i * y_i for x_i, y_i in zip(true_a, X[i])]) + true_b
        else:
            y[i] = random.gauss(0,1)

    # MindOpt Steps
    try:
        # MindOpt Step 1. Initialize an optimization model
        model = MdoModel()
        
        # MindOpt Step 2. Set model inputs.
               
        # Add variables, specify their low bounds, uppder bounds, and minimization coefficients
        # minimize_{a,b,c} 0'a + 0b + 1'c
        INF = MdoModel.get_infinity()
    
        var_a = model.add_vars(d, lb=-INF, ub=INF, name="a")         
        var_b = model.add_var(lb=-INF, ub=INF, name="b")   
        var_c = model.add_vars(m, lb=-INF, ub=INF, name="c")

        # add: y[i] <= a'x[i,] + b + c[i]
        model.add_conss((var_b + quicksum(X[i][j]*var_a[j] for j in range(d)) + var_c[i] >= y[i] for i in range(m)), name="cons_ge")

        # add: a'x[i,] + b - c[i] <= y[i]
        model.add_conss((var_b + quicksum(X[i][j]*var_a[j] for j in range(d)) - var_c[i] <= y[i] for i in range(m)), name="cons_le")

        # objective.
        model.set_objs(quicksum(var_c[i] for i in range(m)))
        model.set_min_obj_sense()

        # MindOpt Step 3. Solve the problem and populate the result.
        # model.write_prob("python_test.lp") # Optional: output the model for futher inspection.
        model.solve_prob()

        # MindOpt Step 4. Display results and compare var_a to true_a, var_b to true_b
        model.display_results()
    
        status_code, status_msg = model.get_status()
        if status_msg == "OPTIMAL":
            print("Optimizer terminated with an OPTIMAL status (code {0}).".format(status_code))
        else:
            print("Optimizer terminated with status {0} (code {1}).".format(status_msg, status_code))
        
        # Display solutions a[0],...,a[d-1]
        print('\n{0:<5}   {1:>9}   {2:>9}'.format('Entry','True','Soln'))
        for j in range(d):
            print('{0:>5}   {1:>9f}   {2:>9f}'.format('a['+'%s'%j+']', true_a[j], var_a[j].get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN)))
        
        # Display solution b
        print('\n{0:<5}   {1:>9}   {2:>9}'.format('    ','True','Soln'))
        print('{0:>5}   {1:>9f}   {2:>9f}'.format('b', true_b, var_b.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN)))

        # Display solutions c[0],...,c[m]
        print('\n{0:>11}  {1:>9}'.format('Observation','Residual'))
        for i in range(m):
            print('{0:>11d}  {1:>9f}'.format(i, var_c[i].get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN)))
        
    except MdoError as e:
        print("Received Mindopt exception.")
        print(" - Code          : {}".format(e.code))
        print(" - Reason        : {}".format(e.message))
    except Exception as e:
        print("Received exception.")
        print(" - Reason        : {}".format(e))
    finally:
        # MindOpt Step 5. Free the model.
        model.free_mdl()

