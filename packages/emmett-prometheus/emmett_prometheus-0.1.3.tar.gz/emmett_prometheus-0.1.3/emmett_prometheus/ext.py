import time

import prometheus_client

from emmett import Pipe, request, response, websocket, sdict
from emmett.extensions import Extension, Signals, listen_signal
from emmett.routing.rules import HTTPRoutingRule, WebsocketRoutingRule


class Prometheus(Extension):
    default_config = dict(
        auto_load=True,
        enable_http_metrics=True,
        enable_ws_metrics=True,
        enable_sys_metrics=False,
        metrics_route_path="/metrics",
        metrics_route_hostname=None,
        metrics_names={
            "http_counter": "emmett_request_count",
            "http_histogram": "emmett_request_latency",
            "ws_gauge": "emmett_websocket_gauge",
            "ws_recv_counter": "emmett_websocket_messages_recv_count",
            "ws_send_counter": "emmett_websocket_messages_send_count"
        },
        http_histogram_buckets=[
            5, 35, 100, 200, 500, 1000, "INF"
        ],
        http_histogram_statuses=[200, 201],
        http_histogram_exclude_methods=["OPTIONS"],
        exclude_routes=[]
    )

    def on_load(self):
        self._excluded_routes = set(self.config.exclude_routes)
        self._httph_only_status = set(self.config.http_histogram_statuses)
        self._httph_filter_methods = set(self.config.http_histogram_exclude_methods)
        self.metrics = sdict()

        if not self.config.enable_sys_metrics:
            prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
            prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
            prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

        if self.config.enable_http_metrics:
            self.metrics.http_counter = prometheus_client.Counter(
                self.config.metrics_names["http_counter"],
                "Requests count",
                labelnames=["route", "method", "status"]
            )
            self.metrics.http_histogram = prometheus_client.Histogram(
                self.config.metrics_names["http_histogram"],
                "Requests latency histogram (ms)",
                labelnames=["route", "method", "status"],
                buckets=self.config.http_histogram_buckets
            )
            self._pipe_http = PrometheusHTTPPipe(self)

        if self.config.enable_ws_metrics:
            self.metrics.ws_gauge = prometheus_client.Gauge(
                self.config.metrics_names["ws_gauge"],
                "Websockets connection gauge",
                labelnames=["websocket"]
            )
            self.metrics.ws_counter_recv = prometheus_client.Counter(
                self.config.metrics_names["ws_recv_counter"],
                "Websockets received messages counter",
                labelnames=["websocket"]
            )
            self.metrics.ws_counter_send = prometheus_client.Counter(
                self.config.metrics_names["ws_send_counter"],
                "Websockets sent messages counter",
                labelnames=["websocket"]
            )
            self._pipe_ws = PrometheusWSPipe(self)

        if self.config.auto_load:
            self.app.route(
                self.config.metrics_route_path,
                methods='get',
                hostname=self.config.metrics_route_hostname,
                output='bytes'
            )(self._metrics_route)

    @listen_signal(Signals.before_route)
    def _inject_pipes(self, route, f):
        if not self.config.auto_load:
            return
        if f == self._metrics_route:
            return
        if self._get_route_name(route, f) in self._excluded_routes:
            return
        if self.config.enable_http_metrics and isinstance(route, HTTPRoutingRule):
            route.pipeline.insert(0, self._pipe_http)
        if self.config.enable_ws_metrics and isinstance(route, WebsocketRoutingRule):
            route.pipeline.insert(0, self._pipe_ws)

    @staticmethod
    def _get_route_name(route, f):
        rv = route.name or route.build_name(f)
        if rv.endswith("."):
            rv = rv + f.__name__
        return rv

    async def _metrics_route(self):
        response.content_type = prometheus_client.exposition.CONTENT_TYPE_LATEST
        return prometheus_client.exposition.generate_latest(prometheus_client.REGISTRY)


class PrometheusHTTPPipe(Pipe):
    def __init__(self, ext: Prometheus):
        self.ext = ext

    @property
    def _http_counter(self) -> prometheus_client.Counter:
        return self.ext.metrics.http_counter

    @property
    def _http_histogram(self) -> prometheus_client.Histogram:
        return self.ext.metrics.http_histogram

    async def open_request(self):
        request._prometheus_http_histogram_ts = time.perf_counter_ns()

    async def close_request(self):
        self._http_counter.labels(
            route=request.name,
            method=request.method,
            status=response.status
        ).inc()
        if (
            self.ext._httph_filter_methods and
            request.method in self.ext._httph_filter_methods
        ):
            return
        if (
            self.ext._httph_only_status and
            request.method not in self.ext._httph_only_status
        ):
            return
        self._http_histogram.labels(
            route=request.name,
            method=request.method,
            status=response.status
        ).observe(
            (
                time.perf_counter_ns() - request._prometheus_http_histogram_ts
            ) / 1_000_000
        )


class PrometheusWSPipe(Pipe):
    def __init__(self, ext: Prometheus):
        self.ext = ext

    @property
    def _ws_gauge(self) -> prometheus_client.Gauge:
        return self.ext.metrics.ws_gauge

    @property
    def _ws_counter_recv(self) -> prometheus_client.Counter:
        return self.ext.metrics.ws_counter_recv

    @property
    def _ws_counter_send(self) -> prometheus_client.Counter:
        return self.ext.metrics.ws_counter_send

    async def open_ws(self):
        self._ws_gauge.labels(websocket=websocket.name).inc()

    async def close_ws(self):
        self._ws_gauge.labels(websocket=websocket.name).dec()

    def on_receive(self, data):
        self._ws_counter_recv.labels(websocket=websocket.name).inc()
        return data

    def on_send(self, data):
        self._ws_counter_send.labels(websocket=websocket.name).inc()
        return data
