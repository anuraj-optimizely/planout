from planout.ops.random import WeightedChoice
import mmh3
import math

class OptimizelyWeightedChoice(WeightedChoice):
    MURMER32_LONG_SCALE = math.pow(2, 32)

    def getHash(self, appended_unit=None):
        hash_str = self.getArgString('unit') + str(self.getArgNumeric('experiment_id'))
        return mmh3.hash(hash_str, self.getArgInt('salt'))

    def getUniform(self, min_val=0.0, max_val=1.0, appended_unit=None):
        def unsigned_right_shift_32(val, n):
            return val >> n if val >= 0 else (val + 0x100000000) >> n

        zero_to_one = unsigned_right_shift_32(self.getHash(), 0) / OptimizelyWeightedChoice.MURMER32_LONG_SCALE
        return min_val + (max_val - min_val) * zero_to_one