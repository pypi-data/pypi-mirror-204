"""Helpers for unit conversions.
"""


def wei_to_eth(wei: int) -> float:
    """Convert wei to ether.
    """
    return int(wei) / 1e18


def wei_to_gwei(wei: int) -> float:
    """Convert wei to gwei.
    """
    return int(wei) / 1e9


def lamport_to_sol(lamport: int) -> int:
    """Convert lamport to sol.
    """
    return int(lamport) / 1e9


def sol_to_lamport(sol: float) -> int:
    """Convert sol to lamport.
    """
    return sol * 1e9
