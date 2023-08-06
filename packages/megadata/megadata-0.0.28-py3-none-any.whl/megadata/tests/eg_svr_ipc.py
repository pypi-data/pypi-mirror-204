import sys
sys.path.append('..')

from mypy import build_address,try_asyncio as async_call,hook_quit,on_quit_default
hook_quit(on_quit_default)

from svr_ipc_bin import my_main_ipc, start_stdin

address = build_address(('wtf'))
print('address',address)

#my_main_ipc(address,mode='asyncio')

async_call(lambda:my_main_ipc(address,mode='asyncio'))
start_stdin()


