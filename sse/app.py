#simulating server sent events 
import asyncio
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent

app = FastAPI()

@app.get("/events", response_class=EventSourceResponse)
async def events():
    for i in range(100):
        await asyncio.sleep(1)
        yield ServerSentEvent(data=f"Message {i}")