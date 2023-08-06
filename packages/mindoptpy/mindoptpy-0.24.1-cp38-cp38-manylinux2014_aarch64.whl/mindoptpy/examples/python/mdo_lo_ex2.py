"""
/**
 *  Description
 *  -----------
 *
 *  Linear optimization (column-wise input).
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

    # Step 1. Create a model and change the parameters.
    model = MdoModel()

    try:
        # Step 2. Input model.
        # Change to minimization problem.
        model.set_int_attr(MDO_INT_ATTR.MIN_SENSE, 1)

        # Add empty constraints. 
        cons = []
        cons.append(model.add_cons(1.0, MDO_INFINITY, None, "c0"))
        cons.append(model.add_cons(1.0, 1.0,          None, "c1"))
        
        # Input columns. 
        col = []
        for j in range(4):
            col.append(MdoCol())
        col[0].add_term(cons[0], 1.0)
        col[0].add_term(cons[1], 1.0)
        col[1].add_term(cons[0], 1.0)
        col[2].add_term(cons[0], 2.0)
        col[2].add_term(cons[1], -1.0)
        col[3].add_term(cons[0], 3.0)
        col[3].add_term(cons[1], 6.0)

        # Add variables.
        # Note that the nonzero elements are inputted in a column-wise order here.
        x = []
        x.append(model.add_var(0.0,         10.0, 1.0, col[0], "x0", False))
        x.append(model.add_var(0.0, MDO_INFINITY, 1.0, col[1], "x1", False))
        x.append(model.add_var(0.0, MDO_INFINITY, 1.0, col[2], "x2", False))
        x.append(model.add_var(0.0, MDO_INFINITY, 1.0, col[3], "x3", False))

        # Step 3. Solve the problem and populate the result.
        model.solve_prob()
        model.display_results()

        status_code, status_msg = model.get_status()
        if status_msg == "OPTIMAL":
            print("Optimizer terminated with an OPTIMAL status (code {0}).".format(status_code))
            print("Primal objective : {0}".format(round(model.get_real_attr(MDO_REAL_ATTR.PRIMAL_OBJ_VAL), 2)))
            for curr_x in x:
                print(" - x[{0}]          : {1}".format(curr_x.get_index(), round(curr_x.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
        else:
            print("Optimizer terminated with a(n) {0} status (code {1}).".format(status_msg, status_code))

    except MdoError as e:
        print("Received Mindopt exception.")
        print(" - Code          : {}".format(e.code))
        print(" - Reason        : {}".format(e.message))
    except Exception as e:
        print("Received exception.")
        print(" - Explanation   : {}".format(e))
    finally:
        # Step 4. Free the model.
        model.free_mdl()
