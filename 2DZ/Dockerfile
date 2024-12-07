FROM alpine:latest
RUN apk update && apk add --no-cache python3 py3-pip py3-yaml
RUN apk update
WORKDIR /app

COPY config.yaml .
COPY apk_dependencies.py .

CMD ["python3", "apk_dependencies.py"]