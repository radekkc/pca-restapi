FROM python:3.9-bullseye

#RUN apt-get update && apt-get install libblas-dev liblapack-dev libatlas-base-dev -y

RUN mkdir /app

# copy the requirements file into the image
ADD app /app

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["restapi.py" ]
