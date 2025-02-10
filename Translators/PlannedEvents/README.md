# Planned Events Translator

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Python Planned Events to TIM message translator that is designed to pull messages from the CDOT Planned Events feed and translate to TIM messages.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

This project supports Python >= 3.10. Packages required to run the translator can be installed via [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

Alternatively, if you are running VSCode there is a task available to run this on your behalf. This can be accessed under Task Explorer -> vscode -> pipinstall.

The scripts also require access to the CDOT Postgres database. This can be accessed by setting the environment variables in the .env file. The .env file is not included in the repository for security reasons, however a sample.env file has been provided to show structure required. 

In addition to the environment variables for accessing the CDOT Postgres database, the scripts also require the following environment variables to scrape the Planned Events endpoint and deposit the resulting TIMs:
<ol>
    <li>CDOT_FEED_ENDPOINT - the CDOT API URL</li>
    <li>CDOT_FEED_API_KEY - the API key for accessing the CDOT Planned Events data</li>
    <li>TIM_MANAGER_ENDPOINT - the TIM Manager URL where translated TIMs will be submitted </li>
</ol>

### Testing
Unit tests are ran with the python pytest module. To run the tests, run the following command from the root of the project:

```bash
python -m pytest ./tests
```

Again, if you are running VSCode there is a task available to run this on your behalf. This can be accessed under Task Explorer -> vscode -> python test and coverage. This task includes a unit test coverage report to indicate how much of the code is covered by unit tests.

## Usage <a name = "usage"></a>

### Running the Translator Locally
Using VSCode, a simple launch.json file has been provided to allow debugging the application. This can be accessed under the Run & Debug tab. The default configuration will run the translator using the functions framework. This runs the translator as a REST service accessed on http://localhost:8085. The translator can be tested by sending a POST request to this endpoint.


### Running the Translator via Docker
The Planned Events to TIM translator can also be run locally using Docker. The translator Dockerfile can be found under Translators/PlannedEvents/. Additionally, there is a docker-compose file which builds and runs the translator. Setting the environment variable RUN_LOCAL to true will run the translator REST service as a flask application that can be accessed on http://localhost:8085. Alternatively, leaving RUN_LOCAL blank will run the translator one time immediately after the build has finished. 