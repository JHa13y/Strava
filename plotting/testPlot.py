from bokeh.plotting import figure, output_file, show, ColumnDataSource, curdoc
from bokeh.layouts import row, widgetbox, column
from tornado.ioloop import IOLoop
from bokeh.application.handlers import FunctionHandler
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.models import CustomJS, Slider
import numpy as np
from scipy import misc
from PIL import Image
import strava_common.Authorize as authorize
import datetime, sys
from ActivityManager import ActivityManager;

map_height= 540
map_width= 1080



username= "joshua_haley"
type ="Ride"
activities = []
source = None
source_past = None
points_x = []
points_y = []
last_slider=1
io_loop = IOLoop.current()

def modify_doc(doc):
    global source, source_past, points_x, points_y
    output_file("image.html")
    p = figure(plot_width=map_width, plot_height=map_height, x_range=(280,310), y_range=(345, 360))
    p.image_url(url=['https://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74443/world.topo.200409.3x5400x2700.jpg'], x=0, y=map_height, w=map_width, h=map_height)

    #Pull one commute GPX File
    client = authorize.get_authorized_client(username)
    act = client.get_activity(955586803)
    streams = client.get_activity_streams(act.id, types=["latlng"])
    stream = streams['latlng']

    for point in stream.data:
        x,y=get_pixel(point[0], point[1])
        points_x.append(x)
        points_y.append(y)


    source = ColumnDataSource(data=dict(x=[points_x[0]], y=[points_y[0]]))
    source_past = ColumnDataSource(data=dict(x=[points_x[0]], y=[points_y[0]]))



    time_slider = Slider(start=0, end=len(points_x), value=1, step=10,
                        title="time")
    time_slider.on_change('value', slider_callback)



    p.circle(source=source, x='x', y='y', size = 15, color="navy" )
    p.line(source=source_past, x='x', y='y',color="red")
    layout = column(p, widgetbox (time_slider))
    doc.add_root(layout)

def slider_callback(attr, old, new):
    N = new  # this works also with slider.value but new is more explicit
    global source, source_past, points_x, points_y, last_slider
    if abs(last_slider - new) < 50:
        return
    last_slider = new
    new_data2 = dict()
    new_data2['x'] = points_x[0:int(new)]
    new_data2['y'] = points_y[0:int(new)]
    source_past.data = new_data2

    new_data = dict()
    new_data['x'] = [points_x[int(new)]]
    new_data['y'] = [points_y[int(new)]]
    source.data = new_data





def get_pixel(lat, long):
    """Translates from Data coordinate space to pixel coordinate space"""


    tmp = lat
    tmp *= -1.0;
    tmp += 90.0;
    tmp *= map_height / 180.0;

    y = map_height - tmp

    tmp = long
    tmp += 180.0;
    tmp *= map_width / (360.0);

    x= tmp

    return x,y;

if __name__ == "__main__":
    print('Opening Bokeh application on http://localhost:5006/')

    bokeh_app = Application(FunctionHandler(modify_doc))


    server = Server({'/': bokeh_app}, io_loop=io_loop)
    server.start()
    io_loop.add_callback(server.show, "/")
    io_loop.start()


