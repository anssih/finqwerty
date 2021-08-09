// SPDX-License-Identifier: Apache-2.0

package fi.onse.qwerty.finnish;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.res.Resources;
import android.hardware.input.InputManager;
import android.os.Build;
import android.os.Parcelable;
import android.util.Log;
import android.view.InputDevice;

import java.lang.reflect.Constructor;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static android.view.InputDevice.KEYBOARD_TYPE_ALPHABETIC;

class FInputDevice {

    private static final String TAG = "FInputDevice";

    private Map<String, String> niceNames;

    private void initNiceNames(Context context) {
        Resources res = context.getResources();
        niceNames = new HashMap<>();
        niceNames.put("stmpe_keypad", res.getText(R.string.device_name_priv_qwerty).toString());
        niceNames.put("stmpe_azerty_keypad", res.getText(R.string.device_name_priv_azerty).toString());
        niceNames.put("stmpe_qwertz_keypad", res.getText(R.string.device_name_priv_qwertz).toString());
    }

    // devices that have been confirmed configurable via Android Settings
    private static final List<String> visibleDevices = Arrays.asList("keypad_8960", "omap4-keypad", "sec_keypad");
    // devices that have been confirmed not configurable via Android Settings
    private static final List<String> hiddenDevices = Arrays.asList("stmpe_keypad", "stmpe_azerty_keypad", "stmpe_qwertz_keypad");
    // devices that lose layout settings on reboot
    private static final List<String> privDevices = Arrays.asList("stmpe_keypad", "stmpe_azerty_keypad", "stmpe_qwertz_keypad");

    FInputDevice(Context context, InputManager inputManager, int deviceId) {
        initNiceNames(context);

        InputDevice idev = inputManager.getInputDevice(deviceId);

        String name = idev.getName();
        displayName = name;
        descriptor = idev.getDescriptor();
        confidence = 0;
        knownVisible = false;
        knownHidden = false;
        vendorId = 0;
        productId = 0;
        isPriv = false;
        if (Build.VERSION.SDK_INT >= 19) {
            vendorId = idev.getVendorId();
            productId = idev.getProductId();
        }

        int keybType = idev.getKeyboardType();
        boolean isVirtual = idev.isVirtual();

        if (keybType == KEYBOARD_TYPE_ALPHABETIC && !isVirtual) {
            confidence = 3;
        }
        else if (keybType == KEYBOARD_TYPE_ALPHABETIC && niceNames.containsKey(name)) {
            confidence = 3;
        }

        if (niceNames.containsKey(name)) {
            displayName = niceNames.get(name);
        }

        knownVisible = visibleDevices.contains(name);
        knownHidden = hiddenDevices.contains(name);
        isPriv = privDevices.contains(name);
    }

    public Parcelable getIdentifier() {
        try {
            /*
             * Find the class via reflection to avoid non-SDK interface warning on Android 9
             * unless this function is *actually* called (and it is not actually called).
             */
            @SuppressLint("PrivateApi")
            Class<?> idicls = Class.forName("android.hardware.input.InputDeviceIdentifier");
            Constructor<?> idictr = idicls.getDeclaredConstructor(String.class, int.class, int.class);
            return (Parcelable)idictr.newInstance(descriptor, vendorId, productId);

        } catch (Exception e) {
            // TODO handle exceptions properly
            Log.e(TAG, "Exception: " + e.toString());
            return null;
        }
    }

    String displayName;
    String descriptor;
    int confidence;
    boolean knownVisible;
    boolean knownHidden;
    boolean isPriv;
    private int vendorId;
    private int productId;
}
