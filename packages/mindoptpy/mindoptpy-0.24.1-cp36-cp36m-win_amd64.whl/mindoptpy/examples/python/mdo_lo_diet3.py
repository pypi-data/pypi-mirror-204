"""
/**
 *  Description
 *  -----------
 *
 *  Linear optimization (diet problem).
 *
 *  The goal is to select foods that satisfy daily nutritional requirements while minimizing the total cost. 
 *  The constraints in this problem limit the number of calories, the volume of good consumed, and the amount of 
 *  vitamins, protein, carbohydrates, calcium, and iron in the diet.
 *
 *  Note
 *  ----
 * 
 *  The model below will be inputted via linear expression.
 * 
 *  Formulation
 *  -----------
 *
 * Minimize
 * Obj:        1.840000000 Cheeseburger + 2.190000000 HamSandwich + 1.840000000 Hamburger + 1.440000000 FishSandwich +
 *             2.290000000 ChickenSandwich + 0.770000000 Fries + 1.290000000 SausageBiscuit + 0.600000000 LowfatMilk + 
 *             0.720000000 OrangeJuice
 * Subject To
 * Cal:        510 Cheeseburger + 370 HamSandwich + 500 Hamburger + 370 FishSandwich +
 *             400 ChickenSandwich + 220 Fries + 345 SausageBiscuit + 110 LowfatMilk + 80 OrangeJuice >= 2000
 * Carbo:      34 Cheeseburger + 35 HamSandwich + 42 Hamburger + 38 FishSandwich + 42 ChickenSandwich + 
 *             26 Fries + 27 SausageBiscuit + 12 LowfatMilk + 20 OrangeJuice <= 375
 * Carbo_low:  34 Cheeseburger + 35 HamSandwich + 42 Hamburger + 38 FishSandwich + 42 ChickenSandwich + 
 *             26 Fries + 27 SausageBiscuit + 12 LowfatMilk + 20 OrangeJuice >= 350
 * Protein:    28 Cheeseburger + 24 HamSandwich + 25 Hamburger + 14 FishSandwich + 31 ChickenSandwich + 
 *             3 Fries + 15 SausageBiscuit + 9 LowfatMilk + OrangeJuice >= 55
 * VitA:       15 Cheeseburger + 15 HamSandwich + 6 Hamburger + 2 FishSandwich + 8 ChickenSandwich + 
 *             4 SausageBiscuit + 10 LowfatMilk + 2 OrangeJuice >= 100
 * VitC:       6 Cheeseburger + 10 HamSandwich + 2 Hamburger + 15 ChickenSandwich + 
 *             15 Fries + 4 LowfatMilk + 120 OrangeJuice >= 100
 * Calc:       30 Cheeseburger + 20 HamSandwich + 25 Hamburger + 15 FishSandwich + 
 *             15 ChickenSandwich + 20 SausageBiscuit + 30 LowfatMilk + 2 OrangeJuice >= 100
 * Iron:       20 Cheeseburger + 20 HamSandwich + 20 Hamburger + 10 FishSandwich + 
 *             8 ChickenSandwich + 2 Fries + 15 SausageBiscuit + 2 OrangeJuice >= 100
 * Volume:     4 Cheeseburger + 7.500000000 HamSandwich + 3.500000000 Hamburger + 5 FishSandwich + 
 *             7.300000000 ChickenSandwich + 2.600000000 Fries + 4.100000000 SausageBiscuit + 8 LowfatMilk + 12 OrangeJuice <= 75
 * Bounds
 * End
 */
"""
from mindoptpy import *


