"""Minimal smoke test: verify the package imports and CLI is wired correctly.

We do NOT download a model in CI (too slow, too big). The actual end-to-end
test against a real GGUF lives in `tests/test_e2e.py` and is opt-in via env var.
"""
import subprocess
import sys


def test_package_imports():
    """The main module must be importable without NameError."""
    import gguf2mlx  # noqa: F401
    from gguf2mlx import gguf2mlx as core
    # Verify the previously-missing imports are present at module level
    assert hasattr(core, "gc"), "gc import was missing — see PR description"
    assert hasattr(core, "warnings"), "warnings import was missing — see PR description"


def test_cli_help():
    """`gguf2mlx --help` should exit 0 and print usage."""
    result = subprocess.run(
        [sys.executable, "-m", "gguf2mlx", "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"--help failed: {result.stderr}"
    assert "input" in result.stdout.lower() or "gguf" in result.stdout.lower()
