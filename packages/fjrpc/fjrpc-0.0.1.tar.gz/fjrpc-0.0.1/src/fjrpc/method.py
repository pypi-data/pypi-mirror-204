

JSONRPC_METHOD = {}

JSONRPC_MIDDLEWARE = []

def set_method(method,func):
    JSONRPC_METHOD[method] = func
    
    
def set_middleware(func):
    JSONRPC_MIDDLEWARE.append(func)