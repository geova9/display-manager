import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from gui import DisplayManagerWindow


def main() -> None:
    window = DisplayManagerWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
