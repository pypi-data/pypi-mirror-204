# Emmett-Prometheus

Emmett-Prometheus is an [Emmett framework](https://emmett.sh) extension integrating [prometheus](https://prometheus.io) client.

[![pip version](https://img.shields.io/pypi/v/emmett-prometheus.svg?style=flat)](https://pypi.python.org/pypi/emmett-prometheus) 

## Installation

You can install Emmett-Prometheus using pip:

    pip install emmett-prometheus

And add it to your Emmett application:

```python
from emmett_prometheus import Prometheus

app.use_extension(Prometheus)
```

## Configuration

Here is the complete list of parameters of the extension configuration:

| param | default | description |
| --- | --- | --- |
| auto\_load | `True` | Automatically inject extension on routes and expose metrics |
| enable\_http\_metrics | `True` | Enable metrics collection on HTTP routes |
| enable\_ws\_metrics | `True` | Enable metrics collection on Websocket routes |
| enable\_sys\_metrics | `False` | Enable default Prometheus client system metrics collection |
| metrics\_route\_path | /metrics | Path for metrics route |
| metrics\_route\_hostname | | Hostname for metrics route |

You also have some additional customisations available (here we show the defaults):

```python
app.config.Prometheus.http_histogram_statuses = [200, 201]
app.config.Prometheus.http_histogram_exclude_methods = ["OPTIONS"]
app.config.Prometheus.http_histogram_buckets = [
    5, 35, 100, 200, 500, 1000, "INF"
]
app.config.Prometheus.exclude_routes = []
app.config.Prometheus.metrics_names={
    "http_counter": "emmett_request_count",
    "http_histogram": "emmett_request_latency",
    "ws_gauge": "emmett_websocket_gauge",
    "ws_recv_counter": "emmett_websocket_messages_recv_count",
    "ws_send_counter": "emmett_websocket_messages_send_count"
}
```

## License

Emmett-prometheus is released under BSD license.
