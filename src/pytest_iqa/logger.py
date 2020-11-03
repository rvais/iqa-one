"""Provide a common interface to the `logging` module."""

from logging import getLogger, Logger, NullHandler


def get_logger(name: str) -> Logger:
    """Return an initialized logger."""
    log: Logger = getLogger(name)
    log.addHandler(NullHandler())
    return log
