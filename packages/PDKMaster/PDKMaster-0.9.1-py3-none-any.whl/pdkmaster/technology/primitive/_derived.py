# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import Tuple, Iterable

from ...typing import cast_MultiT
from .. import rule as _rle, mask as _msk, technology_ as _tch

from ._core import _MaskPrimitive


__all__ = [
    "DerivedPrimitiveT", "IntersectT"
]


class _DerivedPrimitive(_MaskPrimitive):
    """A primitive that is derived from other primitives and not a
    Primitive that can be part of the primitive list of a technology.
    """
    def _generate_rules(self, *, tech: _tch.Technology) -> Tuple[_rle.RuleT, ...]:
        """As _DerivedPrimitive will not be added to the list of primitives
        of a technology node, it does not need to generate rules.
        """
        raise RuntimeError("Internal error") # pragma: no cover
DerivedPrimitiveT = _DerivedPrimitive


class _Intersect(_DerivedPrimitive):
    """A primitive representing the overlap of a list of primitives

    API Notes:
        * This class is private to ``technology.primitive`` and is planned
        to be used in other submodules of ``technology.primitive``.
    """
    def __init__(self, *, prims: Iterable[_MaskPrimitive]):
        prims2: Tuple[_MaskPrimitive, ...] = cast_MultiT(prims)
        if len(prims2) < 2:
            raise ValueError(f"At least two prims needed for '{self.__class__.__name__}'")
        self.prims = prims2

        mask = _msk.Intersect(p.mask for p in prims2)
        _MaskPrimitive.__init__(self, mask=mask)
IntersectT = _Intersect