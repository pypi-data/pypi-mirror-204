"""
/**
 *  Description
 *  -----------
 *
 *  Semidefinite optimization (row-wise input).
 *
 *  Formulation
 *  -----------
 *
 *  Maximize
 *  obj: tr(C X)
 *
 *  Subject To
 *    c0 : tr(A X) = 1
 *  Matrix
 *    C = [ -3  0  1 ]  A = [ 3 0 1 ]
 *        [  0 -2  0 ]      [ 0 4 0 ]
 *        [  1  0 -3 ]      [ 1 0 5 ]
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
        # Change to maximization problem.
        model.set_int_attr(MDO_INT_ATTR.MIN_SENSE, 0)
        
        # Add matrix variable. 
        model.add_sym_mat(3, "X")

        # Input objective coefficients. 
        model.replace_sym_mat_objs(0, [ 0, 0, 1, 2 ], [ 0, 2, 1, 2], [ -3.0, 1.0, -2.0, -3.0])

        # Input first constraint. 
        model.add_cons(1.0, 1.0, name="c0")
        model.replace_sym_mat_elements(0, 0, [ 0, 2, 1, 2 ], [ 0, 0, 1, 2 ], [ 3.0, 1.0, 4.0, 5.0 ])
       
        # Step 3. Solve the problem and populate the result.
        model.solve_prob()
        model.display_results()

        status_code, status_msg = model.get_status()
        if status_msg == "OPTIMAL":
            print("Optimizer terminated with an OPTIMAL status (code {0}).".format(status_code))
            print(" - Primal objective : {:8.6f}".format(model.get_real_attr(MDO_REAL_ATTR.PRIMAL_OBJ_VAL)))
            
            soln = model.get_real_attr_sym_mat(MDO_REAL_ATTR.SYM_MAT_PRIMAL_SOLN, 0, 
                [i * 3 + j for i in range(3) for j in range(3)], 
                [j * 3 + i for i in range(3) for j in range(3)])           
            print("X = ")
            for i in range(3):
                print(" (", end="") 
                for j in range(3):
                    print(" {0:8.6f}".format(soln[i * 3 + j]), end=""), 
                print(" )") 

        else:
            print("Optimizer terminated with a(n) {0} status (code {1}).".format(status_msg, status_code))

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
