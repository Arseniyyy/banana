from index import Publisher
import cv2
import asyncio

cap = cv2.VideoCapture(0)
publisher = Publisher(port=6666)
cap.read()


async def main():
    global cap, publisher, counter

    while True:
        ret, frame = cap.read()

        if frame.any():
            await publisher.send_frame(frame)
        
        await asyncio.sleep(.016)


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(main())
        loop.run_forever()
    except KeyboardInterrupt:
        print('Closing publisher')
        loop.close()
        
