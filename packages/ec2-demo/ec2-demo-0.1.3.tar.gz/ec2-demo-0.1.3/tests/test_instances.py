from unittest import TestCase, mock

from ec2_demo.instances import Instances


class TestInstances(TestCase):

    @mock.patch("ec2_demo.instances.Instances.create")
    def test_create(self, mocked):
        expected = ["i-created"]
        mocked.return_value = expected
        instances = Instances("dev")
        returned = instances.create("instances/demo.yaml")
        self.assertEqual(expected, returned)


    @mock.patch("ec2_demo.instances.Instances.delete")
    def test_delete(self, mocked):
        expected = ["i-deleted"]
        mocked.return_value = expected
        instances = Instances("dev")
        returned = instances.delete("nobody-reads-this")
        self.assertEqual(expected, returned)


if __name__ == "__main__":
    unittest.main()
