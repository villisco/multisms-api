## K8S deployment (helm chart)

Example helm chart to use for K8S deployment.

## Updating environments

Helm template default values: `./helm-chart/values.yaml`\
Override default values for envs: `./helm-chart/*.values.yaml`

## Helm commands

```
# Lint all templates (checks format)
helm lint helm-chart

# Print all templates using default values
helm template helm-chart

# Print all templates (with environment values)
helm template helm-chart -f ./helm-chart/test.values.yaml
```