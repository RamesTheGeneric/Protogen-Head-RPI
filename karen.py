
from nicegui import ui
import manager
import dlib_facemesh
from threading import Thread

class Demo:
    def __init__(self):
        self.number = 1
'''
with ui.column():
    ui.switch('MainLoop', on_change=lambda e: switch_state.set_text('ON' if e.value else'OFF'))
    with ui.row():
        ui.label('the switch is:')
        switch_state = ui.label('OFF')

    ui.switch('Command Sender', on_change=lambda e: switch_state.set_text('ON' if e.value else'OFF'))
    with ui.row():
        ui.label('the switch is:')
        switch_state = ui.label('OFF')

    ui.joystick(
        color='blue',
        size=50,
        on_move=lambda msg: coordinates.set_text(f'{msg.data.vector.x:.3f}, {msg.data.vector.y:.3f}'),
        on_end=lambda _: coordinates.set_text('0, 0'))

    coordinates = ui.label('0, 0')

'''
demo = Demo()
v = ui.checkbox('visible', value=True)
with ui.column().bind_visibility_from(v, 'value'):
    ui.slider(min=1, max=3).bind_value(demo, 'number')
    ui.toggle({1: 'a', 2: 'b', 3: 'c'}).bind_value(demo, 'number')
    ui.number().bind_value(demo, 'number')



print('about to run')
thread = Thread(target=manager.main, args=())
thread.daemon = True
thread.start()
ui.run(host = '10.0.0.5')





