import reflex as rx
from app.states.state import AIOpsState, Incident, Alert
from app.components.dashboard import severity_badge


def alert_item_sm(alert: Alert) -> rx.Component:
    return rx.el.div(
        severity_badge(alert["severity"]),
        rx.el.div(
            rx.el.p(
                alert["message"],
                class_name="text-sm font-medium text-gray-700 dark:text-gray-300 truncate",
            ),
            rx.el.p(
                f"{alert['timestamp']} - {alert['source']}",
                class_name="text-xs text-gray-500 dark:text-gray-400",
            ),
            class_name="flex-1 min-w-0",
        ),
        class_name="flex items-center gap-3 p-2 bg-gray-50 dark:bg-gray-700/50 rounded-lg",
    )


def incident_card(incident: Incident) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"Incident #{incident['id']}",
                    class_name="font-semibold text-gray-800 dark:text-gray-100",
                ),
                rx.el.p(
                    f"Started at {incident['start_time']}",
                    class_name="text-sm text-gray-500 dark:text-gray-400",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.p(
                    incident["status"].capitalize(), class_name="text-sm font-medium"
                ),
                class_name=rx.match(
                    incident["status"],
                    (
                        "active",
                        "w-fit rounded-full bg-red-100 dark:bg-red-500/20 px-3 py-1 text-red-700 dark:text-red-300",
                    ),
                    (
                        "resolved",
                        "w-fit rounded-full bg-green-100 dark:bg-green-500/20 px-3 py-1 text-green-700 dark:text-green-300",
                    ),
                    "w-fit rounded-full bg-gray-100 dark:bg-gray-700 px-3 py-1 text-gray-700 dark:text-gray-300",
                ),
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.div(
            rx.el.p(
                "Summary",
                class_name="text-sm font-semibold text-gray-600 dark:text-gray-300 mb-2",
            ),
            rx.el.p(
                incident["summary"],
                class_name="text-sm text-gray-700 dark:text-gray-300",
            ),
            class_name="mt-3",
        ),
        rx.el.div(
            rx.el.p(
                "Affected Services",
                class_name="text-sm font-semibold text-gray-600 dark:text-gray-300 mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    incident["affected_services"],
                    lambda service: rx.el.div(
                        service,
                        class_name="text-xs bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-2 py-1 rounded-full",
                    ),
                ),
                class_name="flex flex-wrap gap-2",
            ),
            class_name="mt-3",
        ),
        rx.el.div(
            rx.el.p(
                "Clustered Alerts",
                class_name="text-sm font-semibold text-gray-600 dark:text-gray-300 mb-2",
            ),
            rx.el.div(
                rx.foreach(incident["alerts"], alert_item_sm),
                class_name="flex flex-col gap-2",
            ),
            class_name="mt-3",
        ),
        class_name="bg-white dark:bg-gray-800 p-6 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm flex flex-col gap-3",
    )


def incidents_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1(
                "Incidents",
                class_name="text-3xl font-bold text-gray-900 dark:text-white mb-2",
            ),
            rx.el.p(
                "Automatically clustered alerts representing real-world incidents.",
                class_name="text-gray-600 dark:text-gray-400",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            rx.cond(
                AIOpsState.incidents.length() > 0,
                rx.foreach(AIOpsState.incidents, incident_card),
                rx.el.div(
                    rx.icon("shield-check", size=32, class_name="text-gray-400"),
                    rx.el.p(
                        "No active incidents",
                        class_name="text-gray-600 dark:text-gray-400 font-medium",
                    ),
                    class_name="flex flex-col items-center justify-center gap-4 p-8 bg-gray-100/50 dark:bg-gray-800/50 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700",
                ),
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        class_name="flex-1 p-8 overflow-y-auto",
    )