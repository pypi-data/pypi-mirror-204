from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .request import JsonrpcModel
from .response import JsonrpcResponse
from .method import JSONRPC_METHOD,JSONRPC_MIDDLEWARE

api_router = APIRouter()


@api_router.post("/jsonrpc")
async def jsonrpc(jsonrpc:JsonrpcModel):
    
    # 执行拦截器 中间件
    for func_i in JSONRPC_MIDDLEWARE:
        mid_response = func_i(jsonrpc)
        if mid_response:
            return mid_response
        
    #获取执行函数 
    method = jsonrpc.method
    func = JSONRPC_METHOD.get(method) or None

    if not func:
        response = JsonrpcResponse(jsonrpc)
        return JSONResponse(response.method_not_found())
    return func(jsonrpc)