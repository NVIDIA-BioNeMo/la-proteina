# AFDB ID manifests

These lists supplement the [NGC v1.0 archive](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/clara/resources/la_proteina_afdb_ids.zip/files?version=1.0). They contain AFDB identifiers only, exported from the preserved filtered CSV manifests for the Foldseek-clustered AFDB representatives. No structures, new filtering, or train/validation split is included.

All three added lists use the source configuration's length cutoffs of 32 and 512 and average-pLDDT cutoffs of 80 and 100. The actual lengths in these snapshots range from 33 to 511. The following table records the additional **configured thresholds**, not a new recipe for recomputing the snapshots:

| ID list | Maximum coil fraction | Maximum consecutive coil residues | Minimum beta fraction | Unique IDs | IDs additional to NGC `AFDB_IDs-512.txt` |
| --- | --- | --- | --- | ---: | ---: |
| [pLDDT only](AFDB_IDs-32-512-plddt80.txt.gz) | None | None | None | 734,657 | 390,150 |
| [pLDDT + coil](AFDB_IDs-32-512-plddt80-coil.txt.gz) | 0.5 | 20 | None | 498,074 | 153,567 |
| [pLDDT + beta](AFDB_IDs-32-512-plddt80-beta.txt.gz) | None | None | 0.01 | 544,501 | 199,994 |
| Existing NGC `AFDB_IDs-512.txt` | 0.5 | 20 | 0.01 | 344,507 | 0 |

Each added file is a complete list for its filter configuration, not just the additional IDs. The existing NGC short-chain list is a subset of every added list; it is exactly the intersection of the coil and beta lists. The NGC archive and its long-chain `AFDB_IDs-896.txt` remain unchanged. The latter is a separate custom AFDB dataset, not a longer version of these Foldseek representative lists.

## Relationship to the paper

[La-Proteina v2, Appendix C.1–C.2](https://arxiv.org/html/2507.09466v2#A3.SS1) describes training in stages and an approximately 550k set before beta filtering. The preserved manifests do not support identifying a dataset by that rounded count alone: the 544,501-entry list already has a beta filter and no coil filters, whereas the coil-filtered list without a beta filter has 498,074 entries. The pLDDT-only list has 734,657 entries.

These exports make each missing variant available with explicit provenance. They do not establish which exact manifest was consumed by every historical checkpoint. In particular, do not treat the 544,501-entry list as a no-beta VAE training set solely because its size is approximately 550k. The counts above describe these source snapshots; the existing model/dataset cards' count of 344,508 differs by one from the 344,507 unique IDs actually present in the NGC v1.0 short-chain file.

## Format and verification

The gzip files decompress to ASCII text with one full AFDB model identifier per line, no header, sorted lexicographically, without duplicates. Identifiers retain the `AF-…-F1-model_v4` form used by the existing release. For example:

```sh
gzip -dc datasetcard/afdb_ids/AFDB_IDs-32-512-plddt80.txt.gz > AFDB_IDs-32-512-plddt80.txt
python datasetcard/afdb_ids/verify.py
# Also compare against the downloaded, unmodified NGC v1.0 archive:
python datasetcard/afdb_ids/verify.py --ngc-archive /path/to/La-Proteina_AFDB_IDs.zip
```

[manifest.json](manifest.json) records source CSV basenames and SHA-256 checksums, exact counts, observed length extrema, configured thresholds, compressed-file checksums, and checksums of the sorted uncompressed IDs. Source CSVs are provenance records, not required downloads. Verification uses only the Python standard library and checks counts, checksums, identifier syntax, sorting, uniqueness, subset relationships, and the coil/beta intersection. With `--ngc-archive`, it additionally checks exact set equality with the published short-chain list.

The underlying AFDB data is distributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please retain the AFDB attribution and references in the [dataset card](../afdb_datacard.md).
