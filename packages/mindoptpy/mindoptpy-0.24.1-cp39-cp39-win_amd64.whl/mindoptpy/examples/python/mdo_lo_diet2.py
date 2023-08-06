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
 *  The model below will be inputted in a column-wise order.
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

    req = \
    {   
        # requirement: ( lower bound,   upper bound)
        "Cal"        : (         2000, MDO_INFINITY), 
        "Carbo"      : (          350,          375),
        "Protein"    : (           55, MDO_INFINITY), 
        "VitA"       : (          100, MDO_INFINITY),
        "VitC"       : (          100, MDO_INFINITY),
        "Calc"       : (          100, MDO_INFINITY), 
        "Iron"       : (          100, MDO_INFINITY), 
        "Volume"     : (-MDO_INFINITY,           75)
    }

    food = \
    {
        # food            : ( lower bound,  upper bound, cost)
        "Cheeseburger"    : (           0, MDO_INFINITY, 1.84),
        "HamSandwich"     : (           0, MDO_INFINITY, 2.19),
        "Hamburger"       : (           0, MDO_INFINITY, 1.84),
        "FishSandwich"    : (           0, MDO_INFINITY, 1.44),
        "ChickenSandwich" : (           0, MDO_INFINITY, 2.29),
        "Fries"           : (           0, MDO_INFINITY, 0.77),
        "SausageBiscuit"  : (           0, MDO_INFINITY, 1.29),
        "LowfatMilk"      : (           0, MDO_INFINITY, 0.60),
        "OrangeJuice"     : (           0, MDO_INFINITY, 0.72)
    }
    
    req_value = \
    {  
        # (requirement, food              ) : value
        ( "Cal",        "Cheeseburger"    ) : 510,
        ( "Cal",        "HamSandwich"     ) : 370,
        ( "Cal",        "Hamburger"       ) : 500,
        ( "Cal",        "FishSandwich"    ) : 370,
        ( "Cal",        "ChickenSandwich" ) : 400,
        ( "Cal",        "Fries"           ) : 220,
        ( "Cal",        "SausageBiscuit"  ) : 345,
        ( "Cal",        "LowfatMilk"      ) : 110,
        ( "Cal",        "OrangeJuice"     ) : 80,

        ( "Carbo",      "Cheeseburger"    ) : 34,
        ( "Carbo",      "HamSandwich"     ) : 35,
        ( "Carbo",      "Hamburger"       ) : 42,
        ( "Carbo",      "FishSandwich"    ) : 38,
        ( "Carbo",      "ChickenSandwich" ) : 42,
        ( "Carbo",      "Fries"           ) : 26,
        ( "Carbo",      "SausageBiscuit"  ) : 27,
        ( "Carbo",      "LowfatMilk"      ) : 12,
        ( "Carbo",      "OrangeJuice"     ) : 20,

        ( "Protein",    "Cheeseburger"    ) : 28,
        ( "Protein",    "HamSandwich"     ) : 24,
        ( "Protein",    "Hamburger"       ) : 25,
        ( "Protein",    "FishSandwich"    ) : 14,
        ( "Protein",    "ChickenSandwich" ) : 31,
        ( "Protein",    "Fries"           ) : 3,
        ( "Protein",    "SausageBiscuit"  ) : 15,
        ( "Protein",    "LowfatMilk"      ) : 9,
        ( "Protein",    "OrangeJuice"     ) : 1,

        ( "VitA",       "Cheeseburger"    ) : 15,
        ( "VitA",       "HamSandwich"     ) : 15,
        ( "VitA",       "Hamburger"       ) : 6,
        ( "VitA",       "FishSandwich"    ) : 2,
        ( "VitA",       "ChickenSandwich" ) : 8,
        ( "VitA",       "Fries"           ) : 0,
        ( "VitA",       "SausageBiscuit"  ) : 4,
        ( "VitA",       "LowfatMilk"      ) : 10,
        ( "VitA",       "OrangeJuice"     ) : 2,

        ( "VitC",       "Cheeseburger"    ) : 6,
        ( "VitC",       "HamSandwich"     ) : 10,
        ( "VitC",       "Hamburger"       ) : 2,
        ( "VitC",       "FishSandwich"    ) : 0,
        ( "VitC",       "ChickenSandwich" ) : 15,
        ( "VitC",       "Fries"           ) : 15,
        ( "VitC",       "SausageBiscuit"  ) : 0,
        ( "VitC",       "OrangeJuice"     ) : 4,
        ( "VitC",       "LowfatMilk"      ) : 120,

        ( "Calc",       "Cheeseburger"    ) : 30,
        ( "Calc",       "HamSandwich"     ) : 20,
        ( "Calc",       "Hamburger"       ) : 25,
        ( "Calc",       "FishSandwich"    ) : 15,
        ( "Calc",       "ChickenSandwich" ) : 15,
        ( "Calc",       "Fries"           ) : 0,
        ( "Calc",       "SausageBiscuit"  ) : 20,
        ( "Calc",       "LowfatMilk"      ) : 30,
        ( "Calc",       "OrangeJuice"     ) : 2,

        ( "Iron",       "Cheeseburger"    ) : 20,
        ( "Iron",       "HamSandwich"     ) : 20,
        ( "Iron",       "Hamburger"       ) : 20,
        ( "Iron",       "FishSandwich"    ) : 10,
        ( "Iron",       "ChickenSandwich" ) : 8,
        ( "Iron",       "Fries"           ) : 2,
        ( "Iron",       "SausageBiscuit"  ) : 15,
        ( "Iron",       "LowfatMilk"      ) : 0,
        ( "Iron",       "OrangeJuice"     ) : 2,

        ( "Volume",     "Cheeseburger"    ) : 4,
        ( "Volume",     "HamSandwich"     ) : 7.5,
        ( "Volume",     "Hamburger"       ) : 3.5,
        ( "Volume",     "FishSandwich"    ) : 5,
        ( "Volume",     "ChickenSandwich" ) : 7.3,
        ( "Volume",     "Fries"           ) : 2.6,
        ( "Volume",     "SausageBiscuit"  ) : 4.1,
        ( "Volume",     "LowfatMilk"      ) : 8,
        ( "Volume",     "OrangeJuice"     ) : 12
    }

    try:
        # Step 1. Create a model and change the parameters.
        model = MdoModel()

        # Step 2. Input model.
        # Change to minimization problem.
        model.set_int_attr(MDO_INT_ATTR.MIN_SENSE, 1)

        # Add constraints.
        cons = {}
        for req_name, req_data in req.items():
            cons[req_name] = model.add_cons(req_data[0], req_data[1], None, req_name)

        # Add variables.
        var = {}
        for food_name, food_data in food.items():
            col = MdoCol()
            for req_name, req_data in req_value.items():
                if food_name == req_name[1]:
                    col.add_term(cons[req_name[0]], req_data)

            var[food_name] = model.add_var(food_data[0], food_data[1], food_data[2], col, food_name, False)

        # Step 3. Solve the problem and populate the result.
        model.solve_prob()
        model.display_results()
        
        status_code, status_msg = model.get_status()
        if status_msg == "OPTIMAL":
            print("Optimizer terminated with an OPTIMAL status (code {0}).".format(status_code))
            print("Daily cost           : ${0}".format(round(model.get_real_attr(MDO_REAL_ATTR.PRIMAL_OBJ_VAL), 2)))
            for food_name, food_var in var.items():
                val = round(food_var.get_real_attr(MDO_REAL_ATTR.PRIMAL_SOLN), 2)
                if val > 0.01:
                    print(" - {0: <17} : {1}".format(food_name, val))
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
