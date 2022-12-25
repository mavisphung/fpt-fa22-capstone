FROM public.ecr.aws/docker/library/python:3.10.7-alpine

# add tessdata
# RUN mkdir -p /usr/share/tessdata
# ADD https://raw.githubusercontent.com/tesseract-ocr/tessdata/main/vie.traineddata /usr/share/tessdata/vie.traineddata

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add gcc python3-dev musl-dev \
    # && apk add tesseract-ocr-dev \
    && apk add --no-cache mariadb-connector-c-dev

# install dependencies
RUN pip install --upgrade pip
ADD ./requirements.txt .
RUN pip install -r requirements.txt


# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .
RUN chmod +x entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh

EXPOSE 8000
EXPOSE 6969

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]