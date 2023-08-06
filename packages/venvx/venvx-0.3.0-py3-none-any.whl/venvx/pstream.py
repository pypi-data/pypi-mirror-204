# Added these ignores:
# flake8: noqa
# pylint: disable = invalid-name, line-too-long

'''
Code by
Kevin McCarthy
https://kevinmccarthy.org/2016/07/25/streaming-subprocess-stdin-and-stdout-with-asyncio-in-python/
The site appears to be down now.

There are updates to make this work in Windows here
https://stackoverflow.com/questions/636561/how-can-i-run-an-external-command-asynchronously-from-python
See Terrel Shumway's post Jul 24, 2019 at 16:07.
'''

import asyncio
import atexit
import sys


# Enable execute() to be run more than once.
loop = asyncio.new_event_loop()   # asyncio.get_event_loop()
atexit.register(loop.close)


# (TS) Compatibility with Windows:
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


async def _read_stream(stream, cb):
    while True:
        line = await stream.readline()
        if line:
            # Added decode() so stderr/stdout.write() can receive:
            cb(line.decode('ascii'))
        else:
            break


async def _stream_subprocess(cmd, stdout_cb, stderr_cb):
    process = await asyncio.create_subprocess_exec(*cmd,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    # Direct use of coroutine objects with async wait was deprecated in
    # Python 3.8 and will be removed in Python 3.11. Replaced
    # await asyncio.wait([
    #     asyncio.create_task(process.stdout, stdout_cb),
    #     asyncio.create_task(process.stderr, stderr_cb)
    # ])
    # with:
    await asyncio.wait([
        asyncio.create_task(_read_stream(process.stdout, stdout_cb)),
        asyncio.create_task(_read_stream(process.stderr, stderr_cb))
    ])
    return await process.wait()


# Changed the signature from
# def execute(*cmdline, stdout_cb=on_stdout, stderr_cb=on_stderr):
# to
def execute(cmd, stdout_cb=sys.stdout.write, stderr_cb=sys.stderr.write):
    # Made this global: loop = asyncio.get_event_loop()
    rc = loop.run_until_complete(
        _stream_subprocess(
            cmd,
            stdout_cb,
            stderr_cb,
    ))
    # Moved this into the exit handler: loop.close()
    return rc


# Disabled this:
# if __name__ == '__main__':
#     print(execute(
#         ["bash", "-c", "echo stdout && sleep 1 && echo stderr 1>&2 && sleep 1 && echo done"],
#         lambda x: print("STDOUT: %s" % x),
#         lambda x: print("STDERR: %s" % x),
#     ))
