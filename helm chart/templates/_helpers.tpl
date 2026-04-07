{{- define "api.labels" -}}
app: {{ .Values.api.name }}
{{- end}}

{{- define "frontend.labels" -}}
app: {{ .Values.frontend.name }}
{{- end}}
