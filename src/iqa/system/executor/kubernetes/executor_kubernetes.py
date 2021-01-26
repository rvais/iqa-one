import os

from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.kubernetes.execution_kubernetes import ExecutionKubernetes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from iqa.system.command.command_base import CommandBase


class ExecutorKubernetes(ExecutorBase):
    """
    Executor that can be used to run Commands in a Pod running on a Kubernetes cluster.
    This Executor uses the ExecutionKubernetes to run commands through the Kubernetes Client API.
    """

    def __init__(self, **kwargs) -> None:
        """
        :param kwargs:
            :keyword executors_kubernetes_config:
                Kubernetes config file (Default: $HOME/.kube/config).
            :keyword executor_kubernetes_namespace:
                Namespace to use when querying for POD to run your command (Default: default)
            :keyword executor_kubernetes_selector:
                The selector that can be used to identify the pod or deployment containing Pods.
            :keyword executor_kubernetes_context:
                If your client credentials are already defined in your config file, provide the context name.
            :keyword executor_kubernetes_host:
                If you do not want to use a context, you can provide the host (URL) for your cluster.
                The `executor_kubernetes_token` is also required if you are not using a context.
                Example: 'https://192.168.42.99:8443'
            :keyword executor_kubernetes_token:
                If you do not want to use a context, you can provide a valid Token to use for authentication
                and authorization. The `executor_kubernetes_host` is also required when a token is defined.
        """
        super(ExecutorKubernetes, self).__init__(**kwargs)
        self._name: str = 'Kubernetes executor class'

        # Kubernetes config file - defaults to $HOME/.kube/config
        self.config: str = kwargs.get(
            'executor_kubernetes_config', os.environ['HOME'] + os.sep + '.kube/config'
        )

        # Namespace to use for querying PODs
        self.namespace: str = kwargs.get('executor_kubernetes_namespace', 'default')

        #
        # You can provide the context to use (stored in the config file) if you don't
        # want to use host and token for authorization
        #

        # Context to use from kubernetes config (if not using current context or a host/token)
        self.context: str = kwargs.get('executor_kubernetes_context', None)

        #
        # When you do not want to use a context, you can also use a host/token pair
        #

        # Host (if not using context)
        self.host: str = kwargs.get('executor_kubernetes_host', None)

        # Token (if not using context)
        self.token: str = kwargs.get('executor_kubernetes_token', None)

        # Selector to match deployment pod that will be used for execution.
        # If your selector returns multiple pods, only the first matching one will be used.
        self.selector: str = kwargs.get('executor_kubernetes_selector', None)

    @staticmethod
    def implementation() -> str:
        return 'kubernetes'

    def _execute(self, command: 'CommandBase'):
        return ExecutionKubernetes(command, self)
