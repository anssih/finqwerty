// SPDX-License-Identifier: Apache-2.0

package fi.onse.qwerty.finnish;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.hardware.input.InputManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.util.Pair;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.inputmethod.InputMethodInfo;
import android.view.inputmethod.InputMethodManager;
import android.view.inputmethod.InputMethodSubtype;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends Activity {

    /* support for opening the keyboard layout configuration directly via an intent */
    public static final int directModeMinSDK = 21;
    /* physical layout configuration setting is specific to each software input method */
    public static final int directModeMinImiSDK = 24;
    /* maximum SDK where opening the keyboard layout configuration directly (which is
     * not an official API) works */
    private static final int directModeMaxSDK = 27;
    /* separate physical keyboard settings activity (settings not directly in input
     * method settings) */
    private static final int semiModeHardKeybMinSDK = 24;

    private static final String CHANGELOG = "https://github.com/anssih/finqwerty/releases";
    private static final String WEBSITE = "https://android.onse.fi/finqwerty/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        /* TODO: this function is way too long and messy */
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final InputManager inputManager = (InputManager) getSystemService(INPUT_SERVICE);
        final InputMethodManager inputMethodManager = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);

        int[] devices = inputManager.getInputDeviceIds();
        List<FInputDevice> fdevices = new ArrayList<>();

        boolean hiddenDevices = false;
        boolean isPriv = false;

        for (int device : devices) {
            FInputDevice cand = new FInputDevice(this, inputManager, device);
            if (cand.confidence >= 2) {
                hiddenDevices = hiddenDevices || cand.knownHidden;
                isPriv = isPriv || cand.isPriv;
                fdevices.add(cand);
            }
        }

        boolean found = !fdevices.isEmpty();

        /*
         * direct mode: button(s) to open keyboard layout configuration directly
         * semi mode: button to open keyboard settings activity
         */

        View directLayout = findViewById(R.id.directLayout);
        View semiLayout = findViewById(R.id.semiLayout);
        View hideLayout = findViewById(R.id.hideLayout);
        View privLayout = findViewById(R.id.privLayout);
        View privLayout2 = findViewById(R.id.privLayout2);
        TextView hideHelpView = (TextView)findViewById(R.id.hide_help_view);
        TextView belowHelpSemi = (TextView)findViewById(R.id.configure_help_below1);
        TextView belowHelpDirect = (TextView)findViewById(R.id.configure_help_below2);

        TextView semiHelp = (TextView)findViewById(R.id.textViewsemi);
        Button inpsetbut = (Button)findViewById(R.id.LangInputSettings);

        TextView mainTextView = (TextView)findViewById(R.id.mainText);
        mainTextView.setMovementMethod(LinkMovementMethod.getInstance());
        mainTextView.setText(Html.fromHtml(String.format(getText(R.string.main_text).toString(), WEBSITE)));

        boolean directMode = Build.VERSION.SDK_INT >= directModeMinSDK && Build.VERSION.SDK_INT <= directModeMaxSDK;

        // directMode = false;

        if (directMode) {

            final List<Pair<String /* name */, Intent /*intent*/>> configureIntents = new ArrayList<>();

            for (final FInputDevice fdev : fdevices) {

                if (Build.VERSION.SDK_INT >= directModeMinImiSDK) {
                    /* we need to loop through IMs now as well */
                    final List<Pair<InputMethodInfo, InputMethodSubtype>> imCombos = new ArrayList<>();
                    for (InputMethodInfo imi : inputMethodManager.getEnabledInputMethodList()) {
                        final List<InputMethodSubtype> imsList = inputMethodManager.getEnabledInputMethodSubtypeList(imi, true);

                        if (imsList.isEmpty()) {
                            imCombos.add(new Pair<>(imi, null));
                        } else {
                            for (InputMethodSubtype ims : imsList) {
                                if (ims.getMode().equalsIgnoreCase("keyboard")) {
                                    imCombos.add(new Pair<>(imi, ims));
                                }
                            }
                        }
                    }

                    for (Pair<InputMethodInfo, InputMethodSubtype> combo : imCombos) {
                        final Intent intent = new Intent(Intent.ACTION_MAIN);
                        intent.setClassName("com.android.settings", "com.android.settings.Settings$KeyboardLayoutPickerActivity");
                        intent.putExtra("input_device_identifier", fdev.getIdentifier());
                        intent.putExtra("input_method_info", combo.first);
                        intent.putExtra("input_method_subtype", combo.second);
                        CharSequence vkbName = combo.first.loadLabel(getPackageManager());
                        if (combo.second != null) {
                            vkbName = vkbName + " - " + combo.second.getDisplayName(this, combo.first.getPackageName(), combo.first.getServiceInfo().applicationInfo);

                        }
                        final String buttontext = String.format(getText(R.string.configure_button_text_direct_imi).toString(), fdev.displayName, vkbName);
                        configureIntents.add(new Pair<>(buttontext, intent));
                    }


                } else {
                    /* pre-24 */
                    final String buttontext = String.format(getText(R.string.configure_button_text_direct).toString(), fdev.displayName);
                    final Intent intent = new Intent(Settings.ACTION_INPUT_METHOD_SETTINGS);
                    intent.putExtra("input_device_identifier", fdev.getIdentifier());
                    configureIntents.add(new Pair<>(buttontext, intent));
                }
            }


            LinearLayout confButtonsLayout = (LinearLayout) findViewById(R.id.keybuttons);
            LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);

            for (final Pair<String, Intent> configureIntent : configureIntents) {
                Button bt = new Button(this);
                bt.setLayoutParams(params);
                bt.setText(configureIntent.first);
                bt.setOnClickListener(v -> startActivity(configureIntent.second));

                confButtonsLayout.addView(bt);
            }

            directLayout.setVisibility(View.VISIBLE);
            semiLayout.setVisibility(View.GONE);
            hideHelpView.setText(R.string.hide_help_direct);

            if (!found) {
                /* no devices found, alter help text */
                TextView directHelpView = (TextView)findViewById(R.id.configure_help_textview_direct);
                directHelpView.setText(R.string.configure_help_fail);
            }

            if (hiddenDevices || !found) {
                /* devices not configurable via Android Settings or no devices found,
                 * do not allow hiding launcher icon */
                hideLayout.setVisibility(View.GONE);
                /* remove now useless help text */
                belowHelpDirect.setVisibility(View.GONE);
            }


        } else {
            final Intent semiIntent;
            if (Build.VERSION.SDK_INT >= semiModeHardKeybMinSDK) {
                semiIntent = new Intent(Settings.ACTION_HARD_KEYBOARD_SETTINGS);
            } else {
                semiIntent = new Intent(Settings.ACTION_INPUT_METHOD_SETTINGS);
            }
            inpsetbut.setOnClickListener(v -> startActivity(semiIntent));

            directLayout.setVisibility(View.GONE);
            semiLayout.setVisibility(View.VISIBLE);
            hideHelpView.setText(R.string.hide_help_semi);
        }

        if (Build.VERSION.SDK_INT >= directModeMinImiSDK) {
            /* the layout selection dialog is different (and simpler),
             * switch instructions */
            belowHelpDirect.setText(R.string.configure_help_below_imi);
            belowHelpSemi.setText(R.string.configure_help_below_imi);
            semiHelp.setText(R.string.configure_help_semi_imi);
            inpsetbut.setText(R.string.configure_button_text_semi_imi);
        }

        Button hideSwitch = (Button)findViewById(R.id.hideSwitch);
        hideSwitch.setEnabled(isLauncherIconEnabled());
        hideSwitch.setOnClickListener(v -> {
            setLauncherIconEnabled(false);
            Toast.makeText(MainActivity.this, "Removing FinQwerty from launcher", Toast.LENGTH_LONG).show();
            finish();
        });

        if (isPriv) {
            privLayout.setVisibility(View.VISIBLE);
            privLayout2.setVisibility(View.VISIBLE);

            Switch bootSwitch = (Switch)findViewById(R.id.bootSwitch);
            bootSwitch.setChecked(isBootNotificationEnabled());
            bootSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> setBootNotificationEnabled(isChecked));

            if (Build.VERSION.SDK_INT >= 24) {
                /* e.g. BlackBerry KEYone or KEY2 */
                TextView directHelpView = (TextView)findViewById(R.id.configure_help_textview_direct);
                final String keyOneMessage = String.format("<span style=\"color: #ff0000;\">%s</span><br><a href=\"%s\">%s</a><br>",
                        getText(R.string.configure_help_keyone).toString(),
                        getText(R.string.configure_help_keyone_url).toString(),
                        getText(R.string.more_information).toString());
                directHelpView.setText(Html.fromHtml(keyOneMessage, 0));
                directHelpView.setTextSize(19);
                directHelpView.setMovementMethod(LinkMovementMethod.getInstance());
            }

        } else {
            privLayout.setVisibility(View.GONE);
            privLayout2.setVisibility(View.GONE);
        }

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int itemId = item.getItemId();
        if (itemId == R.id.action_changelog) {
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(CHANGELOG)));
            return true;
        } else if (itemId == R.id.action_website) {
            startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(WEBSITE)));
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private boolean isBootNotificationEnabled() {
        PackageManager p = getPackageManager();
        ComponentName ourName = new ComponentName(this, PrivBootupNotification.class);
        return p.getComponentEnabledSetting(ourName) == PackageManager.COMPONENT_ENABLED_STATE_ENABLED;
    }
    private void setBootNotificationEnabled(boolean enable) {
        PackageManager p = getPackageManager();
        ComponentName ourName = new ComponentName(this, PrivBootupNotification.class);
        p.setComponentEnabledSetting(ourName, enable ? PackageManager.COMPONENT_ENABLED_STATE_ENABLED : PackageManager.COMPONENT_ENABLED_STATE_DISABLED, PackageManager.DONT_KILL_APP);
    }

    private boolean isLauncherIconEnabled() {
        PackageManager p = getPackageManager();
        ComponentName ourName = new ComponentName(this, this.getClass());
        return p.getComponentEnabledSetting(ourName) != PackageManager.COMPONENT_ENABLED_STATE_DISABLED;
    }
    @SuppressWarnings("SameParameterValue")
    private void setLauncherIconEnabled(boolean enable) {
        PackageManager p = getPackageManager();
        ComponentName ourName = new ComponentName(this, this.getClass());
        p.setComponentEnabledSetting(ourName, enable ? PackageManager.COMPONENT_ENABLED_STATE_DEFAULT : PackageManager.COMPONENT_ENABLED_STATE_DISABLED, PackageManager.DONT_KILL_APP);
    }

}
