# In the name of GOD, the Most Gracious, the Most Merciful
import numpy as np
import math
import sys
import json
import pandas as pd  
import time
import pickle        
import scipy.stats   
import matplotlib.pyplot as plt     
from mpl_toolkits import mplot3d     
import matplotlib.tri as mtri        
from math import factorial           
from json import JSONEncoder          
import time
import random
from deap import creator, base, tools, algorithms
from deap.benchmarks.tools import diversity, convergence      
import itertools                                              

def dataSettoList(dateSet):
    List=[]
    for idx in range (0,dateSet.size()):
        List.append(dateSet.getY(idx))
    return List

def generateIndividual(num_old_vessels, OfficerminTime, OfficerminFlow, SailorminTime, SailorminFlow, MaxPeriod, 
                       MaxFlow, OfficerlowRec, OfficerhighRec, SailorlowRec, SailorhighRec, MinNumNew, MaxNumNew, 
                       TimeMinRetOld, TimeMinAcqNew, transition_length_ratio, average_operations_time, kronos):
    
    
    
    
    directory_file='conf/Model-Config_OMEGA_n2_new.xlsx'        
    
    kronos.load_config(directory_file)                         
    
    
    #Generate Officer flow time 
    Oft=np.random.randint(OfficerminTime,MaxPeriod, size=(4, 4))
    
    #Generate officer personnel flow amount 
    Opf=np.random.randint(OfficerminFlow,MaxFlow, size=(4, 4))
    
    #Generate sailor flow time 
    Sft=np.random.randint(SailorminTime,MaxPeriod, size=(4, 4))
    #Generate sailor personnel flow 
    Spf=np.random.randint(SailorminTime,MaxFlow, size=(4, 4))
    
    
    #############Rank 4 flows are ZERO
    
    Oft[1,3], Oft[3,3], Sft[1,3], Sft[3,3]=0,0,0,0
   
    Opf[1,3], Opf[3,3], Spf[1,3], Spf[3,3]=0,0,0,0
    
    
    #Generate officer and sialor recruitment rate
    
    num_quarters=int(kronos.conf.sim_length_months/3)
    
    
    
    
    ORec=np.random.randint(OfficerlowRec, OfficerhighRec, size=(num_quarters))
    SRec=np.random.randint(SailorlowRec, SailorhighRec, size=(num_quarters))
    
    #Generate retirement time of old vessels; acquisition time of new vessels; size of new vessels
    
    #we need transition length and end of simulation ratio for 30+10 years it is equal to 0.75
    
    
    transition_length=int(transition_length_ratio*num_quarters) #0.75 equal to 30 years 
    
    NumNewVessels=random.randint(MinNumNew, MaxNumNew)
    
    TimeRetOld=random.sample(range(TimeMinRetOld, transition_length, average_operations_time), num_old_vessels)  
                                                                                          
    TimeAcqNew=random.sample(range(TimeMinAcqNew, transition_length, average_operations_time), NumNewVessels)
                
    return [list(Oft), list(Opf) , list(Sft), list(Spf), list(ORec), list(SRec), list(TimeRetOld), list(TimeAcqNew)]


def Size_fleet_time(policy, kronos):
    
    num_quarters=int(kronos.conf.sim_length_months/3)
    
    new_vessel=np.zeros(int(num_quarters))
    
    for vessel in policy[-1]:
        
        a_inactive=np.zeros(max(0,vessel))
        
        a_active=np.ones(min(num_quarters-vessel,num_quarters))
        
        new_vessel=new_vessel+np.concatenate((a_inactive, a_active),axis=0)
        
    
    old_vessel=np.zeros(int(num_quarters))
    
    for vessel in policy[-2]:
        
        a_inactive=np.zeros(min(num_quarters-vessel,num_quarters))
        
        a_active=np.ones(max(0,vessel))
        
        old_vessel=old_vessel+np.concatenate((a_active, a_inactive),axis=0)
        
        
    fleet_size_time=new_vessel+old_vessel
    
    return new_vessel, old_vessel, fleet_size_time  

def AssetCost(B_old, B_new, Mu_old, Sigma_old, Mu_new, Sigma_new, discountrate, Po, epsilon_asset, kronos, policy):
    
    OM_Cost_New=0
    OM_Cost_Old=0
    Purcahse_Cost=0
    TotalCost=0
    
    
    List_of_OM_Cost_New=[]
    List_of_Purchase_Cost_New=[]
    List_of_OM_Cost_Old=[]

