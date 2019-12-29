# FinQwerty

Various keyboard layouts for the physical QWERTY keyboards of the following Android phones:

- BlackBerry KEYone **Android 7.1 only** (Danish, Finnish, German, Norwegian, Swedish)
- BlackBerry Priv (Danish, Finnish, German, Norwegian, Swedish)
- F(x)tec Pro1 (Czech, Danish, Finnish, German, Norwegian, Swedish, U.S., U.S. international)
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

Some of the Pro1 layouts (fin/nor/swe and cze qwertz) are generated from other layouts automatically by `generate_layouts.sh`
which has to be run manually if the Pro1 cze or Pro1 dan layouts are modified
(TODO: integrate that into the Gradle build and remove the generated files from git).

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

