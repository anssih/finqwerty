// SPDX-License-Identifier: Apache-2.0

package fi.onse.qwerty.finnish;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.hardware.input.InputManager;
import android.os.Build;
import android.provider.Settings;

import java.util.ArrayList;
import java.util.List;

import static fi.onse.qwerty.finnish.MainActivity.directModeMinImiSDK;

public class PrivBootupNotification extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {

        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.LOLLIPOP || Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            /* should not get here on non-Priv */
            return;
        }

        if (!Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())) {
            return;
        }

        /* TODO: duplicates MainActivity.java */
        InputManager inputManager = (InputManager) context.getSystemService(Context.INPUT_SERVICE);

        int[] devices = inputManager.getInputDeviceIds();
        List<FInputDevice> fdevices = new ArrayList<>();

        boolean isPriv = false;

        for (int device : devices) {
            FInputDevice cand = new FInputDevice(context, inputManager, device);
            if (cand.confidence >= 2) {
                isPriv = isPriv || cand.isPriv;
                fdevices.add(cand);
            }
        }

        if (isPriv && !fdevices.isEmpty()) {
            /* TODO: duplicates MainActivity.java */
            final Intent confIntent;
            if (Build.VERSION.SDK_INT < directModeMinImiSDK) {
                /* go directly to settings dialog, we know everything */
                confIntent = new Intent(Settings.ACTION_INPUT_METHOD_SETTINGS);
                confIntent.putExtra("input_device_identifier", fdevices.get(0).getIdentifier());
            } else {
                /* TODO: maybe go directly to settings if only a single input method is enabled? */
                confIntent = new Intent(context, MainActivity.class);
            }

            final PendingIntent pendIntent = PendingIntent.getActivity(
                    context, 0,confIntent,
                    Build.VERSION.SDK_INT >= 23 ? PendingIntent.FLAG_IMMUTABLE : 0);

            Notification.Builder mBuilder =
                    new Notification.Builder(context)
                            .setSmallIcon(Build.VERSION.SDK_INT >= 24 ? R.drawable.silhouette24 : R.drawable.silhouette)
                            .setColor(Color.rgb(0, 53, 128))
                            .setContentIntent(pendIntent)
                            .setAutoCancel(true)
                            .setContentTitle(context.getString(R.string.layout_boot_notification_title))
                            .setContentText(context.getString(R.string.layout_boot_notification_text));

            NotificationManager mNotificationManager =
                    (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
            mNotificationManager.notify(0, mBuilder.build());
        }

    }
}
