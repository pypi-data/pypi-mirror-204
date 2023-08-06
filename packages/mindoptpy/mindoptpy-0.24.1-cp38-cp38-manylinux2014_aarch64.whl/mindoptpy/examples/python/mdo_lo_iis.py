"""
/**
 *  Description
 *  -----------
 *
 *  Linear optimization.
 *   - Compute IIS of an infeasible problem.
 * 
 *  Formulation
 *  -----------
 *
 *  Minimize
 *  Obj:
 *  Subject To
 *  c0:  -0.500000000 x0 + x1 >= 0.500000000
 *  c1:  2 x0 - x1 >= 3
 *  c2:  3 x0 + x1 <= 6
 *  c3:  3 x3 - x4 <= 2 <- conflicts with variable bounds listed below!
 *  c4:  x0 + x4 <= 10
 *  c5:  x0 + 2 x1 + x3 <= 14
 *  c6:  x1 + x3 >= 1
 *  Bounds
 *   5 <= x3
 *   0 <= x4 <= 2
 *  End
 */
"""
from mindoptpy import *


if __name__ == "__main__":

    MDO_INFINITY = MdoModel.get_infinity()

    # Step 1. Create a model and change the parameters.
    model = MdoModel()
    # Turn-off the presolver so that solver won't terminate with an MDO_INF_OR_UBD status.
    model.set_int_param(MDO_INT_PARAM.PRESOLVE, 0)
    model.set_int_param(MDO_INT_PARAM.METHOD, 1)

    try:
        # Step 2. Input model.
        # Change to minimization problem.
        model.set_int_attr(MDO_INT_ATTR.MIN_SENSE, 1)

        # Add variables.
        # Note that the nonzero elements are inputted in a column-wise order here.
        x = []
        x.append(model.add_var(0.0, MDO_INFINITY, 0.0, None, "x0", False))
        x.append(model.add_var(0.0, MDO_INFINITY, 0.0, None, "x1", False))
        x.append(model.add_var(0.0, MDO_INFINITY, 0.0, None, "x2", False))
        x.append(model.add_var(5.0, MDO_INFINITY, 0.0, None, "x3", False))
        x.append(model.add_var(0.0,          2.0, 0.0, None, "x4", False))

        # Add constraints.
        # Note that the nonzero elements are inputted in a row-wise order here.
        conss = []
        conss.append(model.add_cons(-0.5 * x[0]       + x[1]                     >= 0.5,  "c0"))
        conss.append(model.add_cons( 2.0 * x[0]       - x[1]                     >= 3.0,  "c1"))
        conss.append(model.add_cons( 3.0 * x[0]       + x[1]                     <= 6.0,  "c2"))
        conss.append(model.add_cons(                          3.0 * x[3] - x[4]  <= 2.0,  "c3"))
        conss.append(model.add_cons(       x[0]                          + x[4]  <= 10.0, "c4"))
        conss.append(model.add_cons(       x[0] + 2.0 * x[1]      + x[3]         <= 14.0, "c5"))
        conss.append(model.add_cons(       x[1] +                   x[3]         >= 1.0,  "c6"))        

        # Step 3. Solve the problem and populate the result.
        model.solve_prob()
        model.display_results()

        status_code, status_msg = model.get_status()
        if status_msg == "INFEASIBLE":
            print("Optimizer terminated with an MDO_INFEASIBLE status (code {0}).".format(status_code))
            print("Compute IIS.")
            idx_rows, idx_cols = model.compute_iis()

            print("Computed IIS has {0} rows and {1} columns.".format(len(idx_rows), len(idx_cols)))
            print("Populating IIS.")
            for i in idx_rows:
                print("Constraint: {0}".format(conss[i].get_str_attr("RowName")))
            for j in idx_cols:
                print("Variable: {0}".format(x[j].get_str_attr("ColName")))
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
