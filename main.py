# -*- coding: utf-8 -*-
"""
ARES-SPACE TRANSPORT V4.0 — Integrated Mission Simulation Runner
Author: Ranyellson Quintão
Target Window: 2030 | Launch Site: Alcantara, Brazil
"""
import math

class SolarThermalEngine:
    def __init__(self):
        self.total_engines = 2
        self.active_engines = 2
        self.g0 = 9.80665                         
        self.r_methane = 518.3                    # Specific gas constant for Methane (J/kg·K)
        self.gamma_methane = 1.32                 # Heat capacity ratio for superheated LCH4
        self.chamber_coating = "Iridium / Ta4HfC5"
        
    def calculate_nozzle_kinetics(self, distance_au, mass_flow_rate_kg_s=15.0):
        if self.active_engines == 0:
            return {"thrust_kn": 0.0, "isp_seconds": 0.0, "chamber_temp_k": 0.0}

        solar_constant_earth = 1361.0
        available_flux = solar_constant_earth / (distance_au ** 2)
        mirror_area = 1250.0 * self.active_engines
        
        thermal_power_w = available_flux * mirror_area * 0.85 * 0.78
        
        cp_methane = 3500.0
        chamber_temp_k = 112.0 + (thermal_power_w / (mass_flow_rate_kg_s * cp_methane))
        
        if chamber_temp_k > 3200.0:
            chamber_temp_k = 3200.0

        v_exhaust = math.sqrt((2 * self.gamma_methane / (self.gamma_methane - 1)) * self.r_methane * chamber_temp_k)
        real_isp = v_exhaust / self.g0
        thrust_kn = (mass_flow_rate_kg_s * v_exhaust) / 1000.0
        
        return {
            "thrust_kn": round(thrust_kn, 2),
            "isp_seconds": round(real_isp, 1),
            "chamber_temp_k": round(chamber_temp_k, 1),
            "coating_status": "INTEGRATED_NO_DEGRADATION"
        }

class MethaneStorageZBO:
    def __init__(self, initial_mass_tons=1130.0):
        self.max_capacity_tons = 1130.0
        self.current_mass_tons = initial_mass_tons
        self.tank_surface_area_m2 = 565.0       
        self.latent_heat_methane_j_kg = 510000   
        self.cryocooler_efficiency_cop = 0.05   # Operational Coeff of Performance at 110K
        self.cryocoolers_on = True
        
    def simulate_thermal_leak(self, days, distance_au):
        external_thermal_flux = 400.0 / (distance_au ** 2)  
        mli_transmittance = 0.001                            # High-efficiency MLI baseline
        heat_leak_watts = self.tank_surface_area_m2 * external_thermal_flux * mli_transmittance
        
        if self.cryocoolers_on:
            evaporated_tons = 0.0
            electrical_power_watts = heat_leak_watts / self.cryocooler_efficiency_cop
            power_kw = electrical_power_watts / 1000.0
            energy_consumed_kwh = power_kw * 24.0 * days
            status = f"ZBO NORMAL: Fuel boiling locked at {power_kw:.2f} kWe draw."
        else:
            total_joules = heat_leak_watts * (days * 86400.0)
            evaporated_kg = total_joules / self.latent_heat_methane_j_kg
            evaporated_tons = evaporated_kg / 1000.0
            self.current_mass_tons -= evaporated_tons
            if self.current_mass_tons < 0: 
                self.current_mass_tons = 0.0
            energy_consumed_kwh = 0.0
            status = f"CRITICAL LEAK: Venting at {(evaporated_tons / days) * 1000:.2f} kg/day."
            
        return {
            "remaining_fuel_tons": round(self.current_mass_tons, 2),
            "lost_fuel_tons": round(evaporated_tons, 3),
            "cryo_power_used_kwh": round(energy_consumed_kwh, 2),
            "system_status": status
        }
class MissionKinematicsSolver:
    def __init__(self):
        self.dry_mass_tons = 120.0  
        self.tanks_mass_tons = 75.0
        self.max_propellant_tons = 1130.0
        self.g0 = 9.80665
        self.engine = SolarThermalEngine()
        
    def evaluate_target_profile(self, payload_tons, delta_v_target, round_trip=True):
        perf = self.engine.calculate_nozzle_kinetics(distance_au=1.0)
        v_e = perf["isp_seconds"] * self.g0
        
        mass_initial = self.dry_mass_tons + self.tanks_mass_tons + self.max_propellant_tons + payload_tons
        mass_final_required = mass_initial / math.exp(delta_v_target / v_e)
        
        fuel_needed_tons = mass_initial - mass_final_required
        margin_tons = self.max_propellant_tons - fuel_needed_tons
        viable = fuel_needed_tons <= self.max_propellant_tons
        
        return {
            "viable": viable,
            "fuel_needed_tons": round(fuel_needed_tons, 1),
            "margin_tons": round(margin_tons, 1),
            "profile_type": "CISLUNAR_LOOP" if round_trip else "INTERPLANETARY_BURST"
        }

if __name__ == "__main__":
    print("================================================================")
    print("      ARES-AEROMINER V4.0 — SYSTEMS ENGINEERING VALIDATION      ")
    print("================================================================")
    
    # 1. Evaluate Engine Stability
    engine = SolarThermalEngine()
    engine_data = engine.calculate_nozzle_kinetics(distance_au=1.0)
    print(f"[ENGINE] Calculated Isp: {engine_data['isp_seconds']} seconds")
    print(f"[ENGINE] Core Thermal Node: {engine_data['chamber_temp_k']} Kelvin")
    print(f"[ENGINE] Thrust Output: {engine_data['thrust_kn']} kN")
    
    # 2. Evaluate Cryogenic Active Storage
    tank = MethaneStorageZBO()
    thermal_data = tank.simulate_thermal_leak(days=28, distance_au=1.0)
    print(f"[THERMAL] Cryocooler State: {thermal_data['system_status']}")
    print(f"[THERMAL] Accumulated Power Draw: {thermal_data['cryo_power_used_kwh']} kWh")
    
    # 3. Evaluate Mission Closure Trajectories
    solver = MissionKinematicsSolver()
    lunar_flight = solver.evaluate_target_profile(payload_tons=55.0, delta_v_target=8400.0, round_trip=True)
    print(f"[KINETICS] Phase I Lunar Mission Closure: {lunar_flight['viable']}")
    print(f"[KINETICS] Fuel Mass Required: {lunar_flight['fuel_needed_tons']} tons")
    print(f"[KINETICS] Safe Tank Margin: {lunar_flight['margin_tons']} tons")
    print("================================================================")
