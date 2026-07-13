"""
db_upgrade_safe.py — Workaround for Superset 1.4.x `NoInspectionAvailable` bug.

Why this exists
---------------
`superset db upgrade` invokes `flask.cli.with_appcontext` which does NOT push
an app context around `create_app()`. Superset 1.4.x's `create_app()` calls
`init_app()`, which runs `setup_db()` then `with app.app_context():
init_app_in_ctx() -> configure_fab() -> appbuilder.init_app(app, db.session)`.
Flask-AppBuilder's SecurityManager.__init__ runs
`self.session.get_bind(mapper=None, clause=None)`. On a cold-start (no
schema in the metadata DB), the greenlet-scoped session registry has not
been populated for the current greenlet, the fallback `SQLA.__init__()`
fires with `db.get_app()` returning None, and the chain ends with:

    sqlalchemy.exc.NoInspectionAvailable: No inspection system is available
    for object of type <class 'NoneType'>

Reproduces on every fresh deploy / volume swap on Railway.

Strategy
-------
The migration step is the one that's been observed failing in production.
Rather than fighting Superset's `create_app()` (which always runs the broken
path), we:

1. Build a *minimal* Flask app and load `superset_config.py` into it.
   This gives us a working `app.config["SQLALCHEMY_DATABASE_URI"]` without
   instantiating Flask-AppBuilder's SecurityManager. We then run Alembic
   migrations to head via `flask_migrate.upgrade()`. Idempotent — running
   on an already-migrated database is a no-op.
2. For `init` and `fab create-admin` we DO call Superset's `create_app()`,
   so the bug can still fire on a fresh DB with no schema. These calls
   are kept because:
   - On a redeploy with the schema already populated, they succeed
     cleanly.
   - On a cold-start deploy, they may fail; the calling bash script
     treats that as non-fatal and the web server retries lazily on the
     first request.
   - The migration step is the gating dependency — if it succeeds,
     everything else eventually catches up.
CLI flags
---------
--upgrade-only   Run Alembic migrations only.
--init-only      Run `superset init` only.
--admin-only     Run `superset fab create-admin` only.
--all            Run upgrade + init + admin (default).

Exit codes
----------
0 success, 1 on unrecoverable error.
"""

from __future__ import annotations

import os
import sys
import traceback
from typing import Any


def _log(msg: str) -> None:
    print(f"[db_upgrade_safe] {msg}", flush=True)


def _build_minimal_app() -> Any:
    """Build a minimal Flask app loaded with `superset_config.py`.

    This bypasses Superset's `create_app()` and gives us just enough Flask
    machinery to run Alembic migrations against the configured metadata
    database, without instantiating Flask-AppBuilder (which is where the
    cold-start bug lives).
    """
    from flask import Flask
    from flask_migrate import Migrate
    from flask_sqlalchemy import SQLAlchemy

    config_path = os.environ.get(
        "SUPERSET_CONFIG_PATH", "/app/superset_config.py"
    )
    _log(f"Loading config from {config_path}")
    import importlib.util

    spec = importlib.util.spec_from_file_location("superset_user_config", config_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load config from {config_path}")
    user_cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_cfg)

    app = Flask("superset_safe_upgrade")
    # Apply the user config keys we need. We don't want every key — only
    # the SQLAlchemy-related ones — to avoid pulling in app-builder state.
    for key in (
        "SQLALCHEMY_DATABASE_URI",
        "SQLALCHEMY_BINDS",
        "SQLALCHEMY_TRACK_MODIFICATIONS",
        "SQLALCHEMY_ENGINE_OPTIONS",
        "SQLALCHEMY_ECHO",
        "SQLALCHEMY_NATIVE_UNICODE",
        "SQLALCHEMY_POOL_SIZE",
        "SQLALCHEMY_POOL_TIMEOUT",
        "SQLALCHEMY_POOL_RECYCLE",
        "SQLALCHEMY_MAX_OVERFLOW",
    ):
        if hasattr(user_cfg, key):
            app.config[key] = getattr(user_cfg, key)

    db = SQLAlchemy(app)
    # Alembic migrations live inside the installed apache-superset package.
    import superset

    migrations_dir = os.path.join(
        os.path.dirname(superset.__file__), "migrations"
    )
    _log(f"Alembic migrations directory: {migrations_dir}")
    Migrate(app, db, directory=migrations_dir)
    return app, db


