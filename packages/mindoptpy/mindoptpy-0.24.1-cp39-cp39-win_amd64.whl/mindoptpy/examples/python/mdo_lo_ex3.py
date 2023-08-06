"""
/**
 *  Description
 *  -----------
 *
 *  Linear optimization (row-wise input).
 *
 *  Formulation
 *  -----------
 *
 *  Minimize
 *    obj: 1 x0 + 1 x1 + 1 x2 + 1 x3
 *  Subject To
 *   c1 : 1 x0 + 1 x1 + 2 x2 + 3 x3 >= 1
 *   c2 : 1 x0 - 1 x2 + 6 x3 = 1
 *  Bounds
 *    0 <= x0 <= 10
 *    0 <= x1
 *    0 <= x2
 *    0 <= x3
 *  End
 */
"""
from mindoptpy import *


if __name__ == "__main__":

    MDO_INFINITY = MdoModel.get_infinity()
    WRITE_LP = True

    # Step 1. Create a model and change the parameters.
    model = MdoModel()

    try:
        # Step 2. Input model.
        print("\nStep 2. Input model.\n")        
        # Change to minimization problem.
        model.set_int_attr(MDO_INT_ATTR.MIN_SENSE, 1)
        
        # Add variables.
        xs = model.add_vars(4, lb=0, ub=MDO_INFINITY, obj=1.0, name="x")
        x = [ value for key, value in xs.items() ]
        x[0].set_real_attr(MDO_REAL_ATTR.UB, 10.0)

        # Add constraints.
        # Note that the nonzero elements are inputted in a row-wise order here.
        conss = []
        conss.append(model.add_cons(1.0 * x[0] + 1.0 * x[1] + 2.0 * x[2] + 3.0 * x[3] >= 1.0, "c0"))
        conss.append(model.add_cons(1.0 * x[0]              - 1.0 * x[2] + 6.0 * x[3] == 1.0, "c1"))

        # Step 3. Solve the problem and populate the result.
        print("\nStep 3. Solve the problem and populate the result.\n")        
        model.solve_prob()
        model.display_results()
        if WRITE_LP:
            model.write_prob("Step3.lp");

        # Step 4. Add another two variables and then resolve the problem. 
        print("\nStep 4. Add another two variables and then resolve the problem.\n")        
        # Input columns. 
        cols = [ MdoCol() for i in range(2) ]
        cols[0].add_terms(conss, [ 1.0, 2.0 ])
        cols[1].add_terms(conss, [ 3.4, 4.0 ])
        y = []
        y.append(model.add_var( 0.0, MDO_INFINITY,  1.0, cols[0], "y0", False))
        y.append(model.add_var(-2.0, MDO_INFINITY, -1.0, cols[1], "y1", False))

        # Solve the problem. 
        model.solve_prob()
        model.display_results()
        if WRITE_LP:
            model.write_prob("Step4.lp");

        # Step 5. Add another two constraints and then resolve the problem.     
        print("\nStep 5. Add another two constraints and then resolve the problem.\n")
        bgn2 = [ 0, 3, 6 ]
        indices2 = [
            0,   1,        3,
            0,        2,   3  
        ]
        values2 = [
            1.0, 1.0,      -2.0,
            1.0,      -2.0, 6.0
        ]    

        lhss2 = [ 0, 1            ]
        rhss2 = [ 2, MDO_INFINITY ]

        expr = [ MdoExprLinear() for i in range(2) ]
        for i in range(2):
            for e in range(bgn2[i], bgn2[i + 1]):
                expr[i] += values2[e] * x[indices2[e]]
                
        c2 = model.add_conss( [ expr[i] == [lhss2[i], rhss2[i]] for i in range(2) ] )
        for key, value in c2.items():
            conss.append(value)

        # Solve the problem. 
        model.solve_prob()
        model.display_results()
        if WRITE_LP:
            model.write_prob("Step5.lp");

        # Step 6. Obtain optimal basis.     
        print("\nStep 6. Obtain optimal basis.\n")
        
        # isFree = 0,
        # basic = 1,
        # atUpperBound = 2,
        # atLowerBound = 3,
        # superBasic = 4,
        # isFixed = 5,
        col_basis = []
        row_basis = []
        for var in x:
            print("Basis status of variable {0} is {1}".format(var.get_index(), var.get_int_attr(MDO_INT_ATTR.COL_BASIS)))
            col_basis.append(var.get_int_attr(MDO_INT_ATTR.COL_BASIS))
        for var in y:
            print("Basis status of variable {0} is {1}".format(var.get_index(), var.get_int_attr(MDO_INT_ATTR.COL_BASIS)))
            col_basis.append(var.get_int_attr(MDO_INT_ATTR.COL_BASIS))
        for cons in conss:
            print("Basis status of constraint {0} is {1}".format(cons.get_index(), cons.get_int_attr(MDO_INT_ATTR.ROW_BASIS)))
            row_basis.append(cons.get_int_attr(MDO_INT_ATTR.ROW_BASIS))

        if WRITE_LP:
            model.write_prob("Step6.lp");
            model.write_soln("Step6.bas");

        # Step 7. Warm-start Simplex.    
        print("\nStep 7. Warm-start Simplex.\n")

        # Change the objective coefficients. 
        x[1].set_real_attr("Obj", 3.0);
        x[2].set_real_attr("Obj", -3.0);

        # Load the basis. 
        model.set_int_attr_array(MDO_INT_ATTR.ROW_BASIS, 0, row_basis);
        model.set_int_attr_array(MDO_INT_ATTR.COL_BASIS, 0, col_basis);

        # Solve the problem. 
        model.solve_prob()
        model.display_results()
        if WRITE_LP:
            model.write_prob("Step7.lp");

        # Step 8. Model query.     
        print("\nStep 8. Model query.\n")

        # Query 1: Retrieve first constraint. 
        print("Query 1: Retrieve first constraint.")
        
        temp_expr = model.get_expr_linear(conss[0])
        print(temp_expr)
        
        # Query 2: Retrieve second column. 
        print("Query 2: Retrieve second column.")
        
        temp_col = model.get_col(x[1]);
        print(temp_col)

    except MdoError as e:
        print("Received Mindopt exception.")
        print(" - Code          : {}".format(e.code))
        print(" - Reason        : {}".format(e.message))
    except Exception as e:
        print("Received exception.")
        print(" - Reason        : {}".format(e))
    finally:
        # Step 4. Free the model.
        model.free_mdl()
