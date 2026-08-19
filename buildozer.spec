[app]
title = Sania Malik
package.name = saniamalik
package.domain = com.fahadali
source.dir = .
version = 4.4
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE,WAKE_LOCK,RECORD_AUDIO,CAMERA,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,BLUETOOTH,BLUETOOTH_ADMIN,VIBRATE,SYSTEM_ALERT_WINDOW
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
p4a.bootstrap = sdl2
android.private_storage = True
android.ndk = 25b
android.accept_sdk_license = True

# Add these lines for Python version fix:
p4a.branch = develop
p4a.commit = 

# Fix for Python 3.14 issue:
requirements = python3,kivy==2.3.0,cython==0.29.36
