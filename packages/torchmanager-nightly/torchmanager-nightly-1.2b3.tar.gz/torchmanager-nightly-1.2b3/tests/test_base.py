import unittest


class TestBase(unittest.TestCase):
    def test_import(self, target_version: str = "v1.0") -> None:
        import core, lib as torchmanager

        current_version = core.VERSION
        self.assertGreaterEqual(current_version, target_version)