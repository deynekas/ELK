# Nginx access log using file2beat nginx module

1. Donload nginx access logs from speakasap.com 

2. Configure fulebeat.yaml to use elastic search as output 

```
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["https://localhost:9200"]
  username: "elastic"
  password: "-N_ZjZ7XeINg4PBrJs=5"
  ssl.verification_mode: none
  ssl:
    enabled: true
```

3. Enable nginx module 

    >modules simplify the collection, parsing, and visualization of common log formats.A typical module (say, for the Nginx logs) is composed of one or more filesets (in the case of Nginx, access and error). A fileset contains the following:
    Filebeat input configurations, which contain the default paths where to look for the log files. These default paths depend on the operating system. The Filebeat configuration is also responsible with stitching together multiline events when needed.
    Elasticsearch ingest pipeline definition, which is used to parse the log lines.
    Fields definitions, which are used to configure Elasticsearch with the correct types for each field. They also contain short descriptions for each of the fields.* 
`filebeat modules enable nginx`

4. Configure Nginx module to use log location 

```
- module: nginx
  access:
    enabled: true
    var.paths: ["/var/log/nginx/access.log*"]
```

5. Setup elastic asset 
  
`filebeat setup -e`
  > This step loads the recommended index template for writing to Elasticsearch and deploys the sample dashboards for visualizing the data in Kibana.
    This step does not load the ingest pipelines used to parse log lines. By default, ingest pipelines are set up automatically the first time you run the module and connect to Elasticsearch

6. Start filebeat
`sudo service filebeat start`

7. View data in kibana 
    - dicover - to see filebeat data 
    ```
    GET _cat/indices
    GET .ds-filebeat-8.3.3-2022.08.25-000001/_search
    ```
    - dashboard  - find module dashboard for specific data
