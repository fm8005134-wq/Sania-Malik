[app]

title = Sania Malik
package.name = saniamalik
package.domain = com.fahadali

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 4.4

requirements = python3,kivy==2.2.1

p4a.source_dir = /home/runner/p4a-pinned

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 27
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

p4a.bootstrap = sdl2

android.skip_update = False

[buildozer]

log_level = 2
warn_on_root = 1
