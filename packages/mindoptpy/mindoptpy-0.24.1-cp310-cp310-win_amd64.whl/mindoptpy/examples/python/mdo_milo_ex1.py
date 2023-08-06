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
 *  Integers
 *    x0 x1 x2
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
        
        # Add variables.
        x = []
        x.append(model.add_var(0.0,         10.0, 1.0, None, "x0", True))
        x.append(model.add_var(0.0, MDO_INFINITY, 1.0, None, "x1", True))
        x.append(model.add_var(0.0, MDO_INFINITY, 1.0, None, "x2", True))
        x.append(model.add_var(0.0, MDO_INFINITY, 1.0, None, "x3", False))

        # Add constraints.
        # Note that the nonzero elements are inputted in a row-wise order here.
        model.add_cons(1.0, MDO_INFINITY, 1.0 * x[0] + 1.0 * x[1] + 2.0 * x[2] + 3.0 * x[3], "c0")
        model.add_cons(1.0,          1.0, 1.0 * x[0]              - 1.0 * x[2] + 6.0 * x[3], "c1")

        # Step 3. Solve the problem and populate the result.
        model.solve_prob()
        model.display_results()

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
