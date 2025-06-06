pkgname=snaps
pkgver=1.0
pkgrel=1
pkgdesc="A simple system tray screenshot tool for Wayland"
arch=('any')
depends=('python' 'python-gobject' 'gtk3' 'libappindicator-gtk3' 'grim' 'slurp' 'wl-clipboard' 'dunst')
source=('app.py' 'snaps.svg' 'snaps.desktop')
md5sums=('SKIP' 'SKIP' 'SKIP')

package() {
  install -Dm755 app.py "$pkgdir/usr/bin/snaps"
  install -Dm644 snaps.svg "$pkgdir/usr/share/icons/hicolor/scalable/apps/snaps.svg"
  install -Dm644 snaps.desktop "$pkgdir/usr/share/applications/snaps.desktop"
}
