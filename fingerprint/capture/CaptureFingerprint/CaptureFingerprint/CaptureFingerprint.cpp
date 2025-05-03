#include <iostream>
#include <fstream>
#include <windows.h>
#include <direct.h>   // for _mkdir
#include <cerrno>     // for errno
#include "sgfplib.h"

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: capture_fingerprint <username>" << endl;
        return 1;
    }

    string username = argv[1];
    string dirPath = "D:/repo/Auth2X/fingerprint/fingerprints";
    string filePath = dirPath + "/" + username + ".dat";

    // ✅ Create folder if not exists
    if (_mkdir(dirPath.c_str()) != 0 && errno != EEXIST) {
        cerr << "[ERROR] Failed to create directory: " << dirPath << endl;
        return 1;
    }

    HSGFPM hFPM;
    DWORD err = SGFPM_Create(&hFPM);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "[ERROR] SGFPM_Create failed. Code: " << err << endl;
        return 1;
    }

    err = SGFPM_Init(hFPM, SG_DEV_AUTO);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "[ERROR] SGFPM_Init failed. Code: " << err << endl;
        return 1;
    }

    // ✅ Use correct device ID (based on SGDemo) — or try SG_DEV_AUTO
    err = SGFPM_OpenDevice(hFPM, SG_DEV_AUTO);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "[ERROR] SGFPM_OpenDevice failed. Code: " << err << endl;
        SGFPM_Terminate(hFPM);
        return 1;
    }

    SGDeviceInfoParam deviceInfo;
    memset(&deviceInfo, 0, sizeof(deviceInfo));
    err = SGFPM_GetDeviceInfo(hFPM, &deviceInfo);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "[ERROR] SGFPM_GetDeviceInfo failed. Code: " << err << endl;
        SGFPM_CloseDevice(hFPM);
        SGFPM_Terminate(hFPM);
        return 1;
    }

    int imgWidth = deviceInfo.ImageWidth;
    int imgHeight = deviceInfo.ImageHeight;
    BYTE* imageBuffer = new BYTE[imgWidth * imgHeight];

    cout << "[INFO] Image size: " << imgWidth << " x " << imgHeight
        << " = " << imgWidth * imgHeight << " bytes" << endl;

    cout << "[ACTION] Place your finger on the scanner..." << endl;

    // ✅ Optional: Turn LED on before capture
    SGFPM_SetLedOn(hFPM, TRUE);

    DWORD timeout_ms = 30000;  // ⏱ 30 seconds
    err = SGFPM_GetImageEx(hFPM, imageBuffer, timeout_ms, NULL);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "[ERROR] SGFPM_GetImageEx failed. Code: " << err << endl;
        delete[] imageBuffer;
        SGFPM_CloseDevice(hFPM);
        SGFPM_Terminate(hFPM);
        return 1;
    }

    ofstream out(filePath, ios::binary);
    if (!out) {
        cerr << "[ERROR] Cannot open file " << filePath << " for writing." << endl;
        delete[] imageBuffer;
        SGFPM_CloseDevice(hFPM);
        SGFPM_Terminate(hFPM);
        return 1;
    }

    out.write(reinterpret_cast<char*>(imageBuffer), imgWidth * imgHeight);
    out.close();

    cout << "[SUCCESS] Fingerprint captured and saved to " << filePath << endl;

    delete[] imageBuffer;
    SGFPM_CloseDevice(hFPM);
    SGFPM_Terminate(hFPM);
    return 0;
}
