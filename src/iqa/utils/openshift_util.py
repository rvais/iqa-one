#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License
#

"""
Utility class to help executing OpenShift standard operations
"""
import logging
from typing import TYPE_CHECKING

from iqa.system.command.command_base import CommandBase

if TYPE_CHECKING:
    from iqa.system.executor.base.executor import ExecutorBase
    from iqa.system.executor.base.execution import ExecutionBase


class OpenShiftUtil:
    """
    Helper class that helps executing standard operations through the "oc" cli.
    """

    TIMEOUT: int = 30

    def __init__(self, executor: 'ExecutorBase', url: str, token: str) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__module__)
        self.executor: ExecutorBase = executor
        self.url: str = url
        self.token: str = token

    @staticmethod
    def login_first(func):
        """
        Decorator used to enforce a oc login will be issued before another command.
        :return:
        """

        def wrap(*args, **kwargs):
            instance = args[0]
            assert instance.login().completed_successfully()
            return func(*args, **kwargs)

        return wrap

    def login(self, timeout=TIMEOUT) -> 'ExecutionBase':
        """
        Log in to the defined OpenShift URL using the related token.
        It waits for a max of "timeout" seconds before timing out.
        :param timeout:
        :return: The execution result.
        """
        cmd_login = CommandBase(
            args=[
                'oc',
                'login',
                self.url,
                '--token',
                '%s' % self.token,
                '--insecure-skip-tls-verify=true',
            ],
            timeout=timeout,
            stderr=True,
            stdout=True,
        )
        execution: ExecutionBase = await self.executor.execute(cmd_login)
        execution.wait()
        if not execution.completed_successfully():
            self._logger.debug(
                'Login has failed against %s: %s' % (self.url, execution.read_stdout())
            )
        return execution

    @login_first
    def scale(self, replicas: int, deployment: str) -> 'ExecutionBase':
        """
        Perform oc scale, setting the number of replicas provided for the given deployment name.
        It enforces that the "oc login" is executed first.
        :param replicas:
        :param deployment:
        :return: The execution result.
        """
        cmd_scale_up = CommandBase(
            args=['oc', 'scale', '--replicas=%d' % replicas, 'dc', deployment],
            timeout=30,
            stderr=True,
            stdout=True,
        )
        execution: ExecutionBase = await self.executor.execute(cmd_scale_up)
        execution.wait()
        if not execution.completed_successfully():
            self._logger.debug(
                'Scaling deployment %s (replicas: %d) failed: %s'
                % (deployment, replicas, execution.read_stderr())
            )
        return execution
