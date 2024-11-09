testdata_cosmos
###############

*testdata_cosmos* is a package aggregating coadded images and catalogs from the COSMOS field for testing algorithms such as multiband fitting.
The file structure closely mimics an LSST `Butler <https://github.com/lsst/daf_butler>`_, and might one day be implemented as input data for a Butler similarly to `testdata_ci_imsim <https://github.com/lsst/testdata_ci_imsim>`_.

In the meantime, the repo contains (or will contain) scripts to populate the data by downloading public HST coadds, and by either symlinking or rsyncing processed HSC coadds from the USDF.

TESTDATA_COSMOS_DIR
###################

LSST Science Pipelines only need to run `setup` on the root directory to define this required env var.
Other users should add the output of `echo "export TESTDATA_COSMOS_DIR=$PWD"` to their `.bashrc` or equivalent startup script.

HST Data
########

The following files are required to use the COSMOS HST data:

[cosmos_acs_iphot_200709.parq](cosmos_acs_iphot_200709.parq) - A repackaged version of the `2007 COSMOS object catalog <https://irsa.ipac.caltech.edu/data/COSMOS/tables/photometry/cosmos_acs_iphot_200709.tbl>`_. See the `corresponding README <https://irsa.ipac.caltech.edu/data/COSMOS/tables/photometry/readme.cosmos_phot_20081101>`_ for more details.
[cosmos_hst_tiles.ecsv](cosmos_hst_tiles.ecsv) - A table containing filenames and the edges of the COSMOS HST/ACS mosaic tiles provided by Anton M. Koekemoer (STScI). See `the corresponding webpage <https://www.stsci.edu/~koekemoe/cosmos/current/>`_ for more details. These must be downloaded from `IRSA <https://irsa.ipac.caltech.edu/data/COSMOS/images/acs_mosaic_2.0/tiles/>`_ separately. Note that by default, the weight images and science images near the edge of the field are gzip compressed; the science images from complete tiles do not compress efficiently and so are left as-is to reduce read time.

Convenience functions for managing this data are provided in `sciunit_galaxies <https://github.com/lsst-sitcom/sciunit_galaxies>`_.

Users at the USDF should run `ln -s /sdf/group/rubin/shared/hst/cosmos/images/tiles cosmos_hst_tiles`.
For local use, run `python bin.src/make_hst_tile_script.py` and execute the printed commands to download the files.

In principle, data from other surveys like CANDELS may be added, but is not yet supported.

HSC Data
########

Users may add LSST pipelines-processed datasets in the `deepCoadd_*` and `objectTable_tract` folders.
Subsequent version may add the Scarlet models as well.
No convenience scripts are provided yet; users must either symlink the relevant files at the USDF or rsync them locally by running e.g.:

`rsync -avhu slac1:/sdf/group/rubin/repo/main/HSC/runs/RC2/w_2024_30/DM-45425c/step3/group2/job_000/deepCoadd_calexp/9813/40/ deepCoadd_calexp/9813/40/`

Alternatively, users may manage cutouts from the HSC Public Data Releases using `astro_imaging <https://github.com/taranu/astro_imaging>`_, `unagi <https://github.com/dr-guangtou/unagi>`_, or other such tools. 
