# Command Line Interface (CLI)

The CLI is built using [click](https://click.palletsprojects.com/en/8.1.x/). Use the following command to get started with the CLI:

```bash
python3 main.py --help
```


## Testing

pytest docs can be found [here](https://docs.pytest.org/en/stable/). See basic run instructions below (should work from root dir or test dir):

```bash
# following cmds should collect all tests and run them, with default verbosity

python3 -m pytest

# or

pytest
```

## Setting Up the Virtual Environment

Follow these steps to set up a Python virtual environment using `venv`:

1. Create a new virtual environment:

    ```bash
    python3 -m venv .venv
    ```

2. Activate the virtual environment. The command varies based on your operating system:

    - For Linux and macOS:

        ```bash
        source .venv/bin/activate
        ```

    - For Windows:

        ```bash
        .venv\Scripts\activate
        # or
        source .venv/Scripts/activate # for git bash
        ```

3. Once the virtual environment is activated, install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. To deactivate the venv

    ```bash
    deactivate
    ```
