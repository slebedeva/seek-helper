# SEEK Helper

This library serves to facilitate the use of the [FAIRDOM-SEEK](https://seek4science.org) API, abstracting some configurations and commands.

Please check the API documentation to see the responses structure and more.

The FAIRDOMHub API documentation can be found [here](https://fairdomhub.org/api).

This library was created by [Danilo](https://github.com/DaniloBueno) and [Andrew](https://github.com/AndrewWood94) for the [PhenomUK](https://phenomuk.org/) project.

## Table of contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Resources & Operations](#resources--operations)
    1. [Yellow Pages](#yellow-pages)
    2. [Experiments](#experiments)
    3. [Assets](#assets)
4. [Experimental Features](#experimental-features)
5. [Testing](#testing)
6. [TODO](#todo)

## Installation

### Requirements
- Python 3.8+
- Pip 24+

### Steps
1. Clone this repository
2. Install `build`:
    ```bash
    python3 -m pip install --upgrade build
    ```
3. Inside `seek-helper` directory, build the library:
    ```bash
    python3 -m build
    ```
4. Copy the generated `tar.gz` file to your project/code directory
5. Inside your project/code directory, install the library (e.g., version 0.1.0):
    ```bash
    pip install seek_helper-0.1.0.tar.gz
    ```

## Usage

Import the library and instantiate the `SeekHelper` class:

```python
from seek_helper import SeekHelper

seek_helper = SeekHelper('your_token', 'seek_instance_url', 'output_path', 'input_path')
```

`your_token`: your SEEK API Token. It can be generated on SEEK in Profile > Actions > API Token

`seek_instance_url`: the SEEK instance URL to be used, like http://localhost:3000

`output_path`: the relative path to the directory where downloaded files will be stored

`input_path`: the relative path to the directory where files for upload are stored

Then you can instantiate an object of a resource. Example:

```python
project = seek_helper.Project
p = project.get(1)
print(p)
```

This code snippet will print data of the Project of id 1 in `JSON` format.

## Resources & Operations

Users can only manage the resources they are permitted to manage or are public.

Below are the current resources and operations available. Check the API documentation for the correct payloads and responses.

### Yellow Pages
- Institutions
    ```python
    institution = seek_helper.Institution

    # Examples:

    # Get all institutions
    i = institution.get()

    # Get an institution by id
    i = institution.get(1)

    # Create an institution
    institution.create({
        "data": {
            "type": "institutions",
            "attributes": {
                "title": "Institution Example",
                "country": "Brazil",
            },
        }
    })

    # Update an institution
    institution.update(1, {
        "data": {
            "id": "1",
            "type": "institutions",
            "attributes": {
                "title": "Institution Update Example",
            },
        }
    })

    # Delete an institution by id
    institution.delete(1)
    ```

- People
    ```python
    people = seek_helper.People

    # Examples:

    # Get all people
    pe = people.get()

    # Get a person by id
    pe = people.get(1)

    # Create a person
    people.create({
        "data": {
            "type": "people",
            "attributes": {
                "first_name": "Person First Name Example",
                "last_name": "Person Last Name Example",
                "email": "email@example.com"
            },
        }
    })

    # Update a person
    people.update(1, {
        "data": {
            "id": "1",
            "type": "people",
            "attributes": {
                "first_name": "Person First Name Update Example",
            },
        }
    })

    # Delete a person by id
    people.delete(1)

    # Get current person
    pe = people.get_current()
    ```

- Programme
    ```python
    programme = seek_helper.Programme

    # Examples:

    # Get all programmes
    pr = people.programme()

    # Get a programme by id
    pr = people.programme(1)

    # Create a programme
    programme.create({
        "data": {
            "type": "programmes",
            "attributes": {
                "title": "Programme Example",
            },
        }
    })

    # Update a programme
    programme.update(1, {
        "data": {
            "id": "1",
            "type": "programmes",
            "attributes": {
                    "title": "Programme Update Example",
            },
        }
    })

    # Delete a person by id
    programme.delete(1)
    ```

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
            "id": "1",
            "type": "projects",
            "attributes": {
                "description": "This is an example of project update",
            },
        }
    })

    # Download all data files of a project
    project.download_data_files()

    # Upload data files to a project
    project.upload_data_files(1)

    # Delete a project by id
    project.delete(1)
    ```

### Experiments
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
            "id": "1",
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
            "id": "1",
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
            "id": "1",
            "type": "assays",
            "attributes": {
                "description": "This is an example of assay update",
            },
        }
    })

    # Download all data files of an assay
    assay.download_data_files()

    # Upload data files to an assay
    assay.upload_data_files(1)

    # Delete an assay by id
    assay.delete(1)
    ```

### Assets
- Data Files
    ```python
    data_file = seek_helper.DataFile

    # Examples:

    # Get all data files
    df = data_file.get()

    # Get a data file by id
    df = data_file.get(1)

    # Create a data file
    data_file.create({
        "data": {
            "type": "data_files",
            "attributes": {
                "title": "Data File Example",
                    "content_blobs": [
                        {
                            "original_filename": "file.jpg",
                            "content_type": "image/jpeg"
                        }
                    ],
            },
            "relationships": {
                "projects": {
                    "data": [
                        {
                            "id": "1",
                            "type": "projects"
                        }
                    ]
                },
            },
        }
    })

    # Update a data file
    data_file.update(1, {
        "data": {
            "id": "1",
            "type": "data_files",
            "attributes": {
                "description": "This is an example of data file update",
            },
        }
    })

    # Download a data file by id
    data_file.download(1)

    # Delete a data file by id
    data_file.delete(1)
    ```

## Experimental Features
The experimental features are related to the PhenomUK SEEK instance, and can be enabled when instantiating the `SeekHelper` class, in the last `boolean` parameter:

```python
from seek_helper import SeekHelper

seek_helper = SeekHelper('your_token', 'seek_instance_url', 'output_path', 'input_path', True)
```

The only experimental feature currently available is the "Upload to S3" operation, which allows you to send files to an S3 bucket. Example:

```python
data_file = seek_helper.DataFile

df = datafile.upload_to_s3('bucket_name', 'file_name', 'project_id')
```

`bucket_name`: the name of the S3 bucket that will store the file

`file_name`: the name of the file that will be uploaded. It has to be located in the `input_path` directory.

`project_id`: the id of the Project that will be linked to the file in SEEK

## Testing
In the project root, run:
```bash
pytest
```

## TODO
- Include more resources and operations
- Fetch resources by string (e.g., assays that contain "Experiment" in the title)
- Add logs
- Upload the library to a repository like PyPi
- Typify entities
