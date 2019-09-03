# FinQwerty

Various keyboard layouts for the physical QWERTY keyboards of the following slider Android phones:

- BlackBerry KEYone **Android 7.1 only** (Danish, Finnish, German, Norwegian, Swedish)
- BlackBerry Priv (Danish, Finnish, German, Norwegian, Swedish)
- F(x)tec Pro1 (Danish, Finnish, Norwegian, Swedish, U.S.)
- Gemini PDA (Finnish, Swedish)
- Livermorium Keyboard Moto Mod (Danish, Finnish, German, Norwegian, Swedish)
- Motorola Droid 4 (Finnish, Swedish)
- Motorola Photon Q 4G (Finnish, Swedish)
- Samsung Galaxy S Relay 4G (Finnish, Swedish)

See the [FinQwerty website](https://android.onse.fi/finqwerty/) for detailed layout maps.

The layouts are provided via the Android standard layouts mechanism and are selectable in Android settings - no root required.
An in-app workaround is also included for BlackBerry phones that do not have those settings.

## Installing

FinQwerty is available from Google Play: [FinQwerty](https://play.google.com/store/apps/details?id=fi.onse.qwerty.finnish)

## Building

The project uses Gradle and can be built with Android Studio or via commandline, for example:

```
export JAVA_HOME="$HOME/android-studio/jre"
export ANDROID_HOME="$HOME/Android/Sdk"
./gradlew assembleDebug
```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

