FROM python:3.8
USER root

RUN python3 -m pip install pytest toml
