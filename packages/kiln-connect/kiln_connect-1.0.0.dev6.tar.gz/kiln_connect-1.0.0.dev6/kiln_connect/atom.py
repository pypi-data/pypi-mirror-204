"""Atom wrapper class.

This ATOM class is meant to be accessed via KilnConnect.ATOM, it is
publicly exported in the SDK. This file contains helpers to
integration our Atom API with integrations such as Fireblocks. It
provides convenient shortcuts to use our SDK.
"""

from kiln_connect.integrations import Integrations

from kiln_connect.openapi_client import (
    ApiClient,
)
from kiln_connect.openapi_client import (
    AtomApi,
)


class ATOM(AtomApi):
    """Wrapper for the Atom API.
    """

    def __init__(self, api: ApiClient, integrations: Integrations):
        super().__init__(api)
        self.integrations = integrations
