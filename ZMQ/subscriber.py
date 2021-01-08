from index import Subscriber
import asyncio

subscriber = Subscriber(port=6666)

async def main():
    while True:
        frame = await subscriber.receive_frame()
        print(frame)

        await asyncio.sleep(.016)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing subscriber')
        loop.close()
        

