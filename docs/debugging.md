# Debugging CLI Application

This guide will help you set up and debug your CLI application using `pip` in editable mode.

## Installing the CLI in Editable Mode

To install your CLI application in editable mode, follow these steps:

1. Open your terminal.
2. Navigate to the root directory of your CLI project.
3. Run the following command:

```bash
pip install --editable .
```

This command installs your CLI application in editable mode, allowing you to make changes to the code and immediately see the effects without reinstalling.

## Using the CLI for Debugging

Once your CLI is installed, you can start debugging it. Here are some steps to help you debug your CLI application:

1. **Run the CLI Command**: Execute your CLI command in the terminal to see if it works as expected. For example, if your CLI command is `quack`, run:

```bash
quack --help
```

3. **Use a Debugger**: If you prefer using a debugger, you can use tools like `pdb` for Python. Insert the following line where you want to start debugging:

```python
import pdb; pdb.set_trace()
```

When you run your CLI command, the execution will pause at this point, allowing you to inspect variables and step through the code.
