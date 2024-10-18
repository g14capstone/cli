# Command Line Interface (CLI)

The CLI is built using [click](https://click.palletsprojects.com/en/8.1.x/). Use the following command to get started with the CLI:

```bash
quack
```


## Testing

`pytest` docs can be found [here](https://docs.pytest.org/en/stable/). See basic run instructions below, which collects all tests and runs them, with default verbosity (should work from root dir or test dir)

```bash
pytest
```

or

```bash
python3 -m pytest
```

## Setup

Follow these steps to set up a Python virtual environment using `venv`

1. Create a new virtual environment:

```bash
python3 -m venv .venv
```

2. Activate the virtual environment. The command varies based on your operating system

- Linux / macOS:

```bash
source .venv/bin/activate
```

- Windows:

```bash
.venv\Scripts\activate
```
    
- Git Bash:

```bash
source .venv/Scripts/activate
```

3. Once the virtual environment is activated, install the necessary dependencies

```bash
pip install -r requirements.txt
```

4. Install CLI application in editable mode
   
```bash
pip install --editable .
```

5. To deactivate the venv

```bash
deactivate
```
