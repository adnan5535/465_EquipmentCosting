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
LocationFactor = 1.2
ContFeeFactor = 1.18    
AuxFactor = 1.21

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
    
def compcost(Cp_c,F_BM_c,Cp_e,F_BM_e):
    C_BM_c = Cp_c * F_BM_c
    C_BM_e = Cp_e * F_BM_e
    C_BM_2004 = C_BM_c + C_BM_e
    C_BM_2016_CAD = usd04tocad16(C_BM_2004)
    print "Purchase Cost of compressor, Cp_c (U&V Fig 5.30) = ", Cp_c
    print "Bare module factor for compressor, F_BM (U&V Fig 5.30) = ", F_BM_c
    print "Bare module cost for compressor, C_BM = ", C_BM_c
    print "Purchase Cost of engine, Cp_e (U&V Fig 5.21) = ", Cp_e
    print "Bare module factor for engine, F_BM_e (U&V Fig 5.21) = ", F_BM_e
    print "Bare module cost for engine, C_BM_e = ", C_BM_e
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
    
def extracosts(C_BM):
    C_TM = C_BM * ContFeeFactor * LocationFactor
    C_GR = C_TM * AuxFactor
    print "\nTotal module capital, C_TM = ", C_TM
    print "Total Capital Cost Estimation = ", C_GR
    
def usd04tocad16(cost):
    C_BM_2004 = cost
    C_BM_2016 = C_BM_2004 * USGC_Correction
    C_BM_2016_CAD = C_BM_2016 * USDtoCAD
    return C_BM_2016_CAD
    
# Arguments are passed in the format L,D,Cp,Fp,Fm,Fa_BM
print "\nSeparator 1"
C_BM_S1 = separatorcost(1.676,0.3048,1.1e3,1,1,1.5)
print "\nSeparator 2"
C_BM_S2 = separatorcost(1.676,0.4576,1.6e3,1,1,1.5)
print "\nSeparator 3"
C_BM_S3 = separatorcost(1.676,0.3048,1.1e3,1.5,1,4)
print "\nSeparator 4"
C_BM_S4 = separatorcost(1.829,0.3048,1.3e3,1,1,1.5)

print "\nCompressor 1"
C_BM_C1 = compcost(22000,2.2,28000,2)
print "\nCompressor 2"
C_BM_C2 = compcost(85000,2.2,150000,2)

print "\nGlycol Contactor Absorber"

Cp = 95 # From U&V Fig 5.36
F_BM = 2.2 # Used U&V Fig 5.38 for 
           # F_BM = F_p * F_M
N_act = 11
f_q = 1.19
C_BM_GC = absorber(Cp,F_BM,N_act,f_q) # interpolated between number of trays 10 and 20
                               # and f_q 1.2 and 1.05 respectively

print "\nPacked Column"
C_BM_PC = packedcolumn_reboiler_pump(600,1) # Used U&V Fig 5.47 for Cp and F_BM

# Got reboiler duty, Q = 90 kW and delta T = 17 deg C from VMG Sim
# Used Table 4.15c to get the heat coefficient, U = 620 J m^-2 K^-1 s^-1
# Exchanger surface area = Q/(delta T * U) = 8.53 m^2
# Used U&V Fig 5.37 to get Cp = 7100
# Used U&V Fig 5.38 for F_BM = 3, from F_p * F_M = 1.1 * 1 = 1.1

print "\nReboiler"
C_BM_reb = packedcolumn_reboiler_pump(7100,3)

print "\nPump"
C_BM_pump = packedcolumn_reboiler_pump(19000,3.5) # Used U&V Fig 5.36 for Cp = 19000
                                            # Used U&V Fig 5.38 for 
                                            # F_BM = F_p * F_M = 
# Used F_p from Fig 5.50

# Shell and Tube inlet and outlet temperatures are taken from VMG Sim
# Shell Inlet T = 205 deg C. Outlet T = 165.9 deg C
# Tube Inlet T = 125.2 deg C. Outlet T = 164.1 deg C
# Cross-flow heat exchanger

