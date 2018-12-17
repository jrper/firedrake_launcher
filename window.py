import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import jfiredrake

class MyWindow(Gtk.Window):

    def __init__(self):

        css = b"""
* { 
   font-size: 30px; 
}
"""

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        Gtk.Window.__init__(self, title="Launch Jupyter Firedrake")

        self.button = Gtk.Button(label="Launch Jupyter Firedrake")
        self.button.connect("clicked", self.on_button_clicked)
        self.button.set_name("button")
        self.add(self.button)

        self.cont = None

    def on_button_clicked(self, widget):
        if not self.cont:
            print("Launching Jupyter Firedrake")
            self.cont, self.port = jfiredrake.start_instance()
        jfiredrake.open_browser(self.cont, self.port)

    def quit(self, widget):
        if self.cont:
            self.cont.stop()
            self.cont.remove()
            self.cont = None
        Gtk.main_quit(widget)

win = MyWindow()
win.connect("destroy", win.quit)
win.show_all()
Gtk.main()
