from pydantic import BaseModel, Field
from typing import Union



class JsonrpcModel(BaseModel):
    jsonrpc: str = Field(description="jsonrpc版本号")
    method: str = Field(description="请求方法")
    params: Union[dict, None] = Field(description="jsonrpc参数")
    id: Union[str, None] = Field(description="id")
    session: Union[str, None] = Field(description="token or session")
    ctx: Union[dict, None] = Field(description="上下文")
    timestampin: Union[str, None] = Field(description="时间戳")