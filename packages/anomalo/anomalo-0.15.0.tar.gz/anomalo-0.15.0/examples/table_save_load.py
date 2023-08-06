import collections
import functools
import importlib
import os
import sys

from fire import Fire

import anomalo


class UsageError(Exception):
    pass


# Expects ANOMALO_INSTANCE_HOST and ANOMALO_API_SECRET_TOKEN to hold the auth and
# connection info
api_client = anomalo.Client()


Format = collections.namedtuple(
    "Format", ["pkg", "load", "load_args", "save", "save_args", "hint"]
)


class Encoder:
    ENCODERS = {
        "yaml": Format(
            pkg="yaml",
            load="safe_load",
            load_args=None,
            save="dump",
            save_args=None,
            hint='Install anomalo with "pip install anomalo[yaml]"',
        ),
        "json": Format(
            pkg="json",
            load="load",
            load_args=None,
            save="dump",
            save_args={"indent": 4, "sort_keys": True},
            hint=None,
        ),
    }

    def __init__(self, filename):
        self.filename = filename
        self.file_ext = os.path.splitext(filename)[1][1:]
        if self.file_ext not in self.ENCODERS:
            raise UsageError(
                f"Unsupported file type extension {self.file_ext}. "
                f"Supported extensions are: {', '.join(sorted(self.ENCODERS.keys()))}"
            )
        self.file_encoder = self.ENCODERS.get(self.file_ext)
        try:
            self.pkg = importlib.import_module(self.file_encoder.pkg)
        except ModuleNotFoundError as e:
            msg = (
                f'Package "{self.file_encoder.pkg}" for {self.file_ext} '
                "file type support was not found"
            )
            if self.file_encoder.hint:
                msg += os.linesep + f"Hint: {self.file_encoder.hint}"
            raise UsageError(msg) from e

    @property
    def load(self):
        return functools.partial(
            getattr(self.pkg, self.file_encoder.load),
            **(self.file_encoder.load_args or {}),
        )

    @property
    def save(self):
        return functools.partial(
            getattr(self.pkg, self.file_encoder.save),
            **(self.file_encoder.save_args or {}),
        )


def load(filename):
    encoder = Encoder(filename)
    with open(filename) as in_file:
        all_table_configs = encoder.load(in_file)
    for table_id, config in all_table_configs.items():
        print(f"Configuring table ID {table_id}")
        api_client.configure_table(**config)


def save(filename):
    encoder = Encoder(filename)
    all_table_configs = {}
    tables = api_client.configured_tables()
    for listed_table in tables:
        table_id = listed_table["table"]["id"]
        warehouse_id = listed_table["table"]["warehouse_id"]
        table = api_client.get_table_information(
            warehouse_id=warehouse_id, table_id=table_id
        )
        print(f"Retrieved table ID {table_id} ({listed_table['table']['full_name']})")
        all_table_configs[table_id] = table["config"]

    with open(filename, "w") as out_file:
        encoder.save(all_table_configs, out_file)


def main(action, filename="anomalo_tables.json"):
    actions = {
        "save": save,
        "load": load,
    }
    try:
        try:
            act = actions[action.lower()]
        except KeyError as e:
            raise UsageError(
                f'Invalid action "{action}". Choices are: '
                f"{', '.join(a.lower() for a in actions.keys())}"
            ) from e
        return act(filename)
    except UsageError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    Fire(main)
