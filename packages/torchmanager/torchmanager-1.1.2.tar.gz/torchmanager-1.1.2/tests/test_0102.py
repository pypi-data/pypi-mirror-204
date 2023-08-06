import unittest


class Test0102(unittest.TestCase):
    def test_config(self) -> None:
        import shutil
        from lib.configs import Configs as _Configs

        class Configs(_Configs):
            def show_settings(self) -> None:
                print(f"Experiment: name={self.experiment}, replace_experiment={self.replace_experiment}")

        configs = Configs.from_arguments("-exp", "unittest", "--replace_experiment")
        self.assertEqual(configs.experiment, "unittest.exp")
        shutil.rmtree("experiments")

    def test_import(self) -> None:
        import core
        import lib as torchmanager

        current_version = core.API_VERSION
        self.assertGreaterEqual(current_version, "v1.2")

    def test_random(self):
        from torchmanager_core import random

        seed = 0
        random.freeze_seed(seed)
        new_seed = random.unfreeze_seed()
        self.assertNotEqual(seed, new_seed)