#####Truncated Normal distribution of O&M cost growth rate 
    
    Gama_old=np.absolute(random.normalvariate(Mu_old, Sigma_old))
    Gama_new=np.absolute(random.normalvariate(Mu_new, Sigma_new))

    
    num_quarters=int(kronos.conf.sim_length_months/3)
    
    
    #Calculating New Vessels O&M and Purchasing Costs
    
    ### O&M Costs of New Vessels
    
    for j in policy[-1]:
        k=[]
        for t in range(j,num_quarters+1):
            p=((1/((1+discountrate)**(t)))*(B_new*math.exp(Gama_new*(t-j))))
            OM_Cost_New+=p  
            k.append(p) 
            
        ####This list is created for plotting the O&M cost of each new vessel during planning horizon              
        List_of_OM_Cost_New.append(k)
                                     
    ### Purchase Costs of New Vessels
    
    ########## Price of buying new vessels###################
    Price=[]
    for t in policy[-1]:
        Price.append(Po*((1+discountrate+epsilon_asset)**t))
    ########################################################
    
    for n in range(len(policy[-1])):
        
        pc=((1/((1+discountrate)**(policy[-1][n])))*Price[n])
        
        Purcahse_Cost+=pc 
        
        ####This list is created for plotting the purchase cost of new vessels 
        List_of_Purchase_Cost_New.append(pc)
                                     
    
    ### O&M Costs of Old Vessels  
    
    #######Time acquision of old vessels#####  
    TimeAcqOld=np.array([-24,-23,-21,-20,-19,-17])*4 #convert years to quarters
    #########################################
    
    for i in range(len(policy[-2])):
        l=[]             
        for t in range(policy[-2][i]): 
            m=(1/((1+discountrate)**t))*(B_old*math.exp(Gama_old*(t-TimeAcqOld[i])))
            OM_Cost_Old+=m
            l.append(m) 
            
        ####This list is created for plotting the O&M cost of each old vessel during planning horizon       
        List_of_OM_Cost_Old.append(l)
            
    TotalCost=OM_Cost_New+Purcahse_Cost+OM_Cost_Old                         
    
    
    return TotalCost, OM_Cost_New, Purcahse_Cost, OM_Cost_Old, List_of_OM_Cost_New, List_of_Purchase_Cost_New, List_of_OM_Cost_Old  
            
