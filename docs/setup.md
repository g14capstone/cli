# Setup

Follow these steps to get started with `quack`.

## TL;DR

1. Set up a Python virtual environment using `venv`
2. Install Pre-commit hooks
3. Install `quack` as an editable module

## Environment Setup

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
```

### 2. Activate Virtual Environment

- **Linux / macOS:**

  ```bash
  source .venv/bin/activate
  ```

- **Windows:**

  ```bash
  . .venv\Scripts\activate
  ```

- **Git Bash:**

  ```bash
  source .venv/Scripts/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Activate Pre-commit Hooks

```bash
pre-commit install
```

### 5. Install CLI Application in Editable Mode

```bash
pip install --editable .
```

### 6. Deactivate the Virtual Environment

```bash
deactivate
```
