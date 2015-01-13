import unittest
import mock
from planout import optimizely
from planout.optimizely.experiment import OptimizelyExperiment

class TestOptimizelyExperiment(unittest.TestCase):

    def test_disabled_experiment_assignment(self):
        optimizely.project = {
            'id': 123,
            'data': {
                "experiments": {
                    "1900280067": {
                        "enabled": False,
                    }
                }
            }
        }
        optimizely_experiment = OptimizelyExperiment(1900280067)
        optimizely_experiment.log = mock.Mock()
        self.assertEqual(False, optimizely_experiment.in_experiment)
        self.assertEqual(optimizely_experiment.get_params(), {})
        self.assertIsNone(optimizely_experiment.get('foo'))
        self.assertEqual('bar', optimizely_experiment.get('foo', 'bar'))
        self.assertFalse(optimizely_experiment.log.called)

    def test_enabled_experiment_assignment(self):
        optimizely.project = {
            'id': 123,
            'data': {
                "experiments": {
                    "1900280067": {
                        "enabled": True,
                        "enabled_variation_ids": [1898810050],
                        "variations": {
                            "1898810050": {
                                "weight": 6000,
                                "planout_script": "{\"op\":\"seq\",\"seq\":[{\"op\":\"set\",\"var\":\"a\",\"value\":1},{\"op\":\"set\",\"var\":\"b\",\"value\":2}]}"
                            }
                        }
                    }
                }
            }
        }
        optimizely_experiment = OptimizelyExperiment(1900280067)
        optimizely_experiment.log = mock.Mock()

        self.assertEqual(1898810050, optimizely_experiment.get('_variation_id'))
        self.assertEqual(True, optimizely_experiment.in_experiment)
        self.assertEqual(1, optimizely_experiment.get('a'))
        self.assertEqual(2, optimizely_experiment.get('b'))
        self.assertTrue(optimizely_experiment.log.called)

    def test_incorrectly_configured_weight_assignment(self):
        optimizely.project = {
            'id': 123,
            'data': {
                "experiments": {
                    "1900280067": {
                        "enabled": True,
                        "enabled_variation_ids": [1898810050,1904270032],
                        "variations": {
                            "1898810050": {
                                "weight": -3,
                                "planout_script": "{\"op\":\"seq\",\"seq\":[{\"op\":\"set\",\"var\":\"a\",\"value\":1},{\"op\":\"set\",\"var\":\"b\",\"value\":2}]}"
                            },
                            "1904270032": {
                                "weight": 0,
                                "planout_script": "{\"op\":\"seq\",\"seq\":[{\"op\":\"set\",\"var\":\"a\",\"value\":11},{\"op\":\"set\",\"var\":\"b\",\"value\":12}]}"
                            }
                        }
                    }
                }
            }
        }
        optimizely_experiment = OptimizelyExperiment(1900280067)
        optimizely_experiment.log = mock.Mock()
        self.assertEqual(None, optimizely_experiment.get('_variation_id'))
        self.assertEqual(False, optimizely_experiment.in_experiment)
        self.assertIsNone(optimizely_experiment.get('foo'))
        self.assertEqual('bar', optimizely_experiment.get('foo', 'bar'))
        self.assertFalse(optimizely_experiment.log.called)

    def test_invalid_experiment_assignment(self):
        optimizely.project = {
            'id': 123,
            'data': {
                "experiments": {
                    "1900280067": {
                        "enabled": True,
                    }
                }
            }
        }
        optimizely_experiment = OptimizelyExperiment(1900280060)
        optimizely_experiment.log = mock.Mock()
        self.assertEqual(optimizely_experiment.get_params(), {})
        self.assertEqual(False, optimizely_experiment.in_experiment)
        self.assertIsNone(optimizely_experiment.get('foo'))
        self.assertEqual('bar', optimizely_experiment.get('foo', 'bar'))
        self.assertFalse(optimizely_experiment.log.called)

if __name__ == '__main__':
    unittest.main()