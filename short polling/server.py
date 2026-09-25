import asyncio

Jobs = {1: 6} # say the server gives the client 1 as handler (100 represents the time required to finish the task given by client)
def handle_request(handler,exit):
    if Jobs[handler] <= 0:
        print("Done")
        exit[0]=1
    else:
        print("Not Ready")

async def handle_job():
    while True:
        await asyncio.sleep(5)
        for handler in Jobs:
            Jobs[handler] -= 5


async def main():
    asyncio.create_task(handle_job()) #create seperate task for reducing the time taken to complete the task denoted by handler
    exit=[0]
    while not exit[0]:
        Promise = int(await asyncio.to_thread(input)) #to_thread() is used to make a blocking i/o non blocking (creates another working thread and assigns the blocking i/o part to it)
        if Promise:
            handle_request(Promise,exit)

if __name__ == "__main__":
    asyncio.run(main())