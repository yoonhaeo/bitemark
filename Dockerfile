FROM python:3.11-slim

WORKDIR /opt/bitemark
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
COPY configs ./configs
RUN python -m pip install --no-cache-dir .

ENTRYPOINT ["bitemark"]

# This public image contains no models and is not a challenge submission image.
# NEEDS TO BE FINETUNED and integrated with a private inference backend.
