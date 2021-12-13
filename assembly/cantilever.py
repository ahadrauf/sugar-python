from assembly import Assembly
from model.anchor import Anchor
from model.beam2d import Beam2D
from process.SOI_berk import SOI_berk

def create_cantilever(l, w):
    assem = Assembly(2)
    assem.rename_node(0, "gnd")
    assem.rename_node(1, "tip")
    layer = SOI_berk()

    assem.add_model(Anchor(1, 1, layer.p1), ["gnd"])
    assem.add_model(Beam2D(l, w, layer.p1), ["gnd", "tip"])
