FROM python:3.8

RUN pip install poetry
WORKDIR /src
COPY . .
RUN pip install cython && pip install /src/
ENTRYPOINT [ "python", "-m", "demo.demo" ]
