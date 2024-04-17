# SEEK Helper

This library serves to facilitate the use of the SEEK API, abstracting some configurations and commands.

Please check the API documentation to see the response structures and more.

The FAIRDOMHub API documentation is [here](https://fairdomhub.org/api).

## Installation

- TODO

## Usage

Import the library and instantiate the `SeekHelper` class:

```python
from seek_helper import SeekHelper

seek_helper = SeekHelper('your_token', 'seek_instance_url', 'output_path')
```

`your_token`: your SEEK API Token. It can be generated on SEEK in Profile > Actions > API Token

`seek_instance_url`: the SEEK instance URL to be used, like http://localhost:3000

`output_path`: a path where downloaded files will be stored

Then you can instantiate an object of a resource. Example:

```python
project = seek_helper.Project
p = project.get(1)
print(p)
```

This code snippet will print data of the Project of id 1 in JSON format.

### Resources

These are the current resources and operations available:

**Yellow Pages**
- Projects (get, create, update, delete, download_data_files)

**Experiments**
- Investigations (get, create, update, delete)
- Assays (get, create, update, delete)
- Studies (get, create, update, delete)

**Assets**
- Data Files (get, create, update, delete, download)

## TODO
- Include more resources and operations
- Write unit tests
- Typify entities
