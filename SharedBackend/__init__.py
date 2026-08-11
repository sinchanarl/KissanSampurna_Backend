"""Lightweight shim for missing SharedBackend submodule.

This package provides minimal classes required by the backend during
development so the project can run without the full `BackendServicesShared`
submodule. Replace with the real submodule when available.
"""

__all__ = ["managers"]
