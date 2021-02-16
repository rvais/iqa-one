import os

from iqa.system.executor.base.executor import ExecutorBase
from iqa.system.executor.kubernetes.execution_kubernetes import ExecutionKubernetes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike
    from typing import Optional, Dict, Union
    from iqa.system.command.command_base import CommandBase


class ExecutorKubernetes(ExecutorBase):
    """
    Executor that can be used to run Commands in a Pod running on a Kubernetes cluster.
    This Executor uses the ExecutionKubernetes to run commands through the Kubernetes Client API.
    """

    def __init__(
        self,
        host: 'Optional[str]' = None,
        port: 'Optional[int]' = None,
        user: 'Optional[str]' = None,
        password: 'Optional[str]' = None,
        ssh_key_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        ssh_key_passphrase: 'Optional[Union[str, bytes, PathLike]]' = None,
        known_hosts_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        kubernetes_config_path: 'Optional[Union[str, bytes, PathLike]]' = None,
        kubernetes_namespace: 'Optional[str]' = None,
        kubernetes_context: 'Optional[str]' = None,
        kubernetes_token: 'Optional[str]' = None,
        kubernetes_selector: 'Optional[str]' = None,
        **kwargs
    ) -> None:
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
        args: Dict = locals()
        del args["self"]
        del args["kwargs"]
        del args["__class__"]
        kwargs.update(args)
        super(ExecutorKubernetes, self).__init__(**kwargs)

        missing = self._check_required_args(['host'], **kwargs)
        if missing:
            raise ValueError(f"One or more mandatory arguments are missing: [{ ', '.join(missing)}]")

        # Kubernetes config file - defaults to $HOME/.kube/config
        self._config_path: 'Optional[Union[str, bytes, PathLike]]' = args.get(
            'kubernetes_config_path', os.environ['HOME'] + os.sep + '.kube/config'
        )

        # Namespace to use for querying PODs
        self._namespace: 'Optional[str]' = args.get('kubernetes_namespace', 'default')

        #
        # You can provide the context to use (stored in the config file) if you don't
        # want to use host and token for authorization
        #

        # Context to use from kubernetes config (if not using current context or a host/token)
        self._context: 'Optional[str]' = kubernetes_context

        #
        # Token if you are not using the context
        # When you do not want to use a context, you can also use a host/token pair
        # host must be specified if not using context
        #
        self._token: 'Optional[str]' = kubernetes_token

        # Selector to match deployment the pod which will be used for execution.
        # If your selector returns multiple pods, only the first one matching will be used.
        self._selector: 'Optional[str]' = kubernetes_selector

    @staticmethod
    def implementation() -> str:
        return 'kubernetes'

    def _execute(self, command: 'CommandBase'):
        return ExecutionKubernetes(command, self)