def Fitness_Cvar_MultiObj(kronos,  average_operations_time, costSurplus, 
                          B_old, B_new, Mu_old, Sigma_old, Mu_new, Sigma_new,discountrate, Po,
                          epsilon_workforce, epsilon_asset, 
                          var_level, lamda, replication, policy):
    
    #lamda is risk aversion set between 0-1
    #0 risk averse
    #var_level is between 0-100 usully set as 90-95
    
    #var_levels and lamda now lists with 3 elements corresponding to each objective
    
    directory_file='conf/Model-Config_OMEGA_n2_new.xlsx'                
    
    kronos.load_config(directory_file)                                 
   
    workforceTypes=["Officer", "Sailor"]
    flows=["Reset to NSGL", "NSGL to Available","Reset to Readying","Readying to Available"]
    ranks=["Rank 1", "Rank 2","Rank 3","Rank 4"]
    
    
    ######################Decision Variables##############################
    i, j, k=0,0,0
    #i type
    #j flow
    #k rank
    for types in workforceTypes:
        j=0
        for flow in flows:
            k=0
            for rank in ranks:
                kronos.conf.set_average_time( types, flow, rank,  policy[i][j][k])
                kronos.conf.set_max_transfer( types, flow, rank, policy[i+1][j][k] )
                
                k=k+1
            j=j+1
        i=i+2
    ##############realisation of stochastic variables comes##############################
    
    num_quarters=int(kronos.conf.sim_length_months/3)
    
    
    kronos.conf.clear_input_rate_schedules()
    

    ########set recruitment from policy###############
    
    for i in range(0,num_quarters):
        kronos.conf.add_input_rate_schedule(i, "Sailor", policy[-3][i])
        kronos.conf.add_input_rate_schedule(i, "Officer", policy[-4][i])
           

    kronos.conf.clear_fleet_schedules()
    
    
    #size asset function has to be called here
    
    kronos.conf.set_average_operations_time(average_operations_time)
    
    #kronos may not be needed to call
    #=============================================
    SizeAsset=Size_fleet_time(policy, kronos)
    
    for i in range(0, num_quarters, average_operations_time):
        
        kronos.conf.adjust_fleet_size(i, int(SizeAsset[2][i])) #sizeasset should come from function
             
    #=======================================
    
    
    
    TotalCost=[] #list of workforce cost each replication
    TotalAvail=[] #list of total not deployed platforms
    TotalLifeCycleCost=[] #list of total life-cycle cost each replication 
    
    critical_ratio=(1+discountrate+epsilon_workforce)/(1+discountrate)
    
    salary_discounted_increase=np.array([critical_ratio**t for t in range(num_quarters)])
    
    #define normal random parameters for each rank and status here
    
    Officer_Rank1_mu=0.09
    Officer_Rank2_mu=0.07
    Officer_Rank3_mu=0.03
    Officer_Rank4_mu=0.02
    
    Officer_Rank1_std=Officer_Rank1_mu/5.0
    Officer_Rank2_std=Officer_Rank2_mu/5.0
    Officer_Rank3_std=Officer_Rank3_mu/5.0
    Officer_Rank4_std=Officer_Rank4_mu/5.0
    
    Sailor_Rank1_mu=0.16
    Sailor_Rank2_mu=0.13
    Sailor_Rank3_mu=0.05
    Sailor_Rank4_mu=0.04
    
    Sailor_Rank1_std=Sailor_Rank1_mu/5.0
    Sailor_Rank2_std=Sailor_Rank2_mu/5.0
    Sailor_Rank3_std=Sailor_Rank3_mu/5.0
    Sailor_Rank4_std=Sailor_Rank4_mu/5.0
    
        ########set loss as stochastic###############
    for i in range(replication):  
        
        
        kronos.conf.set_loss_wastage( "Officer", "Reset", "Rank 1", np.absolute(random.normalvariate(Officer_Rank1_mu, Officer_Rank1_std)) )
        kronos.conf.set_loss_wastage( "Officer", "Reset", "Rank 2", np.absolute(random.normalvariate(Officer_Rank2_mu, Officer_Rank2_std)) )
        kronos.conf.set_loss_wastage( "Officer", "Reset", "Rank 3", np.absolute(random.normalvariate(Officer_Rank3_mu, Officer_Rank3_std)) )
        kronos.conf.set_loss_wastage( "Officer", "Reset", "Rank 4", np.absolute(random.normalvariate(Officer_Rank4_mu, Officer_Rank4_std)) )
    
        kronos.conf.set_loss_wastage( "Officer", "NSGL", "Rank 4", np.absolute(random.normalvariate(Officer_Rank4_mu, Officer_Rank4_std)) )
        
        
        kronos.conf.set_loss_wastage( "Officer", "Readying", "Rank 1", np.absolute(random.normalvariate(Officer_Rank1_mu, Officer_Rank1_std)))
        kronos.conf.set_loss_wastage( "Officer", "Readying", "Rank 2", np.absolute(random.normalvariate(Officer_Rank2_mu, Officer_Rank2_std))) 
        kronos.conf.set_loss_wastage( "Officer", "Readying", "Rank 3", np.absolute(random.normalvariate(Officer_Rank3_mu, Officer_Rank3_std)))
        
        
        #####################################
        kronos.conf.set_loss_wastage( "Sailor", "Reset", "Rank 1", np.absolute(random.normalvariate(Sailor_Rank1_mu, Sailor_Rank1_std)))
        kronos.conf.set_loss_wastage( "Sailor", "Reset", "Rank 2", np.absolute(random.normalvariate(Sailor_Rank2_mu, Sailor_Rank2_std)))
        kronos.conf.set_loss_wastage( "Sailor", "Reset", "Rank 3", np.absolute(random.normalvariate(Sailor_Rank3_mu, Sailor_Rank3_std)))
        kronos.conf.set_loss_wastage( "Sailor", "Reset", "Rank 4", np.absolute(random.normalvariate(Sailor_Rank4_mu, Sailor_Rank4_std)))
        
        kronos.conf.set_loss_wastage( "Sailor", "NSGL", "Rank 4", np.absolute(random.normalvariate(Sailor_Rank4_mu, Sailor_Rank4_std)))
        
        kronos.conf.set_loss_wastage( "Sailor", "Readying", "Rank 1", np.absolute(random.normalvariate(Sailor_Rank1_mu, Sailor_Rank1_std)) )
        kronos.conf.set_loss_wastage( "Sailor", "Readying", "Rank 2", np.absolute(random.normalvariate(Sailor_Rank2_mu, Sailor_Rank2_std)))
        kronos.conf.set_loss_wastage( "Sailor", "Readying", "Rank 3", np.absolute(random.normalvariate(Sailor_Rank3_mu, Sailor_Rank3_std)) )
        
        
        #####################################
    
        kronos.init_model()             
                
        kronos.conf.set_slot_mode( "ZERO_AVAILABILITY" )            
                    
        kronos.main.write_output = False                            
             
        kronos.run_model()                                            
    
        Sailor1_Gap=np.array(dataSettoList(kronos.main.get_workforce( "Sailor" ).rank_1_gapDS))
        Sailor2_Gap=np.array(dataSettoList(kronos.main.get_workforce( "Sailor" ).rank_2_gapDS))
        Sailor3_Gap=np.array(dataSettoList(kronos.main.get_workforce( "Sailor" ).rank_3_gapDS))
        Sailor4_Gap=np.array(dataSettoList(kronos.main.get_workforce( "Sailor" ).rank_4_gapDS))
        Officer1_Gap=np.array(dataSettoList(kronos.main.get_workforce( "Officer" ).rank_1_gapDS))
        Officer2_Gap=np.array(dataSettoList(kronos.main.get_workforce( "Officer" ).rank_2_gapDS))
        Officer3_Gap=np.array(dataSettoList(kronos.main.get_workforce( "Officer" ).rank_3_gapDS))
        Officer4_Gap=np.array(dataSettoList(kronos.main.get_workforce( "Officer" ).rank_4_gapDS))
    
        #############workforce cost calculation######################
        
        TotalSurplusCost=0
    
        gaps=[Sailor1_Gap,Sailor2_Gap,Sailor3_Gap,Sailor4_Gap, Officer1_Gap,Officer2_Gap,Officer3_Gap,Officer4_Gap]
        
    
        for gap, salary in zip(gaps, costSurplus):
    
            updated_salary=salary*salary_discounted_increase
        
            TotalSurplusCost+=np.sum((gap*updated_salary).clip(min=0))
    
        ###########################################################
    
        docked_platforms=sum(np.array(dataSettoList(kronos.main.docked_platformsDS)))
    
        TotalCost.append(TotalSurplusCost)
        
        TotalAvail.append(docked_platforms)
        
        ACost,_,_,_,_,_,_=AssetCost(B_old, B_new, Mu_old, Sigma_old, Mu_new, Sigma_new, discountrate, Po, epsilon_asset
                                    ,kronos, policy)
    
        TotalLifeCycleCost.append(ACost)
    
    
    TotalCost=np.array(TotalCost)
    varCost = np.percentile(TotalCost, var_level[0])
    cvarCost = TotalCost[TotalCost >= varCost].mean() 
    
    TotalAvail=np.array(TotalAvail)
    varAvail = np.percentile(TotalAvail, var_level[1])
    cvarAvail = TotalAvail[TotalAvail >= varAvail].mean() 
    
    TotalLifeCycleCost=np.array(TotalLifeCycleCost)
    varLifeCycleCost = np.percentile(TotalLifeCycleCost, var_level[2])
    cvarLifeCycleCost = TotalLifeCycleCost[TotalLifeCycleCost >= varLifeCycleCost].mean() 
    
    
    
    return lamda[0]*np.mean(TotalCost)+ (1-lamda[0])*cvarCost, lamda[1]*np.mean(TotalAvail)+ (1-lamda[1])*cvarAvail, lamda[2]*np.mean(TotalLifeCycleCost)+(1-lamda[2])*cvarLifeCycleCost



