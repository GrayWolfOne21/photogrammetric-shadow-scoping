"""Public data contracts for Photogrammetric Shadow Scoping.

These models describe inputs and outputs only; they intentionally do not encode
private comparison tolerances, thresholds, or calculation rules.
"""
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ExifMetadataInput(ContractModel):
    """Best-effort image metadata with caller-supplied provenance state.

    EXIF fields are not cryptographically authenticated. ``verified`` must only
    be true when a separate trusted process has verified the metadata.
    """

    source: Literal["exif", "manual", "unavailable"] = "unavailable"
    verified: bool = False
    latitude: float | None = Field(default=None, ge=-90, le=90, allow_inf_nan=False)
    longitude: float | None = Field(default=None, ge=-180, le=180, allow_inf_nan=False)
    altitude_m: float | None = Field(default=None, allow_inf_nan=False)
    focal_length_mm: float | None = Field(default=None, gt=0, allow_inf_nan=False)
    captured_at: datetime | None = None


class GeospatialAnchor(ContractModel):
    latitude: float = Field(ge=-90, le=90, allow_inf_nan=False)
    longitude: float = Field(ge=-180, le=180, allow_inf_nan=False)
    verified: bool = False
    source: Literal["exif", "manual"] = "exif"


class GeometricScalingBaseline(ContractModel):
    """A scale reference; does not specify how downstream comparisons work."""

    status: Literal["calibrated", "estimate_only", "unscaled"] = "unscaled"
    scale_ft_per_pixel: float | None = Field(default=None, gt=0, allow_inf_nan=False)
    source: Literal[
        "verified_reference", "manual_reference", "provider_estimate", "unavailable"
    ] = "unavailable"
    anchor: GeospatialAnchor | None = None
    reference_id: str | None = None

    @model_validator(mode="after")
    def calibrated_baseline_requires_scale(self) -> GeometricScalingBaseline:
        if self.status == "calibrated" and self.scale_ft_per_pixel is None:
            raise ValueError("a calibrated baseline requires a scale")
        return self


ScalarEvidence = str | int | float | bool | None


class DeterministicFinding(ContractModel):
    message: str
    evidence: dict[str, ScalarEvidence] = Field(default_factory=dict)


class GeometricImpossibilityFinding(DeterministicFinding):
    code: Literal["ERR_GEOMETRIC_IMPOSSIBILITY"] = "ERR_GEOMETRIC_IMPOSSIBILITY"


class YieldPaddingFinding(DeterministicFinding):
    code: Literal["ERR_YIELD_PADDING"] = "ERR_YIELD_PADDING"


class MathMismatchFinding(DeterministicFinding):
    code: Literal["ERR_MATH_MISMATCH"] = "ERR_MATH_MISMATCH"


DeterministicErrorOutput = Annotated[
    Union[
        GeometricImpossibilityFinding,
        YieldPaddingFinding,
        MathMismatchFinding,
    ],
    Field(discriminator="code"),
]
