import time

from .status import *
'''
{
	"jsonrpc": "2.0",
	"result": null,
	"id": "1",
	"ctx": null,
	"timestampin": "123456789",
	"timestampout": "1675400598414",
	"route": {
		"TTL": 0,
		"DestAddr": "",
		"SourceAddr": ""
	},
	"error": {
		"message": "success",
		"code": 200,
		"data": null
	}
}
'''

class JsonrpcResponse(object):
    
    def __init__(self,rpc_conn) -> None:
        self.response = {
            "jsonrpc": rpc_conn.jsonrpc,
            "result": None,
            "id": rpc_conn.id,
            "ctx": rpc_conn.ctx,
            "timestampin": rpc_conn.timestampin,
            "timestampout": str(int(time.time())),
            "route": {
                "TTL": 0,
                "DestAddr": "",
                "SourceAddr": ""
            },
            "error": {
                "message": "success",
                "code": 200,
                "data": None
            }
        }
    
    
    def write_result(self,result):
        self.response["result"] = result
        return self.response
    
    def method_not_found(self):
        self.response["error"] = {
            "message": "method not found",
            "code": JSONRPC_405_METHOD_NOT_ALLOWED,
            "data": None
        }
        return self.response