import asyncio 
# lets say client sends a req to do a large calculation or read a large file from a disk 
# so now server sends a handle but doesnt respond back to client when client asks "is X ready" and continues doing its work
#server only responds when the task has been completed 
Jobs = {1: 50}

def handle_request(Jobs, handle):
    if Jobs[handle] <= 0:
        print("It's done bro")

async def handle_job(Jobs, handler):
    while Jobs[handler] > 0:
        await asyncio.sleep(5)
        Jobs[handler] -= 5


async def main():
    asyncio.create_task(handle_job(Jobs, 1))

    ask = await asyncio.to_thread(input)
    if ask == "is job 1 ready":
        while Jobs[1] > 0:
            await asyncio.sleep(1)

        handle_request(Jobs, 1)


if __name__ == "__main__":
    asyncio.run(main())
