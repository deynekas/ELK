# Greylog
## installation

1. add  repository and install
```
wget https://packages.graylog2.org/repo/packages/graylog-4.3-repository_latest.deb
sudo dpkg -i graylog-4.3-repository_latest.deb
sudo apt-get update && sudo apt-get install graylog-server graylog-enterprise-plugins graylog-integrations-plugins graylog-enterprise-integrations-plugins
```

2. create root passwords
`echo -n "Enter Password: " && head -1 </dev/stdin | tr -d '\n' | sha256sum | cut -d" " -f1`

Longman195
9e5a18c74bb0c722675bb9c05c7f7ff6f44fb62acccbaf593c27b636befa7181

3. create sercret to protect user paswrds
```
sudo apt install pwgen
pwgen -N 1 -s 96
NWj65v939a67eQoIoIK32oIh6KJC3cPmsvwBkjL37TaVhojDTJcq4tiqBiRHGXCrrxT8CAapUwrimJCqVlQqbPzZgEA2bMQn
```
4. Set in greylog config 

sudo nano /etc/graylog/server/server.conf
password_secret
root_password_sha2


## Mongodb 


```

docker pull mongo

mkdir learning/elastic/MongoDockerData

docker network create mongo-network

docker run -v /home/olga/learning/elastic/MongoDockerData:/data/db --name mongodb --network mongo-network  -e MONGO_INITDB_ROOT_USERNAME=deyneka -e MONGO_INITDB_ROOT_PASSWORD=Longman195 -p 27017:27017 mongo
```

### TO check coonection to mongo

#### using mongo client
1. install mongo client
`sudo apt install mongodb-clients`

2. connet fdo mongo
`mongo localhost:27017 -u deyneka -p Longman195 --authenticationDatabase admin`

#### using another container 
```
docker run -it --rm --network mongo-network mongo mongosh --host mongodb -u deynekaa -p Longman195 --authenticationDatabase admin some-db
> db.getName();

```

## Collecting data

### Collectig in active mode

> in active mode  you configure graylog sidecar or directly logging collector (filebeat,...) to send logs to graylog inputs


1. Access Web UI
http://127.0.0.1:9000/gettingstarted

2. Set up input listening on port 5045

>Inputs define the method by which Graylog collects logs. Out of the box, Graylog supports multiple methods to collect logs, including:
    Syslog (TCP, UDP, AMQP, Kafka)
    GELF (TCP, UDP, AMQP, Kafka, HTTP)
    AWS - AWS Logs, FlowLogs, CloudTrail
    Beats/Logstash
    CEF (TCP, UDP, AMQP, Kafka)
    JSON Path from HTTP API
    Netflow (UDP)
    Plain/Raw Text (TCP, UDP, AMQP, Kafka)
3. setup filebeat to send messages to configured input
```
filebeat.inputs:
- type: filestream
  id: my-nginx-id
  enabled: true
  paths:
    - /var/log/nginx/access.log*

setup.template.settings:
  index.number_of_shards: 1

output.logstash:
  hosts: ["localhost:5044"]
```
4. Start filebeat 
`sudo filebeat -e -c /etc/filebeat/filebeat-fail2ban-graylog.yml -d "publish"`

5. manually configure extractor on input to extract data from message
> extractor can be based on Grok patterns, regular expressions, json,....

> Pattern: %{IPORHOST:clientip} [a-zA-Z\.\@\-\+_%]+ [a-zA-Z\.\@\-\+_%]+ \[%{HTTPDATE:timestamp}\] "%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}" %{NUMBER:response} (?:%{NUMBER:bytes}|-) (?:"(?:%{URI:referrer}|-)"|%{QS:referrer}) 

### Collectig in passive mode

> in passive mode nginx is configured to send dta to graylog  
` access_log syslog:server=192.168.251.3:12301,facility=local0,tag=nginx,severity=info graylog2_json;`
1.  download and install nginx content pack. It will do thefollowing:
    - create input with corresponding port
    - create a stream for nginx logs 
    - create dashboards
2. configure nginx to send logs to graylog
```
             '"remote_addr": "$remote_addr", '
             '"remote_user": "$remote_user", '
             '"body_bytes_sent": $body_bytes_sent, '
             '"request_time": $request_time, '
             '"status": $status, '
             '"request": "$request", '
             '"request_method": "$request_method", '
             '"host": "$host",'
             '"source": "192.168.251.3",'
             '"upstream_cache_status": "$upstream_cache_status",'
             '"upstream_addr": "$upstream_addr",'
             '"http_x_forwarded_for": "$http_x_forwarded_for",'
             '"http_referrer": "$http_referer", '
             '"http_user_agent": "$http_user_agent" }';
access_log syslog:server=192.168.251.3:12301 graylog2_json;
error_log syslog:server=192.168.251.3:12302;
```
