from everytime import every
import everytime


@every(5).seconds
async def greet():
    print("Hello")

everytime.run_forever()
