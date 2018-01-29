#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import fileinput
import collections

import yaml, json
import jsonpath_ng.ext
import jsonschema

jsonpath = jsonpath_ng.ext
optiondefaults = {"yaml": "{explicit_start: True, explicit_end: True, allow_unicode: True}", "json": "{indent: 2, encoding: utf-8}", "python": "{}"}

def validate(schemafile, args, encoding='utf-8'):
    schema = yaml.load("".join(fileinput.input(schemafile)))
    documents = yaml.load_all("".join(fileinput.input(args, openhook=fileinput.hook_encoded(encoding))))
    for filename in args:
        with open(filename) as infile:
            for document in yaml.load_all(infile):
                try:
                    jsonschema.validate(document, schema)
                except jsonschema.exceptions.ValidationError, e:
                    sys.stderr.write("%s: %s\n" % (filename, e.message))
                    sys.stderr.write("  document-path: %s\n" % (list(e.absolute_path)))
                    sys.stderr.write("  schema-path:   %s\n" % (list(e.absolute_schema_path)))
                    return False
    return True

def dump(args, path='$', format='yaml', yaml_options=optiondefaults['yaml'], json_options=optiondefaults['json'], encoding='utf-8'):
    dict_constructor = lambda loader, node: dict(loader.construct_pairs(node))
    orderedDict_constructor = lambda loader, node: collections.OrderedDict(loader.construct_pairs(node))
    orderedDict_representer = lambda dumper, data: dumper.represent_dict(data.iteritems())
    dumpers = {
        "yaml": {"dumper": yaml.dump, "kwargs": yaml_options, "yaml_constructor": orderedDict_constructor, "yaml_representer": orderedDict_representer},
        "json": {"dumper": json.dumps, "kwargs": json_options, "yaml_constructor": orderedDict_constructor, "yaml_representer": orderedDict_representer},
        "python": {"dumper": lambda x, **kwargs: x, "kwargs": '{}', "yaml_constructor": dict_constructor, "yaml_representer": orderedDict_representer}
    }
    yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dumpers[format]["yaml_constructor"])
    yaml.add_representer(collections.OrderedDict, dumpers[format]["yaml_representer"])
    documents = yaml.load_all("".join(fileinput.input(args, openhook=fileinput.hook_encoded(encoding))))
    formatoptions = dict(yaml.load(optiondefaults[format]), **yaml.load(dumpers[format]["kwargs"]))
    for document in documents:
        for match in jsonpath.parse(path).find(document):
            print dumpers[format]["dumper"](match.value, **formatoptions)
