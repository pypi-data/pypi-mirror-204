"""Test samplers module."""

from dataclasses import dataclass
from slot_machine import SlotsSerializer


@dataclass(slots=True)
class Basket(SlotsSerializer):
    """Define basket class."""

    chicken_nuggets: int
    price: float


def test_sample_basket():
    basket_distribution = """
chicken_nuggets: !RangeSampler 10..20
price: !UniformSampler 9.99..20.0
"""
    basket = Basket.from_yaml(basket_distribution)
    assert isinstance(basket.chicken_nuggets, int)
    assert isinstance(basket.price, float)
    assert 10 <= basket.chicken_nuggets <= 20
    assert 9.99 <= basket.price <= 20.0
