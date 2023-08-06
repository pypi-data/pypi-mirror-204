# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
from typing import Tuple, Dict, Sequence, Mapping, Iterable, Union, Optional, Any, cast

from ...typing import MultiT, cast_MultiT, OptMultiT, cast_OptMultiT
from ...technology import (
    property_ as _prp,  geometry as _geo, net as _net, primitive as _prm, technology_ as _tch,
)
from ...technology.primitive._param import _PrimParam

from ... import _util, dispatch as _dsp

from .layout_ import _MaskShapesSubLayout, LayoutT
# also imports at end of file to avoid circular import problems


def _rect(
    left: float, bottom: float, right: float, top: float, *,
    enclosure: Optional[Union[float, Sequence[float], _prp.Enclosure]]=None,
) -> _geo.Rect:
    """undocumented deprecated function;
    see: https://gitlab.com/Chips4Makers/PDKMaster/-/issues/39
    """
    if enclosure is not None:
        if isinstance(enclosure, _prp.Enclosure):
            enclosure = enclosure.spec
        if isinstance(enclosure, float):
            left -= enclosure
            bottom -= enclosure
            right += enclosure
            top += enclosure
        else:
            left -= enclosure[0]
            bottom -= enclosure[1]
            right += enclosure[0]
            top += enclosure[1]

    return _geo.Rect(
        left=left, bottom=bottom, right=right, top=top,
    )


def _via_array(
    left: float, bottom: float, width: float, pitch: float, rows: int, columns: int,
):
    """undocumented deprecated function;
    see: https://gitlab.com/Chips4Makers/PDKMaster/-/issues/39
    """
    via = _geo.Rect.from_size(width=width, height=width)
    xy0 = _geo.Point(x=(left + 0.5*width), y=(bottom + 0.5*width))

    if (rows == 1) and (columns == 1):
        return via + xy0
    else:
        return _geo.ArrayShape(
            shape=via, offset0=xy0, rows=rows, columns=columns, pitch_x=pitch, pitch_y=pitch,
        )


class _LayoutParam(_PrimParam):
    """_LayoutParam is a param that can be specified when generating the layout of a
    technology primitive. This is also valid for non-device; e.g. for generating the
    layouts of a wire etc.
    """
    pass


class _IntLayoutParam(_LayoutParam):
    value_conv = None
    value_type = int
    value_type_str = "int"


class _BoolLayoutParam(_LayoutParam):
    value_conv = None
    value_type = bool
    value_type_str = "bool"


class _PrimitiveLayoutParam(_LayoutParam):
    value_conv = None
    value_type = _prm.PrimitiveT
    value_type_str = "Primitive"

    def __init__(self, *,
        primitive: _prm.PrimitiveT, name: str, allow_none=False, default=None,
        choices: OptMultiT[_prm.PrimitiveT]=None,
    ):
        self.choices = cast_OptMultiT(choices)

        super().__init__(
            primitive=primitive, name=name, allow_none=allow_none, default=default,
        )

    def cast(self, value):
        value = super().cast(value)
        if self.choices is not None:
            if not ((value is None) or (value in self.choices)):
                raise ValueError(
                    f"Param '{self.name}' value '{value}' is not one of the allowed values:\n"
                    f"    {self.choices}"
            )

        return value


class _EnclosureLayoutParam(_LayoutParam):
    value_type = (_prp.Enclosure, float, Iterable[float])
    value_type_str = "'Enclosure'"

    def cast(self, value):
        if value is None:
            if hasattr(self, "default"):
                value = self.default
            elif not self.allow_none:
                raise TypeError(
                    f"'None' value not allowed for parameter '{self.name}'"
                )
        elif not (
            isinstance(value, _prp.Enclosure)
            or (value in ("wide", "tall"))
        ):
            try:
                value = _prp.Enclosure(value)
            except:
                raise TypeError(
                    f"value {repr(value)} can't be converted to an Enclosure object"
                )

        return value


class _EnclosuresLayoutParam(_LayoutParam):
    value_type_str = "iterable of 'Enclosure'"

    def __init__(self, *,
        primitive: _prm.PrimitiveT, name: str, allow_none=False, default=None, n: int,
    ):
        self.n = n
        super().__init__(
            primitive=primitive, name=name, allow_none=allow_none, default=default,
        )

    def cast(self, value):
        if value is None:
            if hasattr(self, "default"):
                value = self.default
            elif not self.allow_none:
                raise TypeError(
                    f"'None' value not allowed for parameter '{self.name}'"
                )
        elif not _util.is_iterable(value):
            try:
                value = self.n*(_prp.Enclosure(value),)
            except:
                raise TypeError(
                    f"param '{self.name}' has to be an enclosure value or an iterable \n"
                    f"of type 'Enclosure' with length {self.n}"
                )
        else:
            try:
                value = tuple(
                    (None if elem is None
                     else elem if isinstance(elem, _prp.Enclosure)
                     else _prp.Enclosure(elem)
                    ) for elem in value
                )
            except:
                raise TypeError(
                    f"param '{self.name}' has to be an enclosure value or an iterable \n"
                    f"of type 'Enclosure' with length {self.n}"
                )
        return value


class _NetLayoutParam(_LayoutParam):
    value_type = _net.NetT
    value_type_str = "Net"


