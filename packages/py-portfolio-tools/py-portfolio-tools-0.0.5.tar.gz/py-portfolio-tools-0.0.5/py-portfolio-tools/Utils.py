import os
import sys
import OpenGL.GL as gl
import glfw
import imgui
import numpy as np
from PIL import Image
import PIL
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

class Object(object):
    pass

def SetupImGuiTheme():
    """Setup the imgui theme"""
    style = imgui.get_style()
    style.window_padding = (15, 15)
    style.window_rounding = 5.0
    style.frame_padding = (5, 5)
    style.frame_rounding = 4.0
    style.item_spacing = (12, 8)
    style.item_inner_spacing = (8, 6)
    style.indent_spacing = 25.0
    style.scrollbar_size = 15.0
    style.scrollbar_rounding = 9.0
    style.grab_min_size = 5.0
    style.grab_rounding = 3.0
    style.window_border_size = 0
    style.child_border_size = 0
    style.popup_border_size = 0
    style.frame_border_size = 0
    style.colors[imgui.COLOR_TEXT] = (0.80, 0.80, 0.83, 1.00)
    style.colors[imgui.COLOR_TEXT_DISABLED] = (0.24, 0.23, 0.29, 1.00)
    style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.06, 0.05, 0.07, 1.00)
    style.colors[imgui.COLOR_POPUP_BACKGROUND] = (0.07, 0.07, 0.09, 1.00)
    style.colors[imgui.COLOR_BORDER] = (0.80, 0.80, 0.83, 0.88)
    style.colors[imgui.COLOR_BORDER_SHADOW] = (0.92, 0.91, 0.88, 0.00)
    style.colors[imgui.COLOR_FRAME_BACKGROUND] = (0.10, 0.09, 0.12, 1.00)
    style.colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (0.24, 0.23, 0.29, 1.00)
    style.colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (0.56, 0.56, 0.58, 1.00)
    style.colors[imgui.COLOR_TITLE_BACKGROUND] = (0.10, 0.09, 0.12, 1.00)
    style.colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED] = (1.00, 0.98, 0.95, 0.75)
    style.colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.07, 0.07, 0.09, 1.00)
    style.colors[imgui.COLOR_SCROLLBAR_BACKGROUND] = (0.10, 0.09, 0.12, 1.00)
    style.colors[imgui.COLOR_SCROLLBAR_GRAB] = (0.80, 0.80, 0.83, 0.31)
    style.colors[imgui.COLOR_SCROLLBAR_GRAB_HOVERED] = (0.56, 0.56, 0.58, 1.00)
    style.colors[imgui.COLOR_SCROLLBAR_GRAB_ACTIVE] = (0.06, 0.05, 0.07, 1.00)
    style.colors[imgui.COLOR_SCROLLBAR_GRAB_ACTIVE] = (0.06, 0.05, 0.07, 1.00)
    style.colors[imgui.COLOR_CHECK_MARK] = (0.80, 0.80, 0.83, 0.31)
    style.colors[imgui.COLOR_SLIDER_GRAB] = (0.80, 0.80, 0.83, 0.31)
    style.colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = (0.06, 0.05, 0.07, 1.00)
    style.colors[imgui.COLOR_BUTTON] = (0.10, 0.09, 0.12, 1.00)
    style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.24, 0.23, 0.29, 1.00)
    style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.56, 0.56, 0.58, 1.00)
    style.colors[imgui.COLOR_HEADER] = (0.10, 0.09, 0.12, 1.00)
    style.colors[imgui.COLOR_HEADER_HOVERED] = (0.56, 0.56, 0.58, 1.00)
    style.colors[imgui.COLOR_HEADER_ACTIVE] = (0.06, 0.05, 0.07, 1.00)
    style.colors[imgui.COLOR_RESIZE_GRIP] = (0.00, 0.00, 0.00, 0.00)
    style.colors[imgui.COLOR_RESIZE_GRIP_HOVERED] = (0.56, 0.56, 0.58, 1.00)
    style.colors[imgui.COLOR_RESIZE_GRIP_ACTIVE] = (0.06, 0.05, 0.07, 1.00)
    style.colors[imgui.COLOR_PLOT_LINES] = (0.40, 0.39, 0.38, 0.63)
    style.colors[imgui.COLOR_PLOT_LINES_HOVERED] = (0.25, 1.00, 0.00, 1.00)
    style.colors[imgui.COLOR_PLOT_HISTOGRAM] = (0.40, 0.39, 0.38, 0.63)
    style.colors[imgui.COLOR_PLOT_HISTOGRAM_HOVERED] = (0.25, 1.00, 0.00, 1.00)
    style.colors[imgui.COLOR_TEXT_SELECTED_BACKGROUND] = (0.25, 1.00, 0.00, 0.43)
    style.colors[imgui.COLOR_HEADER] = (0.61, 0.61, 0.62, 0.22)
    style.colors[imgui.COLOR_HEADER_HOVERED] = (0.61, 0.62, 0.62, 0.51)
    style.colors[imgui.COLOR_HEADER_ACTIVE] = (0.61, 0.62, 0.62, 0.83)

def ImGuiShowComboBox(label, items, selected):
    """Shows a combo box"""
    with imgui.begin_combo(label, items[selected]) as combo:
        if combo.opened:
            for i, item in enumerate(items):
                is_selected = (i == selected)
                if imgui.selectable(item, is_selected)[0]:
                    selected = i
                if is_selected:
                    imgui.set_item_default_focus()
    return selected

def CreateGLTexture(something):
    """Creates a GL texture from a file"""
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    image = Image.open(something)
    image_data = image.convert("RGBA").tobytes()
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.width, image.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, image_data)
    result = Object()
    result.id = texture
    result.width = image.width
    result.height = image.height
    result.data = image_data
    return result


def DeleteGLTexture(texture):
    """Deletes a GL texture"""
    gl.glDeleteTextures(1, [texture])

def InitializeGLFW():
    """Initializes GLFW"""
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

def ShowFileOpenWindow():
    """Shows a file chooser dialog"""
    return askopenfilename()

def ShowFileSaveWindow():
    """Shows a file chooser dialog"""
    return asksaveasfilename()

def SaveImageAsFile(data, path: str):
    """Saves an image as a file"""
    image = Image.frombytes("RGBA", (data.width, data.height), data.data)
    image.save(path)

def SaveAsFile(data, path: str):
    with open(path, 'wb') as f:
        f.write(data)

def CreateWindow(width : int, height : int, title : str):
    """Creates a GLFW window"""
    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")
    glfw.make_context_current(window)
    return window

def PathExists(path):
    """Checks if a path exists"""
    return os.path.exists(path)

def VerifyPath(path):
    """Verifies that a path exists, and if not, creates it"""
    if not os.path.exists(path):
        os.makedirs(path)

def GetDataPath():
    """Returns the user data path for the application"""
    if sys.platform == 'win32':
        return os.path.join(os.environ['APPDATA'], 'py-portfolio-tools')
    elif sys.platform == 'darwin':
        return os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'py-portfolio-tools')
    else:
        return os.path.join(os.environ['HOME'], '.config', 'py-portfolio-tools')