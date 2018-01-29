# ytools

Command-line tool for selectively dumping nodes from `yaml` (or `json`) documents in `yaml` or `json` format.

###### Features

+ Output `yaml` as `json` or `python`
+ Output `json` as `yaml` or `python` (provided that there are no duplicate mapping entry in the `json` source)
+ Extract particular nodes from `yaml` and `json` files.
  + If `yaml` is used as output format (default) the output is a valid `yaml` document.
+ Validate `yaml` and `json` documents.
  + The `json-schema` can be provided in `yaml` format as well, which improves readability and writability.
+ Multi-document support
  + Multiple input files
  + ... as well as multiple `yaml` documents within a file
  + ... and a combination of both

###### Installation

`pip install ytools`

###### Description

For selecting nodes, `ytools` uses `jsonpath_ng.ext`.  
The syntax is documented at https://pypi.python.org/pypi/jsonpath-ng/1.4.2.

By default (if no path is provided), complete input documents are dumped in `yaml` format (path defaults to `'$'`).  
This can be used to get `yaml` output for `json` documents or vice versa:
- `python ytools.py input.json`  
  ... for converting json to yaml, or ...  
- `python ytools.py input.yaml -f json`  
  ... for the opposite direction.


Additionally, `yaml` and `json` documents can be validated against a `json-schema` which may be provided in `yaml` or `json` format.  
`schema.yaml` is a sample for `json-schema` in `yaml` format.

`ytools -h`

```
$ ytools -h
Usage: /usr/local/bin/ytools [OPTION] -p JSONPATH_EXPRESSION FILE...

Dumps data from json (or yaml) documents in yaml format. Command line wrapper
for jsonpath-ng.

Options:
  -h, --help            show this help message and exit
  -p PATH, --json-path=PATH
                        Syntax for jsonpath expression:
                        https://pypi.python.org/pypi/jsonpath-ng/1.4.2
  -f OUTPUTFORMAT, --output-format=OUTPUTFORMAT
                        Output format. Can be "yaml", "json" or "python".
                        [default: yaml]
  -y YAML_OPTIONS, --yaml-options=YAML_OPTIONS
                        kwargs for yaml.dump (pyYaml) as yaml.mapping (for
                        experts). [default: '{explicit_start: True,
                        explicit_end: True, allow_unicode: True}']
  -j JSON_OPTIONS, --json-options=JSON_OPTIONS
                        kwargs for json.dumps as yaml.mapping (for experts).
                        [default: '{indent: 2, encoding: utf-8}']
  -v SCHEMA, --validate=SCHEMA
                        Validate documents against json-schema
  --encoding=ENCODING   Set encoding of input documents (if different from
                        utf-8)
```

## Samples

The samples are based on the following data.

### Sample Data

#### Input data
`input.yaml`:

```yaml
documents:
  - title: Some document title
    sections:
    - title: Some section title
      description: Some section description
      text: Some text for some section
      chapters:
      - title: Some chapter title
        description: Some chapter description
        text: The text of some chapter
      - title: Some other chapter title
        description:
        - descriptionparagraph1: Some description for other chapter
        - descriptionparagraph2: Some description for other chapter
        text: The text of some other chapter
    - title: Some other section title
      description: Some other section description
      text: Some text for some other section
      chapters:
        - title: About encoding
          description: "Some German: äöü,ÄÖY,ß"
```

#### Schema for validating `input.yaml`

`schema.yaml`

```yaml
$schema: "http://json-schema.org/schema#"

definitions:
  chapter:
    type: object
    properties:
      title: {type: string}
      description:
        oneOf: [{type: string}, {type: array}]
      text: {type: string}
    additionalProperties: false
    required: [title, description]
  chapters:
    type: array
    items: {$ref: "#/definitions/chapter"}
    additionalItems: false
  section:
    type: object
    properties:
      title: {type: string}
      description: {type: string}
      text: {type: string}
      chapters: {$ref: "#/definitions/chapters"}
    additionalProperties: false
    required: [title, description]
  sections:
    type: array
    items: {$ref: "#/definitions/section"}
    additionalItems: false
  document:
    type: object
    properties:
      title: {type: string}
      description: {type: string}
      sections: {$ref: "#/definitions/sections"}
    additionalProperties: false
    required: [title, description]
  documents:
    type: array
    items: {$ref: "#/definitions/document"}
    additionalItems: false
type: object
properties:
  documents: {$ref: "#/definitions/documents"}
additionalProperties: false
```

### Outputs

#### When not providing a jsonpath expression
If you don't provide a jsonpath expression using the `-p` option ytools uses `'$'` as default and therefore dumps the complete input:

```
🎼  ytools input.yaml
---
documents:
- title: Some document title
  description: The document's description
  sections:
  - title: Some section title
    description: Some section description
    text: Some text for some section
    chapters:
    - {title: Some chapter title, description: Some chapter description, text: The
        text of some chapter}
    - title: Some other chapter title
      description:
      - {descriptionparagraph1: Some description for other chapter}
      - {descriptionparagraph2: Some description for other chapter}
      text: The text of some other chapter
  - title: Some other section title
    description: Some other section description
    text: Some text for some other section
    chapters:
    - {title: About encoding, description: 'Some German: äöü,ÄÖY,ß'}
...

```

#### Output format `yaml` (default)

With the `yaml` output format by default, each match is output as a separate `yaml` document. This way we achieve that the output is valid `yaml`.:

```
🎼  ytools -p '$..chapters[*].description' input.yaml
--- Some chapter description
...

---
- {descriptionparagraph1: Some description for other chapter}
- {descriptionparagraph2: Some description for other chapter}
...

--- 'Some German: äöü,ÄÖY,ß'
...

```

If you want different behavior you can set `explicit_start` and/or `explicit_end` to `False`. In this case the output will no longer be guaranteed to be valid `yaml`:

```
🎼  ytools -p '$..chapters[*].description' input.yaml --yaml-options='{explicit_start: False, explicit_end: False}'
Some chapter description
...

- {descriptionparagraph1: Some description for other chapter}
- {descriptionparagraph2: Some description for other chapter}

'Some German: äöü,ÄÖY,ß'

```
#### Other output formats

Unfortunately, when using the `json` or `python` output format the same selection can't produce valid `json` or `python` output. That's because neither json nor python support the concept of (multiple) documents:

```
🎼  ytools -p '$..chapters[*].description' input.yaml -f json --json-options='{indent: 4}'
"Some chapter description"
[
    {
        "descriptionparagraph1": "Some description for other chapter"
    },
    {
        "descriptionparagraph2": "Some description for other chapter"
    }
]
"Some German: \u00e4\u00f6\u00fc,\u00c4\u00d6Y,\u00df"
```

That's definitely not valid json.

Neither is the following valid python:

```
🎼  ytools -p '$..chapters[*].description' input.yaml -f python
Some chapter description
[{'descriptionparagraph1': 'Some description for other chapter'}, {'descriptionparagraph2': 'Some description for other chapter'}]
Some German: äöü,ÄÖY,ß
```

So **if you ever want to process the output automatically please stick to `yaml`**.
