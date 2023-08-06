"""Sampler classes."""

from __future__ import annotations

__all__ = [
    "Sampler",
    "ScalarSampler",
    "MappingSampler",
    "UniformSampler",
    "IntegerSampler",
    "RangeSampler",
    "NormalSampler",
]

from abc import ABC, abstractclassmethod

import random
import yaml

from typing_extensions import Self

from .serializers import SlotsLoader


class Sampler(ABC):
    """Base class for samplers."""

    def __init_subclass__(cls) -> None:
        SlotsLoader.add_constructor(f"!{cls.__name__}", cls._construct_yaml)

    @abstractclassmethod
    def _construct_yaml(cls, loader: yaml.Loader, node: yaml.nodes.Node) -> Self:
        """Construct the sampler from YAML."""
        pass

    @abstractclassmethod
    def get_sample(cls, **kwargs):
        """Get the sample."""
        pass


class ScalarSampler(Sampler):
    """Define scalar sampler."""

    _value_type = str

    @classmethod
    def _construct_yaml(cls, loader: yaml.Loader, node: yaml.nodes.Node) -> Self:
        value = loader.construct_scalar(node)
        return cls.get_sample(value=value)


class MappingSampler(Sampler):
    """Define mapping sampler."""

    @classmethod
    def _construct_yaml(cls, loader: yaml.Loader, node: yaml.nodes.Node) -> Self:
        mapping = loader.construct_mapping(node)
        return cls.get_sample(**mapping)


class UniformSampler(ScalarSampler):
    """Sample from uniform distribution."""

    @classmethod
    def get_sample(cls, value: str) -> float:
        """Get the sample."""
        return random.uniform(*map(float, value.split("..")))


class IntegerSampler(ScalarSampler):
    """Sample from integer distribution."""

    @classmethod
    def get_sample(cls, value: str) -> int:
        """Get the sample."""
        return random.randint(*map(int, value.split("..")))


class RangeSampler(ScalarSampler):
    """Sample from range distribution."""

    @classmethod
    def get_sample(cls, value: str) -> int:
        """Get the sample."""
        return random.randrange(*map(int, value.split("..")))


class NormalSampler(ScalarSampler):
    """Sample from normal distribution."""

    @classmethod
    def get_sample(cls, **kwargs) -> float:
        """Get the sample."""
        return random.normalvariate(**kwargs)
