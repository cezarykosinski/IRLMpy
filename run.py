from models.map_context import MapContext
ctx = MapContext()
ctx.start()
print()
ctx.maps[(0, 0)].display()
