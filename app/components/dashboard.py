import reflex as rx
from app.states.state import AIOpsState, Alert


def metric_card(icon: str, label: str, value: rx.Var, icon_color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                icon,
                size=24,
                class_name=rx.match(
                    icon_color,
                    ("blue", "text-blue-500"),
                    ("red", "text-red-500"),
                    ("yellow", "text-yellow-500"),
                    ("green", "text-green-500"),
                    "text-gray-500",
                ),
            ),
            class_name=rx.match(
                icon_color,
                ("blue", "p-3 bg-blue-100 dark:bg-blue-500/20 rounded-lg"),
                ("red", "p-3 bg-red-100 dark:bg-red-500/20 rounded-lg"),
                ("yellow", "p-3 bg-yellow-100 dark:bg-yellow-500/20 rounded-lg"),
                ("green", "p-3 bg-green-100 dark:bg-green-500/20 rounded-lg"),
                "p-3 bg-gray-100 dark:bg-gray-700 rounded-lg",
            ),
        ),
        rx.el.div(
            rx.el.p(
                label, class_name="text-sm font-medium text-gray-500 dark:text-gray-400"
            ),
            rx.el.p(
                value,
                class_name="text-2xl font-semibold text-gray-800 dark:text-gray-100",
            ),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 p-6 bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm transition-shadow hover:shadow-lg",
    )


def severity_badge(severity: rx.Var[str]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name=rx.match(
                severity,
                ("critical", "h-2 w-2 rounded-full bg-red-500"),
                ("warning", "h-2 w-2 rounded-full bg-yellow-500"),
                ("info", "h-2 w-2 rounded-full bg-blue-500"),
                "h-2 w-2 rounded-full bg-gray-500",
            )
        ),
        rx.el.p(severity.capitalize(), class_name="text-sm font-medium"),
        class_name=rx.match(
            severity,
            (
                "critical",
                "flex items-center gap-2 w-fit rounded-full bg-red-100 dark:bg-red-500/20 px-3 py-1 text-red-700 dark:text-red-300",
            ),
            (
                "warning",
                "flex items-center gap-2 w-fit rounded-full bg-yellow-100 dark:bg-yellow-500/20 px-3 py-1 text-yellow-700 dark:text-yellow-300",
            ),
            (
                "info",
                "flex items-center gap-2 w-fit rounded-full bg-blue-100 dark:bg-blue-500/20 px-3 py-1 text-blue-700 dark:text-blue-300",
            ),
            "flex items-center gap-2 w-fit rounded-full bg-gray-100 dark:bg-gray-700 px-3 py-1 text-gray-700 dark:text-gray-300",
        ),
    )


def alert_card(alert: Alert) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                alert["timestamp"],
                class_name="text-sm font-medium text-gray-500 dark:text-gray-400",
            ),
            severity_badge(alert["severity"]),
            class_name="flex items-center justify-between w-full",
        ),
        rx.el.div(
            rx.el.p(
                alert["message"],
                class_name="font-semibold text-gray-800 dark:text-gray-100",
            ),
            rx.el.p(
                f"Source: {alert['source']}",
                class_name="text-sm text-gray-500 dark:text-gray-400",
            ),
            class_name="flex flex-col gap-1",
        ),
        rx.el.div(
            rx.icon("lightbulb", size=16, class_name="text-yellow-600"),
            rx.el.p(
                rx.el.span("Hint: ", class_name="font-semibold"),
                alert["root_cause_hint"],
                class_name="text-sm text-gray-700 dark:text-yellow-200",
            ),
            class_name="flex items-start gap-2 p-3 bg-yellow-50 dark:bg-yellow-500/10 border border-yellow-100 dark:border-yellow-900/50 rounded-lg mt-2",
        ),
        class_name="flex flex-col gap-3 p-4 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 transition-shadow hover:shadow-md",
    )


def dashboard_content() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1(
                "Dashboard",
                class_name="text-3xl font-bold text-gray-900 dark:text-white mb-2",
            ),
            rx.el.p(
                "Overview of system health and active alerts.",
                class_name="text-gray-600 dark:text-gray-400",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            metric_card("activity", "Active Alerts", AIOpsState.active_alerts, "blue"),
            metric_card("siren", "Incidents", AIOpsState.total_incidents, "red"),
            metric_card("timer", "Avg. MTTR", AIOpsState.mttr, "yellow"),
            metric_card(
                "server", "Affected Services", AIOpsState.affected_services, "green"
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.h2(
                "Real-time Alert Feed",
                class_name="text-2xl font-bold text-gray-900 dark:text-white mb-4",
            ),
            rx.el.div(
                rx.foreach(AIOpsState.filtered_alerts, alert_card),
                class_name="flex flex-col gap-4 max-h-[60vh] overflow-y-auto p-4 bg-gray-50 dark:bg-gray-800/50 rounded-2xl border border-gray-200 dark:border-gray-700",
            ),
            class_name="bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm",
        ),
        class_name="flex-1 p-8 overflow-y-auto font-['Raleway']",
    )