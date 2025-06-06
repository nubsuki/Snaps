#!/usr/bin/env python3

import gi
import subprocess
import os
import time
from threading import Thread
from pathlib import Path
import shutil
import webbrowser

#check dependencies
REQUIRED_COMMANDS = ["grim", "slurp", "wl-copy", "dunstify"]

def check_dependencies():
    missing = [cmd for cmd in REQUIRED_COMMANDS if not shutil.which(cmd)]
    if missing:
        dialog = Gtk.MessageDialog(
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.CLOSE,
            text="Missing dependencies",
        )
        dialog.format_secondary_text(
            f"The following required tools are missing:\n" + "\n".join(missing)
        )
        dialog.run()
        dialog.destroy()
        exit(1)
    else:
        print("All dependencies found: " + ", ".join(REQUIRED_COMMANDS))

check_dependencies()

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3
Gtk.Window.set_default_icon_name("snaps")

#save location
save_location = Path.home() / "Pictures" / "Screenshots"
save_location.mkdir(parents=True, exist_ok=True)  # Create if not exists

#Path to your tray icon
dev_icon_path = Path("icons/snaps.svg").resolve()
system_icon_path = Path("/usr/share/icons/hicolor/scalable/apps/snaps.svg")

icon_path = str(dev_icon_path if dev_icon_path.exists() else system_icon_path)

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

#opens the screenshot saved fodler
def open_screenshot_folder(_=None):
    try:
        subprocess.Popen(["xdg-open", str(save_location)])
    except Exception:
        # fallback to specific FM if needed
        for fm in ["nautilus", "thunar", "dolphin", "pcmanfm"]:
            if shutil.which(fm):
                subprocess.Popen([fm, str(save_location)])
                break


#Quit function
def quit_app(_=None):
    Gtk.main_quit()

# Open GitHub page in default browser
def open_github(_=None):
    url = "https://github.com/nubsuki/Snaps"
    webbrowser.open(url)

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
add_menu_item("📁 Screenshots", open_screenshot_folder)
add_menu_item("ⵌ About", open_github)
menu.append(Gtk.SeparatorMenuItem())
add_menu_item("❌ Quit", quit_app)

menu.show_all()
indicator.set_menu(menu)

Gtk.main()


#Made by ©nubsuki
#This project i made for my personal use