def simple_mutation_sailor(SailorminTime, SailorminFlow, MaxPeriod, MaxFlow, policy):
    #Sailor time flow of amount
    #decide one or two points will be mutated######
    flow_or_amount=np.random.randint(2,4)
   
    which_rank=np.random.randint(4)
    
    if which_rank!=3:
        which_flow=np.random.randint(4)
    else:
        which_flow=np.random.choice([0,2])
    
    if flow_or_amount==2:
        policy[flow_or_amount][which_flow] [which_rank]=np.random.randint(SailorminTime,MaxPeriod)
    else:
        policy[flow_or_amount][which_flow] [which_rank]=np.random.randint(SailorminFlow,MaxFlow)
        
    return policy,
    
def simple_mutation_officer(OfficerminTime, OfficerminFlow, MaxPeriod, MaxFlow, policy):
    #need to check if it is taking the right policy
    #office time flow or amount random 0-1
    flow_or_amount=np.random.randint(2)
    #takes rank from 1-4 0-3
    which_rank=np.random.randint(4)
    #takes flow type 0-3
    if which_rank!=3:
        which_flow=np.random.randint(4)
    else:
        which_flow=np.random.choice([0,2])
    
    if flow_or_amount==0:
        policy[flow_or_amount][which_flow][which_rank]=np.random.randint(OfficerminTime,MaxPeriod)
    else:
        policy[flow_or_amount] [which_flow][which_rank]=np.random.randint(OfficerminFlow,MaxFlow)
    
    
    return policy,


