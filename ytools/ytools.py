#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import fileinput
import collections

import yaml, json
import jsonpath_ng.ext as jsonpath
import jsonschema

optiondefaults = {"yaml": "{explicit_start: True, explicit_end: True, allow_unicode: True}", "json": "{indent: 2, encoding: utf-8}", "python": "{}"}

def validate(schemafile, datafiles, encoding='utf-8'):
    schema = yaml.load("".join(fileinput.input(schemafile)))
    documents = yaml.load_all("".join(fileinput.input(datafiles, openhook=fileinput.hook_encoded(encoding))))
    for filename in datafiles:
        with open(filename) as infile:
            for document in yaml.load_all(infile):
                try:
                    jsonschema.validate(document, schema, format_checker=jsonschema.FormatChecker())
                except jsonschema.exceptions.ValidationError, e:
                    e.filename = filename
                    raise e

def dump(datafiles, path='$', format='yaml', yaml_options=optiondefaults['yaml'], json_options=optiondefaults['json'], encoding='utf-8'):
    def orderedDict_constructor(loader, node, deep=False):
        data = collections.OrderedDict()
        yield data
        if isinstance(node, yaml.MappingNode):
            loader.flatten_mapping(node)
        data.update(collections.OrderedDict(loader.construct_pairs(node, deep)))
    dict_constructor = lambda loader, node: dict(loader.construct_pairs(node))
    encoders = {
        "yaml": {"dumper": yaml.dump, "kwargs": yaml_options, "yaml_constructor": orderedDict_constructor},
        "json": {"dumper": json.dumps, "kwargs": json_options, "yaml_constructor": orderedDict_constructor},
        "python": {"dumper": lambda x, **kwargs: x, "kwargs": '{}', "yaml_constructor": dict_constructor}
    }
    yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, encoders[format]["yaml_constructor"])
    yaml.add_constructor(u'tag:yaml.org,2002:timestamp', yaml.constructor.SafeConstructor.construct_yaml_str)
    yaml.add_representer(collections.OrderedDict, lambda dumper, data: dumper.represent_dict(data.iteritems()))
    documents = yaml.load_all("".join(fileinput.input(datafiles, openhook=fileinput.hook_encoded(encoding))))
    formatoptions = dict(yaml.load(optiondefaults[format]), **yaml.load(encoders[format]["kwargs"]))
    for document in documents:
        for match in jsonpath.parse(path).find(document):
            print encoders[format]["dumper"](match.value, **formatoptions)
