"""Verify the released AFDB ID snapshots using only the standard library."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import zipfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ngc-archive", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "manifest.json").read_text())
    sets = {}
    for entry in manifest["datasets"]:
        if entry["location"] != "repository":
            continue
        name = entry["file"]
        compressed = (root / name).read_bytes()
        require(digest(compressed) == entry["gzip_sha256"], f"{name}: gzip checksum")
        data = gzip.decompress(compressed)
        require(digest(data) == entry["ids_sha256"], f"{name}: ID checksum")
        require(data.endswith(b"\n") and b"\r" not in data, f"{name}: line endings")
        ids = data.decode("ascii").splitlines()
        require(len(ids) == entry["count"], f"{name}: count")
        require(ids == sorted(set(ids)), f"{name}: sorting or duplicate IDs")
        require(all(re.fullmatch(r"AF-[A-Z0-9]+-F[1-9][0-9]*-model_v4", i) for i in ids),
                f"{name}: invalid AFDB ID")
        sets[name] = set(ids)
        print(f"{name}: {len(ids):,} unique IDs verified")

    full = sets["AFDB_IDs-32-512-plddt80.txt.gz"]
    coil = sets["AFDB_IDs-32-512-plddt80-coil.txt.gz"]
    beta = sets["AFDB_IDs-32-512-plddt80-beta.txt.gz"]
    require(coil <= full and beta <= full, "Filtered lists must be subsets of pLDDT-only")
    overlap = coil & beta
    published = next(e for e in manifest["datasets"] if e.get("ngc_file") == "AFDB_IDs-512.txt")
    require(sets[published["file"]] == overlap, "Both-filter list differs from coil/beta intersection")
    require(len(overlap) == published["count"], "Coil/beta intersection count")
    normalized = ("\n".join(sorted(overlap)) + "\n").encode("ascii")
    require(digest(normalized) == published["ids_sha256"], "Coil/beta intersection checksum")

    if args.ngc_archive:
        require(digest(args.ngc_archive.read_bytes()) == manifest["ngc_archive_sha256"],
                "Expected the original NGC v1.0 archive")
        with zipfile.ZipFile(args.ngc_archive) as archive:
            ids = archive.read("AFDB_IDs-512.txt").decode("ascii").splitlines()
        require(len(ids) == len(set(ids)) == published["count"], "NGC count or duplicates")
        require(set(ids) == overlap, "NGC IDs differ from coil/beta intersection")
        print("NGC short-chain release matches the intersection exactly")
    print(f"Verified {len(full - overlap):,} additional IDs in the pLDDT-only list")


if __name__ == "__main__":
    main()