if __name__ == "__main__":

    MDO_INFINITY = MdoModel.get_infinity()

    try:
        # Step 1. Create a model and change the parameters.
        model = MdoModel()

        # Step 2. Input model.
        # Change to minimization problem.
        model.set_int_attr(MDO_INT_ATTR.MIN_SENSE, 1)
        
        # Add variables.
        Cheeseburger    = model.add_var(0, MDO_INFINITY, 1.84, None, "Cheeseburger",    False);
        HamSandwich     = model.add_var(0, MDO_INFINITY, 2.19, None, "HamSandwich",     False);
        Hamburger       = model.add_var(0, MDO_INFINITY, 1.84, None, "Hamburger",       False);
        FishSandwich    = model.add_var(0, MDO_INFINITY, 1.44, None, "FishSandwich",    False);
        ChickenSandwich = model.add_var(0, MDO_INFINITY, 2.29, None, "ChickenSandwich", False);
        Fries           = model.add_var(0, MDO_INFINITY, 0.77, None, "Fries",           False);
        SausageBiscuit  = model.add_var(0, MDO_INFINITY, 1.29, None, "SausageBiscuit",  False);
        LowfatMilk      = model.add_var(0, MDO_INFINITY, 0.60, None, "LowfatMilk",      False);
        OrangeJuice     = model.add_var(0, MDO_INFINITY, 0.72, None, "OrangeJuice",     False);

        # Add constraints.
        model.add_cons(200, MDO_INFINITY, 
            510 * Cheeseburger + 370 * HamSandwich + 500 * Hamburger + 370 * FishSandwich + 
            400 * ChickenSandwich + 220 * Fries + 345 * SausageBiscuit + 110 * LowfatMilk + 
            80 * OrangeJuice, 
            "Cal");
        model.add_cons(350, 375, 
            34 * Cheeseburger + 35 * HamSandwich + 42 * Hamburger + 38 * FishSandwich + 
            42 * ChickenSandwich + 26 * Fries + 27 * SausageBiscuit + 12 * LowfatMilk +
            20 * OrangeJuice, 
            "Carbo"); 
        model.add_cons(55, MDO_INFINITY, 
            28 * Cheeseburger + 24 * HamSandwich + 25 * Hamburger + 14 * FishSandwich + 
            31 * ChickenSandwich + 3 * Fries + 15 * SausageBiscuit + 9 * LowfatMilk + 
            OrangeJuice, 
            "Protein");
        model.add_cons(100, MDO_INFINITY, 
            15 * Cheeseburger + 15 * HamSandwich + 6 * Hamburger + 2 * FishSandwich + 
            8 * ChickenSandwich + 4 * SausageBiscuit + 10 * LowfatMilk + 2 * OrangeJuice, 
            "VitA");
        model.add_cons(100, MDO_INFINITY, 
            6 * Cheeseburger + 10 * HamSandwich + 2 * Hamburger + 15 * ChickenSandwich + 
            15 * Fries + 4 * LowfatMilk + 120 * OrangeJuice, "VitC");
        model.add_cons(100, MDO_INFINITY,
            30 * Cheeseburger + 20 * HamSandwich + 25 * Hamburger + 15 * FishSandwich + 
            15 * ChickenSandwich + 20 * SausageBiscuit + 30 * LowfatMilk + 2 * OrangeJuice,
            "Calc");
        model.add_cons(100, MDO_INFINITY, 
            20 * Cheeseburger + 20 * HamSandwich + 20 * Hamburger + 10 * FishSandwich + 
            8 * ChickenSandwich + 2 * Fries + 15 * SausageBiscuit + 2 * OrangeJuice, 
            "Iron");
        model.add_cons(-MDO_INFINITY, 75,
             4 * Cheeseburger + 7.5 * HamSandwich + 3.5 * Hamburger + 5 * FishSandwich + 
            7.3 * ChickenSandwich + 2.6 * Fries + 4.1 * SausageBiscuit + 8 *  LowfatMilk + 
            12 * OrangeJuice , 
            "Volume");

        # Step 3. Solve the problem and populate the result.
        model.solve_prob()
        model.display_results()
        
        status_code, status_msg = model.get_status()
        if status_msg == "OPTIMAL":
            print("Optimizer terminated with an OPTIMAL status (code {0}).".format(status_code))
            print("Daily cost          : ${0}".format(round(model.get_real_attr(MDO_REAL_ATTR.PRIMAL_OBJ_VAL), 2)))
            print(" - Cheeseburger     : {0}".format(round(Cheeseburger.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
            print(" - Hamburger        : {0}".format(round(Hamburger.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
            print(" - FishSandwich     : {0}".format(round(FishSandwich.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
            print(" - ChickenSandwich  : {0}".format(round(ChickenSandwich.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
            print(" - Fries            : {0}".format(round(Fries.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
            print(" - SausageBiscuit   : {0}".format(round(SausageBiscuit.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
            print(" - LowfatMilk       : {0}".format(round(LowfatMilk.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
            print(" - OrangeJuice      : {0}".format(round(OrangeJuice.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)))
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
        pass
