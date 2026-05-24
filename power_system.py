# -*- coding: utf-8 -*-
"""
ARES-SPACE TRANSPORT V4.0 — Electrical Power Subsystem (EPS)
Author: Ranyellson Quintão
Description: Dimensions solar array area and Li-ion battery capacity for 
             ZBO cryocoolers during deep-space transits and planetary eclipses.
"""
import math

class ElectricalPowerSubsystem:
    def __init__(self):
        self.BASE_HOTEL_LOAD_KW = 15.0       # Life support, avionics, and comms base load
        self.ZBO_POWER_REQ_KW = 2.5          # Active cryocooler continuous consumption
        self.SOLAR_CELL_EFFICIENCY = 0.28    # 28% efficiency Space-grade Triple-Junction GaAs cells
        self.SOLAR_CONSTANT_EARTH = 1.361    # kW/m² at 1.0 AU
        
        # Battery Subsystem Constants (100 kWe peak backup)
        self.BATTERY_ENERGY_DENSITY_WH_KG = 260.0 # Li-ion space-qualified cell metrics
        self.MAX_ECLIPSE_DURATION_HR = 1.2   # Worst-case LEO/Lunar shadow window
        self.DEPTH_OF_DISCHARGE = 0.70       # 70% DoD to guarantee battery life for 2030 horizon

    def dimension_solar_arrays(self, distance_au):
        """Calculates required solar array area (m²) decaying with distance squared."""
        total_demand_kw = self.BASE_HOTEL_LOAD_KW + self.ZBO_POWER_REQ_KW
        available_flux_kw_m2 = self.SOLAR_CONSTANT_EARTH / (distance_au ** 2)
        
        # Required raw solar power considering cell degradation and geometry factor (cos losses ~ 0.9)
        required_area_m2 = total_demand_kw / (available_flux_kw_m2 * self.SOLAR_CELL_EFFICIENCY * 0.9)
        array_mass_kg = required_area_m2 * 2.5 # 2.5 kg/m² for ultra-light rigid composite deployment arrays
        
        return {
            "total_electrical_demand_kw": round(total_demand_kw, 1),
            "required_array_area_m2": round(required_area_m2, 1),
            "solar_array_mass_kg": round(array_mass_kg, 1),
            "solar_flux_at_distance_kw_m2": round(available_flux_kw_m2, 3)
        }

    def dimension_battery_backup(self):
        """Dimensions emergency Li-ion battery matrix for eclipse operations."""
        total_demand_kw = self.BASE_HOTEL_LOAD_KW + self.ZBO_POWER_REQ_KW
        required_capacity_wh = (total_demand_kw * 1000.0 * self.MAX_ECLIPSE_DURATION_HR) / self.DEPTH_OF_DISCHARGE
        battery_mass_kg = required_capacity_wh / self.BATTERY_ENERGY_DENSITY_WH_KG
        
        return {
            "required_battery_capacity_kwh": round(required_capacity_wh / 1000.0, 2),
            "battery_matrix_mass_kg": round(battery_mass_kg, 1),
            "max_eclipse_hold_hours": self.MAX_ECLIPSE_DURATION_HR
        }

if __name__ == "__main__":
    eps = ElectricalPowerSubsystem()
    print("--- EPS Sizing at Mars Transition (1.52 AU) ---")
    print(eps.dimension_solar_arrays(distance_au=1.52))
    print(eps.dimension_battery_backup())
