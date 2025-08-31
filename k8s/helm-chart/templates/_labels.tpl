{{/* Generate basic labels */}}
{{- define "common.labels" }}
    app: {{ .Values.appName }}
    environment: {{ .Values.environment }}
    # Kubernetes Recommended Labels
    app.kubernetes.io/name: {{ .Values.appName }}
    app.kubernetes.io/instance: "{{ .Values.appName }}-{{ .Values.environment }}"
    app.kubernetes.io/version: ""
    app.kubernetes.io/component: {{ .Values.labels.component }}
    app.kubernetes.io/part-of: {{ .Values.labels.part_of }}
    app.kubernetes.io/managed-by: {{ .Values.labels.managed_by }}
{{- end }}