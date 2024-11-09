import argparse

import lsst.daf.butler as dafButler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--butler", type=str, help="Butler path", default="/repo/main")
    parser.add_argument("-c", "--collection", type=str, help="HSC/RC2 collection", required=True)
    parser.add_argument("-p", "--patch", type=int, help="Patch number", default=44)
    parser.add_argument("-t", "--tract", type=int, help="Tract number", default=9813)
    parser.add_argument("-s", "--skymap", type=str, help="Skymap name", default="hsc_rings_v1")
    args = parser.parse_args()

    butler = dafButler.Butler(parser.butler, collections=[args.collection])
    bands = ("g", "r", "i", "z", "y")
    patch = args.patch
    tract = args.tract

    for dataset_type, has_band, has_patch in (
        ("deepCoadd_calexp", True, True), ("deepCoadd_meas", True, True), ("deepCoadd_ref", False, True),
        ("objectTable_tract", False, False),
    ):
        subdir = f"{dataset_type}/{tract}"
        kwargs = {}
        if has_patch:
            subdir = f"{subdir}/{patch}"
            kwargs["patch"] = patch
        bands = bands if has_band else (None,)
        for band in bands:
            if band:
                kwargs["band"] = band
            uri = butler.getURI(dataset_type, skymap=args.skymap, tract=tract, **kwargs)


if __name__ == "__main__":
    main()
