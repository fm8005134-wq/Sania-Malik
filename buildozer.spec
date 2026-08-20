[app]

title = Sania Malik
package.name = saniamalik
package.domain = com.fahadali

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 4.4

requirements = python3,kivy==2.2.1

orientation = portrait

fullscreen = 0

android.permissions = INTERNET

android.api = 33
android.minapi = 21

android.ndk = 25b

android.archs = arm64-v8a

android.accept_sdk_license = True

p4a.bootstrap = sdl2

# Faster build
android.skip_update = False

[buildozer]

log_level = 2
warn_on_root = 1
