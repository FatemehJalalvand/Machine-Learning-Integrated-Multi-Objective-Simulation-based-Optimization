from MOSO_AMC_Risk_Averse import *

from javaconnector import KronosModelConnector

kronos = KronosModelConnector()

costSurplus=[22187,24435,26722,28963,26135,28397,33329,36164]
var_level, lamda=[90, 90, 90], [1, 1, 0] 


#################################
OfficerminTime=2 
OfficerminFlow=0 
SailorminTime=4 
SailorminFlow=0 
MaxPeriod=26
MaxFlow=25
OfficerlowRec=0
OfficerhighRec=13
SailorlowRec=0
SailorhighRec=90

###Vessel renewal parameters
num_old_vessels=6
MinNumNew=12
MaxNumNew=14
TimeMinRetOld=0
TimeMinAcqNew=0
transition_length_ratio=0.75
average_operations_time=2 #dont change this without updating excel

#################################
B_old=42*(10**6)
B_new=47*(10**6)

discountrate=0.02/4 
epsilon_workforce=0.005/4 
epsilon_asset=0.01/4 

Mu_old=0.04/4
Sigma_old=0.005
Mu_new=0.03/4
Sigma_new=0.0015
       
Po=58*(10**8)
##############################


##############Algorithm Parameters#############
replication=30
NGEN = 300
CXPB = 0.7
MUTPB = 0.3


pop, logbook, stats, hof, stop_time=GA_Workforce_Asset(kronos, NGEN, CXPB, MUTPB, costSurplus, var_level, lamda, 
                       OfficerminTime, 
                       OfficerminFlow, 
                       SailorminTime, 
                       SailorminFlow, 
                       MaxPeriod, 
                       MaxFlow, 
                       OfficerlowRec, 
                       OfficerhighRec, 
                       SailorlowRec, 
                       SailorhighRec,  
                       num_old_vessels,
                       MinNumNew, 
                       MaxNumNew, 
                       TimeMinRetOld, TimeMinAcqNew, transition_length_ratio, average_operations_time,
                       B_old, B_new, Mu_old, Sigma_old, Mu_new, Sigma_new,
                       discountrate, Po, epsilon_workforce, epsilon_asset, replication)


#Best values for objective functions
front=np.array([ind.fitness.values for ind in hof])
    
#Best values for decision variables
solution=np.array([ind for ind in hof])

        
Results=[]

Statistics={}

Statistics["lamda"]=lamda

Statistics["var_level"]=var_level

Statistics["pareto_front_values"]=front
    
Statistics["run_time"]=stop_time
    
Statistics["pareto_solutions"]=solution

Statistics["logbook"]=logbook
           
Results.append(Statistics)

        
class NumpyArrayEncoder(JSONEncoder):
      def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
        if isinstance(obj, np.int32):
            return int(obj)
        
        return JSONEncoder.default(self, obj)  
    
class npEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int32):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
    
    
with open('MOSO_AMC_Risk_Averse.json', 'w') as outfile:

    json.dump(Results, outfile, cls=NumpyArrayEncoder)
            
    

