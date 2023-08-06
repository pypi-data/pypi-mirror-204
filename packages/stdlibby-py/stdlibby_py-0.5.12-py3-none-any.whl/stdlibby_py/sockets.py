import readline
import asyncio, os, sys
from pathlib import Path
from typing import Callable, Coroutine, Any

def gen_socket(dir: str="/tmp", name: str="testing")->str:
    p = Path(os.path.join(dir, f"{name}.socket"))
    if p.is_socket():
        os.remove(p)
        return str(p)
    else:
        return str(p)

async def client(socket_path: str="/tmp/htmlize.socket"):
    reader, writer = await asyncio.open_unix_connection(socket_path)
    try:
        while True:
            request = input('/> ')
            writer.write((request).encode("utf8"))
            await writer.drain()
            response = (await reader.read(255)).decode("utf8")
            print(response.strip())
    except ConnectionResetError:
        print("Dropped Connection")
    except ConnectionError:
        print("HOI")
    except Exception as e:
        print(e.__dict__)
        print(e)
    finally:
        writer.close()

async def echo_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter)->None:
    request = None
    try:
        while request != 'quit':
            request = (await reader.read(255)).decode('utf8').strip()
            req = eval(request)
            writer.write(f"{req}\n".encode('utf8'))
            await writer.drain()

    except ConnectionResetError:
        print("Dropped Connection")
    except Exception as e:
        print(e.__dict__)
        print(e)
    finally:
        writer.close()

async def run_unix_server(handler: Callable[[asyncio.StreamReader, asyncio.StreamWriter], Coroutine[Any, Any, Any]]=echo_handler):
    socket_path = "/tmp/htmlize.socket"
    if os.path.exists(socket_path):
        os.remove(socket_path)

    server = await asyncio.start_unix_server(handler, path=socket_path)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    if sys.argv[1] == "server":
        asyncio.run(run_unix_server())
    else:
        asyncio.run(client())
