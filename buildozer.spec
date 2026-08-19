[app]
title = Sania Malik
package.name = saniamalik
package.domain = com.fahadali
source.dir = .
version = 4.4
requirements = python3,kivy==2.2.1,cython==0.29.36
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE,WAKE_LOCK,RECORD_AUDIO,CAMERA,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,BLUETOOTH,BLUETOOTH_ADMIN,VIBRATE,SYSTEM_ALERT_WINDOW
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.ndk = 25b
android.private_storage = True
p4a.bootstrap = sdl2
p4a.branch = develop
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

[buildozer]
log_level = 2
warn_on_root = 1
