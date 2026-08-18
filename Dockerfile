FROM python:3.12
USER root

RUN python3 -m pip install pytest toml
