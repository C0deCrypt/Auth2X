package com.ramlah.fingerprintconnection;
import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.biometric.BiometricManager;
import androidx.biometric.BiometricPrompt;
import androidx.core.content.ContextCompat;

import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import java.util.concurrent.Executor;


public class MainActivity extends AppCompatActivity {

    private TextView statusText;
    private Button authButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        authButton = findViewById(R.id.authButton);

        BiometricManager biometricManager = BiometricManager.from(this);
        switch (biometricManager.canAuthenticate(BiometricManager.Authenticators.BIOMETRIC_STRONG)) {
            case BiometricManager.BIOMETRIC_SUCCESS:
                statusText.setText("You can use fingerprint to login.");
                break;
            case BiometricManager.BIOMETRIC_ERROR_NO_HARDWARE:
                statusText.setText("The device doesn't have fingerprint hardware.");
                break;
            case BiometricManager.BIOMETRIC_ERROR_HW_UNAVAILABLE:
                statusText.setText("Fingerprint hardware is currently unavailable.");
                break;
            case BiometricManager.BIOMETRIC_ERROR_NONE_ENROLLED:
                statusText.setText("No fingerprint enrolled. Please check settings.");
                break;
        }

        Executor executor = ContextCompat.getMainExecutor(this);
        BiometricPrompt biometricPrompt = new BiometricPrompt(MainActivity.this, executor, new BiometricPrompt.AuthenticationCallback() {
            @Override
            public void onAuthenticationSucceeded(BiometricPrompt.AuthenticationResult result) {
                super.onAuthenticationSucceeded(result);
                runOnUiThread(() -> {
                    statusText.setText("Authentication successful!");
                    Toast.makeText(MainActivity.this, "Fingerprint matched!", Toast.LENGTH_SHORT).show();
                });
            }

            @Override
            public void onAuthenticationError(int errorCode, CharSequence errString) {
                super.onAuthenticationError(errorCode, errString);
                runOnUiThread(() -> {
                    statusText.setText("Authentication error: " + errString);
                });
            }

            @Override
            public void onAuthenticationFailed() {
                super.onAuthenticationFailed();
                runOnUiThread(() -> {
                    statusText.setText("Authentication failed. Try again.");
                });
            }
        });

        BiometricPrompt.PromptInfo promptInfo = new BiometricPrompt.PromptInfo.Builder()
                .setTitle("Fingerprint Login")
                .setSubtitle("Authenticate with your fingerprint")
                .setNegativeButtonText("Cancel")
                .build();

        authButton.setOnClickListener(view -> biometricPrompt.authenticate(promptInfo));
    }
}
