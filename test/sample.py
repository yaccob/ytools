#!/usr/bin/env python2
from __future__ import print_function
import ytools

if __name__ == "__main__":
    print(ytools.__version__)
    ytools.validate("test/sampleschema.yaml", ["test/sampledata.yaml"])
    ytools.dump("test/sampledata.yaml", path="$.metrics", yaml_options="default_flow_style: false")
