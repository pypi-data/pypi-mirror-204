from src.datamodelsFrontier.downstream import ChildProduct


def test_child_product():
    cp = ChildProduct(
        id="id",
        title="title",
        barcode="barcode",
        releaseDate="rd",
        rrp="rrp",
        length="1",
        height="2",
        width="3",
        weight="4",
        releaseDateEstimated=True
    )

    assert cp.id == "id"
    assert cp.title == "title"
    assert cp.barcode == "barcode"
    assert cp.releaseDate == "rd"
    assert cp.rrp == "rrp"
    assert cp.length == "1"
    assert cp.height == "2"
    assert cp.width == "3"
    assert cp.weight == "4"
    assert cp.releaseDateEstimated is True
