# Photogrammetric Shadow Scoping

**Architectural specification**
Designed by Andrew Stevens

Copyright (c) 2026 Andrew Stevens. All rights reserved. See [LICENSE](./LICENSE).

## What this is

Photogrammetric Shadow Scoping builds a shadow scope: a baseline the system
constructs itself from the evidence side alone. The evidence is photographs
and telemetry documents, including measurement reports from providers such as
RoofSnap, Hover, and EagleView. The baseline is measured against building
codes, mandates, manufacturer specifications, and ground truth physics.

The submitted estimate is never an ingredient of the baseline. That
separation is the method. It is not a reading of shadows in a photograph, and
it is not a comparison that starts from the estimate it is checking.

This document defines a public, implementation-neutral contract. It describes
data boundaries, not proprietary calculation math, thresholds, or internal
rule weights.

## Modes

- Evidence alone yields the baseline.
- An estimate alone still yields its internal audit.
- Evidence and estimate together yield the comparison.

The baseline constructor is a general construction layer for every file type.
It is not locked to roofing or to any single trade. When an input is missing,
the missing item is recorded as a specific outstanding ask and everything
else is still produced. Baseline findings report; they never block or alter
the audit's own results.

## Pricing discipline

A price enters the baseline only when it is tied to a named, verifiable
source record. Each line carries one designated pricing record. Corroborating
sources are filed beside it and are never averaged or blended into it. A fair
market line is labeled region specific, with the region and the source named.
A price with no source does not enter the baseline at all.

## Evidence handling

- **EXIF / geospatial anchor.** Image metadata is read when available and
  retained with its source and verification state. EXIF is user-editable and
  is not proof of capture time or location by itself. A geospatial anchor is
  usable only when its coordinates have passed an independent verification
  step. If metadata is stripped, absent, or unverified, processing continues
  without that anchor.
- **Provider observations.** A Vision provider may return image observations,
  and a telemetry provider may add sourced environmental observations.
  Provider estimates remain observations, not measured or calibrated
  dimensions. Provider unavailability or missing metadata must not be turned
  into invented measurements; the result remains explicitly unscaled or
  incomplete unless a separate scale baseline is supplied.

## Deterministic findings

The comparison emits stable machine-readable findings. This public contract
names `ERR_GEOMETRIC_IMPOSSIBILITY`, `ERR_YIELD_PADDING`, and
`ERR_MATH_MISMATCH`; it intentionally does not publish comparison tolerances,
thresholds, or internal weights. Findings report variance for review and do
not infer intent, fraud, or causation.

## Public contracts

- [`schemas.py`](./schemas.py) defines EXIF metadata, geospatial anchors,
  geometric scaling baselines, and discriminated finding schemas. The models
  describe inputs and outputs only; they intentionally do not encode private
  comparison tolerances, thresholds, or calculation rules.
- [`interfaces.py`](./interfaces.py) defines abstract Vision and Telemetry
  provider boundaries and metadata-safe context preparation. Proprietary
  calculations and provider-specific heuristics are intentionally outside
  this public interface.
- Provider integrations are optional. An absent provider or an unusable
  anchor is represented as unavailable context, not a positive finding or a
  fabricated observation.
- The HMAC-SHA256 evidence manifest authenticates a canonical payload only
  when its key is protected and independently associated with the signer. It
  does not prove that source observations are true.

## UPE / UPL / UPPA boundary

The system is limited to factual intake, sourced observations, arithmetic,
and mathematical variance reporting. It does not offer or imply an
engineering opinion, legal interpretation, public-adjusting service, coverage
opinion, negotiation, or recommendation. In particular, a geometric variance
is not an engineering determination; a numeric discrepancy is not a legal
conclusion; and a yield-related review finding is not an adjustment
recommendation.

These are product-boundary statements, not a legal-compliance certification.
Applicable requirements depend on jurisdiction and deployment; qualified
counsel should review the actual product and its use.

## Example evidence payload

The signature below is computed over the UTF-8 JSON encoding of the manifest
body using sorted keys and compact separators. It uses the public,
example-only key `public-example-key-not-secret`; this is not a production
secret and provides no security.

```json
{
  "algorithm": "HMAC-SHA256",
  "input_sha256": {
    "photo.jpg": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  },
  "payload": {
    "findings": [
      {
        "code": "ERR_MATH_MISMATCH",
        "message": "Submitted arithmetic differs from the deterministic check."
      }
    ],
    "verdict": "REVIEW"
  },
  "hmac_sha256": "19e71b014e54d62a7a7c7ec99506ab002a009d9c4d4495d06e8df05a54eec010"
}
```

For production, use a protected key-management service, define
canonicalization and key rotation operationally, and independently verify
each input digest.

## Viewing, requests, and licensing

This repository is public so the specification can be read and discussed. It
is not open source. Copyright (c) 2026 Andrew Stevens, all rights reserved.
Publication grants no right to use, copy, modify, or distribute this work.
Use requires a paid license granted in writing by the owner. Requests to
license this work, or to propose changes to it, may be opened as issues in
this repository.
