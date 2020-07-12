FROM python:3

COPY . /

RUN chmod a+x job.sh

CMD [ "./job.sh"]