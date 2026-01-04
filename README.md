# get-frontend-config-action

GitHub Action to extract frontend configuration from repository-config.yml with
optional dockerized execution.

## Features

- ✅ Reads `.github/repository-config.yml` (or provided YAML) to find frontend
  working directory and Node.js version
- ✅ Defaults safely when config is missing (dir: `web`, node: `22`)
- ✅ Supports dockerized execution via GHCR-published image
- ✅ Emits step summary for quick visibility

## Usage

### Basic Example

```yaml
jobs:
  frontend-config:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: jdfalk/get-frontend-config-action@v1
        id: frontend

      - name: Show frontend config
        run: |
          echo "Dir: ${{ steps.frontend.outputs.dir }}"
          echo "Node: ${{ steps.frontend.outputs['node-version'] }}"
          echo "Has frontend: ${{ steps.frontend.outputs['has-frontend'] }}"
```

### Provide YAML Content Directly

```yaml
- uses: jdfalk/get-frontend-config-action@v1
  id: frontend
  with:
    repository-config: |
      working_directories:
        frontend: ui
      versions:
        node:
          - '20'
```

### Force Docker Execution

```yaml
- uses: jdfalk/get-frontend-config-action@v1
  id: frontend
  with:
    use-docker: true
    docker-image: ghcr.io/jdfalk/get-frontend-config-action:main
```

## Inputs

| Input               | Description                                                          | Required | Default                                          |
| ------------------- | -------------------------------------------------------------------- | -------- | ------------------------------------------------ |
| `repository-config` | Repository configuration YAML content                                | Yes      | (none)                                           |
| `config-file`       | Path to repository-config.yml file (alternative to repository input) | No       | `.github/repository-config.yml`                  |
| `use-docker`        | Run the action inside the published container image                  | No       | `false`                                          |
| `docker-image`      | Docker image reference (tag or digest) when `use-docker` is true     | No       | `ghcr.io/jdfalk/get-frontend-config-action:main` |

## Outputs

| Output         | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| `dir`          | Frontend working directory (e.g., `web`, `frontend`, `client`) |
| `node-version` | Node.js version from config                                    |
| `has-frontend` | Whether frontend configuration was found                       |

## Requirements

- Python 3.8+
- PyYAML (installed automatically when missing)

## Author

jdfalk
