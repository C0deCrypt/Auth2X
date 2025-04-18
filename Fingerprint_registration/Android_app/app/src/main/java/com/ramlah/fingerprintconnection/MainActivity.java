package com.ramlah.fingerprintconnection;

import android.os.Bundle; import android.widget.Button; import android.widget.EditText; import android.widget.RadioButton; import android.widget.RadioGroup; import android.widget.TextView; import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity; import androidx.biometric.BiometricManager; import androidx.biometric.BiometricPrompt; import androidx.core.content.ContextCompat;

import java.io.OutputStream; import java.net.HttpURLConnection; import java.net.URL; import java.util.concurrent.Executor;

public class MainActivity extends AppCompatActivity {

    private TextView statusText;
    private TextView instructionText;
    private Button authButton;
    private RadioGroup modeGroup;
    private EditText usernameInput;

    private void sendAuthToServer() {
        new Thread(() -> {
            try {
                int selectedId = modeGroup.getCheckedRadioButtonId();
                String mode = (selectedId == R.id.registerRadio) ? "register" : "login";
                String username = usernameInput.getText().toString().trim();

                URL url = new URL("http://192.168.1.4:5000/fingerprint");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);

                String jsonInputString = String.format(
                        "{\"auth\": \"success\", \"mode\": \"%s\", \"user\": \"%s\"}",
                        mode, username);

                OutputStream os = conn.getOutputStream();
                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);
                os.flush();
                os.close();

                int responseCode = conn.getResponseCode();

                runOnUiThread(() ->
                        Toast.makeText(MainActivity.this, "Server response: " + responseCode, Toast.LENGTH_LONG).show()
                );

            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() ->
                        Toast.makeText(MainActivity.this, "Exception: " + e.getMessage(), Toast.LENGTH_LONG).show()
                );
            }
        }).start();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        statusText = findViewById(R.id.statusText);
        authButton = findViewById(R.id.authButton);
        modeGroup = findViewById(R.id.modeGroup);
        usernameInput = findViewById(R.id.usernameInput);
        instructionText = findViewById(R.id.instructionText);

        RadioButton registerRadio = findViewById(R.id.registerRadio);
        RadioButton loginRadio = findViewById(R.id.loginRadio);

        modeGroup.setOnCheckedChangeListener((group, checkedId) -> {
            if (checkedId == R.id.registerRadio) {
                instructionText.setText("Enter your username to register your fingerprint.");
            } else if (checkedId == R.id.loginRadio) {
                instructionText.setText("Enter your username to login with fingerprint.");
            }
        });

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
                    int selectedId = modeGroup.getCheckedRadioButtonId();
                    if (selectedId == R.id.registerRadio) {
                        Toast.makeText(MainActivity.this, "Fingerprint registered successfully!", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(MainActivity.this, "Login fingerprint verified!", Toast.LENGTH_SHORT).show();
                    }
                    sendAuthToServer();
                });
            }

            @Override
            public void onAuthenticationError(int errorCode, CharSequence errString) {
                super.onAuthenticationError(errorCode, errString);
                runOnUiThread(() ->
                        statusText.setText("Authentication error: " + errString)
                );
            }

            @Override
            public void onAuthenticationFailed() {
                super.onAuthenticationFailed();
                runOnUiThread(() ->
                        statusText.setText("Authentication failed. Try again.")
                );
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