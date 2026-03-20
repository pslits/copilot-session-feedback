"""pytest conftest — project-wide fixtures and path setup.

Keep this file import-free at module level so VS Code's unittest discoverer
(which does not run pytest's collection machinery) never fails on it.
Shared helper logic lives in helpers.py and is imported by test files directly.
"""
