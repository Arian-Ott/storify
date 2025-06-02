from pydantic import BaseModel, Field

class S4Request(BaseModel):
    """
    Schema for S4 request.
    """
    file_name: str = Field(..., description="Name of the file to be processed")
    