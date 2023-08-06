"""ATOM commands.

This file contains multiple CLI commands showcasing how to use the
KilnConnect SDK to interact with the Ethereum blockchain.

Code here is voluntarily kept simple: it could be refactored with some
levels of abstraction to avoid repetitions, but would imply readers to
understand things unrelated to what their primary goal is: use the
SDK. So let's keep it stupid simple so the integration work is
simpler.
"""

import typer

from rich.console import Console
from rich.table import Table

import kiln_connect

atom_cli = typer.Typer(
    name='atom', help='Staking utilities for ATOM', no_args_is_help=True)


console = Console()
error_console = Console(stderr=True)


@atom_cli.command("stakes")
def atom_stakes(delegators: list[str] = None, validators: list[str] = None, accounts: list[str] = None):
    """List Atom Stake status.
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        params = {}

        if delegators:
            params['delegators'] = delegators
        if validators:
            params['validators'] = validators
        if accounts:
            params['accounts'] = accounts

        stakes = kc.atom.get_atom_stakes(**params).data

        table = Table('Delegator', 'Validator', 'Balance',
                      'Available Rewards', 'Rewards', 'Net APY')
        for stake in stakes:
            table.add_row(
                stake.delegator_address,
                stake.validator_address,
                stake.balance,
                stake.available_rewards,
                stake.rewards,
                str(stake.net_apy))

        console.print(table)


@atom_cli.command("rewards")
def atom_stakes(delegators: list[str] = None, validators: list[str] = None, accounts: list[str] = None):
    """List Atom Stake status.
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        params = {}

        if delegators:
            params['delegators'] = delegators
        if validators:
            params['validators'] = validators
        if accounts:
            params['accounts'] = accounts

        rewards = kc.atom.get_atom_rewards(**params).data

        table = Table('Date', 'Balance', 'Rewards', 'Net APY')
        for reward in rewards:
            table.add_row(
                str(reward.var_date),
                reward.balance,
                reward.rewards,
                str(reward.net_apy))

        console.print(table)
