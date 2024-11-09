import argparse
import glob
import os

import lsst.daf.butler as dafButler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--butler", type=str, help="Butler path", default="/repo/main")
    parser.add_argument("-c", "--collection", type=str, help="HSC/RC2 collection", required=True)
    parser.add_argument("--clean", action="store_true")
    parser.add_argument("-p", "--patch", type=int, help="Patch number", default=40)
    parser.add_argument("-t", "--tract", type=int, help="Tract number", default=9813)
    parser.add_argument("-s", "--skymap", type=str, help="Skymap name", default="hsc_rings_v1")
    args = parser.parse_args()

    butler = dafButler.Butler(args.butler, collections=[args.collection])
    bands = ("g", "r", "i", "z", "y")
    patch = args.patch
    tract = args.tract
    testdata_cosmos_dir = os.getenv("TESTDATA_COSMOS_DIR")
    if not len(testdata_cosmos_dir) > 0:
        raise RuntimeError("TESTDATA_COSMOS_DIR is not defined; did you run setup -jr . ?")

    for dataset_type, has_band, has_patch in (
        ("deepCoadd_calexp", True, True), ("deepCoadd_meas", True, True), ("deepCoadd_ref", False, True),
        ("objectTable_tract", False, False),
    ):
        subdir = f"{testdata_cosmos_dir}/{dataset_type}/{tract}"
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        kwargs = {}
        if has_patch:
            subdir = f"{subdir}/{patch}"
            kwargs["patch"] = patch
            if not os.path.exists(subdir):
                os.mkdir(subdir)
        bands = bands if has_band else (None,)
        for band in bands:
            subdir_band = subdir
            if band:
                kwargs["band"] = band
                subdir_band = f"{subdir_band}/{band}"
                if not os.path.exists(subdir_band):
                    os.mkdir(subdir_band)
            if args.clean:
                for filename in glob.glob(f"{subdir_band}/*"):
                    if os.path.islink(filename):
                        os.remove(filename)
            path = butler.getURI(dataset_type, skymap=args.skymap, tract=tract, **kwargs).path
            filename = path.rsplit("/", 1)[1]
            os.symlink(path, f"{subdir_band}/{filename}")


if __name__ == "__main__":
    main()
