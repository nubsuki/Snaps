
# Snaps - Simple System Tray Screenshot Tool for Wayland

Snaps is a lightweight screenshot tool for Wayland users, sitting quietly in your system tray and letting you snap full or snip screenshots with ease. It copies your screenshot to clipboard, saves it to your Pictures folder, and notifies you when done — all wrapped up in a nice GTK tray app.

---

## Snaps
[![Snaps Demo Video](https://img.youtube.com/vi/YOUTUBE_VIDEO_ID/hqdefault.jpg)](https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID)


## Features

- 📷 Take a **Full Screenshot**
- ✂️ Take a **Snip Screenshot** (select area)
- 📁 Open your **Screenshots folder**

---

## Installation Arch Linux

```bash
git clone https://github.com/nubsuki/Snaps.git
cd Snaps
makepkg -si
````

This will build and install the `snaps` package on your system.

---

## Uninstallation

```bash
sudo pacman -R snaps
```

---

## Set Your Default File Manager (optional)

If your screenshots folder opens in the wrong app (like VSCode instead of your file manager), you can set your default file manager manually:

```bash
ls /usr/share/applications | grep -i nautilus
# Example output:
# nautilus-autorun-software.desktop
# org.gnome.Nautilus.desktop

xdg-mime default org.gnome.Nautilus.desktop inode/directory
```

Replace `org.gnome.Nautilus.desktop` with the desktop file for your preferred file manager if different.

---

## Dependencies

Make sure these tools are installed on your system (usually handled by `makepkg`):

* grim
* slurp
* wl-copy
* dunstify
* python-gobject
* gtk3
* libappindicator-gtk3

---

## Usage

Launch Snaps from your app menu or via terminal with:

```bash
snaps
```

Use the tray icon menu to take screenshots or open your screenshots folder.


---

Enjoy snapping! 

