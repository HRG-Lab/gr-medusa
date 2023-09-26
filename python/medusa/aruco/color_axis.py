from OpenGL import GL

from pyqtgraph.opengl import GLAxisItem


class ColorAxisItem(GLAxisItem):
    def __init__(
        self,
        x_color=(1., 0., 0.),
        y_color=(0., 1., 0.),
        z_color=(0., 0., 1.),
        **kwargs
    ):
        super().__init__(**kwargs)

        self.x_color = x_color
        self.y_color = y_color
        self.z_color = z_color

    def paint(self):
        self.setupGLState()

        if self.antialias:
            GL.glEnable(GL.GL_LINE_SMOOTH)
            GL.glHint(GL.GL_LINE_SMOOTH_HINT, GL.GL_NICEST)

        GL.glBegin(GL.GL_LINES)

        x, y, z = self.size()
        GL.glColor4f(*self.z_color, .6)
        GL.glVertex3f(0, 0, 0)
        GL.glVertex3f(0, 0, z)

        GL.glColor4f(*self.y_color, .6)
        GL.glVertex3f(0, 0, 0)
        GL.glVertex3f(0, y, 0)

        GL.glColor4f(*self.x_color, .6)
        GL.glVertex3f(0, 0, 0)
        GL.glVertex3f(x, 0, 0)
        GL.glEnd()
