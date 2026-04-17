from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.Tools import tool_investigar_version, tool_marcar_error_version
from schemas.schemas import ReporteInvestigacion
from dotenv import load_dotenv


load_dotenv(override=True)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt_investigador = """
Eres el Investigador Experto de Oracle. Tu misión es extraer y PERSISTIR los datos de la versión solicitada.

FLUJO OBLIGATORIO:
1. **EXTRACCIÓN:** Ejecuta `tool_investigar_version`.
3. **CONFIRMACIÓN:** Solo después de que se haya ejecutado correctamente la herramienta `tool_investigar_version`, informa al Supervisor: "PERSISTENCIA_COMPLETADA: Los datos ya están en la base de datos".

GESTIÓN DE ERRORES (CRÍTICO):
- Si la herramientas de extracción falla o no encuentras datos, DEBES ejecutar 'tool_marcar_error_version' explicando el motivo.
- Esto es fundamental para desbloquear la versión en la base de datos.

SALIDA:
- No devuelvas las listas de impactos al chat. Solo confirma el éxito o el error de la persistencia.
"""


# Agente Investigador: Solo busca información
investigador = create_react_agent(
    model, 
    tools=[tool_investigar_version,  tool_marcar_error_version],
    name="investigador",
    prompt=prompt_investigador,
    response_format=ReporteInvestigacion
    )
