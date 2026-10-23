"""Provider interfaces and metadata-safe fallback contracts.

Implementations supply provider integrations. Proprietary calculations and
provider-specific heuristics are intentionally outside this public interface.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal, Mapping

from .schemas import ExifMetadataInput, GeospatialAnchor


@dataclass(frozen=True)
class ProviderContext:
    """Safe provider inputs plus an explicit reason an anchor is unavailable."""

    status: Literal["READY", "EXIF_ABSENT", "EXIF_UNVERIFIED", "NO_GEOSPATIAL_ANCHOR"]
    metadata: ExifMetadataInput | None
    anchor: GeospatialAnchor | None


def prepare_provider_context(metadata: ExifMetadataInput | None) -> ProviderContext:
    """Permit geospatial context only for verified metadata with both coordinates.

    If EXIF is missing or unverified, providers may still analyze the image, but
    receive no metadata or geospatial anchor. Callers must retain an unscaled
    result unless an independently verified scale baseline is available.
    """
    if metadata is None or metadata.source == "unavailable":
        return ProviderContext("EXIF_ABSENT", None, None)

    if not metadata.verified:
        return ProviderContext("EXIF_UNVERIFIED", None, None)

    if metadata.latitude is None or metadata.longitude is None:
        return ProviderContext("NO_GEOSPATIAL_ANCHOR", metadata, None)

    anchor = GeospatialAnchor(
        latitude=metadata.latitude,
        longitude=metadata.longitude,
        verified=True,
        source="exif" if metadata.source == "exif" else "manual",
    )
    return ProviderContext("READY", metadata, anchor)


class VisionProvider(ABC):
    """Adapter for image observations; it must not invent calibrated dimensions."""

    @abstractmethod
    def analyze(
        self,
        image: Path,
        *,
        metadata: ExifMetadataInput | None,
        anchor: GeospatialAnchor | None,
    ) -> Mapping[str, object]:
        """Return provider observations without asserting independent verification."""
        pass


class TelemetryProvider(ABC):
    """Adapter for optional environmental observations tied to a verified anchor."""

    @abstractmethod
    def observe(
        self,
        *,
        anchor: GeospatialAnchor,
        captured_at: datetime | None,
    ) -> Mapping[str, object]:
        """Return sourced observations; an empty mapping means no observation."""
        pass


def telemetry_anchor(context: ProviderContext) -> GeospatialAnchor | None:
    """Return an anchor only when metadata has passed the verification gate."""
    if context.status != "READY":
        return None
    return context.anchor
