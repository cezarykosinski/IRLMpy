from src.maps.map_context import MapContext
from src.maps.rogue import DefaultRogue
ctx = MapContext()
r = DefaultRogue()
ctx.start_with_rogue(r)
# print()
# ctx.maps[(0, 0)].display()
