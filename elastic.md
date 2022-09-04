## Elastic

### prerequiseites
`docker network create elastic`
`sudo sysctl -w vm.max_map_count=262144`


### run container

`docker run -e CLI_JAVA_OPTS="-Xms1g -Xmx1g" --name es-node01 --net elastic -p 9200:9200 -p 9300:9300  -t docker.elastic.co/elasticsearch/elasticsearch:8.3.3`

### Password for the elastic user (reset with `bin/elasticsearch-reset-password -u elastic`):
  -N_ZjZ7XeINg4PBrJs=5


## Kibana

### Install
`docker run --name kib-01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.3.3`

* Copy the following enrollment token and paste it into Kibana in your browser (valid for the next 30 minutes):
  eyJ2ZXIiOiI4LjMuMyIsImFkciI6WyIxNzIuMTkuMC4yOjkyMDAiXSwiZmdyIjoiMmU4YTU2ZDY5MWVmNGM4NGZlZTlkODBhMWYwMjQzOWJhYzM2MTZiMTdhNDlkMWY0NzAxYzViNGRjNTAwNGE4ZSIsImtleSI6Il9rWVd6SUlCX2tmTGhhd0I3UGtZOl92dk56UjlZVEptcDBRMFdoY1R2TkEifQ==

### access kibana
http://localhost:5601/login?next=%2F


## Logstash

### install
`wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -`
`echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-8.x.list`
`wget https://download.elastic.co/demos/logstash/gettingstarted/logstash-tutorial.log.gz`
`sudo apt-get update && sudo apt-get install logstash`


### Test
`sudo /usr/share/logstash/bin/logstash -e 'input { stdin { } } output { stdout {} }'`

### configure your Logstash instance to use the Beats input plugin by adding the following lines to the input section
`sudo nano /usr/share/logstash/first-pipeline.conf`

```
input {
    beats {
        port => "5044"
    }
}
output {
    stdout { codec => rubydebug }
}
```

### start logstash
`sudo bin/logstash -f first-pipeline.conf --config.reload.automatic`


## FILEBEAT
`sudo apt-get update && sudo apt-get install filebeat`


### run Filebeat with the following command 
`sudo filebeat -e -c /etc/filebeat/filebeat.yml -d "publish"`

### to reread log file 
- stop filebeat 
- remove registry `sudo rm -r /var/lib/filebeat/registry/`
- start fielbeat `sudo filebeat -e -c /etc/filebeat/filebeat.yml -d "publish"`


### accessing the data 
Get indices
GET _cat/indices
GET .ds-logs-generic-default-2022.08.24-000001/_search

