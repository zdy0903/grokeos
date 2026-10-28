"""Aluminum EOS table from FEOS 16.7 with Maxwell construction.

Pressures below P(1e-7 g/cm^3, 1000 K) are stored as that vacuum pressure.
Density is in g/cm^3 and temperature is in K. No extrapolation.
"""
from pathlib import Path

import numpy as np

_DATA = Path(__file__).resolve().parent / "data" / "al_maxwell.npz"
_TABLE = np.load(_DATA)
RHO = _TABLE["rho_g_cm3"]
TEMPERATURE_K = _TABLE["temperature_K"]
PRESSURE_PA = _TABLE["P_Pa"]
ENERGY_J_G = _TABLE["E_J_g"]
TWO_PHASE = _TABLE["two_phase"]
PRESSURE_FLOORED = _TABLE["pressure_floored"]
VACUUM_PRESSURE_PA = float(_TABLE["vacuum_pressure_Pa"])
VACUUM_DENSITY_G_CM3 = float(_TABLE["vacuum_reference_density_g_cm3"])
VACUUM_TEMPERATURE_K = float(_TABLE["vacuum_reference_temperature_K"])


def _locate(axis, value, name):
    if np.any(value < axis[0]) or np.any(value > axis[-1]):
        raise ValueError(
            f"{name} is outside {axis[0]:.6g}..{axis[-1]:.6g}; grokeos does not extrapolate"
        )
    index = np.searchsorted(axis, value, side="right") - 1
    return np.clip(index, 0, axis.size - 2)


def _bilinear(values, rho, temperature):
    rho = np.asarray(rho, dtype=float)
    temperature = np.asarray(temperature, dtype=float)
    i = _locate(RHO, rho, "density")
    j = _locate(TEMPERATURE_K, temperature, "temperature")
    rho0, rho1 = RHO[i], RHO[i + 1]
    t0, t1 = TEMPERATURE_K[j], TEMPERATURE_K[j + 1]
    ar = np.clip((rho - rho0) / (rho1 - rho0), 0.0, 1.0)
    at = np.clip((temperature - t0) / (t1 - t0), 0.0, 1.0)
    v00, v10 = values[i, j], values[i + 1, j]
    v01, v11 = values[i, j + 1], values[i + 1, j + 1]
    return (1.0 - ar) * ((1.0 - at) * v00 + at * v01) + ar * ((1.0 - at) * v10 + at * v11)


def pressure(rho_g_cm3, temperature_K):
    """Total pressure in Pa. Values below the vacuum pressure are already raised."""
    return _bilinear(PRESSURE_PA, rho_g_cm3, temperature_K)


def energy(rho_g_cm3, temperature_K):
    """Specific internal energy in J/g. The vacuum floor does not change energy."""
    return _bilinear(ENERGY_J_G, rho_g_cm3, temperature_K)


def state(rho_g_cm3, temperature_K):
    """Pressure, energy, and whether the source cell was inside the two-phase region."""
    p = pressure(rho_g_cm3, temperature_K)
    e = energy(rho_g_cm3, temperature_K)
    phase = _bilinear(TWO_PHASE.astype(float), rho_g_cm3, temperature_K)
    raised = _bilinear(PRESSURE_FLOORED.astype(float), rho_g_cm3, temperature_K)
    return {
        "P_Pa": p,
        "E_J_g": e,
        "two_phase": phase >= 0.5,
        "pressure_floored": raised >= 0.5,
    }
