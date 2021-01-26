import pytest
import logging
from iqa.instance.instance import Instance as IQA

test_logger = logging.getLogger(__name__)


class TestIQAinstanceInventory:

    def test_inventory(self) -> None:
        iqa = IQA('/home/rvais/Projects/IQA/custom/iqa-one/tests/inventory/inventory.yml')
        assert iqa.components.count() > 0
