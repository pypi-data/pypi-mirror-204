from src.datamodelsFrontier.external import InventoryItemDimension
from src.datamodelsFrontier.external import Barcode
from src.datamodelsFrontier.external import InventoryItem


def test_inventory_item_dimension():
    iid = InventoryItemDimension(height_mm=3, width_mm=4, depth_mm=5, mass_kg=5)
    assert iid.height_mm == 3
    assert iid.width_mm == 4
    assert iid.depth_mm == 5
    assert iid.mass_kg == 5


def test_barcode():
    barcode = Barcode(barcode_type="type", barcode="barcode")

    assert barcode.barcode == "barcode"
    assert barcode.barcode_type == "type"


def test_inventory_item():
    barcode = Barcode(barcode_type="type", barcode="barcode")
    iid = InventoryItemDimension(height_mm=3, width_mm=4, depth_mm=5, mass_kg=5)
    ii = InventoryItem(inventory_item_id="id",
                       sku="sku",
                       name="name",
                       country_of_origin="coo",
                       harmonized_system_code="hsc",
                       has_hazmat=True,
                       barcodes=[barcode],
                       dimensions=iid,
                       alternative_inventory_items=["aii1", "aii2"],
                       thg_id="thg_id",
                       status="status")
    assert ii.inventory_item_id == "id"
    assert ii.sku == "sku"
    assert ii.name == "name"
    assert ii.country_of_origin == "coo"
    assert ii.harmonized_system_code == "hsc"
    assert ii.has_hazmat is True
    assert ii.barcodes == [barcode]
    assert ii.dimensions == iid
    assert ii.alternative_inventory_items == ["aii1", "aii2"]
    assert ii.thg_id == "thg_id"
    assert ii.status == "status"
