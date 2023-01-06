from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.color = color.rgb(0,200,211)
window.exit_button.visible = False

grassStrokeTex = load_texture('grass_14.png')

def input(key):
    if key == 'q' or key == 'escape':
        quit()

def update():
   pass

terrain = Entity(model=None, collider=None)

terrainWidth=10
for i in range(terrainWidth*terrainWidth):
    bud = Entity(model='cube', color=color.green,
                 texture=grassStrokeTex)
    bud.x = i / terrainWidth
    bud.z = i % terrainWidth
    bud.y = 0
    bud.parent = terrain

terrain.combine()
terrain.collider = 'mesh'


subject = FirstPersonController()
subject.x = subject.z = 5
subject.y = 12

app.run()