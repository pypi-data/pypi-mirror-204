# src/tessif_examples/chp.py
"""Tessif minimum working example energy system model."""
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_chp():
    """Create a minimum CHP centered example.

    Create a minimal working example using :mod:`tessif's
    model <tessif.model>` optimizing it for costs to demonstrate
    a chp application.

    Return
    ------
    :class:`tessif.system_model.AbstractEnergySystem`
        Tessif energy system.

    Examples
    --------
    Generic System Visualization

    .. image:: ../../_static/system_model_graphs/chp.png
        :align: center
        :alt: Image showing the chp energy system graph
    """
    # 2. Create a simulation time frame of four one-hour timesteps as a
    # :class:`pandas.DatetimeIndex`:
    timeframe = date_range("7/13/1990", periods=4, freq="H")

    global_constraints = {"emissions": float("+inf")}

    # 3. Creating the individual energy system components:
    gas_supply = components.Source(
        name="Gas Source",
        outputs=("gas",),
        # Minimum number of arguments required
    )

    gas_grid = components.Bus(
        name="Gas Grid",
        inputs=("Gas Source.gas",),
        outputs=("CHP.gas",),
        # Minimum number of arguments required
    )

    # conventional power supply is cheaper, but has emissions allocated to it
    chp = components.Transformer(
        name="CHP",
        inputs=("gas",),
        outputs=("electricity", "heat"),
        conversions={
            ("gas", "electricity"): 0.3,
            ("gas", "heat"): 0.2,
        },
        # Minimum number of arguments required
        # flow_rates={
        #     'electricity': (0, 9),
        #     'heat': (0, 6),
        #     'gas': (0, float('+inf'))
        # },
        flow_costs={"electricity": 3, "heat": 2, "gas": 0},
        flow_emissions={"electricity": 2, "heat": 3, "gas": 0},
    )

    # back up power, expensive
    backup_power = components.Source(
        name="Backup Power",
        outputs=("electricity",),
        flow_costs={"electricity": 10},
    )

    # Power demand needing 10 energy units per time step
    power_demand = components.Sink(
        name="Power Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        flow_rates={"electricity": nts.MinMax(min=10, max=10)},
    )

    power_line = components.Bus(
        name="Powerline",
        inputs=("Backup Power.electricity", "CHP.electricity"),
        outputs=("Power Demand.electricity",),
        # Minimum number of arguments required
    )

    # Back up heat source, expensive
    backup_heat = components.Source(
        name="Backup Heat",
        outputs=("heat",),
        flow_costs={"heat": 10},
    )

    # Heat demand needing 10 energy units per time step
    heat_demand = components.Sink(
        name="Heat Demand",
        inputs=("heat",),
        # Minimum number of arguments required
        flow_rates={"heat": nts.MinMax(min=10, max=10)},
    )

    heat_grid = components.Bus(
        name="Heat Grid",
        inputs=("CHP.heat", "Backup Heat.heat"),
        outputs=("Heat Demand.heat",),
        # Minimum number of arguments required
    )

    # 4. Creating the actual energy system:
    explicit_es = system_model.AbstractEnergySystem(
        uid="CHP_Example",
        busses=(gas_grid, power_line, heat_grid),
        sinks=(power_demand, heat_demand),
        sources=(gas_supply, backup_power, backup_heat),
        transformers=(chp,),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return explicit_es
