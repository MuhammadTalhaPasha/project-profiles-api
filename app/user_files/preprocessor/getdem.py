
import ezdxf


from ezdxf.groupby import groupby
# doc = ezdxf.readfile("D:\dxf files\wc.dxf")
#doc = ezdxf.readfile("D:\dxf files\Drawing2.dxf")
#msp = doc.modelspace()
# wall = msp.query('LINE[layer=="wall"]')
group = groupby(entities=msp, dxfattrib='layer')


group = msp.groupby(dxfattrib='layer')

def print_entity(e):
    print("LINE on layer: %s\n" % e.dxf.layer)
    print("color of layer: %s\n" % e.dxf.color)
    print("start point: %s\n" % e.dxf.start)
    print("end point: %s\n" % e.dxf.end)

# for layer, entities in group.items():
#     if layer
#     print(f'Layer "{layer}" contains following entities:')
#     for entity in entities:
#         print('    {}'.format(str(entity)))
#     print('-'*40)

def layer_and_color_key(entity):
    # return None to exclude entities from result container
    if entity.dxf.layer == '0':  # exclude entities from default layer '0'
        print_entity(entity)
        return entity.dxf.layer, entity.dxf.color
    else:
        return None

group = msp.groupby(key=layer_and_color_key)
for key, entities in group.items():
    print(f'Grouping criteria "{key}" matches following entities:')
    for entity in entities:
        print('    {}'.format(str(entity)))
    print('-'*40)
