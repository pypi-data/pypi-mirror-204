import numpy as np

from ht_pricing_module.one_asset_pricing_module.one_asset_option_base import *
from ht_pricing_module.one_asset_pricing_module.binary.binary_as import Binary
from ht_pricing_module.one_asset_pricing_module.vanilla.vanilla_as import Vanilla


class SharkfinYield(OneAssetOptionBase):

    def __calculate_present_value__(self):
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        rebate = self.param.annual_rebate * 1
        min_yield = self.param.annual_min_yield * 1

        param = Struct({})
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.strike_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['year_base'] = self.param.year_base
        vanilla1 = Vanilla(param)

        param = Struct({})
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.barrier_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['year_base'] = self.param.year_base
        vanilla2 = Vanilla(param)

        param = Struct({})
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.barrier_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['payoff'] = rebate
        param['year_base'] = self.param.year_base
        binary1 = Binary(param)

        return self.param.notional * (self.param.participation_rate * (vanilla1.present_value() - vanilla2.present_value()) - binary1.present_value() + min_yield)


if __name__ == '__main__':
    param = Struct({})
    param['option_type'] = OptionType.CALL
    param['exercise_type'] = ExerciseType.EUROPEAN
    param['notional'] = 1
    param['spot_price'] = 100
    param['entrance_price'] = 100
    param['strike_price'] = 100
    param['barrier_price'] = 118
    param['expiry_date'] = 0
    param['current_date'] = 0
    param['volatility'] = 0.14
    param['riskfree_rate'] = 0.03
    param['dividend'] = 0.03
    param['year_base'] = 365
    param['annual_rebate'] = 0.07
    param['annual_min_yield'] = 0.02
    param['participation_rate'] = 1

    pricer = SharkfinYield(param=param)
    print(pricer.present_value())