def simple_mutation_officerRecruitment(OfficerlowRec, OfficerhighRec, policy):
    #Officer recruitment amount 6-13
    
    nORec=len(policy[-4])

    which_recruitment=np.random.randint(nORec)
    policy[-4][which_recruitment]=np.random.randint(OfficerlowRec, OfficerhighRec+1)
    
        
    return policy, 
    
    
def simple_mutation_sailorRecruitment(SailorlowRec, SailorhighRec, policy):
    #Sailor recruitment amount 14-83 
    
    nSRec=len(policy[-3])
        
    which_recruitment=np.random.randint(nSRec)
    policy[-3][which_recruitment]=np.random.randint(SailorlowRec,SailorhighRec+1)
    
        
    return policy,

def simple_mutation_TimeRetOld(TimeMinRetOld, transition_length_ratio, average_operations_time, kronos, policy):
    
    nTRetOld=len(policy[-2])
        
    which_TRetOld=np.random.randint(nTRetOld)
    
    num_quarters=int(kronos.conf.sim_length_months/3)
    
    transition_length=int(transition_length_ratio*num_quarters)  
    
    policy[-2][which_TRetOld]=random.sample(range(TimeMinRetOld, transition_length, average_operations_time), 1)[0]
    
        
    return policy,

def simple_mutation_TimeAcqNew(TimeMinAcqNew,transition_length_ratio, average_operations_time, kronos, policy):
    
    nTAcqNew=len(policy[-1])
        
    which_TAcqNew=np.random.randint(nTAcqNew)

    num_quarters=int(kronos.conf.sim_length_months/3)
    
    transition_length=int(transition_length_ratio*num_quarters) 
    
    policy[-1][which_TAcqNew]=random.sample(range(TimeMinAcqNew, transition_length, average_operations_time), 1)[0]
        
    return policy,


def choice_mutation(OfficerminTime, OfficerminFlow, SailorminTime, SailorminFlow, MaxPeriod, MaxFlow, OfficerlowRec, 
                    OfficerhighRec, SailorlowRec, SailorhighRec, TimeMinRetOld, 
                    TimeMinAcqNew, transition_length_ratio, average_operations_time, kronos, 
                    policy):

    weight= random.choice(range(6))
    
    if weight==0:

        return simple_mutation_officer(OfficerminTime, OfficerminFlow, MaxPeriod, MaxFlow, policy)
    
    elif weight==1:
        
        return simple_mutation_sailor(SailorminTime, SailorminFlow, MaxPeriod, MaxFlow, policy)
    
    elif weight==2:
        
        return simple_mutation_officerRecruitment(OfficerlowRec, OfficerhighRec, policy)

    elif weight==3:
        
        return simple_mutation_sailorRecruitment(SailorlowRec, SailorhighRec, policy)
    
    elif weight==4:
            
        return simple_mutation_TimeRetOld(TimeMinRetOld, transition_length_ratio, average_operations_time, kronos, policy)
    
    elif weight==5:
        
        return simple_mutation_TimeAcqNew(TimeMinAcqNew, transition_length_ratio, average_operations_time, kronos, policy)
    
    else:
        
        raise Exception("Mutation Error")

