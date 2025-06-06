import gi
import subprocess
import os
import time
from threading import Thread
from pathlib import Path

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3
Gtk.Window.set_default_icon_name("snaps")

# save location
save_location = Path.home() / "Pictures" / "Screenshots"
save_location.mkdir(parents=True, exist_ok=True)  # Create if not exists

# 🖼️ Path to your tray icon
icon_path = os.path.abspath("icons/icon.svg")
if not Path(icon_path).exists():
    raise FileNotFoundError(f"Icon not found at: {icon_path}")


#Full screenshot function
def take_fullshot(_=None):
    filename = save_location / f"full-{time.strftime('%F_%T')}.png"
    subprocess.run(f"grim - | tee >(wl-copy) > '{filename}'", shell=True)
    subprocess.run(["dunstify", "📷 Full screenshot saved!"])

#Snip screenshot function
def take_snipshot(_=None):
    area = subprocess.getoutput("slurp").strip()
    if not area or "x" not in area or "," not in area:
        subprocess.run(["dunstify", "⚠️ Snip canceled or invalid area"])
        return
    filename = save_location / f"snip-{time.strftime('%F_%T')}.png"
    subprocess.run(f"grim -g '{area}' - | tee >(wl-copy) > '{filename}'", shell=True)
    subprocess.run(["dunstify", "✂️ Snip saved!"])

#Quit function
def quit_app(_=None):
    Gtk.main_quit()

#Set up tray icon
indicator = AppIndicator3.Indicator.new(
    "snaps-tray",
    icon_path,
    AppIndicator3.IndicatorCategory.APPLICATION_STATUS
)
indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
indicator.set_title("Snaps Screenshot Tool")

#Build menu
menu = Gtk.Menu()

def add_menu_item(label, callback):
    item = Gtk.MenuItem(label=label)
    item.connect("activate", lambda w: Thread(target=callback).start())
    menu.append(item)

add_menu_item("📷 Full Screenshot", take_fullshot)
add_menu_item("✂️ Snip Screenshot", take_snipshot)
menu.append(Gtk.SeparatorMenuItem())
add_menu_item("❌ Quit", quit_app)

menu.show_all()
indicator.set_menu(menu)

Gtk.main()