# main.py
import asyncio
import uuid
import nest_asyncio
from agents.supervisor import team
from langgraph.checkpoint.memory import MemorySaver 
from langchain_core.messages import HumanMessage

from common.common_utl import get_embeddings_model

nest_asyncio.apply()

async def ejecutar_agencia():

    memory = MemorySaver()
    get_embeddings_model() 
    app = team.compile(checkpointer=memory)
    
    thread_id = f"oracle_project_{uuid.uuid4().hex[:8]}"
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 100 # Aumentado para evitar errores de límite
    }
    
    # Mensaje inicial
    inputs = {"messages": [HumanMessage(content="Analiza los impactos de la versión 24D de Oracle Cloud.")]}
    print(f"🚀 Iniciando Oracle Cloud Analyzer [Thread: {thread_id}]")

    while True:
        # Ejecutamos hasta el próximo punto de interrupción o final
        async for event in app.astream(inputs, config=config, stream_mode="values"):
            if "messages" in event:
                # Opcional: imprimir el último mensaje para ver progreso
                last_msg = event["messages"][-1]
                if hasattr(last_msg, 'name') and last_msg.name:
                    print(f"[{last_msg.name.upper()}]: {last_msg.content[:100]}...")

        # Verificación de estado tras astream
        state = await app.aget_state(config)

        # Caso 1: flujo terminado
        if not state.next:
            print("\n✅ [PROCESO FINALIZADO]")
            final_messages = state.values.get("messages", [])
            if final_messages:
                print(f"\nResumen Final:\n{final_messages[-1].content}")
            break

if __name__ == "__main__":
    try:
        asyncio.run(ejecutar_agencia())
    except KeyboardInterrupt:
        print("\nTerminado por el usuario.")
