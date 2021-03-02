FROM python:3.8

COPY . /src
RUN pip install cython && pip install /src/
ENTRYPOINT [ "python", "-m", "demo.demo" ]
