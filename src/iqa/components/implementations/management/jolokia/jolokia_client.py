"""
Generic client for communicating with Jolokia API through POST requests.
"""

import copy
import json
import logging

from typing import TYPE_CHECKING
from iqa.components.abstract.component import Component
from iqa.components.abstract.management.broker import ManagementBroker
from iqa.system.command.command_http import CommandHTTP

import requests
from requests import RequestException, Response

from iqa.system.executor.executor_factory import ExecutorFactory

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional, List, Type, Union
    from iqa.system.executor.http.executor_http import ExecutorBase
    from iqa.system.executor.base.execution import ExecutionBase


class ArtemisJolokiaClient(Component, ManagementBroker):
    """
    Provides a generic mechanism to query Jolokia API exposed by ActiveMQ Artemis.
    """

    @property
    def implementation(self):
        return "jolokia"

    def __init__(
            self,
            broker_name: str,
            hostname_or_ip: str,
            port: 'Optional[Union[int, str]]' = None,  # 8161
            user: 'Optional[str]' = 'admin',
            password: 'Optional[str]' = 'admin'
    ) -> None:
        # Internal only
        self._host: Optional[str] = hostname_or_ip
        self._port: str = port
        self._user: str = user
        self._password: str = password
        self._executor: ExecutorBase = ExecutorFactory.create_executor("http")

        # Request url
        self._url: str
        if port is not None:
            self._url = 'http://%s:%s/console/jolokia' % (self._host, self._port)

        # Request info (generic)
        self.type: str = 'exec'
        self.mbean: str = 'org.apache.activemq.artemis:broker="%s"' % broker_name

    def list_queues(
            self, queue_name: str = '', exact: bool = False
    ) -> 'List[str]':
        """
        Calls listQueues operation and returns queues matching filtering arguments
        through the data property of the returned object.
        :param queue_name:
        :param exact:
        :rtype: ArtemisJolokiaClientResult
        :return:
        """
        filter = {'field': 'NAME',
                     'operation': '"CONTAINS" if not exact else "EQUALS"',
                     "value": "queue_name"
                     }

        args = [
            ('type', self.type),
            ('mbean', self.mbean),
            ('operation', 'listQueues(java.lang.String,int,int)'),
            ('arguments', [json.dump(filter), 1, 100]),
        ]
        request: CommandHTTP = CommandHTTP(args=args, method_post=True, url=self._url)
        return

    def list_addresses(
            self, address_name: str = '', exact: bool = False
    ) -> 'List[str]':
        """
        Calls listAddresses operation and returns addresses matching filtering arguments
        through the data property of the returned object.
        :param address_name:
        :param exact:
        :return:
        """
        request: ArtemisJolokiaClient = copy.copy(self)
        request.operation = 'listAddresses(java.lang.String,int,int)'
        filter_operation: str = '"CONTAINS" if not exact else "EQUALS"'
        request.arguments = [
            '{"field": "NAME", "operation": "%s", "value": "%s"}'
            % (filter_operation, address_name),
            1,
            100,
        ]
        return self._get_all_pages(request, 1)

    def delete_address(
            self, name: str, force: bool = False
    ) -> bool:
        """
        Deletes the given address.
        :param name: Address name
        :param force: Force address removal
        :return:
        """
        request: ArtemisJolokiaClient = copy.copy(self)
        request.operation = 'deleteAddress(java.lang.String,boolean)'
        request.arguments = [name, force]
        return self._execute(request)

    def delete_queue(
            self, name: str, remove_consumers: bool = False
    ) -> bool:
        """
        Deletes the given queue.
        :param name: Queue name
        :param remove_consumers: Whether or not to remove connected consumers.
        :return:
        """
        request: ArtemisJolokiaClient = copy.copy(self)
        request.operation = 'destroyQueue(java.lang.String,boolean)'
        request.arguments = [name, remove_consumers]
        return self._execute(request)

    def create_address(
            self, name: str, routing_type: str = 'ANYCAST'
    ) -> bool:
        """
        Creates a new address
        :param name:
        :param routing_type:
        :return:
        """
        request: ArtemisJolokiaClient = copy.copy(self)
        request.operation = 'createAddress(java.lang.String,java.lang.String)'
        request.arguments = [name, routing_type]
        return self._execute(request)

    def create_queue(
            self,
            address_name: str,
            queue_name: str,
            durable: bool = True,
            routing_type: str = 'ANYCAST',
    ) -> bool:
        """
        Creates a new queue nested to the provided Address
        :param address_name:
        :param queue_name:
        :param durable:
        :param routing_type:
        :return:
        """
        request: ArtemisJolokiaClient = copy.copy(self)
        request.operation = (
            "createQueue(java.lang.String,java.lang.String,boolean,java.lang.String)"
        )
        request.arguments = [address_name, queue_name, durable, routing_type]
        return self._execute(request)

    def _get_all_pages(
            self, request, page_arg_index: int
    ):
        """
        Common private method to retrieve paged results from Jolokia API.
        :param request:
        :param page_arg_index:
        :return:
        """

        all_data: list = []
        # result: ArtemisJolokiaClientResult = ArtemisJolokiaClientResult()

        # Process all pages
        while True:
            result = self._execute(request)

            # If something wrong happened, stop processing
            if result.error:
                break

            json_res = result.response.json()

            # Expect 'value' key to be present
            if "value" not in json_res:
                break

            # Returned value must have count and data
            value = json.loads(json_res['value'])
            total_queues = value['count']
            all_data.extend(value['data'])

            # In case all queues retrieve, skip
            if total_queues == 0 or total_queues == len(all_data):
                break

            # Increase page size and execute again
            request.arguments[page_arg_index] += 1

        if all_data and result:
            result.data = all_data

        return result
