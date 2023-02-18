# Contributing to KiUtils

## Running KiUtils' tests

### Set up / enter virtual enviroment (venv module)

Create a new Python virtual enviroment and enter it.  This can be done with Python's built-in virtual enviroment module:

```bash
python3 -m venv env
```

And to enter the newly created virtual enviroment:

```bash
source env/bin/activate
```

### Install dev dependencies

KiUtils requires some dependencies for running tests.  Install them via `pip` in your virtual enviroment with the following:

```bash
pip install -r requirements_dev.txt
```

### Run tests

In KiUtil's root directory and in your virtual enviroment created earlier, running the tests is done with:

```bash
python test.py
```

### Leaving virtual enviroment (venv module)

With Python's built-in virtual enviroment module `venv`, leaving a virtual enviroment is done with the command:

```bash
deactivate
```