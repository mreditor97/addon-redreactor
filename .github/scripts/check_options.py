"""Check the app's options schema against the redreactor service it installs.

Every limit in the schema (the ends of each `int(...)` and `float(...)` range,
and each `list(...)` choice) is set in turn on top of the default options,
turned into the service's configuration the way the app's run script does,
and loaded with redreactor's own configuration checks. A value the schema lets
through but the service refuses would stop the app at start, so it fails here
instead.

Run with the redreactor version the app installs, for example:

    pip install -r redreactor/requirements-edge.txt pyyaml
    python .github/scripts/check_options.py redreactor/config.yaml
"""

from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml
from redreactor.configuration import ConfigurationError, LinkedConfiguration

RANGE = re.compile(r"^(int|float)\((-?[\d.]*),(-?[\d.]*)\)\??$")
CHOICES = re.compile(r"^list\((.+)\)\??$")


def limits(schema: Any, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    """Return each (option path, value) at the edge of the schema."""
    found: list[tuple[tuple[str, ...], Any]] = []
    if isinstance(schema, dict):
        for key, value in schema.items():
            found += limits(value, (*path, key))
    elif isinstance(schema, str):
        if match := RANGE.match(schema):
            kind = int if match[1] == "int" else float
            found += [(path, kind(end)) for end in match.groups()[1:] if end]
        elif match := CHOICES.match(schema):
            # The Supervisor passes a choice as text
            found += [(path, choice) for choice in match[1].split("|")]
    # Lists of options, such as the battery curve, are checked by redreactor's
    # own tests
    return found


def service_configuration(options: dict[str, Any]) -> dict[str, Any]:
    """Turn the app options into the service's configuration, as `run` does."""
    configuration = copy.deepcopy(options)
    configuration.setdefault("mqtt", {})["exit_on_fail"] = False
    battery = configuration.get("battery", {})
    if battery.get("curve"):
        battery["curve"] = [[point["voltage"], point["level"]] for point in battery["curve"]]
    else:
        battery.pop("curve", None)
    return configuration


def set_option(options: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    """Set one option, creating the sections on the way."""
    section = options
    for key in path[:-1]:
        section = section.setdefault(key, {})
    section[path[-1]] = value


def main() -> int:
    """Check every limit, and print each one the service refuses."""
    app = yaml.safe_load(Path(sys.argv[1]).read_text())
    failures = 0
    checked = 0
    with tempfile.TemporaryDirectory() as folder:
        for path, value in limits(app["schema"]):
            options = copy.deepcopy(app["options"])
            set_option(options, path, value)
            configuration_file = Path(folder) / "config.json"
            configuration_file.write_text(json.dumps(service_configuration(options)))
            database = Path(folder) / "database.db"
            database.unlink(missing_ok=True)
            checked += 1
            try:
                LinkedConfiguration(str(configuration_file), str(database))
            except ConfigurationError as error:
                failures += 1
                print(f"{'.'.join(path)}: {value!r} is allowed by the schema but refused: {error}")

    print(f"Checked {checked} schema limits, {failures} refused")
    return 1 if failures or not checked else 0


if __name__ == "__main__":
    sys.exit(main())
