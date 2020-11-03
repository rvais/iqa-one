"""PyTest Ansible Plugin
Defines mandatory options and configuration that can be applied to all test suites.
"""

import atexit
import os
from logging import Logger

from pytest import mark

from _pytest.config.argparsing import Parser, OptionGroup
from _pytest.python import Function

from iqa.instance.instance import Instance
from .logger import get_logger

# Default timeout settings

CLIENTS_TIMEOUT: int = 60
DEFAULT_LOG_FORMAT: str = '%(asctime)s [%(levelname)s] (%(pathname)s:%(lineno)s) - %(message)s'
DEFAULT_LOG_DATE_FORMAT: str = '%Y-%m-%d %H:%M:%S'
cleanup_file_list: list = []

# linting
# (iqa)

log: Logger = get_logger(__name__)


def pytest_addoption(parser: Parser) -> None:
    """Add options to control ansible."""
    log.debug('pytest_addoption() called')

    group: OptionGroup = parser.getgroup('pytest-iqa')
    group.addoption(
        '--inventory',
        action='store',
        dest='inventory',
        required=False,
        metavar='INVENTORY',
        help='Inventory file to use',
    )

    # Default values for pytest.ini files (if absent)
    parser.addini(
        'log_level',
        default='WARNING',
        type=None,
        help='logging level used by the logging module',
    )

    parser.addini(
        'log_format',
        default=DEFAULT_LOG_FORMAT,
        type=None,
        help='log format as used by the logging module.',
    )

    parser.addini(
        'log_date_format',
        default=DEFAULT_LOG_DATE_FORMAT,
        type=None,
        help='log date format as used by the logging module.',
    )

    parser.addini(
        'log_cli',
        default=True,
        type='bool',
        help='enable log display during test run (also known as "live logging").',
    )


def cleanup_files() -> None:
    """
    Remove temporary files.
    :return:
    """
    for f in cleanup_file_list:
        os.unlink(f)


def pytest_configure(config) -> None:
    """
    Loads IQA instance based on provided environment and extra command line args.
    All arguments will be available as variables that can be used inside the inventory.
    The same can be done when using Ansible CLI (using -e cli_arg=value).
    :param config:
    :return:
    """

    # Adding all arguments as environment variables, so child executions of Ansible
    # will be able to use the same variables.
    options: dict = dict(config.option.__dict__)

    # Insert array elements with _0, _1, such as --router 1.1.1.1 and --router 2.2.2.2
    # would become: router_0: 1.1.1.1 and router_1: 2.2.2.2
    new_options: dict = dict()
    for (key, value) in options.items():
        if not isinstance(value, list):
            continue
        for n in range(len(value)):
            new_options.update({'%s_%d' % (key, n): str(value[n])})

    options.update(new_options)
    options = {
        key: str(value) for (key, value) in options.items() if key not in os.environ
    }
    os.environ.update(options)

    # Loading the inventory
    iqa: Instance = Instance(
        inventory=config.getvalue('inventory'), cli_args=config.option.__dict__
    )

    # Adjusting clients timeout
    for client in iqa.clients:
        client.command.control.timeout = CLIENTS_TIMEOUT  # type: ignore

    config.iqa = iqa

    # Register some markers for tests' requirements
    config.addinivalue_line("markers", "component(name): Test requires <name> / <type> of component to be able to run. "
                                       "A 'Broker' for example or more specifically 'artemis'.")
    config.addinivalue_line("markers", "components(name, count): Test requires number <count> of <name> / <type> "
                                       "components to be able to run. Five or 'broker' type components for example.")

    # Clean up temporary files at exit
    atexit.register(cleanup_files)


def pytest_collection_modifyitems(config, items) -> None:
    """
    Hook which is supposed to skip the tests that can't be run due to missing
    deployment or component in that deployment
    :param config:
    :param items:
    :return:
    """
    skip_marker = mark.skip(reason="Inventory containing items needed by the test is ")
    iqa = config.iqa  # type: Instance
    for item in items:

        # filter list of types of components based on 'component' marker(s)
        required = [marker.args[0] for marker in item.iter_markers(name="component")]
        # filter and append list of tuples containing types and counts of components based on 'components' marker(s)
        required.append([(marker.args[0], marker.args[1]) for marker in item.iter_markers(name="components")])

        for rc in required:  # rc - required component
            # 'component' marker has only name so default number of these components is 1
            count = 1
            if isinstance(rc, tuple):
                rc, count = rc

            available = [
                component for component in iqa.components if isinstance(component, rc)
            ]

            # if there is lesser number then required count of some type of component, mark test to be skipped
            if available < count:
                item.add_marker(skip_marker)
            break
    return


def pytest_runtest_call(item: Function) -> None:
    """
    Hook that runs before each test method and can iterate through
    parametrized items adding a generic "param:<argname>':"<argvalue>"
    to the user_properties dictionary.

    When generating a junit xml, these params will be added as "<property>"
    elements for each test case.

    If test method takes no parameter, then nothing will be added.
    :param item:
    :return:
    """

    if not hasattr(item, 'callspec'):
        return

    for (argname, argvalue) in item.callspec.params.items():
        item.user_properties.append(('param:%s' % argname, argvalue))
