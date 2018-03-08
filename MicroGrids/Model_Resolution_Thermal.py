
from pyomo.opt import SolverFactory
from pyomo.environ import Objective, minimize, Constraint


def Model_Resolution(model,datapath="Example/data.dat"):   
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    :param datapath: path to the input data file
    
    :return: The solution inside an object call instance.
    '''
    
    from Constraints import  Net_Present_Cost, Solar_Energy,State_of_Charge,\
    Maximun_Charge, Minimun_Charge, Max_Power_Battery_Charge, Max_Power_Battery_Discharge, Max_Bat_in, Max_Bat_out, \
    Financial_Cost, Energy_balance, Maximun_Lost_Load,Scenario_Net_Present_Cost, Scenario_Lost_Load_Cost, \
    Initial_Inversion, Operation_Maintenance_Cost, Total_Finalcial_Cost, Battery_Reposition_Cost, Maximun_Diesel_Energy, Diesel_Comsuption,Diesel_Cost_Total, \
    Solar_Thermal_Energy, Tank_Thermal_Energy, State_Of_Charge_Tank, Tank_Nominal_Capacity, Maximum_Tank_Charge, Environmental_Thermal_Losses, Boiler_Thermal_Energy, Maximum_Boiler_Energy, \
    NG_Consumption, Resistance_Thermal_Energy, Number_of_Tank, Total_Thermal_Energy_Demand, Thermal_Energy_Balance, Total_Electrical_Resistance_Demand, SC_Financial_Cost, \
    Tank_Financial_Cost, Boiler_Financial_Cost ,NG_Cost_Total
    
    
    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.scenario,model.periods, rule=Energy_balance)
    model.MaximunLostLoad = Constraint(model.scenario, rule=Maximun_Lost_Load) # Maximum permissible lost load
    model.ScenarioLostLoadCost = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost)
    model.TotalEnergyDemand = Constraint(model.scenario, model.periods, model.classes, rule = Total_Thermal_Energy_Demand)
    model.ThermalEnergyBalance = Constraint(model.scenario, model.periods, model.classes, rule = Thermal_Energy_Balance)
    model.TotalElectricalResistanceDemand = Constraint(model.scenario, model.periods, model.classes, rule =Total_Electrical_Resistance_Demand)

    # Solar Collectors Constraints    
    model.SolarThermalEnergy = Constraint(model.scenario, model.periods, model.classes, rule=Solar_Thermal_Energy)

    # PV constraints
    model.SolarEnergy = Constraint(model.scenario, model.periods, rule=Solar_Energy)  # Energy output of the solar panels
    
    # Battery constraints
    model.StateOfCharge = Constraint(model.scenario, model.periods, rule=State_of_Charge) # State of Charge of the battery
    model.MaximunCharge = Constraint(model.scenario, model.periods, rule=Maximun_Charge) # Maximun state of charge of the Battery
    model.MinimunCharge = Constraint(model.scenario, model.periods, rule=Minimun_Charge) # Minimun state of charge
    model.MaxPowerBatteryCharge = Constraint(rule=Max_Power_Battery_Charge)  # Max power battery charge constraint
    model.MaxPowerBatteryDischarge = Constraint(rule=Max_Power_Battery_Discharge)    # Max power battery discharge constraint
    model.MaxBatIn = Constraint(model.scenario, model.periods, rule=Max_Bat_in) # Minimun flow of energy for the charge fase
    model.Maxbatout = Constraint(model.scenario, model.periods, rule=Max_Bat_out) #minimun flow of energy for the discharge fase

    # Tank Constraints     
    model.TankThermalEnergy = Constraint(model.scenario, model.periods, model.classes, rule=Tank_Thermal_Energy)
    model.StateOfChargeTank = Constraint(model.scenario, model.periods, model.classes, rule =State_Of_Charge_Tank)
    model.TankNominalCapacity = Constraint(model.scenario, model.periods, model.classes, rule =Tank_Nominal_Capacity)
    model.MaximumTankCharge = Constraint(model.scenario, model.periods, model.classes, rule =Maximum_Tank_Charge)
    model.EnvironmentalThermalLosses = Constraint(model.scenario, model.periods, model.classes, rule =Environmental_Thermal_Losses)
    
    # Boiler Constraints     
    model.BoilerThermalEnergy = Constraint(model.scenario, model.periods, model.classes, rule =Boiler_Thermal_Energy)
    model.MaximumBoilerEnergy = Constraint(model.scenario, model.periods, model.classes, rule =Maximum_Boiler_Energy) 
    model.NGConsumption = Constraint(model.scenario, model.periods, model.classes, rule = NG_Consumption)
    model.NGCostTotal = Constraint(model.scenario, model.periods, model.classes, rule = NG_Cost_Total)
    
    # Electrical Resistance Constraint     
    model.ResistanceThermalEnergy = Constraint(model.scenario, model.periods, model.classes, rule =Resistance_Thermal_Energy)
     
    # Number Constraints      
    model.NumberOfTank = Constraint(model.scenario, model.periods, model.classes, rule =Number_of_Tank) 
    
    # Diesel Generator constraints
    model.MaximunDieselEnergy = Constraint(model.scenario, model.periods, rule=Maximun_Diesel_Energy) # Maximun energy output of the diesel generator
    model.DieselComsuption = Constraint(model.scenario, model.periods, rule=Diesel_Comsuption)    # Diesel comsuption 
    model.DieselCostTotal = Constraint(model.scenario, rule=Diesel_Cost_Total)
    
    # Financial Constraints
    model.SCFinancialCost = Constraint(model.scenario, model.periods, model.classes, rule = SC_Financial_Cost ) 
    model.TankFinancialCost = Constraint(model.scenario, model.periods, model.classes, rule = Tank_Financial_Cost ) 
    model.BoilerFinancialCost = Constraint(model.scenario, model.periods, model.classes, rule =Boiler_Financial_Cost )
    model.FinancialCost = Constraint(rule=Financial_Cost) # Financial cost
    model.ScenarioNetPresentCost = Constraint(model.scenario, rule=Scenario_Net_Present_Cost)    
    model.InitialInversion = Constraint(rule=Initial_Inversion)
    model.OperationMaintenanceCost = Constraint(rule=Operation_Maintenance_Cost)
    model.TotalFinalcialCost = Constraint(rule=Total_Finalcial_Cost)
    model.BatteryRepositionCost = Constraint(rule=Battery_Reposition_Cost) 

    
    instance = model.create_instance(datapath) # load parameters       
    opt = SolverFactory('cplex') # Solver use during the optimization    
    results = opt.solve(instance, tee=True) # Solving a model instance 
    instance.solutions.load_from(results)  # Loading solution into instance
    return instance
    
    
    #\
def Model_Resolution_binary(model,datapath="Example/data_binary.dat"):   
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    
    :return: The solution inside an object call instance.
    '''
    from Constraints_binary import  Net_Present_Cost, Solar_Energy, State_of_Charge, Maximun_Charge, \
    Minimun_Charge, Max_Power_Battery_Charge, Max_Power_Battery_Discharge, Max_Bat_in, Max_Bat_out, \
    Financial_Cost, Energy_balance, Maximun_Lost_Load, Generator_Cost_1_binary, Generator_Total_Period_Energy_binary, \
    Total_Cost_Generator_binary, Initial_Inversion, Operation_Maintenance_Cost,Total_Finalcial_Cost,\
    Battery_Reposition_Cost, Scenario_Lost_Load_Cost, Sceneario_Generator_Total_Cost, \
    Scenario_Net_Present_Cost, Generator_Bounds_Min_binary, Generator_Bounds_Max_binary,Energy_Genarator_Energy_Max_binary

    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.scenario,model.periods, rule=Energy_balance)  # Energy balance
    model.MaximunLostLoad = Constraint(model.scenario,rule=Maximun_Lost_Load) # Maximum permissible lost load
    # PV constraints
    model.SolarEnergy = Constraint(model.scenario,model.periods, rule=Solar_Energy)  # Energy output of the solar panels
    # Battery constraints
    model.StateOfCharge = Constraint(model.scenario,model.periods, rule=State_of_Charge) # State of Charge of the battery
    model.MaximunCharge = Constraint(model.scenario,model.periods, rule=Maximun_Charge) # Maximun state of charge of the Battery
    model.MinimunCharge = Constraint(model.scenario,model.periods, rule=Minimun_Charge) # Minimun state of charge
    model.MaxPowerBatteryCharge = Constraint(rule=Max_Power_Battery_Charge)  # Max power battery charge constraint
    model.MaxPowerBatteryDischarge = Constraint(rule=Max_Power_Battery_Discharge)    # Max power battery discharge constraint
    model.MaxBatIn = Constraint(model.scenario,model.periods, rule=Max_Bat_in) # Minimun flow of energy for the charge fase
    model.Maxbatout = Constraint(model.scenario,model.periods, rule=Max_Bat_out) #minimun flow of energy for the discharge fase
   
    #Diesel Generator constraints
    model.GeneratorBoundsMin = Constraint(model.scenario,model.periods, rule=Generator_Bounds_Min_binary) 
    model.GeneratorBoundsMax = Constraint(model.scenario,model.periods, rule=Generator_Bounds_Max_binary)
    model.GeneratorCost1 = Constraint(model.scenario, model.periods,  rule=Generator_Cost_1_binary)
    model.EnergyGenaratorEnergyMax = Constraint(model.scenario,model.periods, rule=Energy_Genarator_Energy_Max_binary)
    model.TotalCostGenerator = Constraint(model.scenario, rule=Total_Cost_Generator_binary)
    model.GeneratorTotalPeriodEnergybinary = Constraint(model.scenario,model.periods, rule=Generator_Total_Period_Energy_binary) 
    
    # Financial Constraints
    model.FinancialCost = Constraint(rule=Financial_Cost) # Financial cost
    model.InitialInversion = Constraint(rule=Initial_Inversion)
    model.OperationMaintenanceCost = Constraint(rule=Operation_Maintenance_Cost)
    model.TotalFinalcialCost = Constraint(rule=Total_Finalcial_Cost)
    model.BatteryRepositionCost = Constraint(rule=Battery_Reposition_Cost) 
    model.ScenarioLostLoadCost = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost)
    model.ScenearioGeneratorTotalCost = Constraint(model.scenario, rule=Sceneario_Generator_Total_Cost)
    model.ScenarioNetPresentCost = Constraint(model.scenario, rule=Scenario_Net_Present_Cost) 
    
    
    instance = model.create_instance("Example/data_binary.dat") # load parameters       
    opt = SolverFactory('cplex') # Solver use during the optimization    
