from models.map_context import MapContext
ctx = MapContext()
ctx.start()
ctx.maps[(0,0)].groups_connecting()
