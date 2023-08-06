import unittest


class Test0101(unittest.TestCase):
    def test_data(self) -> None:
        from lib import data
        from torchvision import datasets, transforms

        # test batched decorator
        @data.batched
        def mnist():
            compose = transforms.Compose([transforms.ToTensor()])
            return datasets.MNIST("~/Downloads/MNIST", transform=compose, train=False, download=True)
        mnist_dataset = mnist(batch_size=1024, drop_last=True, shuffle=True)

        # loop for each data
        for x, y in mnist_dataset:
            # test batch size
            self.assertEqual(len(x), 1024)
            self.assertEqual(len(y), 1024)

    def test_import(self) -> None:
        import core
        import lib as torchmanager

        api_version = core.API_VERSION
        current_version = torchmanager.version
        self.assertGreaterEqual(current_version, "v1.1")
        self.assertEqual(api_version, "v1.1")

    def test_sliding_window(self) -> None:
        import torch
        from lib import data

        x = torch.randn((3, 224, 224))
        slided_img = data.sliding_window(x, (64, 64), stride=(32, 32))
        self.assertEqual(len(slided_img), 36)
