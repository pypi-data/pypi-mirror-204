from pydantic import BaseModel


class XArrayDims(BaseModel):
    x: str = 'x'
    y: str = 'y'
    band: str = 'band'
    time: str = 'time'


x_array_dims = XArrayDims()
