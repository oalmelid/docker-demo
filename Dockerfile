FROM python:3.8

WORKDIR /src
COPY . .
RUN pip install cython && pip install /src/
ENTRYPOINT [ "python", "-m", "demo.demo" ]
