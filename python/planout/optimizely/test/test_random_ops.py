import unittest
from planout.optimizely.ops.random import OptimizelyWeightedChoice

class TestOptimizelyRandomOperators(unittest.TestCase):

    def setUp(self):
      experiment_id = 1886780721
      self.tests = [{
          'ppid': 'ppid1',
          'experiment_id': experiment_id,
          'expect': 5254
        }, {
          'ppid': 'ppid2',
          'experiment_id': experiment_id,
          'expect': 4299
        }, {
          'ppid': 'ppid2',
          'experiment_id': experiment_id + 1,
          'expect': 2434
        }, {
          'ppid': 'ppid3',
          'experiment_id': experiment_id,
          'expect': 5439
        }, {
          'ppid': 'a very very very very very very very very very very very very very very very long ppd string',
          'experiment_id': experiment_id,
          'expect': 6128
        }]


    def test_get_uniform(self):
        for test in self.tests:
            self.assertEqual(test['expect'],
                             int(OptimizelyWeightedChoice(experiment_id=test['experiment_id'],
                                                      unit=test['ppid'],
                                                      salt=1).getUniform(max_val=10000)))


if __name__ == '__main__':
    unittest.main()