# Hephaestus Tests

This directory contains tests for the Hephaestus system components.

## Setup

Before running tests, make sure you have installed all dependencies:

```bash
pip install -r ../requirements.txt
```

Copy the `.env.template` file to `.env` and fill in your API keys:

```bash
cp ../.env.template ../.env
# Edit .env with your editor of choice
```

## Running Tests

To run all tests:

```bash
python run_tests.py
```

To run a specific test:

```bash
python test_llm_service.py  # Test LLM service integration
python test_flow_builder.py  # Test FlowBuilder with LLM integration
```

## Test Output

Test results and generated code will be saved to the `output` directory inside the tests folder.

## Adding New Tests

To add new tests:
1. Create a file named `test_<component>.py`
2. Implement a `main()` function that runs all tests in the file
3. Make the file executable with `if __name__ == "__main__": main()`

The test runner will automatically discover and run your test. 