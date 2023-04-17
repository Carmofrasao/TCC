FROM docker.elastic.co/logstash/logstash:7.12.0
COPY logstash.conf /usr/share/logstash/pipeline/
EXPOSE 5044
ENV ELASTICSEARCH_HOST elasticsearch
CMD ["-f", "/usr/share/logstash/pipeline/logstash.conf"]