#    opt.options['emphasis_memory'] = 'y'
#    opt.options['node_select'] = 3
    results = opt.solve(instance, tee=True,options_string="mipgap=0.11") # Solving a model instance 

    #    instance.write(io_options={'emphasis_memory':True})
    #options_string="mipgap=0.03", timelimit=1200
    instance.solutions.load_from(results) # Loading solution into instance
    return instance
    
def Model_Resolution_Integer(model,datapath="Example/data_Integer.dat"):   
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    
    :return: The solution inside an object call instance.
    '''
    from Constraints_Integer import  Net_Present_Cost, Solar_Energy, State_of_Charge, Maximun_Charge, \
    Minimun_Charge, Max_Power_Battery_Charge, Max_Power_Battery_Discharge, Max_Bat_in, Max_Bat_out, \
    Financial_Cost, Energy_balance, Maximun_Lost_Load, Generator_Cost_1_Integer,  \
    Total_Cost_Generator_Integer, Initial_Inversion, Operation_Maintenance_Cost,Total_Finalcial_Cost,\
    Battery_Reposition_Cost, Scenario_Lost_Load_Cost, Sceneario_Generator_Total_Cost, \
    Scenario_Net_Present_Cost, Generator_Bounds_Min_Integer, Generator_Bounds_Max_Integer,Energy_Genarator_Energy_Max_Integer

    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.scenario,model.periods, rule=Energy_balance)  # Energy balance
    model.MaximunLostLoad = Constraint(model.scenario,rule=Maximun_Lost_Load) # Maximum permissible lost load
    # PV constraints
    model.SolarEnergy = Constraint(model.scenario,model.periods, rule=Solar_Energy)  # Energy output of the solar panels
    # Battery constraints
    model.StateOfCharge = Constraint(model.scenario,model.periods, rule=State_of_Charge) # State of Charge of the battery
    model.MaximunCharge = Constraint(model.scenario,model.periods, rule=Maximun_Charge) # Maximun state of charge of the Battery
    model.MinimunCharge = Constraint(model.scenario,model.periods, rule=Minimun_Charge) # Minimun state of charge
    model.MaxPowerBatteryCharge = Constraint(rule=Max_Power_Battery_Charge)  # Max power battery charge constraint
    model.MaxPowerBatteryDischarge = Constraint(rule=Max_Power_Battery_Discharge)    # Max power battery discharge constraint
    model.MaxBatIn = Constraint(model.scenario,model.periods, rule=Max_Bat_in) # Minimun flow of energy for the charge fase
    model.Maxbatout = Constraint(model.scenario,model.periods, rule=Max_Bat_out) #minimun flow of energy for the discharge fase
   
    #Diesel Generator constraints
    model.GeneratorBoundsMin = Constraint(model.scenario,model.periods, rule=Generator_Bounds_Min_Integer) 
    model.GeneratorBoundsMax = Constraint(model.scenario,model.periods, rule=Generator_Bounds_Max_Integer)
    model.GeneratorCost1 = Constraint(model.scenario, model.periods,  rule=Generator_Cost_1_Integer)
    model.EnergyGenaratorEnergyMax = Constraint(model.scenario,model.periods, rule=Energy_Genarator_Energy_Max_Integer)
    model.TotalCostGenerator = Constraint(model.scenario, rule=Total_Cost_Generator_Integer)
    
    # Financial Constraints
    model.FinancialCost = Constraint(rule=Financial_Cost) # Financial cost
    model.InitialInversion = Constraint(rule=Initial_Inversion)
    model.OperationMaintenanceCost = Constraint(rule=Operation_Maintenance_Cost)
    model.TotalFinalcialCost = Constraint(rule=Total_Finalcial_Cost)
    model.BatteryRepositionCost = Constraint(rule=Battery_Reposition_Cost) 
    model.ScenarioLostLoadCost = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost)
    model.ScenearioGeneratorTotalCost = Constraint(model.scenario, rule=Sceneario_Generator_Total_Cost)
    model.ScenarioNetPresentCost = Constraint(model.scenario, rule=Scenario_Net_Present_Cost) 
    
    
    instance = model.create_instance("Example/data_Integer.dat") # load parameters       
    opt = SolverFactory('cplex') # Solver use during the optimization    
#    opt.options['emphasis_memory'] = 'y'
#    opt.options['node_select'] = 3
    results = opt.solve(instance, tee=True,options_string="mipgap=0.07") # Solving a model instance 

    #    instance.write(io_options={'emphasis_memory':True})
    #options_string="mipgap=0.03", timelimit=1200
    instance.solutions.load_from(results) # Loading solution into instance
    return instance

    
def Model_Resolution_Dispatch(model,datapath="Example/data_Dispatch.dat"):   
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    
    :return: The solution inside an object call instance.
    '''
    from Constraints_Dispatch import  Net_Present_Cost,  State_of_Charge, Maximun_Charge, \
    Minimun_Charge, Max_Bat_in, Max_Bat_out, \
    Energy_balance, Maximun_Lost_Load, Generator_Cost_1_Integer,  \
    Total_Cost_Generator_Integer, \
    Scenario_Lost_Load_Cost, \
     Generator_Bounds_Min_Integer, Generator_Bounds_Max_Integer,Energy_Genarator_Energy_Max_Integer

    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.periods, rule=Energy_balance)  # Energy balance
    model.MaximunLostLoad = Constraint(rule=Maximun_Lost_Load) # Maximum permissible lost load
    
    # Battery constraints
    model.StateOfCharge = Constraint(model.periods, rule=State_of_Charge) # State of Charge of the battery
    model.MaximunCharge = Constraint(model.periods, rule=Maximun_Charge) # Maximun state of charge of the Battery
    model.MinimunCharge = Constraint(model.periods, rule=Minimun_Charge) # Minimun state of charge
    model.MaxBatIn = Constraint(model.periods, rule=Max_Bat_in) # Minimun flow of energy for the charge fase
    model.Maxbatout = Constraint(model.periods, rule=Max_Bat_out) #minimun flow of energy for the discharge fase
   
    #Diesel Generator constraints
    model.GeneratorBoundsMin = Constraint(model.periods, rule=Generator_Bounds_Min_Integer) 
    model.GeneratorBoundsMax = Constraint(model.periods, rule=Generator_Bounds_Max_Integer)
    model.GeneratorCost1 = Constraint(model.periods,  rule=Generator_Cost_1_Integer)
    model.EnergyGenaratorEnergyMax = Constraint(model.periods, rule=Energy_Genarator_Energy_Max_Integer)
    model.TotalCostGenerator = Constraint(rule=Total_Cost_Generator_Integer)
    
    # Financial Constraints
    model.ScenarioLostLoadCost = Constraint(rule=Scenario_Lost_Load_Cost)
    
    instance = model.create_instance("Example/data_dispatch.dat") # load parameters       
    opt = SolverFactory('cplex') # Solver use during the optimization    
#    opt.options['emphasis_memory'] = 'y'
#    opt.options['node_select'] = 3
    results = opt.solve(instance, tee=True,options_string="mipgap=0.03") # Solving a model instance 

    #    instance.write(io_options={'emphasis_memory':True})
    #options_string="mipgap=0.03", timelimit=1200
    instance.solutions.load_from(results) # Loading solution into instance
    return instance

