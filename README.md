# The NC Doughnuts API

This API concerns sales of yummy doughnuts from the Northcoders bakery.

The code should be deployable in any Unix-like OS. The build process outlined below requires Python
be installed along with [GNU Make](https://www.gnu.org/software/make/). MacOS users can get access
to the `make` command via Homebrew or MacOS Command Line Tools. 

To run the API locally:
1. Fork and clone the repo.
1. Ensure that your Python interpreter is Python at least 3.11.x - you may use a tool like `pyenv`.
1. In the root of the project, create the run environment with:
    ```bash
    make requirements
    ```
1. Set up the required dev tools:
    ```bash
    make dev-setup
    ```
1. Run the tests.
    ```bash
    make run-checks
    ```
1. Start the server by running:
    ```bash
    make start-server
    ```
1. In your browser, navigate to `localhost:8000/docs/` to view the API documentation page.
1. Then you can navigate to the endpoint of your choice, e.g. `localhost:8000/api/doughnuts`.

API logs are available in `logs/app.log`.