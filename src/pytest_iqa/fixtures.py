"""PyTest fixtures."""
from typing import Optional

import pytest

from iqa.instance.instance import Instance
from iqa.utils.types import ComponentType, ReceiverSubtype, SenderSubtype

@pytest.yield_fixture(autouse=True)
def newline_before_logging(request):
    if request.config.getoption('capture') == 'no':
        print()  # new-line

@pytest.fixture()
def iqa(request) -> Instance:
    return request.config.iqa


def first_or_none(components: list) -> Optional[ComponentType]:
    """
    Returns first component provided or None
    :param components:
    :return:
    """
    if components:
        return components[0]
    return None


@pytest.fixture()
def router(iqa: Instance):
    """
    Returns the first Router instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_routers())


@pytest.fixture()
def java_receiver(iqa: Instance):
    """
    Returns the first Java Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(ReceiverSubtype, 'java'))


@pytest.fixture()
def java_sender(iqa: Instance):
    """
    Returns the first Java Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(SenderSubtype, 'java'))


@pytest.fixture()
def python_receiver(iqa: Instance):
    """
    Returns the first Python Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(ReceiverSubtype, 'python'))


@pytest.fixture()
def python_sender(iqa: Instance):
    """
    Returns the first Python Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(SenderSubtype, 'python'))


@pytest.fixture()
def nodejs_receiver(iqa: Instance):
    """
    Returns the first NodeJS Receiver instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(ReceiverSubtype, 'nodejs'))


@pytest.fixture()
def nodejs_sender(iqa: Instance):
    """
    Returns the first NodeJS Sender instance or None
    :param iqa:
    :return:
    """
    assert iqa
    return first_or_none(iqa.get_clients(SenderSubtype, 'nodejs'))
