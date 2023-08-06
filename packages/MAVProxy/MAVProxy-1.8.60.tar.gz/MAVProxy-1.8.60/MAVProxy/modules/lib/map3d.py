#!/usr/bin/env python3
'''
3d path viewer
'''

from panda3d_viewer import Viewer, ViewerConfig
from pymavlink.quaternion import QuaternionBase, Quaternion
from pymavlink.rotmat import Vector3, Matrix3
from pymavlink import mavutil
import math, sys

def qtuple(q):
    '''
    return a quaternion tuple. We mirror on the Z axis by changing
    the sign of two elements to cope with the different conventions
    '''
    return (q[0],-q[1],-q[2],q[3])

config = ViewerConfig()
config.set_window_size(320, 240)
config.enable_antialiasing(True, multisamples=4)

def view_path(viewer, path, color):
    idx = 0
    print("Plotting %u points" % len(path))
    m = Matrix3()
    m.from_euler(0, math.radians(90), 0)
    qorient = Quaternion(m)

    for i in range(1,len(path)):
        p0 = path[i-1]
        p1 = path[i]
        dx = p1.pos[0] - p0.pos[0]
        dy = p1.pos[1] - p0.pos[1]
        dz = p1.pos[2] - p0.pos[2]
        dt = p1.t - p0.t
        if dt > 0.5:
            continue
        dist = math.sqrt(dx**2+dy**2+dz**2)+0.001
        if dist <= 0:
            continue
        pname = 'p%u' % i
        viewer.append_box('root', pname, (dist, 0.1, 0.002), frame=(p1.pos,qtuple(p1.q)))
        viewer.set_material('root', pname, color_rgba=color)

class LogPoint(object):
    def __init__(self, x,y,z,q,t):
        self.pos = (x,y,z)
        self.q = q
        self.t = t

def extract_paths(mlog, types):
    paths = {}
    ATT = None

    types.append('ATT')

    while True:
        m = mlog.recv_match(type=types)
        if m is None:
            break
        mtype = m.get_type()
        if mtype == 'ATT':
            ATT = m
            continue
        if mtype in types:
            if mtype not in paths:
                paths[mtype] = []
            paths[mtype].append(LogPoint(m.px*scale, m.py*scale, -m.pz*scale, Quaternion([m.q1, m.q2, m.q3, m.q4]), m.TimeUS*1.0e-6))
    return paths

class Map3D(MPDataLogChildTask):
    '''A class used to launch the 3D map view in a child process'''

    def __init__(self, *args, **kwargs):
        '''
        Parameters
        ----------
        title : str
            The title of the application
        mlog : DFReader
            A dataflash or telemetry log
        xlimits: MAVExplorer.XLimits
            An object capturing timestamp limits
        '''

        super(MagFit, self).__init__(*args, **kwargs)

        # all attributes are implicitly passed to the child process 
        self.title = kwargs['title']
        self.xlimits = kwargs['xlimits']

    # @override
    def child_task(self):
        '''Launch the 3D view'''
        from MAVProxy.modules.lib import wx_processguard
        from MAVProxy.modules.lib.wx_loader import wx

        # create wx application
        app = wx.App(False)
        app.frame = MagFitUI(title=self.title,
                             close_event=self.close_event,
                             mlog=self.mlog,
                             timestamp_in_range=self.xlimits.timestamp_in_range)

        app.frame.SetDoubleBuffered(True)
        app.frame.Show()
        app.MainLoop()

viewer = Viewer(window_type='onscreen', window_title=filename, config=config)
viewer.append_group('root')
show_log(viewer, sys.argv[1])
viewer.reset_camera(pos=(0, -6, 1), look_at=(0, 0, 1))
viewer.join()
