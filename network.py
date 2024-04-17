import pypsa
import numpy as np

import logging

# Get the logger for 'pypsa.pf'
logger = logging.getLogger('pypsa.pf')
# Set the logging level to suppress INFO messages
logger.setLevel(logging.FATAL)

def network_defination(chromosome):
    # Create a simple power system network
    network = pypsa.Network()

    # Add buses (nodes)
    network.add("Bus", "Bus 1", v_nom=chromosome)
    network.add("Bus", "Bus 2", v_nom=chromosome)

    # Add a generator
    network.add("Generator", "Generator 1", bus="Bus 1", p_set=100.0)

    # Add loads
    network.add("Load", "Load 1", bus="Bus 2", p_set=80.0)

    # Add lines (lines connect buses)
    network.add("Line", "Line 1", bus0="Bus 1", bus1="Bus 2", x=0.1, s_nom=100.0)

    # Solve the power flow
    network.pf()

    # Return the network for evaluation
    return network

# Assess voltage stability margin
def voltage_stability_margin(network):
    v_mag_pu_float = network.buses_t.v_mag_pu.squeeze().astype(float)  # Extract and convert to float
    min_voltage = min(v_mag_pu_float)
    v_nom = network.buses.v_nom.astype(float)
    v_nom_min = min(v_nom)
    VSM = ((abs(min_voltage*v_nom_min - v_nom_min)) / v_nom_min) * 100
    return VSM



if __name__ == "__main__":
  # Perform voltage stability analysis
  VSM = voltage_stability_margin(network_defination(np.random.rand() * 100))
  print("Voltage Stability Margin:", VSM, "%")
