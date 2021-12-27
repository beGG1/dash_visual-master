# import asyncio
#
#
# async def say(phrase, seconds):
#     await asyncio.sleep(seconds)
#     print(phrase)
#
#
# async def wicked():
#     task_1 = asyncio.create_task(say('Surrender', 2))
#     task_2 = asyncio.create_task(say('Word', 2))
#     await task_2
#     await task_1
#
# asyncio.run(wicked())
