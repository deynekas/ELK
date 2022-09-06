## Fail2ban logs using file2beat and logstash

1. upload fail2ban logs from speakasap.com

2. create grok parser using grok debugger tool https://grokdebug.herokuapp.com/
    - take log entry
    2022-08-18 23:04:56,949 fail2ban.actions: WARNING [ssh] Ban 34.85.207.110
    - create matching pattern
    %{TIMESTAMP_ISO8601:date} %{PROG}: %{WORD:kind}%{SPACE}\[%{GREEDYDATA:jail}\]%{SPACE}%{GREEDYDATA:action} %{IP:ip}

3. configure logstash pipeline to listen for beats and ourput to stdout
    `sudo nano /usr/share/logstash/fail2ban-pipeline.conf`

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
4. configure filebeat to read fail2ban logfiles and output to logstash
    ```                                                                                 
    filebeat.inputs:
    - type: log
    paths:
        - /var/log/faile2ban/fail2ban.log*
    output.logstash:
    hosts: ["localhost:5044"]
    ```
5. run filebeat and logstash and check the terminal output
    '''
    sudo filebeat -e -c /etc/filebeat/filebeat-faile2ban.yml -d "publish"
    sudo bin/logstash -f fail2ban-pipeline.conf --config.reload.automatic
    ```
6. reconfigure logstach to aply groc filter, add geoip and date. set output to elasticsearch 
    ```
    input {
    beats {
       port => 5044
    }
    }

    filter {
        
        if [loglevel] == "debug" {
        drop { }
        
        grok { match => [ "message", "%{TIMESTAMP_ISO8601:date} %{PROG}: %{WORD:kind}%{SPACE}\[%{GREEDYDATA:jail}\]%{SPACE}%{GREEDYDATA:action}>
        }

        date {
            match => [ "date", "ISO8601" ]
            target => "date"
        }

        geoip {
            source => "ip"
            ecs_compatibility => disable
        }
    }

    output {
        elasticsearch {
            hosts => [ "https://localhost:9200" ]
            cacert => '/etc/logstash/http_ca.crt'
            user => elastic
            password => "-N_ZjZ7XeINg4PBrJs=5"
            index => "logstash-fail2ban-%{+YYYY.MM.dd}"
        }
    }
    ```
    > problem: goip fileds are mapped as text not ge_point
    > reason: because there is no template for those data dynamic mapping is applied. it will assign field to an objec ti lat and lan subfields of float         type

7. Create index template (use ucrrent index mapping with location field set to *geo_point*
    > this will allow to use region maps dashboards to visualize

8. Reimport log data
    - stop filebeat 
    - remove registry `sudo rm -r /var/lib/filebeat/registry/`
    - start fielbeat `sudo filebeat -e -c /etc/filebeat/filebeat-fail2ban.yml -d "publish"`

9. In discovery page check that location has geo_point data type

10. Create dashboard 
