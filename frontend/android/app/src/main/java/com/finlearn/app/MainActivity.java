package com.finlearn.app;

import android.os.Bundle;
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
    }
}
