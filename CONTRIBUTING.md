# Contributing to KiUtils
Thanks for considering to contribute to `kiutils`. Please create an issue first if you want to add
new functionality and propose what you are going to do beforehand. This may not be neccessary for
simple bug fixes or enhancements. 

## Testing
Whenever you are contributing a new feature to `kiutils`, be sure to provide unittests that 
explicitly test the functionality you implemented. Check out the `tests` folder in the repository 
root for some examples. The following folders are of interest:
- `tests/testdata/`: Put files your test case may need to parse here
- `tests/test_XXXX.py`: Test cases can be found in their respective Python file
- `tests/testfunctions.py`: Functions to aid in testing and report generation

## Local setup
An example of how to run the unittests is described here.

## Fork and clone the repository
Create a fork of `kiutils` and clone it to your computer using:
```bash
git clone https://github.com/<your_name>/kiutils
cd kiutils
```

### Set up / enter virtual enviroment (venv module)
You may want to create a new Python virtual environment when developing `kiutils`. This can be 
done with Python's built-in virtual environment module:
```bash
python3 -m venv env
```

To enter the newly created virtual enviroment, run:
```bash
source env/bin/activate
```

### Install dev dependencies
`kiutils` requires some dependencies for running tests. Install them using `pip` in your virtual 
environment using:

```bash
pip install -r requirements_dev.txt
```

### Run tests
In the `kiutils` root directory, running the tests is done using:
```bash
python test.py
```

A test report is automatically generated that shows the passing/failing tests. If a test is failing, 
the report will show you what went wrong.

### Leaving virtual environment (venv module)
When done, leaving the virtual environment is done using:
```bash
deactivate
```

### Submit your changes
Create a pull request of your forked changes to discuss and merge your implementation into `kiutils`.