from astropy.table import Table
import os

testdata_cosmos_dir = os.getenv("TESTDATA_COSMOS_DIR")
if testdata_cosmos_dir is None:
    raise ValueError("TESTDATA_COSMOS_DIR must be set")

tiles = Table.read(f"{testdata_cosmos_dir}/cosmos_hst_tiles.ecsv")

url_tiles = "https://irsa.ipac.caltech.edu/data/COSMOS/images/acs_mosaic_2.0/tiles/"
path_out = f"{testdata_cosmos_dir}/cosmos_hst_tiles"

print(f"mkdir {path_out}")

extension = ".gz"

for row in tiles:
    sci, wht = (row[f"path_{suffix}"] for suffix in ("science", "weight"))
    for filename in (sci, wht):
        is_gz = filename.endswith(extension)
        url_tile = f"{url_tiles}{filename}{extension if not is_gz else ''}"
        print(f"wget -P {path_out}/ {url_tile}")
        if not is_gz:
            print(f"gunzip {path_out}/{filename}")
