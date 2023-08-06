from pydantic import BaseModel


class ChildProduct(BaseModel):
    id: str
    title: str
    barcode: str
    releaseDate: str
    rrp: str
    length: str
    height: str
    width: str
    weight: str
    releaseDateEstimated: bool