def GA_Workforce_Asset(kronos,  NGEN, CXPB, MUTPB,costSurplus, var_level, lamda, 
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
                       discountrate, Po, epsilon_workforce, epsilon_asset, replication):

    # 1 is for maximization -1 for minimization
    # Maximize the number of platforms deployed
    
    creator.create("FitnessMax", base.Fitness, weights=(-1.0,-1.0,-1.0)) #for minimization of three objectives
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    
    ################Indivdual Generator#################################################
    NOBJ = 3
    P = 12
    H = factorial(NOBJ + P - 1) / (factorial(P) * factorial(NOBJ - 1))
    MU = int(H + (4 - H % 4))
    
    def generateIndividual(num_old_vessels, OfficerminTime, OfficerminFlow, SailorminTime, SailorminFlow, MaxPeriod, 
                       MaxFlow, OfficerlowRec, OfficerhighRec, SailorlowRec, SailorhighRec, MinNumNew, MaxNumNew, 
                       TimeMinRetOld, TimeMinAcqNew, transition_length_ratio, average_operations_time, kronos):
    
    
        
    
        directory_file='conf/Model-Config_OMEGA_n2_new.xlsx'
    
        kronos.load_config(directory_file)
    
    
        #Generate Officer flow time 
        Oft=np.random.randint(OfficerminTime,MaxPeriod, size=(4, 4))
    
        #Generate officer personnel flow amount 
        Opf=np.random.randint(OfficerminFlow,MaxFlow, size=(4, 4))
    
        #Generate sailor flow time 
        Sft=np.random.randint(SailorminTime,MaxPeriod, size=(4, 4))
        #Generate sailor personnel flow 
        Spf=np.random.randint(SailorminTime,MaxFlow, size=(4, 4))
    
    
        #############Rank 4 flows are ZERO
    
        Oft[1,3], Oft[3,3], Sft[1,3], Sft[3,3]=0,0,0,0
   
        Opf[1,3], Opf[3,3], Spf[1,3], Spf[3,3]=0,0,0,0
    
    
        #Generate officer and sialor recruitment rate
    
        num_quarters=int(kronos.conf.sim_length_months/3)
    
    
        ORec=np.random.randint(OfficerlowRec, OfficerhighRec, size=(num_quarters))
        SRec=np.random.randint(SailorlowRec, SailorhighRec, size=(num_quarters))
    
        #Generate retirement time of old vessels; acquisition time of new vessels; size of new vessels
    
        #we need transition length and end of simulation ratio for 30+10 years it is equal to 0.75
    
    
        transition_length=int(transition_length_ratio*num_quarters) #0.75 equal to 30 years 
        
        NumNewVessels=random.randint(MinNumNew, MaxNumNew)
    
        TimeRetOld=random.sample(range(TimeMinRetOld, transition_length, average_operations_time), num_old_vessels) 
                                                                                          
        TimeAcqNew=random.sample(range(TimeMinAcqNew, transition_length, average_operations_time), NumNewVessels)
                
        return creator.Individual([list(Oft), list(Opf) , list(Sft), list(Spf), list(ORec), list(SRec), list(TimeRetOld), list(TimeAcqNew)])
    
    
    #####Create Uniform Reference Point###########
    
    ref_points = tools.uniform_reference_points(NOBJ, P)
    
    ####################################################

    toolbox = base.Toolbox()

    
    toolbox.register("individual", generateIndividual, 
                     num_old_vessels, OfficerminTime, OfficerminFlow, SailorminTime, SailorminFlow, MaxPeriod, 
                       MaxFlow, OfficerlowRec, OfficerhighRec, SailorlowRec, SailorhighRec, MinNumNew, MaxNumNew, 
                       TimeMinRetOld, TimeMinAcqNew, transition_length_ratio, average_operations_time, kronos)
    
     # define the population to be a list of individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # register the goal / fitness function
    toolbox.register("evaluate", Fitness_Cvar_MultiObj, 
                     kronos,  average_operations_time, costSurplus, 
                          B_old, B_new, Mu_old, Sigma_old, Mu_new, Sigma_new,discountrate, Po,
                          epsilon_workforce, epsilon_asset, 
                          var_level, lamda, replication)

    # register the crossover operators
    
    toolbox.register("mate", tools.cxOnePoint)
    
    toolbox.register("select", tools.selNSGA3, ref_points=ref_points)
    
    # register a mutation operator with a probability to
    toolbox.register("mutate", choice_mutation, OfficerminTime, OfficerminFlow, SailorminTime, SailorminFlow, MaxPeriod, 
                     MaxFlow, OfficerlowRec, OfficerhighRec, SailorlowRec, SailorhighRec, TimeMinRetOld, 
                    TimeMinAcqNew, transition_length_ratio, average_operations_time, kronos)  

    
    
    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront(similar=np.array_equal)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)
    
    
    start_time = time.time() #start time
    
   
    pop, logbook = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, stats,halloffame=hof, verbose=True)
    
    stop_time = time.time() - start_time
    
    
    return pop, logbook, stats, hof, stop_time
        






