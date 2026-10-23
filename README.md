# Photogrammetric Shadow Scoping

**Architectural specification**  
Designed by Andrew Stevens

This document defines a public, implementation-neutral contract for turning
image and claim inputs into traceable geometric observations and deterministic
variance findings. It describes data boundaries, not proprietary calculation
math, thresholds, or internal rule weights.

## Pipeline

1. **EXIF / Geospatial Anchor** — Read image metadata when available and retain
   its source and verification state. EXIF is user-editable and is not proof of
   capture time or location by itself. A geospatial anchor is usable only when
   its coordinates have passed an independent verification step. If metadata is
   stripped, absent, or unverified, processing continues without that anchor.
2. **Background Shadow Scope Generation** — An optional Vision provider may
   return image observations. A telemetry provider may add sourced environmental
   observations only when a verified anchor is available. Provider estimates
   remain observations, not measured or calibrated dimensions. Provider
   unavailability or missing metadata must not be turned into invented
   measurements; the result remains explicitly unscaled or incomplete unless a
   separate scale baseline is supplied.
3. **Deterministic Reality-Diff** — Compare available, appropriately sourced
   inputs and emit stable machine-readable findings. This public contract names
   `ERR_GEOMETRIC_IMPOSSIBILITY`, `ERR_YIELD_PADDING`, and
   `ERR_MATH_MISMATCH`; it intentionally does not publish comparison
   tolerances, thresholds, or internal weights. Findings report variance for
   review and do not infer intent, fraud, or causation.

## Public contracts

- [`schemas.py`](./schemas.py) defines EXIF metadata, geospatial anchors,
  geometric scaling baselines, and discriminated finding schemas.
- [`interfaces.py`](./interfaces.py) defines abstract Vision and Telemetry
  provider boundaries and metadata-safe context preparation.
- Provider integrations are optional. An absent provider or an unusable anchor
  is represented as unavailable context, not a positive finding or a fabricated
  observation.
- The HMAC-SHA256 evidence manifest authenticates a canonical payload only when
  its key is protected and independently associated with the signer. It does
  not prove that source observations are true.

## UPE / UPL / UPPA boundary

The system is limited to factual intake, sourced observations, arithmetic, and
mathematical variance reporting. It does not offer or imply an engineering
opinion, legal interpretation, public-adjusting service, coverage opinion,
negotiation, or recommendation. In particular, a geometric variance is not an
engineering determination; a numeric discrepancy is not a legal conclusion;
and a yield-related review finding is not an adjustment recommendation.

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

For production, use a protected key-management service, define canonicalization
and key rotation operationally, and independently verify each input digest.
