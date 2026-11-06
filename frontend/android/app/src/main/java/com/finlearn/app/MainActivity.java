package com.finlearn.app;

import android.graphics.Color;
import android.os.Bundle;
import android.view.View;

import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Strip the "wv" WebView flag from the user agent.
        // Google blocks OAuth when it detects the wv flag (since 2021).
        // Removing it makes Google treat this WebView like a regular Chrome browser.
        String ua = getBridge().getWebView().getSettings().getUserAgentString();
        getBridge().getWebView().getSettings().setUserAgentString(ua.replace("; wv", ""));

        // Android 15+ draws apps edge to edge. Pad the content by the status bar, gesture bar and
        // keyboard so the header, bottom tabs and form fields are never hidden underneath them.
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        View root = findViewById(android.R.id.content);
        root.setBackgroundColor(Color.parseColor("#FAFAFA"));
        ViewCompat.setOnApplyWindowInsetsListener(root, (v, insets) -> {
            Insets bars = insets.getInsets(WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout());
            Insets ime = insets.getInsets(WindowInsetsCompat.Type.ime());
            v.setPadding(bars.left, bars.top, bars.right, Math.max(bars.bottom, ime.bottom));
            return WindowInsetsCompat.CONSUMED;
        });
        // The app background is light, so use dark status bar and navigation bar icons.
        WindowInsetsControllerCompat controller = WindowCompat.getInsetsController(getWindow(), root);
        controller.setAppearanceLightStatusBars(true);
        controller.setAppearanceLightNavigationBars(true);
    }
}