def _run_alembic_upgrade() -> None:
    """Build a minimal app, push a context, run Alembic to head."""
    app, db = _build_minimal_app()
    with app.app_context():
        engine = db.engine
        _log(
            "SQLAlchemy engine: "
            f"{engine.url.render_as_string(hide_password=True)}"
        )
        from flask_migrate import upgrade as alembic_upgrade

        _log("Running Alembic upgrade() to head...")
        alembic_upgrade()
        _log("Alembic upgrade() complete.")


def _run_superset_cli(subcommand: str, args: list[str]) -> None:
    """Run a Superset CLI command via FlaskGroup, but inside our app context.

    This avoids the upstream bug because we already have an app context
    pushed when `appbuilder.init_app` runs.
    """
    from flask.cli import FlaskGroup

    flask_app = os.environ.get("FLASK_APP", "superset.app:create_app()")
    if ":" not in flask_app:
        raise RuntimeError(
            f"FLASK_APP must be in module:attr form (got {flask_app!r})"
        )
    module_name, attr_name = flask_app.split(":", 1)
    import importlib

    factory = getattr(importlib.import_module(module_name), attr_name)
    app = factory()

    with app.app_context():
        cli = FlaskGroup(app=app)
        cli.main([subcommand, *args])


def _run_superset_init() -> None:
    """Seed default roles, permissions, and menu."""
    _log("Seeding roles and permissions (superset init)...")
    _run_superset_cli("init", [])
    _log("`superset init` complete.")


def _run_fab_create_admin() -> None:
    """Create the default admin user via Flask-AppBuilder.

    Idempotent: FAB create_admin raises on existing user; we swallow that.
    """
    username = os.environ.get("ADMIN_USERNAME")
    password = os.environ.get("ADMIN_PASSWORD")
    email = os.environ.get("ADMIN_EMAIL")
    if not (username and password and email):
        _log(
            "ADMIN_USERNAME/ADMIN_PASSWORD/ADMIN_EMAIL not all set; "
            "skipping admin creation"
        )
        return

    firstname = os.environ.get("ADMIN_FIRSTNAME", "Superset")
    lastname = os.environ.get("ADMIN_LASTNAME", "Admin")
    _log(f"Creating admin user {username!r}...")
    try:
        _run_superset_cli(
            "fab",
            [
                "create-admin",
                "--username",
                username,
                "--firstname",
                firstname,
                "--lastname",
                lastname,
                "--email",
                email,
                "--password",
                password,
            ],
        )
        _log(f"Admin user {username!r} created.")
    except SystemExit as exc:
        if exc.code not in (None, 0):
            _log(
                f"Admin user {username!r} likely already exists "
                f"(exit={exc.code})."
            )


def _parse_args(argv: list[str]) -> dict[str, bool]:
    flags = {
        "upgrade_only": False,
        "init_only": False,
        "admin_only": False,
        "all": False,
    }
    for arg in argv:
        if arg == "--upgrade-only":
            flags["upgrade_only"] = True
        elif arg == "--init-only":
            flags["init_only"] = True
        elif arg == "--admin-only":
            flags["admin_only"] = True
        elif arg == "--all":
            flags["all"] = True
    if not any(flags.values()):
        flags["all"] = True
    return flags


def main() -> int:
    flags = _parse_args(sys.argv[1:])
    try:
        if flags["all"] or flags["upgrade_only"]:
            _run_alembic_upgrade()

        if flags["all"] or flags["init_only"]:
            try:
                _run_superset_init()
            except Exception as init_exc:
                _log(
                    f"WARNING: superset init seeding failed (non-fatal): "
                    f"{init_exc!r}"
                )

        if flags["all"] or flags["admin_only"]:
            _run_fab_create_admin()

        _log("OK")
        return 0
    except SystemExit as exc:
        return int(exc.code or 0)
    except Exception:
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
