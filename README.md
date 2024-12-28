# FinQwerty

Various keyboard layouts for the physical QWERTY keyboards of the following Android phones:

- BlackBerry KEYone **Android 7.1 only** (Danish, Finnish, German, Norwegian, Swedish)
- BlackBerry Priv (Danish, Finnish, German, Norwegian, Swedish)
- F(x)tec Pro1 (Bulgarian, Czech, Danish, Finnish, German, Greek, Hungarian, Italian, Norwegian, Polish, Portuguese, Slovakian, Swedish, Swiss French, Ukrainian, U.S., U.S. international)
- F(x)tec Pro1 X (Czech, Danish, Finnish, German, Greek, Hungarian, Norwegian, Portuguese, Swedish, Swiss French, U.S., U.S. international)
- Gemini PDA / Cosmo Communicator (Bulgarian, Finnish, Swedish)
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

Python 3 is required to build FinQwerty.

The project uses Gradle and can be built with Android Studio or via commandline, for example:

```
export JAVA_HOME="$HOME/android-studio/jre"
export ANDROID_HOME="$HOME/Android/Sdk"
./gradlew assembleDebug
```

## Layout files

Some of the Pro1 layouts (e.g. fin/nor/swe, cze qwerty) and all Pro1 X QWERTZ layouts are generated from other layouts automatically by `generate_layouts.py`
during the build process and are therefore not found in this repository.

For convenience, all the `.kcm` files, including automatically generated ones, from the latest FinQwerty release can be found here:
https://android.onse.fi/finqwerty/kcm/

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

