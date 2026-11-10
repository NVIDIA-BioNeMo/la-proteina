# AFDB diffusion training IDs

Both datasets use Foldseek-clustered AFDB representatives with configured length cutoffs of 32–512 and average pLDDT cutoffs of 80–100.

| Training stage | ID list | Unique IDs | Filters |
| --- | --- | ---: | --- |
| Initial training | [Beta-only](AFDB_IDs-32-512-plddt80-beta.txt.gz) | 544,501 | Minimum beta fraction 0.01 |
| Fine-tuning | [Coil + beta](AFDB_IDs-32-512-plddt80-coil-beta.txt.gz) | 344,507 | Minimum beta fraction 0.01; maximum coil fraction 0.5; maximum consecutive coil residues 20 |

Each gzip file contains the complete list of sorted, unique AFDB model IDs, one per line. The fine-tuning list contains exactly the same IDs as `AFDB_IDs-512.txt` in the [NGC release](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/clara/resources/la_proteina_afdb_ids.zip/files).

Extract a list with `gzip -dc <file.txt.gz> > <file.txt>`. See the [dataset card](../afdb_datacard.md) for AFDB attribution and license information.