print "\nSurge Tank Heat Exchanger"
tube_outlet_T = 164.1
tube_inlet_T = 125.2
shell_outlet_T = 165.9
shell_inlet_T = 205.2
S_R = hex_s_r_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T)
print "S = ", S_R[0]
print "R = ", S_R[1]
F_T = 0.8 # From fig 4.22
print "MTD correction factor, F_T from Fig 4.22 = ", F_T
U = 306 # From Table 4.15c J m^-2 K^-1 s^-1
print "Heat coefficient from Table 4.15c = ", U
Q = 67 # kW from VMG SIM
print "Surge Tank Heat Exchanger Duty = ", Q
hex_surfarea = hex_surfarea_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T,F_T,U,(Q*1e3))
print "Heat Exchanger Surface Area = ", hex_surfarea
Cp_vessel = 5000 # From Fig 5.23a
F_BM_vessel = 3 # From Fig 5.23a
F_p_vessel = 1 # From Fig 5.23a
Cp_coils = 4200 # From Fig 5.23b
F_BM_coils = 1 # From Fig 5.23b
C_BM_ST_HEX = hex_costing(Cp_vessel,F_BM_vessel,F_p_vessel,Cp_coils,F_BM_coils)

print "\nHeat Exchanger 2"
tube_outlet_T = 136.7
tube_inlet_T = 165.9
shell_outlet_T = 118.1
shell_inlet_T = 73.1
F_T = 1 # Unnecessary in this hex
U = 306 # From Table 4.15c J m^-2 K^-1 s^-1
print "Heat coefficient from Table 4.15c = ", U
Q = 48.4 # kW from VMG SIM
print "Heat Exchanger 2 Duty (in kW) = ", Q
hex_surfarea = hex_surfarea_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T,F_T,U,(Q*1e3))
print "Heat Exchanger Surface Area = ", hex_surfarea

Cp = 2300 # From Fig 5.36
F_m = 1 # Fig 5.36
F_p = 1 # Fig 5.37
F_BM = 3 # From Fig 5.38
Cp_coils = 0 # Because this is a counter current heat exchanger
F_BM_coils = 0 # Because this is a counter current heat exchanger
C_BM_HEX2 = hex_costing(Cp,F_BM,F_p,Cp_coils,F_BM_coils)

print "\nAir Cooler 1"
tube_outlet_T = 90.7
tube_inlet_T = 136.7
shell_outlet_T = 70
shell_inlet_T = 30
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
C_BM_AC1 = hex_costing(Cp,F_BM,F_p,Cp_coils,F_BM_coils)

print "\nAir Cooler 2"
tube_outlet_T = 44.7
tube_inlet_T = 90.7
shell_outlet_T = 40
shell_inlet_T = 30
S_R = hex_s_r_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T)
print "S = ", S_R[0]
print "R = ", S_R[1]
F_T = 0.95 # From fig 4.22
print "MTD correction factor, F_T from Fig 4.22 = ", F_T
U = 306 # From Table 4.15c J m^-2 K^-1 s^-1
print "Heat coefficient from Table 4.15c (J m^-2 K^-1 s^-1) = ", U
Q = 67.9 # kW from VMG SIM
print "Air Cooler 2 Heat Exchanger Duty (in kW) = ", Q
hex_surfarea = hex_surfarea_calc(tube_outlet_T,tube_inlet_T,shell_outlet_T,shell_inlet_T,F_T,U,(Q*1e3))
print "Heat Exchanger Surface Area = ", hex_surfarea
Cp = 11000 # From Fig 5.40
F_m = 1 # From Fig 5.40
F_p = 1 # From Fig 5.37
F_BM = 3 # From Fig 5.38
Cp_coils = 0 # No coils in air cooler
F_BM_coils = 0 # No coils in air cooler
C_BM_AC2 = hex_costing(Cp,F_BM,F_p,Cp_coils,F_BM_coils)

extracosts(C_BM_S1+C_BM_S2+C_BM_S3+C_BM_S4+C_BM_C1+C_BM_C2+C_BM_GC+C_BM_PC+C_BM_reb+C_BM_pump+C_BM_ST_HEX+C_BM_HEX2+C_BM_AC1+C_BM_AC2)