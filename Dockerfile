FROM python:3.8

RUN pip install poetry
WORKDIR /src
COPY . .
RUN poetry config virtualenvs.create false && poetry install --no-dev
ENTRYPOINT [ "python", "/src/demo/demo.py" ]