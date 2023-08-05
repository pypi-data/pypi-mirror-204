# IBM Data Fabric Orchestrator python SDK

Python client library to interact with various IBM Data Fabric Orchestrator Services APIs.

Disclaimer: this SDK is being released initially as a **pre-release** version.
Changes might occur which impact applications that use this SDK.

## Table of Contents

<!--
  The TOC below is generated using the `markdown-toc` node package.

      https://github.com/jonschlinkert/markdown-toc

  You should regenerate the TOC after making changes to this file.

      npx markdown-toc -i README.md
  -->

<!-- toc -->

- [IBM Data Fabric Orchestrator python SDK](#ibm-data-fabric-orchestrator-python-sdk)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Using the SDK](#using-the-sdk)
  - [Questions](#questions)
  - [Issues](#issues)
  - [Open source @ IBM](#open-source--ibm)
  - [Contributing](#contributing)
  - [License](#license)

<!-- tocstop -->

## Overview

The IBM Data Fabric Orchestrator Services Python SDK allows developers to programmatically interact with the following
IBM Cloud services:

Service Name | Module Name | Imported Class Name
--- | --- | ---
Data Fabric Orchestrator Service | ibm_dfo_sdk | ibm_data_fabric_orchestrator_v1

## Prerequisites

* Access to an IBM Data Fabric Orchestrator service.
* Python 3.8 or above.

## Installation

To install, use `pip`:

```bash
pip install --upgrade ibm-dfo-sdk
```

Then in your code, you can import the appropriate service like this:
```
from ibm-dfo-sdk.ibm_data_fabric_orchestrator_v1 import *
```

## Using the SDK

Examples and a demo are available in the [examples](/examples) folder.  The `basic_use_of_get_service.py` example is probably the easiest to get started with.  Other examples cover more specific cases and detailed APIs.

Note that while this SDK is intended for use with the IBM Data Fabric Orchestrator on IBM Cloud CPDaaS or on-prem CPD instances with the IBM Data Fabric Orchestrator add-on installed, it can also be used when IBM Data Fabric Orchestrator add-on not installed. So the sdk user should always use the high-level `get_service()` function create a DFO service, which will automatically adapt to these senarios. After get the service instance from `get_service()` function, can use or configure the service instance as your needs.

For general SDK usage information, please see [this link](https://github.com/IBM/ibm-cloud-sdk-common/blob/main/README.md)

## Questions

If you are having difficulties using this SDK or have a question about the IBM Cloud services,
please ask a question
[Stack Overflow](http://stackoverflow.com/questions/ask?tags=ibm-cloud).

## Issues
If you encounter an issue with the project, you are welcome to submit a
[bug report](https://github.ibm.com/IBM-Data-Fabric/dfo-python-sdk.git/issues).
Before that, please search for similar issues. It's possible that someone has already reported the problem.

## Open source @ IBM
Find more open source projects on the [IBM Github Page](http://ibm.github.io/)

## Contributing
See [CONTRIBUTING.md](https://github.ibm.com/IBM-Data-Fabric/dfo-python-sdk.git/blob/main/CONTRIBUTING.md).

## License

This SDK is released under the Apache 2.0 license.
The license's full text can be found in [LICENSE](https://github.ibm.com/IBM-Data-Fabric/dfo-python-sdk.git/blob/main/LICENSE).
