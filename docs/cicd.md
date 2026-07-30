# CI/CD

The repository includes a GitHub Actions workflow that runs the test suite on every push and pull request.

## Workflow overview

The workflow defined in `.github/workflows/main.yml` performs the following steps:

1. checks out the repository
2. sets up Python 3.10
3. installs the project dependencies
4. runs `pytest -q`

## Local equivalent

```bash
pytest -q
```

## Suggested next steps

- add code formatting checks such as Ruff or Black
- publish container images to a registry
- deploy the service automatically to a cloud platform
