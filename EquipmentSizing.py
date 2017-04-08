# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 14:16:44 2016

@author: Adnan
"""
import math

# Assumptions: 
# - Can use Figs 5.45 and 5.46 in U&V despite them being for operating 
#   pressures above 4 barg.
# - Going to use a contingency and fee factor of 1.18 even though U&V uses
#   it only for a heat exchanger

USGC_Correction = 1.35
USDtoCAD = 1.35
LocationFactor = 0.2
ProjectContFeeFactor = 0.4
ProcessContFeeFactor = 0.15
ContractorFeeFactor = 0.03
SiteDevCost = 0.21
WorkingCapitalFactor = 0.1


def plate_frame_hex_cost(UA_product,U_heattransfcoeff,SandTmodifier,Fp_Fm_prod,Fa_BM,Cp):
    U_heattransfcoeff_modified = U_heattransfcoeff * SandTmodifier    
    hex_surf_area_A = UA_product/U_heattransfcoeff_modified
    C_BM_2004 = Cp * Fa_BM
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "U*A = %s (From VMGSim Simulation)" % (UA_product)
    print "U value from U&V Table 4.15 = ", U_heattransfcoeff   
    print "Plate and Frame modifier from U&V Table 4.15 = ", SandTmodifier    
    print "Modified U value for Plate and Frame Heat Exchangers = ", U_heattransfcoeff_modified 
    print "Fp*Fm = ", Fp_Fm_prod
    print "Fa_BM = ", Fa_BM 
    print "Heat Exchanger Surface Area = ", hex_surf_area_A    
    print ""    
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD    
    return C_BM_2016_CAD

def separatorcost(L,D,Cp,Fp,Fm,Fa_BM):  
    print "\nLength = ", L
    print "Diameter = ", D
    print "Fp = ", Fp
    print "Fm = ", Fm
    C_BM_2004 = Cp * Fa_BM
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "Purchase Cost, Cp (from U&V fig 5.44) = ", Cp
    print "Bare module factor, Fa_BM (from U&V fig 5.46) = ", Fa_BM
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD
    return C_BM_2016_CAD
    
def comp_blow_cost(Cp_c,F_BM_c,C_BM_d):
    C_BM_c = Cp_c * F_BM_c
    C_BM_2004 = C_BM_c + C_BM_d
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "Purchase Cost of compressor, Cp_c (U&V Fig 5.30) = ", Cp_c
    print "Bare module factor for compressor, F_BM (U&V Fig 5.30) = ", F_BM_c
    print "Bare module cost for compressor, C_BM = ", C_BM_c
    print "Bare module cost for engine (U&V Fig 5.20), C_BM_e = ", C_BM_d
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD
    return C_BM_2016_CAD
    
def absorber(Cp,F_BM,N_act,f_q):
    C_BM_2004 = Cp * F_BM * N_act* f_q
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004    
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD    
    return C_BM_2016_CAD

def packedcolumn_reboiler_pump(Cp,F_BM):
    C_BM_2004 = Cp * F_BM
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004    
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD    
    return C_BM_2016_CAD
   
def hex_s_r_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T):
    S = (tube_outlet_T - tube_inlet_T)/(shell_inlet_T - tube_inlet_T)    
    R = (shell_inlet_T - shell_outlet_T)/(tube_outlet_T - tube_inlet_T)        
    return [S,R]

def hex_surfarea_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T,F_T,U,Q):    
    dt1 = abs(shell_outlet_T - tube_inlet_T)
    dt2 = abs(shell_inlet_T - tube_outlet_T)
    MTD = (dt1 - dt2)/math.log(dt1/dt2)
    hex_surfarea = Q / (MTD * U * F_T)
    return hex_surfarea
    
def hex_costing(Cp_vessel,F_BM_vessel,F_p_vessel,Cp_coils,F_BM_coils):
    C_BM_2004 = (Cp_vessel * F_BM_vessel * F_p_vessel) + (Cp_coils*F_BM_coils)
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004    
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD 
    return C_BM_2016_CAD
    
def fuelcell_costing(C_BM_fc_04):
    C_BM_2004 = C_BM_fc_04  
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)    
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004    
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD 
    return C_BM_2016_CAD
    
def pump_costing(Cp,Fm,Fp,Fa_BM):
    C_BM_2004 = Cp * Fa_BM
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "Fm (U&V Fig 5.49)= ", Fm    
    print "Fp (U&V Fig 5.50) = ", Fp  
    print "Purchase Cost, Cp (from U&V fig 5.49) = ", Cp
    print "Bare module factor, Fa_BM (from U&V fig 5.52) = ", Fa_BM
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004    
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD 
    return C_BM_2016_CAD

def expander_costing(Cp,F_BM):
    C_BM_2004 = Cp * F_BM
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "Bare Module Cost ($US, 2004), C_BM_2004 = ", C_BM_2004    
    print "Bare Module Cost ($CA, 2016), C_BM_2016_CAD = ", C_BM_2016_CAD 
    return C_BM_2016_CAD

def extracosts(C_BM):
    C_BM_Contingency = (C_BM * ProjectContFeeFactor) + (C_BM * ProcessContFeeFactor)
    C_BM_Location = C_BM * LocationFactor
    C_BM_Site = C_BM * SiteDevCost
    C_BM_Contractor = C_BM * ContractorFeeFactor
    C_FC = C_BM + C_BM_Contingency + C_BM_Location + C_BM_Site + C_BM_Contractor
    C_WC = C_FC * WorkingCapitalFactor    
    print "\nTotal Bare Module cost, C_BM = ", C_BM    
    print "Total Fixed Capital, C_FC = ", C_FC
    print "Total Capital Cost Estimation = ", C_FC+C_WC
    print "Total Working Capital  = ", C_WC
    
def usd04tocad16(cost):
    C_BM_2004 = cost
    C_BM_2016 = C_BM_2004 * USGC_Correction
    C_BM_2016_CAD = C_BM_2016 * USDtoCAD
    return C_BM_2016_CAD
    

print "\nPlate and Frame Heat Exchanger Hx100"
C_BM_pf_hex100 = plate_frame_hex_cost(14138.13,100,2,2.3,5,12000)

print "\nPlate and Frame Heat Exchanger Hx110"
C_BM_pf_hex110 = plate_frame_hex_cost(34764.31,100,2,2.3,5,20000)

print "\nPlate and Frame Heat Exchanger Hx120"
C_BM_pf_hex120 = plate_frame_hex_cost(1559.12,40,2,2.3,5,5000)

print "\nPlate and Frame Heat Exchanger Hx130"
C_BM_pf_hex130 = plate_frame_hex_cost(754.19,100,2,2.3,5,2500)

print "\nPlate and Frame Heat Exchanger Hx140"
C_BM_pf_hex140 = plate_frame_hex_cost(1176.64,331,2,2.3,5,1500)

print "\nPlate and Frame Heat Exchanger Hx150"
C_BM_pf_hex150 = plate_frame_hex_cost(3734.99,40,2,2.3,5,80000)

print "\nPlate and Frame Heat Exchanger Hx160"
C_BM_pf_hex160 = plate_frame_hex_cost(571.75,106,2,2.3,5,1800)

print "\nPlate and Frame Heat Exchanger Hx170"
C_BM_pf_hex170 = plate_frame_hex_cost(195.96,100,2,2.3,5,950)

print "\nPlate and Frame Heat Exchanger Hx180"
C_BM_pf_hex180 = plate_frame_hex_cost(4653.02,40,2,2.3,5,10000)

print "\nPlate and Frame Heat Exchanger Hx190"
C_BM_pf_hex190 = plate_frame_hex_cost(969.35,100,2,2.3,5,2500)

print "\nPlate and Frame Heat Exchanger Hx200"
C_BM_pf_hex200 = plate_frame_hex_cost(313.22,106,2,2.3,5,1300)

print "\nPlate and Frame Heat Exchanger Hx210"
C_BM_pf_hex210 = plate_frame_hex_cost(1774.05,40,2,2.3,5,5000)

print "\nPlate and Frame Heat Exchanger Hx220"
C_BM_pf_hex220 = plate_frame_hex_cost(1069.06,106,2,2.3,5,2500)

print "\nPlate and Frame Heat Exchanger Hx230"
C_BM_pf_hex230 = plate_frame_hex_cost(10563.62,243,2,2.3,5,5000)

print "\nPlate and Frame Heat Exchanger Hx240"
C_BM_pf_hex240 = plate_frame_hex_cost(5235.44,106,2,2.3,5,5500)

print "\nTotal Heat Exchangers C_BM = ", C_BM_pf_hex100+C_BM_pf_hex110+C_BM_pf_hex120+ \
                C_BM_pf_hex130+C_BM_pf_hex140+C_BM_pf_hex150+C_BM_pf_hex160+ \
                C_BM_pf_hex170+C_BM_pf_hex180+C_BM_pf_hex190+C_BM_pf_hex200+ \
                C_BM_pf_hex210+C_BM_pf_hex220+C_BM_pf_hex230+C_BM_pf_hex240

print "\n***********************************************************************************"

# Arguments are passed in the format L,D,Cp,Fp,Fm,Fa_BM
print "\nSeparator Sep100"
C_BM_S100 = separatorcost(2.13,0.762,5500,1.1,4,10)
print "\nSeparator Sep110"
C_BM_S110 = separatorcost(1.98,0.762,5100,1.1,4,10)
print "\nSeparator Sep120"
C_BM_S120 = separatorcost(1.37,0.3048,2500,1.3,4,10)
print "\nSeparator Sep130"
C_BM_S130 = separatorcost(1.9812,0.762,5100,1.15,4,10)
print "\nSeparator Sep140"
C_BM_S140 = separatorcost(1.98,0.6096,4900,1.1,4,10)
print "\nSeparator Sep150"
C_BM_S150 = separatorcost(1.68,0.6096,4500,1.1,4,10)
print "\nSeparator Sep160"
C_BM_S160 = separatorcost(1.6764,0.6096,4000,1.1,4,10)
print "\nSeparator Sep170"
C_BM_S170 = separatorcost(2.7432,0.4572,5500,1.1,4,10)
print "\nSeparator Sep180"
C_BM_S180 = separatorcost(3.048,0.6096,10000,1.1,4,10)

print "\nTotal Separator C_BM = ", C_BM_S100+C_BM_S110+C_BM_S120+C_BM_S130+C_BM_S140+C_BM_S150+ \
                C_BM_S160+C_BM_S170+C_BM_S180

print "\n***********************************************************************************"

#Arguments are in the format Cp_c,F_BM_c,C_BM_d
print "\nBlower C110"
C_BM_C110 = comp_blow_cost(60000,6.3,35000)
print "\nBlower C120"
C_BM_C120 = comp_blow_cost(25000,6.3,14000)
print "\nBlower C130"
C_BM_C130 = comp_blow_cost(50000,6.3,35000)
print "\nTotal Blower C_BM = ", C_BM_C110+C_BM_C120+C_BM_C130
                
print "\n***********************************************************************************"

#Arguments are in the format Cp,Fm,Fp,Fa_BM
print "\nPump P110"
C_BM_P110 = pump_costing(2000,1.9,1,5)
print "\nPump P120"
C_BM_P120 = pump_costing(900,1.9,1,5)
print "\nPump P130"
C_BM_P130 = pump_costing(5500,1.9,1,5)
print "\nTotal Pump C_BM = ", C_BM_P110+C_BM_P120+C_BM_P130

print "\n***********************************************************************************"

print "\nAir Cooler - AC110"
tube_outlet_T = 20
tube_inlet_T = 128.8
shell_outlet_T = 78
shell_inlet_T = 15
S_R = hex_s_r_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T)
print "S = ", S_R[0]
print "R = ", S_R[1]
F_T = 0.93 # From fig 4.22
print "MTD correction factor, F_T from Fig 4.22 = ", F_T
U = 306 # From Table 4.15c J m^-2 K^-1 s^-1
print "Heat coefficient from Table 4.15c = ", U
Q = 72.7 # kW from VMG SIM
print "Air Cooler 1 Exchanger Duty (in kW) = ", Q
hex_surfarea = hex_surfarea_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T,F_T,U,(Q*1e3))
print "Heat Exchanger Surface Area = ", hex_surfarea
Cp = 8000 # From Fig 5.40
F_m = 1 # From Fig 5.40
F_p = 1 # From Fig 5.37
F_BM = 3 # From Fig 5.38
Cp_coils = 0 # No coils in air cooler
F_BM_coils = 0 # No coils in air cooler
C_BM_AC110 = hex_costing(Cp,F_BM,F_p,Cp_coils,F_BM_coils)

print "\n***********************************************************************************"

print "\nMolten Carbonate Fuel Cell"
C_BM_fc_04 = 2e6 #US$ 2004. From U&V Fig 5.9
C_BM_fc_16 = fuelcell_costing(C_BM_fc_04)

print "\n***********************************************************************************"

print "\nExpander E110"
C_BM_exp110 = expander_costing(18000,3.5)

print "\n***********************************************************************************"

print "\nHeat Exchanger - Hx100 modelled as S&T Hx"
tube_outlet_T = 149.6
tube_inlet_T = 400
shell_outlet_T = 398
shell_inlet_T = 52.4
S_R = hex_s_r_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T)
print "S = ", S_R[0]
print "R = ", S_R[1]
F_T = 1 # From fig 4.22
print "MTD correction factor, F_T from Fig 4.22 = ", F_T
U = 44.36 # From Table 4.15c J m^-2 K^-1 s^-1
print "Heat coefficient from Table 4.15c = ", U
Q = 3.464e5 # kW from VMG SIM
print "Air Cooler 1 Exchanger Duty (in kW) = ", Q
hex_surfarea = hex_surfarea_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T,F_T,U,(Q*1e3))
print "Heat Exchanger Surface Area = ", hex_surfarea
Cp = 8000 # From Fig 5.40
F_m = 1 # From Fig 5.40
F_p = 1 # From Fig 5.37
F_BM = 3 # From Fig 5.38
Cp_coils = 0 # No coils in air cooler
F_BM_coils = 0 # No coils in air cooler
C_BM_AC110 = hex_costing(Cp,F_BM,F_p,Cp_coils,F_BM_coils)

print "\n***********************************************************************************"


extracosts(C_BM_pf_hex100+C_BM_pf_hex110+C_BM_pf_hex120+ \
                C_BM_pf_hex130+C_BM_pf_hex140+C_BM_pf_hex150+C_BM_pf_hex160+ \
                C_BM_pf_hex170+C_BM_pf_hex180+C_BM_pf_hex190+C_BM_pf_hex200+ \
                C_BM_pf_hex210+C_BM_pf_hex220+C_BM_pf_hex230+C_BM_pf_hex240+ \
                C_BM_S100+C_BM_S110+C_BM_S120+C_BM_S130+C_BM_S140+C_BM_S150+ \
                C_BM_S160+C_BM_S170+C_BM_S180+ \
                C_BM_C110+C_BM_C120+C_BM_C130+ \
                C_BM_P110+C_BM_P120+C_BM_P130+ \
                C_BM_AC110+ \
                C_BM_fc_16+ \
                C_BM_exp110)
                
wait_input_var = input()