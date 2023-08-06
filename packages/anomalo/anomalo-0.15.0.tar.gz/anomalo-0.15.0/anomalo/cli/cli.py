from __future__ import annotations

from ..client import Client
from .state import StateMachine


class CLI(Client):
    output_style = "text"

    def save_config(
        self,
        filename: str,
        warehouse_id: int | None = None,
        table_id: int | None = None,
    ) -> None:
        self.output_style = "json"
        StateMachine(self).save_config(filename, warehouse_id, table_id)

    def load_config(
        self,
        filename: str,
        warehouse_id: int | None = None,
        table_id: int | None = None,
        force: bool = False,
    ) -> None:
        self.output_style = "json"
        StateMachine(self).load_config(filename, warehouse_id, table_id, force)
