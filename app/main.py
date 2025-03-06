from fastapi import FastAPI
from app.routers import users, auth, trainings, notifications
from dotenv import load_dotenv
import os

from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

# Cargar variables de entorno
load_dotenv()

# Configurar Application Insights
from app.config.app_insights import configure_azure_monitor

# Configurar OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
exporter = AzureMonitorTraceExporter.from_connection_string(os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY"))
span_processor = BatchSpanProcessor(exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI()

# Instrumentar FastAPI
FastAPIInstrumentor.instrument_app(app)

# Instrumentar otras bibliotecas
LoggingInstrumentor().instrument()
RequestsInstrumentor().instrument()
URLLibInstrumentor().instrument()
URLLib3Instrumentor().instrument()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(trainings.router)
app.include_router(notifications.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Gym Management API"}
