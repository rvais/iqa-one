from typing import TYPE_CHECKING

from iqa.system.executor.base.execution import ExecutionBase

if TYPE_CHECKING:
    from typing import Optional, Union, List


class ExecutionAsyncSsh(ExecutionBase):
    def _run(self) -> None:
        raise NotImplemented

    def wait(self) -> None:
        raise NotImplemented

    def is_running(self) -> bool:
        raise NotImplemented

    def completed_successfully(self) -> bool:
        raise NotImplemented

    def on_timeout(self) -> None:
        raise NotImplemented

    def terminate(self) -> None:
        raise NotImplemented

    def read_stdout(self, lines: bool = False, closefd: bool = True) -> 'Optional[Union[str, List[str]]]':
        raise NotImplemented

    def read_stderr(self, lines: bool = False, closefd: bool = True) -> 'Optional[Union[str, List[str]]]':
        raise NotImplemented
