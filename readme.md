# Python Workflow Framework

> Internal Python automation framework for integrating and
orchestrating business platform workflows.



## Overview

This project is an internal python based workflow execution framework
used to interact with external business APIs like GoHighLevel,
ServiceM8, and Xero with more APIs planed in the future as the demand
requires.

As of writing, GoHighLevel is the only API that is available, and not
all endpoints are implimented. The currently available endpoints are:
 - Forms Submissions: Get
 - Custom Object Records: Get, Search, Create, and Update
 - Object Relations: Create
 - Custom Fields: Upload files



## Architecture

The application is designed around dynamically loaded workflows that
perform a specific automation task before exiting.

### Application Entry Point

The main application entry point is `/app/main.py` which simply
imports and executes whichever server is assigned in the environment
variables. The given server python file is responsible for creating a
flask instance, verifying webhook auth, loading and executing the
configured workflows, and returning success or failure response.

### Workflow Loading and Requirements

Servers are imported and run based off the `SERVER_NAME` environment
variable. And the files must be found within `app.servers`.

Workflows must be stored within `/app/workflows` and must define a
`main()` function. Currently, no arguments are passed to the function
when run but this will likely change in the future if the need arises.
Furthermore, anything returned from the main function will be
discarded, which will also likely change in the future.



## Local Development Setup

It is recommended to use VSCode with this project. For users that do
use VSCode, provided is the recommended extensions along with a launch
setup that allows for you to use the Python Debugger out of the box.

### 1. Clone Repository

```bash
git clone https://github.com/GHHS-Fahren/Python-Workflow-Framework.git
cd Python-Workflow-Framework
```

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv .venv
.\venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 4. Configure Environment Variables

Create a `.env` file in the repository root

Example:

```env
WEBHOOK_TOKEN="DEBUG_TOKEN"
SERVER_NAME="vehicle_logs_server"
GHL_TOKEN=your_ghl_token
```

> Requirements for what tokens will be needed depends on the workflow
and what APIs it communicates with.

### 5. Run the Application

```bash
python -m app.main
```

or if using VSCode, you can run it with `Run and Debug`



## Application Deployment

It is assumed that these workflows will be run on Google Cloud Run as
services. As such, deployment is automatic with github automatically
pushing changes from main down to the cloud to rebuild the container.



## Coding Standards

### Workflow Documentation

Workflows must have a note block at the top of the file which should
include:
 - The important notice from the template
 - High level description of the workflow
 - Breakdown of desired workflow steps
 - Any limitations or warnings

### Code Lines

All code published must be no longer than 70 characters with
exceptions only allowed for important developer notes that need to
stand out, such as:

```py
# TODO: THIS IS A CRITICAL SECURITY ERROR! MUST FIX BEFORE PUSHING TO PRODUCTION!
```

### Naming Conventions

| Item              | Convention  | Example                    |
|-------------------|-------------|----------------------------|
| Variables         | Snake Case  | `vehicle_id`               |
| Private Variables | Snake Case  | `_vehicle_data`            |
| Constants         | Snake Case  | `MAX_RETRIES`              |
| Functions         | Snake Case  | `download_vehicles()`      |
| Files             | Snake Case  | `vehicle_log_submitted.py` |
| Classes           | Pascal Case | `WebhookValidator`         |

### Function Definition

Function definitions must annotate parameter types and return types.
Furthermore functions should split the function params across multiple
lines to keep within the 70 character limit. If a class only needs to
be imported for annotation purposes, then the following is acceptable:

```py
from __future__ import annotations

# Other imports here

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api_framework import GoHighLevel



class ExampleClass():
    def __init__(
        self,
        api_client: GoHighLevel
    ) -> None:
        self._api_client = api_client
```

### Import ordering

Imports should be broadly grouped in 4 categories:
 1. Future import
 2. External module imports
 3. Application module imports
 4. Typing imports

Each of these categories should be seperated by one empty line and
after the last import there should be three empty lines. For example:

```py
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, AliasPath, Field \
    model_validator, field_validator, field_serializer
from datetime import datetime

from app.core.file_models import RemoteFile
from app.core.generic_client import BaseAPIClient

from typing import Literal, Self, overload, Any



def function() -> None: ...
```

### File Structure

Generally the file structure for the individual APIs should match
their documentation. For example, the documentation specify a group
for form related endpoints. The code will file structure will reflect
this by adding a form folder which will hold the API handler for those
form related endpoints in the API documentation.



## GoHighLevel Information

For this project the only thing to keep in mind is that when a vehicle
needs to be added, there should be 4 places to add its registration:
 1. Create New Vehicle Log
 2. Create New Service Log



## Extras

### Updating requirements.txt

Due to the project itself being within the requirements as an editable
package, `requirements.txt` must be updated without that entry:

```bash
pip freeze --exclude-editable > requirements.txt 
```