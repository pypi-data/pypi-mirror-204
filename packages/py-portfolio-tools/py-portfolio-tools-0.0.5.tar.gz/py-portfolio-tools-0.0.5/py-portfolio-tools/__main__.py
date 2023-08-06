from .DataFetch import *
from .Portfolio import *
from .PortfolioInputWindow import *

import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer

def main():
    # df = DataFetch()
    # print(df.GetStockInfo('GOOG'))
    # print(df.GetStockHistory("GOOG", "1d", "2005-01-01", "2022-12-31"))
    # pf = Portfolio("Test", ["GOOG", "MSFT", "AAPL", "NVDA"])
    # pf.Analyse("2020-01-01", "2022-12-31")

    portfolioInputWindow = PortfolioInputWindow()

    InitializeGLFW()
    window = CreateWindow(500, 500, "Portfolio Tools 2.0 - Jaysmito Mukherjee")
    gl.glClearColor(0.2, 0.2, 0.2, 1.0)
    imgui.create_context()
    SetupImGuiTheme()
    impl = GlfwRenderer(window)
    while not glfw.window_should_close(window):
        window_size = glfw.get_window_size(window)
        gl.glViewport(0, 0, window_size[0], window_size[1])
        gl.glClearColor(0.2, 0.2, 0.2, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        imgui.new_frame()
        
        portfolioInputWindow.Show()
        
        imgui.end_frame()

        imgui.render()
        impl.render(imgui.get_draw_data())
        
        glfw.swap_buffers(window)
        glfw.poll_events()
        impl.process_inputs()
    
    impl.shutdown()
    glfw.terminate()

if __name__ == "__main__":
    main()