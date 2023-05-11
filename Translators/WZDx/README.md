# Project Title

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Python WZDx to TIM message translator that is designed to pull messages from the CDOT public WZDx feed and translate to TIM messages.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

This project supports Python >= 3.5. Packages required to run the translator can be installed via [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

Alternatively, if you are running VSCode there is a task available to run this on your behalf. This can be accessed under Task Explorer -> vscode -> pipinstall.

The scripts also require access to the CDOT Postgres database. This can be accessed by setting the environment variables in the .env file. The .env file is not included in the repository for security reasons, however a sample.env file has been provided to show structure required. 

In addition to the environment variables for accessing the CDOT Postgres database, the scripts also require the following environment variables to scrape the WZDx endpoint:
<ol>
    <li>WZDX_ENDPOINT - the CDOT WZDx URL</li>
    <li>WZDX_API_KEY - the API key for accessing the WZDx data</li>
    <li>ODE_ENDPOINT - the ODE URL where translated TIMs will be submitted </li>
</ol>

### Testing
Unit tests are ran with the python pytest module. To run the tests, run the following command from the root of the project:

```bash
python -m pytest ./tests
```

Again, if you are running VSCode there is a task available to run this on your behalf. This can be accessed under Task Explorer -> vscode -> python test and coverage. This task includes a unit test coverage report to indicate how much of the code is covered by unit tests.

## Usage <a name = "usage"></a>

**Note:** This project is currently in development and is not yet ready for production use. Limitations are expected.

### Running the Translator Locally
Using VSCode, a simple launch.json file has been provided to allow debugging the application. This can be accessed under the Run & Debug tab. The default configuration will run the translator using the functions framework. This runs the translator as a REST service accessed on http://localhost:8080. The translator can be tested by sending a POST request to this endpoint with a WZDx message in the body. The translator will respond with a series of TIM messages in the body of the response.


### Current Known Limitations
- Public GIS endpoint is in the process of being deployed and is currently inaccessible.
- Translator currently supports only WZDx v4.1 messages
- Only 'CLOSED' ITIS code is supported. Further support is planned
    -  "all-lanes-closed" is only supported type at this time