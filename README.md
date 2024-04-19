# SEEK Helper

This library serves to facilitate the use of the SEEK API, abstracting some configurations and commands.

Please check the API documentation to see the response structures and more.

The FAIRDOMHub API documentation is [here](https://fairdomhub.org/api).

## Installation

### Requirements
- Python 3.8+
- Pip 24+

### Steps
1) Clone this repository
2) Install `build`:
    ```python
    python3 -m pip install --upgrade build
    ```
3) Inside `seek-helper` directory, build the library:
    ```python
    python3 -m build
    ```
3) Copy the generated `tar.gz` file to your project/code directory
4) Inside your project/code directory, install the library:
    ```python
    pip install seek_helper-0.1.0.tar.gz
    ```

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

This code snippet will print data of the Project of id 1 in `JSON` format.

### Resources & Operations

Users can only manage the resources they are permitted to manage or are public.

Below are the current resources and operations available. Check the API documentation for the correct payloads and responses.

**Yellow Pages**
- Projects
    ```python
    project = seek_helper.Project

    # Examples:

    # Get all projects
    p = project.get()

    # Get a project by id
    p = project.get(1)

    # Create a project
    project.create({
        "data": {
            "type": "projects",
            "attributes": {
                "title": "Project Example",
                "description": "This is an example of project creation",
            },
        }
    })

    # Update a project
    project.update(1, {
        "data": {
            "type": "projects",
            "attributes": {
                "description": "This is an example of project update",
            },
        }
    })

    # Download all data files of a project
    project.download_data_files()

    # Delete a project by id
    project.delete(1)
    ```

**Experiments**
- Investigations
    ```python
    investigation = seek_helper.Investigation

    # Examples:

    # Get all investigations
    i = investigation.get()

    # Get an investigation by id
    i = investigation.get(1)

    # Create an investigation
    investigation.create({
        "data": {
            "type": "investigations",
            "attributes": {
                "title": "Investigation Example",
                "description": "This is an example of investigation creation",
            },
            "relationships": {
                "projects": {
                    "data": [
                        {
                            "type": "projects",
                            "id": "1"
                        },
                    ]
                },
            }
        }
    })

    # Update an investigation
    investigation.update(1, {
        "data": {
            "type": "investigations",
            "attributes": {
                "description": "This is an example of investigation update",
            },
        }
    })

    # Delete an investigation by id
    investigation.delete(1)
    ```

- Studies
    ```python
    study = seek_helper.Study

    # Examples:

    # Get all studies
    s = study.get()

    # Get a study by id
    s = study.get(1)

    # Create a study
    study.create({
        "data": {
            "type": "studies",
            "attributes": {
                "title": "Study Example",
                "description": "This is an example of study creation",
            },
            "relationships": {
                "investigation": {
                    "data": {
                        "id": "1",
                        "type": "investigations"
                    }
                },
            }
        }
    })

    # Update a study
    study.update(1, {
        "data": {
            "type": "studies",
            "attributes": {
                "description": "This is an example of study update",
            },
        }
    })

    # Delete a study by id
    study.delete(1)
    ```

- Assays
    ```python
    assay = seek_helper.Assay

    # Examples:

    # Get all assays
    a = assay.get()

    # Get an assay by id
    a = assay.get(1)

    # Create an assay
    assay.create({
        "data": {
            "type": "assays",
            "attributes": {
                "title": "Assay Example",
                "assay_class": {
                    "key": "EXP"
                },
                "assay_type": {
                    "uri": "http://jermontology.org/ontology/JERMOntology#Transcriptomics"
                },
                "description": "This is an example of assay creation",
            },
            "relationships": {
                "study": {
                    "data": {
                        "id": "1",
                        "type": "studies"
                    }
                },
            }
        }
    })

    # Update an assay
    assay.update(1, {
        "data": {
            "type": "assays",
            "attributes": {
                "description": "This is an example of assay update",
            },
        }
    })

    # Delete an assay by id
    assay.delete(1)
    ```

**Assets**
- Data Files
    ```python
    data_file = seek_helper.DataFile

    # Examples:

    # Get all data files
    df = data_file.get()

    # Get a data file by id
    df = data_file.get(1)

    # Download a data file
    data_file.download(1)

    # Delete a data file by id
    data_file.delete(1)
    ```

## TODO
- Include more resources and operations
- Write unit tests
- Upload the library to a repository like PyPi
- Typify entities
