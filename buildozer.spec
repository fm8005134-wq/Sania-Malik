[app]
title = Sania Malik
package.name = saniamalik
package.domain = com.fahadali

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 4.4

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE,WAKE_LOCK,RECORD_AUDIO,CAMERA

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

android.allow_backup = True
android.accept_sdk_license = True

p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
