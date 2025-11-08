import reflex as rx
import asyncio
import random
from typing import TypedDict, Literal
from datetime import datetime, timedelta

Severity = Literal["critical", "warning", "info"]


class Alert(TypedDict):
    id: int
    timestamp: str
    source: str
    message: str
    severity: Severity
    root_cause_hint: str


class Incident(TypedDict):
    id: int
    start_time: str
    end_time: str | None
    alert_ids: list[int]
    alerts: list[Alert]
    affected_services: list[str]
    status: Literal["active", "resolved"]
    root_cause_hypothesis: str
    confidence: float
    summary: str


class AIOpsState(rx.State):
    alerts: list[Alert] = []
    incidents: list[Incident] = []
    active_alerts: int = 0
    mttr: str = "18m"
    active_page: str = "Dashboard"
    incident_counter: int = 0
    _mock_sources = [
        "api-gateway",
        "user-db",
        "auth-service",
        "payment-processor",
        "k8s-cluster",
    ]
    _mock_messages = [
        "CPU utilization over 90%",
        "Database connection timeout",
        "API latency > 2s",
        "Disk space running low",
        "Pod CrashLoopBackOff",
        "SSL certificate expired",
        "5xx server error rate high",
    ]
    _mock_severities: list[Severity] = ["critical", "warning", "info"]
    _mock_hints: list[str] = [
        "Check for recent code deployments.",
        "Inspect database query performance.",
        "Review network ACLs and security groups.",
        "Verify disk space on affected hosts.",
        "Possible memory leak in auth-service.",
        "High number of 5xx errors from upstream API.",
    ]

    @rx.var
    def total_incidents(self) -> int:
        return len(self.incidents)

    @rx.var
    def affected_services(self) -> int:
        services = set()
        for inc in self.incidents:
            for service in inc["affected_services"]:
                services.add(service)
        return len(services)

    @rx.var
    def filtered_alerts(self) -> list[Alert]:
        return sorted(self.alerts, key=lambda x: x["id"], reverse=True)

    def _cluster_alerts(self) -> list[list[Alert]]:
        if not self.alerts:
            return []
        sorted_alerts = sorted(self.alerts, key=lambda a: (a["source"], a["timestamp"]))
        clusters = []
        current_cluster = [sorted_alerts[0]]
        for i in range(1, len(sorted_alerts)):
            prev_alert = current_cluster[-1]
            current_alert = sorted_alerts[i]
            time_format = "%H:%M:%S"
            t1 = datetime.strptime(prev_alert["timestamp"], time_format)
            t2 = datetime.strptime(current_alert["timestamp"], time_format)
            if current_alert["source"] == prev_alert["source"] and t2 - t1 < timedelta(
                minutes=2
            ):
                current_cluster.append(current_alert)
            else:
                clusters.append(current_cluster)
                current_cluster = [current_alert]
        clusters.append(current_cluster)
        return clusters

    def _create_incident_from_cluster(self, cluster: list[Alert]):
        self.incident_counter += 1
        start_time = min((a["timestamp"] for a in cluster))
        affected_services = list(set((a["source"] for a in cluster)))
        critical_alerts = [a for a in cluster if a["severity"] == "critical"]
        hypothesis = (
            "Multiple issues detected"
            if not critical_alerts
            else critical_alerts[0]["root_cause_hint"]
        )
        new_incident = Incident(
            id=self.incident_counter,
            start_time=start_time,
            end_time=None,
            alert_ids=[a["id"] for a in cluster],
            alerts=cluster,
            affected_services=affected_services,
            status="active",
            root_cause_hypothesis=hypothesis,
            confidence=round(random.uniform(0.65, 0.95), 2),
            summary=f"{len(cluster)} alerts from {', '.join(affected_services)}",
        )
        self.incidents.append(new_incident)
        clustered_ids = set(new_incident["alert_ids"])
        self.alerts = [a for a in self.alerts if a["id"] not in clustered_ids]

    @rx.event
    async def detect_incidents(self):
        clusters = self._cluster_alerts()
        for cluster in clusters:
            if len(cluster) > 1:
                cluster_alert_ids = {a["id"] for a in cluster}
                is_existing = False
                for inc in self.incidents:
                    if cluster_alert_ids.intersection(inc["alert_ids"]):
                        is_existing = True
                        break
                if not is_existing:
                    self._create_incident_from_cluster(cluster)

    @rx.event(background=True)
    async def simulate_alerts(self):
        id_counter = 0
        while True:
            await asyncio.sleep(random.uniform(1.5, 4.0))
            async with self:
                if len(self.alerts) < 50:
                    new_alert = Alert(
                        id=id_counter,
                        timestamp=datetime.now().strftime("%H:%M:%S"),
                        source=random.choice(self._mock_sources),
                        message=random.choice(self._mock_messages),
                        severity=random.choice(self._mock_severities),
                        root_cause_hint=random.choice(self._mock_hints),
                    )
                    self.alerts.append(new_alert)
                    self.active_alerts = len(self.alerts)
                    id_counter += 1
            yield AIOpsState.detect_incidents

    @rx.event
    def set_active_page(self, page: str):
        self.active_page = page

    @rx.event
    def on_load_event(self):
        return AIOpsState.simulate_alerts