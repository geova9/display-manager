import gi
import traceback

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from backend_factory import available_backends, create_backend
from profile import MonitorProfile, get_profile, load_profiles, save_profiles


class DisplayManagerWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Display Manager")
        self.set_default_size(760, 420)

        self.backend = create_backend("hyprland")
        self.profiles = load_profiles()
        self.monitors = []

        self.header_bar = Gtk.HeaderBar(title="Display Manager")
        self.header_bar.set_show_close_button(True)
        self.set_titlebar(self.header_bar)

        self.refresh_button = Gtk.Button(label="Actualizar")
        self.refresh_button.connect("clicked", self.on_refresh_clicked)
        self.header_bar.pack_start(self.refresh_button)

        self.default_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.default_box.set_margin_top(12)
        self.default_box.set_margin_bottom(12)
        self.default_box.set_margin_start(12)
        self.default_box.set_margin_end(12)
        self.add(self.default_box)

        self.backend_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.default_box.pack_start(self.backend_box, False, False, 0)

        self.backend_combo = Gtk.ComboBoxText()
        self.backend_combo.set_entry_text_column(0)
        for label in available_backends().values():
            self.backend_combo.append_text(label)
        self.backend_combo.set_active(0)
        self.backend_combo.connect("changed", self.on_backend_changed)
        self.backend_box.pack_start(Gtk.Label(label="Compositor:"), False, False, 0)
        self.backend_box.pack_start(self.backend_combo, False, False, 0)

        self.profile_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.default_box.pack_start(self.profile_box, False, False, 0)

        self.profile_combo = Gtk.ComboBoxText()
        self.profile_combo.set_entry_text_column(0)
        self.profile_combo.connect("changed", self.on_profile_changed)
        self.profile_box.pack_start(self.profile_combo, True, True, 0)

        self.load_profiles_combo()

        self.apply_button = Gtk.Button(label="Aplicar perfil")
        self.apply_button.connect("clicked", self.on_apply_profile)
        self.profile_box.pack_start(self.apply_button, False, False, 0)

        self.save_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.default_box.pack_start(self.save_box, False, False, 0)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("Nombre de perfil")
        self.save_box.pack_start(self.name_entry, True, True, 0)

        self.save_button = Gtk.Button(label="Guardar perfil")
        self.save_button.connect("clicked", self.on_save_profile)
        self.save_box.pack_start(self.save_button, False, False, 0)

        self.monitor_view = Gtk.TextView()
        self.monitor_view.set_editable(False)
        self.monitor_view.set_cursor_visible(False)
        self.monitor_buffer = self.monitor_view.get_buffer()

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.add(self.monitor_view)
        self.default_box.pack_start(scroll, True, True, 0)

        self.on_refresh_clicked(None)

    def load_profiles_combo(self) -> None:
        self.profile_combo.remove_all()
        for profile in self.profiles:
            self.profile_combo.append_text(profile.name)
        if self.profiles:
            self.profile_combo.set_active(0)

    def on_refresh_clicked(self, button) -> None:
        try:
            self.monitors = self.backend.list_monitors()
            self.monitor_buffer.set_text(self.format_monitor_text())
        except Exception as exc:
            self.show_error("Error al leer monitores", str(exc))

    def on_backend_changed(self, combo) -> None:
        active = combo.get_active_text()
        if not active:
            return

        try:
            self.backend = create_backend(active)
            self.on_refresh_clicked(None)
        except Exception as exc:
            self.show_error("Backend no soportado", str(exc))

    def on_save_profile(self, button) -> None:
        name = self.name_entry.get_text().strip()
        if not name:
            self.show_error("Nombre inválido", "Debe proporcionar un nombre de perfil.")
            return

        if not self.monitors:
            self.show_error("Monitores vacíos", "No hay configuración de monitores para guardar.")
            return

        profile = MonitorProfile(name=name, monitors=self.monitors)
        existing = get_profile(self.profiles, name)
        if existing:
            self.profiles = [p for p in self.profiles if p.name != name]

        self.profiles.append(profile)
        save_profiles(self.profiles)
        self.load_profiles_combo()
        self.name_entry.set_text("")

    def on_apply_profile(self, button) -> None:
        active_profile = self.get_selected_profile()
        if not active_profile:
            self.show_error("Perfil no seleccionado", "Seleccione un perfil para aplicar.")
            return

        try:
            self.backend.apply_profile(active_profile)
            self.show_info("Perfil aplicado", f"El perfil '{active_profile.name}' se ha aplicado correctamente.")
        except Exception as exc:
            self.show_error("Error al aplicar perfil", str(exc))

    def on_profile_changed(self, combo) -> None:
        pass

    def get_selected_profile(self) -> MonitorProfile | None:
        active = self.profile_combo.get_active_text()
        if not active:
            return None
        return get_profile(self.profiles, active)

    def format_monitor_text(self) -> str:
        if not self.monitors:
            return "No se detectaron monitores."

        lines = []
        for monitor in self.monitors:
            lines.append(monitor.layout_description())
            lines.append(f"  Activo: {monitor.active}    Principal: {monitor.primary}")
            lines.append("")
        return "\n".join(lines)

    def show_error(self, title: str, message: str) -> None:
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def show_info(self, title: str, message: str) -> None:
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()
