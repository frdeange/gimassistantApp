import os
from azure.monitor.opentelemetry import configure_azure_monitor

instrumentation_key = os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")

if not instrumentation_key:
    raise ValueError("Please set the APPINSIGHTS_INSTRUMENTATIONKEY environment variable.")

configure_azure_monitor(connection_string=instrumentation_key)