class _LayoutParamCaster(_dsp.PrimitiveDispatcher):
    """Support class that will cast parameters given to _PrimitiveLayouter
    """
    def __call__(self, prim: _prm.PrimitiveT, **params: Any) -> Dict[str, Any]:
        return super().__call__(prim, **params)

    def cast_params(self, *,
        layout_params: MultiT[_LayoutParam], prim_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """cast parameters for a list of given layout parameters

        Arguments:
            layout_params: The list params specification
            prim_params: The parameters to cast.
                Params specified in layout_params will be removed from prim_params
        """
        layout_params = cast_MultiT(layout_params)
        return {
            param.name: param.cast(prim_params.pop(param.name, None))
            for param in layout_params
        }

    def _Primitive(self, prim: _prm.PrimitiveT, **params: Any) -> Dict[str, Any]:
        out = {}
        if isinstance(prim, _prm.PinAttrPrimitiveT) and prim.pin is not None:
            out.update(self.cast_params(
                layout_params=_PrimitiveLayoutParam(
                    primitive=prim, name="pin", allow_none=True, choices=prim.pin,
                ),
                prim_params=params,
            ))

        if len(prim.ports) > 0:
            try:
                portnets = params.pop("portnets")
            except KeyError:
                # Specifying nets is optional
                pass
            else:
                # If nets are specified all nets need to be specified
                portnames = {p.name for p in prim.ports}
                portnetnames = set(portnets.keys())
                if (
                    (portnames != portnetnames)
                    or (len(prim.ports) != len(portnets)) # Detect removal of doubles in set
                ):
                    raise ValueError(
                        f"Nets for ports {portnetnames} specified but prim '{prim.name}'"
                        f" has ports {portnames}"
                    )
                out["portnets"] = portnets

        if len(params) != 0:
            raise TypeError(
                f"primitive '{prim.name}' got unexpected parameter(s) "
                f"{tuple(params.keys())}"
            )

        return out

    def _DevicePrimitive(self, prim: _prm.DevicePrimitiveT, **params: Any) -> Dict[str, Any]:
        dev_params = prim.cast_params(params)

        super_params = super()._DevicePrimitive(prim=prim, **params)
        super_params.update(dev_params)

        return super_params

    def _WidthSpacePrimitive(self,
        prim: _prm.WidthSpacePrimitiveT, **params: Any,
    ) -> Dict[str, Any]:
        ws_params = self.cast_params(
            layout_params=(
                _LayoutParam(primitive=prim, name="width", default=prim.min_width),
                _LayoutParam(primitive=prim, name="height", default=prim.min_width),
            ),
            prim_params=params,
        )
        super_params = super()._WidthSpacePrimitive(prim=prim, **params)
        super_params.update(ws_params)

        return super_params

    def Marker(self, prim: _prm.Marker, **params: Any) -> Dict[str, Any]:
        marker_params = self.cast_params(
            layout_params=(
               _LayoutParam(primitive=prim, name="width", allow_none=True),
               _LayoutParam(primitive=prim, name="height", allow_none=True),
            ),
            prim_params=params,
        )
        super_params = super().Marker(prim, **params)
        super_params.update(marker_params)

        return super_params

    def WaferWire(self, prim: _prm.WaferWire, **params) -> Dict[str, Any]:
        layparams = []
        ww_params = {}
        if len(prim.implant) > 1:
            layparams.extend((
                _PrimitiveLayoutParam(
                    primitive=prim, name="implant", choices=prim.implant,
                ),
                _EnclosureLayoutParam(
                    primitive=prim, name="implant_enclosure", allow_none=True,
                ),
            ))
        else:
            ww_params["implant"] = prim.implant[0]
            layparams.append(
                _EnclosureLayoutParam(
                    primitive=prim, name="implant_enclosure",
                    default=prim.min_implant_enclosure[0],
                ),
            )
        if (len(prim.well) > 1) or prim.allow_in_substrate:
            layparams.extend((
                _PrimitiveLayoutParam(
                    primitive=prim, name="well", allow_none=prim.allow_in_substrate,
                    choices=prim.well
                ),
                _EnclosureLayoutParam(
                    primitive=prim, name="well_enclosure", allow_none=True,
                ),
            ))
        else:
            ww_params["well"] = prim.well[0]
            layparams.append(
                _EnclosureLayoutParam(
                    primitive=prim, name="well_enclosure", default=prim.min_well_enclosure[0],
                ),
            )
        layparams.append(_NetLayoutParam(
            primitive=prim, name="well_net", allow_none=prim.allow_in_substrate,
        ))
        if prim.oxide is not None:
            layparams.extend((
                _PrimitiveLayoutParam(
                    primitive=prim, name="oxide", choices=prim.oxide, allow_none=True,
                ),
                _EnclosureLayoutParam(
                    primitive=prim, name="oxide_enclosure", allow_none=True,
                ),
            ))
        ww_params.update(self.cast_params(layout_params=layparams, prim_params=params))

        implant = ww_params["implant"]
        enc = ww_params["implant_enclosure"]
        if (implant is not None) and (enc is None):
            idx = prim.implant.index(implant)
            ww_params["implant_enclosure"] = prim.min_implant_enclosure[idx]

        if (ww_params["well"] is not None) and (ww_params["well_net"] is None):
            raise ValueError("well_net needs to be provided if well is specified")

        if ("oxide" in ww_params):
            oxide = ww_params["oxide"]
            if oxide is not None:
                assert prim.oxide is not None
                assert prim.min_oxide_enclosure is not None
                oxide_enclosure = ww_params["oxide_enclosure"]
                if oxide_enclosure is None:
                    idx = prim.oxide.index(oxide)
                    ww_params["oxide_enclosure"] = prim.min_oxide_enclosure[idx]

        super_params = super().WaferWire(prim, **params)
        super_params.update(ww_params)

        return super_params

    def Via(self, prim, **params) -> Dict[str, Any]:
        layparams = [
            _LayoutParam(primitive=prim, name="space", default=prim.min_space),
            _IntLayoutParam(primitive=prim, name="rows", allow_none=True),
            _IntLayoutParam(primitive=prim, name="columns", allow_none=True),
            _EnclosureLayoutParam(primitive=prim, name="bottom_enclosure", allow_none=True),
            _LayoutParam(primitive=prim, name="bottom_width", allow_none=True),
            _LayoutParam(primitive=prim, name="bottom_height", allow_none=True),
            _EnclosureLayoutParam(primitive=prim, name="top_enclosure", allow_none=True),
            _LayoutParam(primitive=prim, name="top_width", allow_none=True),
            _LayoutParam(primitive=prim, name="top_height", allow_none=True),
        ]
        via_params = {}

        if len(prim.bottom) > 1:
            default = prim.bottom[0]
            if not isinstance(default, _prm.MetalWire) or isinstance(default, _prm.MIMTop):
                default = None
            layparams.append(_PrimitiveLayoutParam(
                primitive=prim, name="bottom", default=default, choices=prim.bottom,
            ))
        else:
            via_params["bottom"] = prim.bottom[0]

        choices = sum(
            (cast(_prm.WaferWire, wire).implant for wire in filter(
                lambda w: isinstance(w, _prm.WaferWire),
                prim.bottom,
            )),
            tuple(),
        )
        if choices:
            layparams.extend((
                _PrimitiveLayoutParam(
                    primitive=prim, name="bottom_implant",
                    allow_none=True, choices=choices,
                ),
                _EnclosureLayoutParam(
                    primitive=prim, name="bottom_implant_enclosure", allow_none=True,
                ),
                _PrimitiveLayoutParam(primitive=prim, name="bottom_well", allow_none=True),
                _NetLayoutParam(primitive=prim, name="well_net", allow_none=True),
                _EnclosureLayoutParam(
                    primitive=prim, name="bottom_well_enclosure", allow_none=True,
                ),
            ))

        choices = sum(
            (cast(Tuple[_prm.Insulator, ...], cast(_prm.WaferWire, wire).oxide)
            for wire in filter(
                lambda w: isinstance(w, _prm.WaferWire) and (w.oxide is not None),
                prim.bottom,
            )),
            tuple(),
        )
        if choices:
            layparams.extend((
                _PrimitiveLayoutParam(
                    primitive=prim, name="bottom_oxide", allow_none=True, choices=choices,
                ),
                _EnclosureLayoutParam(
                    primitive=prim, name="bottom_oxide_enclosure", allow_none=True,
                ),
            ))

        if len(prim.top) > 1:
            default = prim.top[0]
            assert isinstance(default, _prm.MetalWire), "Not implemented"
            layparams.append(_PrimitiveLayoutParam(
                primitive=prim, name="top", default=default, choices=prim.top,
            ))
        else:
            via_params["top"] = prim.top[0]

        via_params.update(self.cast_params(layout_params=layparams, prim_params=params))

        def get_via_param(name: str):
            try:
                return via_params[name]
            except KeyError:
                return None

        bottom = via_params["bottom"]
        bottom_impl = get_via_param("bottom_implant")
        bottom_impl_enc = get_via_param("bottom_implant_enclosure")
        bottom_well = get_via_param("bottom_well")
        well_net = get_via_param("well_net")
        bottom_well_enc = get_via_param("bottom_well_enclosure")
        if isinstance(bottom, _prm.WaferWire):
            if bottom_impl is None:
                raise TypeError(
                    "bottom_implant parameter not provided for "
                    f"bottom '{bottom.name}' of via '{prim.name}'"
                )

            if bottom_impl_enc is None:
                idx = bottom.implant.index(bottom_impl)
                via_params["bottom_implant_enclosure"] = bottom.min_implant_enclosure[idx]

            if bottom_well is not None:
                if bottom_well not in bottom.well:
                    raise ValueError(
                        f"bottom_well '{bottom_well.name}' not a valid well for "
                        f"bottom wire '{bottom.name}'"
                    )
                if bottom_well_enc is None:
                    idx = bottom.well.index(bottom_well)
                    via_params["bottom_well_enclosure"] = (
                        bottom.min_well_enclosure[idx]
                    )
                # well_net will be checked during layout generation
            elif not bottom.allow_in_substrate:
                raise TypeError(
                    f"bottom wire '{bottom.name}' needs a well"
                )
        else:
            if bottom_impl is not None:
                raise TypeError(
                    f"bottom_implant '{bottom_impl.name}' not a valid implant for "
                    f"bottom wire '{bottom.name}'"
                )
            if bottom_impl_enc is not None:
                raise TypeError(
                    "bottom_implant_enclosure wrongly provided for bottom wire "
                    f"'{bottom.name}'"
                )
            if bottom_well is not None:
                raise TypeError(
                    f"bottom_well '{bottom_well.name}' not a valid well for "
                    f"bottom wire '{bottom.name}'"
                )
            if bottom_well_enc is not None:
                raise TypeError(
                    "bottom_well_enclosure wrongly provided for bottom wire "
                    f"'{bottom.name}'"
                )
            if well_net is not None:
                raise TypeError(
                    "well_net wrongly provided for bottom wire "
                    f"'{bottom.name}'"
                )

        super_params = super().Via(prim, **params)
        super_params.update(via_params)

        return super_params

    def MIMCapacitor(self, prim: _prm.MIMCapacitor, **params) -> Dict[str, Any]:
        mim_params = self.cast_params(
            layout_params=_BoolLayoutParam(
                primitive=prim, name="bottom_connect_up", default=True,
            ),
            prim_params=params,
        )

        super_params = super().MIMCapacitor(prim, **params)
        super_params.update(mim_params)

        return super_params

    def MOSFET(self, prim: _prm.MOSFET, **params) -> Dict[str, Any]:
        for impl in prim.implant:
            try:
                idx = prim.gate.active.implant.index(impl)
            except: # pragma: no cover
                continue
            else:
                impl_act_enc = prim.gate.active.min_implant_enclosure[idx]
                break
        else: # pragma: no cover
            raise AssertionError("Internal error: no default active implant enclosure")

        layparams = [
            _EnclosureLayoutParam(
                primitive=prim, name="activeimplant_enclosure",
                default=impl_act_enc,
            ),
            _LayoutParam(
                primitive=prim, name="sd_width", default=prim.computed.min_sd_width),
            _LayoutParam(
                primitive=prim, name="polyactive_extension",
                default=prim.computed.min_polyactive_extension,
            ),
            _EnclosuresLayoutParam(
                primitive=prim, name="gateimplant_enclosures", n=len(prim.implant),
                default=prim.min_gateimplant_enclosure,
            ),
        ]
        spc = prim.computed.min_gate_space
        if spc is not None:
            layparams.append(
                _LayoutParam(primitive=prim, name="gate_space", default=spc)
            )

        if prim.computed.contact is not None:
            spc = prim.computed.min_contactgate_space
            assert spc is not None
            layparams.append(
                _LayoutParam(primitive=prim, name="contactgate_space", default=spc)
            )
        mos_params = self.cast_params(layout_params=layparams, prim_params=params)

        super_params = super().MOSFET(prim, **params)
        super_params.update(mos_params)

        return super_params


class _PrimitiveLayouter(_dsp.PrimitiveDispatcher):
    """Support class to generate layout for a `_Primitive`.

    TODO: Proper docs after fixing the API.
    see https://gitlab.com/Chips4Makers/PDKMaster/-/issues/25

    API Notes:
        The API is not finalized yet; backwards incompatible changes are still
            expected.
    """
    def __init__(self, fab: "LayoutFactory"):
        self.fab = fab
        self._caster = _LayoutParamCaster()

    def __call__(self, prim: _prm.PrimitiveT, **prim_params) -> LayoutT:
        return super().__call__(prim, **self._caster(prim, **prim_params))

    @property
    def tech(self) -> _tch.Technology:
        return self.fab.tech

    # Dispatcher implementation
    def _Primitive(self, prim: _prm.PrimitiveT, **params) -> LayoutT:
        raise NotImplementedError(
            f"Don't know how to generate minimal layout for primitive '{prim.name}'\n"
            f"of type '{prim.__class__.__name__}'"
        )

    def Marker(self, prim: _prm.Marker, **params) -> LayoutT:
        if (params["width"] is not None) and (params["height"] is not None):
            return self._WidthSpacePrimitive(cast(_prm.WidthSpacePrimitiveT, prim), **params)
        else:
            return super().Marker(prim, **params)

    def _WidthSpacePrimitive(self,
        prim: _prm.WidthSpacePrimitiveT, **widthspace_params,
    ) -> LayoutT:
        if len(prim.ports) != 0: # pragma: no cover
            raise NotImplementedError(
                f"Don't know how to generate minimal layout for primitive '{prim.name}'\n"
                f"of type '{prim.__class__.__name__}'"
            )
        width = widthspace_params["width"]
        height = widthspace_params["height"]
        r = _geo.Rect.from_size(width=width, height=height)

        l = self.fab.new_layout()
        assert isinstance(prim, _prm.DesignMaskPrimitiveT)
        l.add_shape(layer=prim, net=None, shape=r)
        return l

    def _WidthSpaceConductor(self,
        prim: _prm.WidthSpaceConductorT, **conductor_params,
    ) -> LayoutT:
        assert (
            (len(prim.ports) == 1) and (prim.ports[0].name == "conn")
        ), "Internal error"
        width = conductor_params["width"]
        height = conductor_params["height"]
        r = _geo.Rect.from_size(width=width, height=height)

        try:
            portnets = conductor_params["portnets"]
        except KeyError:
            net = prim.ports.conn
        else:
            net = portnets["conn"]

        layout = self.fab.new_layout()
        layout.add_shape(layer=prim, net=net, shape=r)
        pin = conductor_params.get("pin", None)
        if pin is not None:
            layout.add_shape(layer=pin, net=net, shape=r)

        return layout

    def WaferWire(self, prim: _prm.WaferWire, **waferwire_params) -> LayoutT:
        width = waferwire_params["width"]
        height = waferwire_params["height"]

        implant = waferwire_params.pop("implant")
        implant_enclosure = waferwire_params.pop("implant_enclosure")
        assert implant_enclosure is not None

        well = waferwire_params.pop("well", None)
        well_enclosure = waferwire_params.pop("well_enclosure", None)

        oxide = waferwire_params.pop("oxide", None)
        oxide_enclosure = waferwire_params.pop("oxide_enclosure", None)

        layout = self._WidthSpaceConductor(prim, **waferwire_params)
        layout.add_shape(layer=implant, net=None, shape=_rect(
            -0.5*width, -0.5*height, 0.5*width, 0.5*height,
            enclosure=implant_enclosure,
        ))
        if well is not None:
            well_net = waferwire_params["well_net"]
            assert well_net is not None, "Internal error"
            layout.add_shape(layer=well, net=well_net, shape=_rect(
                -0.5*width, -0.5*height, 0.5*width, 0.5*height,
                enclosure=well_enclosure,
            ))
        if oxide is not None:
            layout.add_shape(layer=oxide, net=None, shape=_rect(
                -0.5*width, -0.5*height, 0.5*width, 0.5*height,
                enclosure=oxide_enclosure,
            ))
        return layout

    def MIMTop(self, prim: _prm.MIMTop, **_) -> LayoutT:
        raise ValueError("No generation of MIMTop layer; use MIMCapacitor instead")

    def Via(self, prim: _prm.Via, **via_params) -> LayoutT:
        tech = self.tech

        try:
            portnets = via_params["portnets"]
        except KeyError:
            net = prim.ports["conn"]
        else:
            net = portnets["conn"]

        bottom = via_params["bottom"]
        bottom_enc = via_params["bottom_enclosure"]
        if (bottom_enc is None) or isinstance(bottom_enc, str):
            idx = prim.bottom.index(bottom)
            enc = prim.min_bottom_enclosure[idx]
            if bottom_enc is None:
                bottom_enc = enc
            elif bottom_enc == "wide":
                bottom_enc = enc.wide()
            else:
                assert bottom_enc == "tall"
                bottom_enc = enc.tall()
        assert isinstance(bottom_enc, _prp.Enclosure)
        bottom_enc_x = bottom_enc.spec[0]
        bottom_enc_y = bottom_enc.spec[1]

        top = via_params["top"]
        top_enc = via_params["top_enclosure"]
        if (top_enc is None) or isinstance(top_enc, str):
            idx = prim.top.index(top)
            enc = prim.min_top_enclosure[idx]
            if top_enc is None:
                top_enc = enc
            elif top_enc == "wide":
                top_enc = enc.wide()
            else:
                assert top_enc == "tall"
                top_enc = enc.tall()
        assert isinstance(top_enc, _prp.Enclosure)
        top_enc_x = top_enc.spec[0]
        top_enc_y = top_enc.spec[1]

        width = prim.width
        space = via_params["space"]
        pitch = width + space

        rows = via_params["rows"]
        bottom_height = via_params["bottom_height"]
        top_height = via_params["top_height"]
        if (rows is None) and (bottom_height is None) and (top_height is None):
            rows = 1
        if rows is None:
            if bottom_height is None:
                assert top_height is not None
                rows = int(self.tech.on_grid(top_height - 2*top_enc_y - width)//pitch + 1)
                via_height = rows*pitch - space
                bottom_height = tech.on_grid(
                    via_height + 2*bottom_enc_y, mult=2, rounding="ceiling",
                )
            else:
                rows = int(self.tech.on_grid(bottom_height - 2*bottom_enc_y - width)//pitch + 1)
                if top_height is not None:
                    rows = min(
                        rows,
                        int(self.tech.on_grid(top_height - 2*top_enc_y - width)//pitch + 1),
                    )
                via_height = rows*pitch - space
                if top_height is None:
                    top_height = tech.on_grid(
                        via_height + 2*top_enc_y, mult=2, rounding="ceiling",
                    )
        else:
            assert (bottom_height is None) and (top_height is None)
            via_height = rows*pitch - space
            bottom_height = tech.on_grid(
                via_height + 2*bottom_enc_y, mult=2, rounding="ceiling",
            )
            top_height = tech.on_grid(
                via_height + 2*top_enc_y, mult=2, rounding="ceiling",
            )

        columns = via_params["columns"]
        bottom_width = via_params["bottom_width"]
        top_width = via_params["top_width"]
        if (columns is None) and (bottom_width is None) and (top_width is None):
            columns = 1
        if columns is None:
            if bottom_width is None:
                assert top_width is not None
                columns = int(self.tech.on_grid(top_width - 2*top_enc_x - width)//pitch + 1)
                via_width = columns*pitch - space
                bottom_width = tech.on_grid(
                    via_width + 2*bottom_enc_x, mult=2, rounding="ceiling",
                )
            else:
                columns = int(self.tech.on_grid(bottom_width - 2*bottom_enc_x - width)//pitch + 1)
                if top_width is not None:
                    columns = min(
                        columns,
                        int(self.tech.on_grid(top_width - 2*top_enc_x - width)//pitch + 1)
                    )
                via_width = columns*pitch - space
                if top_width is None:
                    top_width = tech.on_grid(
                        via_width + 2*top_enc_x, mult=2, rounding="ceiling",
                    )
        else:
            assert (bottom_width is None) and (top_width is None)
            via_width = columns*pitch - space
            bottom_width = tech.on_grid(
                via_width + 2*bottom_enc_x, mult=2, rounding="ceiling",
            )
            top_width = tech.on_grid(
                via_width + 2*top_enc_x, mult=2, rounding="ceiling",
            )

        bottom_left = tech.on_grid(-0.5*bottom_width, rounding="floor")
        bottom_bottom = tech.on_grid(-0.5*bottom_height, rounding="floor")
        bottom_right = bottom_left + bottom_width
        bottom_top = bottom_bottom + bottom_height
        bottom_rect = _geo.Rect(
            left=bottom_left, bottom=bottom_bottom,
            right=bottom_right, top=bottom_top,
        )

        top_left = tech.on_grid(-0.5*top_width, rounding="floor")
        top_bottom = tech.on_grid(-0.5*top_height, rounding="floor")
        top_right = top_left + top_width
        top_top = top_bottom + top_height
        top_rect = _geo.Rect(
            left=top_left, bottom=top_bottom,
            right=top_right, top=top_top,
        )

        via_bottom = tech.on_grid(-0.5*via_height)
        via_left = tech.on_grid(-0.5*via_width)

        layout = self.fab.new_layout()

        layout.add_shape(layer=bottom, net=net, shape=bottom_rect)
        layout.add_shape(layer=prim, net=net, shape=_via_array(
            via_left, via_bottom, width, pitch, rows, columns,
        ))
        layout.add_shape(layer=top, net=net, shape=top_rect)
        try:
            impl = via_params["bottom_implant"]
        except KeyError:
            impl = None
        else:
            if impl is not None:
                enc = cast(_prp.Enclosure, via_params["bottom_implant_enclosure"])
                assert enc is not None, "Internal error"
                if enc in ("wide", "tall"):
                    idx = bottom.implant.index(impl)
                    enc2 = bottom.min_implant_enclosure[idx]
                    if enc == "wide":
                        enc = enc2.wide()
                    else:
                        assert enc == "tall", "Internal error"
                        enc = enc2.tall()
                layout.add_shape(layer=impl, net=None, shape=_geo.Rect.from_rect(
                    rect=bottom_rect, bias=enc,
                ))
        try:
            oxide = via_params["bottom_oxide"]
        except KeyError:
            oxide = None
        else:
            if oxide is not None:
                assert (
                    isinstance(bottom, _prm.WaferWire) and (bottom.oxide is not None)
                    and (bottom.min_oxide_enclosure is not None)
                )
                enc = cast(_prp.Enclosure, via_params["bottom_oxide_enclosure"])
                if enc is None:
                    idx = bottom.oxide.index(oxide)
                    enc = bottom.min_oxide_enclosure[idx]
                assert (enc is not None), "Unknown enclosure"
                layout.add_shape(layer=oxide, net=None, shape=_geo.Rect.from_rect(
                    rect=bottom_rect, bias=enc,
                ))
        try:
            well = via_params["bottom_well"]
        except KeyError:
            well = None
        else:
            if well is not None:
                well_net = via_params.get("well_net", None)
                enc = via_params["bottom_well_enclosure"]
                assert enc is not None, "Internal error"
                if (impl is not None) and (impl.type_ == well.type_):
                    if well_net is not None:
                        if well_net != net:
                            raise ValueError(
                                f"Net '{well_net}' for well '{well.name}' of WaferWire"
                                f" {bottom.name} is different from net '{net}''\n"
                                f"\tbut implant '{impl.name}' is same type as the well"
                            )
                    else:
                        well_net = net
                elif well_net is None:
                    raise TypeError(
                        f"No well_net specified for WaferWire '{bottom.name}' in"
                        f" well '{well.name}'"
                    )
                layout.add_shape(layer=well, net=well_net, shape=_geo.Rect.from_rect(
                    rect=bottom_rect, bias=enc,
                ))

        return layout

    def DeepWell(self, prim: _prm.DeepWell, **deepwell_params) -> LayoutT:
        raise NotImplementedError("layout generation for DeepWell primitive")

    def Resistor(self, prim: _prm.Resistor, **resistor_params) -> LayoutT:
        try:
            portnets = resistor_params["portnets"]
        except KeyError:
            port1 = prim.ports.port1
            port2 = prim.ports.port2
        else:
            port1 = portnets["port1"]
            port2 = portnets["port2"]
        if prim.contact is None:
            raise NotImplementedError("Resistor layout without contact layer")

        res_width = resistor_params["width"]
        res_length = resistor_params["length"]

        wire = prim.wire

        cont = prim.contact
        cont_space = prim.min_contact_space
        assert cont_space is not None
        try:
            wire_idx = cont.bottom.index(wire)
        except ValueError: # pragma: no cover
            raise NotImplementedError("Resistor connected from the bottom")
            try:
                wire_idx = cont.top.index(wire)
            except ValueError:
                raise AssertionError("Internal error")
            else:
                cont_enc = cont.min_top_enclosure[wire_idx]
                cont_args = {"top": wire, "x": 0.0, "top_width": res_width}
        else:
            cont_enc = cont.min_bottom_enclosure[wire_idx]
            cont_args = {"bottom": wire, "x": 0.0, "bottom_width": res_width}
        if (prim.implant is not None) and isinstance(wire, _prm.WaferWire):
            cont_args["bottom_implant"] = prim.implant
        cont_y1 = -0.5*res_length - cont_space - 0.5*cont.width
        cont_y2 = -cont_y1

        wire_ext = cont_space + cont.width + cont_enc.min()

        layout = self.fab.new_layout()

        # Draw indicator layers
        for idx, ind in enumerate(prim.indicator):
            ext = prim.min_indicator_extension[idx]
            layout += self(ind, width=(res_width + 2*ext), height=res_length)

        # Draw wire layer
        mp = _geo.MultiPartShape(
            fullshape=_geo.Rect.from_size(
                width=res_width, height=(res_length + 2*wire_ext),
            ),
            parts = (
                _geo.Rect.from_floats(values=(
                    -0.5*res_width, -0.5*res_length - wire_ext,
                    0.5*res_width, -0.5*res_length,
                )),
                _geo.Rect.from_floats(values=(
                    -0.5*res_width, -0.5*res_length,
                    0.5*res_width, 0.5*res_length,
                )),
                _geo.Rect.from_floats(values=(
                    -0.5*res_width, 0.5*res_length,
                    0.5*res_width, 0.5*res_length + wire_ext,
                )),
            )
        )
        layout.add_shape(layer=wire, net=port1, shape=mp.parts[0])
        layout.add_shape(layer=wire, net=None, shape=mp.parts[1])
        layout.add_shape(layer=wire, net=port2, shape=mp.parts[2])

        # Draw contacts
        # Hack to make sure the bottom wire does not overlap with the resistor part
        # TODO: Should be fixed in MultiPartShape handling
        # layout.add_wire(net=port1, wire=cont, y=cont_y1, **cont_args)
        # layout.add_wire(net=port2, wire=cont, y=cont_y2, **cont_args)
        x = cont_args.pop("x")
        _l_cont = self.fab.layout_primitive(
            prim=cont, portnets={"conn": port1}, **cont_args
        )
        _l_cont.move(dxy=_geo.Point(x=x, y=cont_y1))
        for sl in _l_cont._sublayouts:
            if isinstance(sl, _MaskShapesSubLayout):
                for msl in sl.shapes:
                    if msl.mask == wire.mask:
                        assert isinstance(msl.shape, _geo.Rect)
                        msl._shape = _geo.Rect.from_rect(
                            rect=msl.shape, top=(-0.5*res_length - self.tech.grid)
                        )
        layout += _l_cont
        _l_cont = self.fab.layout_primitive(
            prim=cont, portnets={"conn": port2}, **cont_args
        )
        _l_cont.move(dxy=_geo.Point(x=x, y=cont_y2))
        for sl in _l_cont._sublayouts:
            if isinstance(sl, _MaskShapesSubLayout):
                for msl in sl.shapes:
                    if msl.mask == wire.mask:
                        assert isinstance(msl.shape, _geo.Rect)
                        msl._shape = _geo.Rect.from_rect(
                            rect=msl.shape, bottom=(0.5*res_length + self.tech.grid)
                        )
        layout += _l_cont

        if prim.implant is not None:
            impl = prim.implant
            try:
                enc = prim.min_implant_enclosure.max() # type: ignore
            except AttributeError:
                assert isinstance(wire, _prm.WaferWire), "Internal error"
                idx = wire.implant.index(impl)
                enc = wire.min_implant_enclosure[idx].max()
            impl_width = res_width + 2*enc
            impl_height = res_length + 2*wire_ext + 2*enc
            layout.add_shape(
                layer=impl, net=None, shape=_geo.Rect.from_size(width=impl_width, height=impl_height),
            )

        return layout

    def MIMCapacitor(self, prim: _prm.MIMCapacitor, **mimcapargs) -> LayoutT:
        try:
            portnets = mimcapargs.pop("portnets")
        except KeyError:
            top = prim.ports.top
            bottom = prim.ports.bottom
        else:
            top = portnets["top"]
            bottom = portnets["bottom"]

        via = prim.via

        # Params
        top_width = mimcapargs["width"]
        top_height = mimcapargs["height"]
        connect_up = mimcapargs["bottom_connect_up"]

        # TODO: Allow to specify top of the via layer
        upper_metal = via.top[0]
        assert isinstance(upper_metal, _prm.MetalWire)
        assert upper_metal.pin is not None
        upper_pin: _prm.Marker = upper_metal.pin

        # Compute dimensions
        if connect_up:
            bottomvia_outerwidth = (
                top_width + 2*prim.min_bottomvia_top_space + 2*via.width
            )
            bottomvia_outerheight = (
                top_height + 2*prim.min_bottomvia_top_space + 2*via.width
            )
            bottomvia_outerbound = _geo.Rect.from_size(
                width=bottomvia_outerwidth, height=bottomvia_outerheight,
            )

            idx = via.bottom.index(prim.bottom)
            enc = via.min_bottom_enclosure[idx].max()
            bottom_width = bottomvia_outerwidth + 2*enc
            bottom_height = bottomvia_outerheight + 2*enc

            enc = via.min_top_enclosure[0].max()
            bottomupper_outerwidth = bottomvia_outerwidth + 2*enc
            bottomupper_outerheight = bottomvia_outerheight + 2*enc
            bottomupper_ringwidth = via.width + 2*enc

            topupper_width = (
                bottomupper_outerwidth - 2*bottomupper_ringwidth - 2*upper_metal.min_space
            )
            topupper_height = (
                bottomupper_outerheight - 2*bottomupper_ringwidth - 2*upper_metal.min_space
            )
        else:
            enc = prim.min_bottom_top_enclosure.max()
            bottom_width = top_width + 2*enc
            bottom_height = top_height + 2*enc

            topupper_width = None
            topupper_height = None

        # Draw the shapes
        layout = self.fab.new_layout()
        via_lay = layout.add_primitive(
            prim=via, bottom=prim.top, portnets={"conn": top},
            bottom_width=top_width, bottom_height=top_height,
            top_width=topupper_width, top_height=topupper_height,
            bottom_enclosure=prim.min_top_via_enclosure,
        )
        via_upmbb = via_lay.bounds(mask=upper_metal.mask)
        layout.add_shape(layer=upper_pin, net=top, shape=via_upmbb)

        shape = _geo.Rect.from_size(width=bottom_width, height=bottom_height)
        layout.add_shape(layer=prim.bottom, net=bottom, shape=shape)

        if connect_up:
            shape = _geo.RectRing(
                outer_bound=bottomvia_outerbound,
                rect_width=via.width, min_rect_space=via.min_space,
            )
            layout.add_shape(layer=via, net=bottom, shape=shape)

            shape = _geo.Ring(
                outer_bound=_geo.Rect.from_size(
                    width=bottomupper_outerwidth, height=bottomupper_outerheight,
                ),
                ring_width=bottomupper_ringwidth,
            )
            layout.add_shape(layer=upper_metal, net=bottom, shape=shape)
            layout.add_shape(layer=upper_pin, net=bottom, shape=shape)

        bottom_space = (
            prim.min_bottom_space
            if prim.min_bottom_space is not None
            else 0.0
        )
        layout.boundary = _geo.Rect.from_size(
            width=(bottom_width + bottom_space),
            height=(bottom_height + bottom_space),
        )

        return layout

    def Diode(self, prim: _prm.Diode, **diode_params) -> LayoutT:
        try:
            portnets = diode_params.pop("portnets")
        except KeyError:
            an = prim.ports.anode
            cath = prim.ports.cathode
        else:
            an = portnets["anode"]
            cath = portnets["cathode"]

        wirenet_args = {
            "implant": prim.implant,
            "portnets": {"conn": an if prim.implant.type_ == _prm.pImpl else cath},
        }
        if prim.min_implant_enclosure is not None:
            wirenet_args["implant_enclosure"] = prim.min_implant_enclosure
        if prim.well is not None:
            wirenet_args.update({
                "well": prim.well,
                "well_net": cath if prim.implant.type_ == _prm.pImpl else an,
            })

        layout = self.fab.new_layout()
        layout.add_primitive(prim=prim.wire, **wirenet_args, **diode_params)
        wireact_bounds = layout.bounds(mask=prim.wire.mask)
        act_width = wireact_bounds.right - wireact_bounds.left
        act_height = wireact_bounds.top - wireact_bounds.bottom

        for i, ind in enumerate(prim.indicator):
            enc = prim.min_indicator_enclosure[i].max()
            layout += self(ind, width=(act_width + 2*enc), height=(act_height + 2*enc))

        return layout

    def MOSFET(self, prim: _prm.MOSFET, **mos_params) -> LayoutT:
        l = mos_params["l"]
        w = mos_params["w"]
        impl_enc = mos_params["activeimplant_enclosure"]
        gate_encs = mos_params["gateimplant_enclosures"]
        sdw = mos_params["sd_width"]

        try:
            portnets = cast(Mapping[str, _net.NetT], mos_params["portnets"])
        except KeyError:
            portnets = prim.ports

        gate_left = -0.5*l
        gate_right = 0.5*l
        gate_top = 0.5*w
        gate_bottom = -0.5*w

        layout = self.fab.new_layout()

        active = prim.gate.active
        active_width = l + 2*sdw
        active_left = -0.5*active_width
        active_right = 0.5*active_width
        active_bottom = gate_bottom
        active_top = gate_top

        mps = _geo.MultiPartShape(
            fullshape=_geo.Rect.from_size(width=active_width, height=w),
            parts=(
                _geo.Rect(
                    left=active_left, bottom=active_bottom,
                    right=gate_left, top=active_top,
                ),
                _geo.Rect(
                    left=gate_left, bottom =active_bottom,
                    right=gate_right, top=active_top,
                ),
                _geo.Rect(
                    left=gate_right, bottom =active_bottom,
                    right=active_right, top=active_top,
                ),
            )
        )
        layout.add_shape(layer=active, net=portnets["sourcedrain1"], shape=mps.parts[0])
        layout.add_shape(layer=active, net=portnets["bulk"], shape=mps.parts[1])
        layout.add_shape(layer=active, net=portnets["sourcedrain2"], shape=mps.parts[2])

        for impl in prim.implant:
            if impl in active.implant:
                layout.add_shape(layer=impl, net=None, shape=_rect(
                    active_left, active_bottom, active_right, active_top,
                    enclosure=impl_enc
                ))

        poly = prim.gate.poly
        ext = prim.computed.min_polyactive_extension
        poly_left = gate_left
        poly_bottom = gate_bottom - ext
        poly_right = gate_right
        poly_top = gate_top + ext
        layout.add_shape(layer=poly, net=portnets["gate"], shape=_geo.Rect(
            left=poly_left, bottom=poly_bottom, right=poly_right, top=poly_top,
        ))

        if prim.well is not None:
            enc = active.min_well_enclosure[active.well.index(prim.well)]
            layout.add_shape(layer=prim.well, net=portnets["bulk"], shape=_rect(
                active_left, active_bottom, active_right, active_top, enclosure=enc,
            ))

        oxide = prim.gate.oxide
        if oxide is not None:
            assert (active.oxide is not None) and (active.min_oxide_enclosure is not None)
            enc = getattr(
                prim.gate, "min_gateoxide_enclosure", _prp.Enclosure(self.tech.grid),
            )
            layout.add_shape(layer=oxide, net=None, shape=_rect(
                gate_left, gate_bottom, gate_right, gate_top, enclosure=enc,
            ))
            idx = active.oxide.index(oxide)
            enc = active.min_oxide_enclosure[idx]
            if enc is not None:
                layout.add_shape(layer=oxide, net=None, shape=_rect(
                    active_left, active_bottom, active_right, active_top,
                    enclosure=enc,
                ))
        if prim.gate.inside is not None:
            # TODO: Check is there is an enclosure rule from oxide around active
            # and apply the if so.
            for i, inside in enumerate(prim.gate.inside):
                enc = (
                    prim.gate.min_gateinside_enclosure[i]
                    if prim.gate.min_gateinside_enclosure is not None
                    else _prp.Enclosure(self.tech.grid)
                )
                layout.add_shape(layer=inside, net=None, shape=_rect(
                    gate_left, gate_bottom, gate_right, gate_top, enclosure=enc,
                ))
        for i, impl in enumerate(prim.implant):
            enc = gate_encs[i]
            layout.add_shape(layer=impl, net=None, shape=_rect(
                gate_left, gate_bottom, gate_right, gate_top, enclosure=enc,
            ))

        return layout

    def Bipolar(self, prim: _prm.Bipolar, **deepwell_params) -> LayoutT:
        # Currently it is assumed that fixed layouts are provided by the
        # technology
        raise NotImplementedError("layout generation for Bipolar primitive")


# import at end of file to avoid circular import problems
from .factory_ import LayoutFactory
