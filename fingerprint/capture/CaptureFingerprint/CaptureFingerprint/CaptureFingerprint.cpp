#include <iostream>
#include <fstream>
#include <windows.h>
#include "sgfplib.h"

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: capture_fingerprint <username>" << endl;
        return 1;
    }

    string username = argv[1];
    string filePath = "../fingerprints/" + username + ".dat";

    HSGFPM hFPM;
    DWORD err = SGFPM_Create(&hFPM);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "Error: SGFPM_Create failed. Code: " << err << endl;
        return 1;
    }

    err = SGFPM_Init(hFPM, SG_DEV_AUTO);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "Error: SGFPM_Init failed. Code: " << err << endl;
        return 1;
    }

    SGDeviceInfoParam deviceInfo;
    memset(&deviceInfo, 0, sizeof(deviceInfo));
    err = SGFPM_GetDeviceInfo(hFPM, &deviceInfo);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "Error: SGFPM_GetDeviceInfo failed. Code: " << err << endl;
        return 1;
    }

    int imgWidth = deviceInfo.ImageWidth;
    int imgHeight = deviceInfo.ImageHeight;
    BYTE* imageBuffer = new BYTE[imgWidth * imgHeight];

    cout << "Place your finger on the scanner..." << endl;
    Sleep(2000);  // Let the user place the finger

    err = SGFPM_GetImage(hFPM, imageBuffer);
    if (err != SGFDX_ERROR_NONE) {
        cerr << "Error: SGFPM_GetImage failed. Code: " << err << endl;
        delete[] imageBuffer;
        return 1;
    }

    ofstream out(filePath, ios::binary);
    if (!out) {
        cerr << "Error: Cannot open file " << filePath << " for writing." << endl;
        delete[] imageBuffer;
        return 1;
    }

    out.write(reinterpret_cast<char*>(imageBuffer), imgWidth * imgHeight);
    out.close();

    cout << "Fingerprint captured and saved to " << filePath << endl;

    delete[] imageBuffer;
    SGFPM_Terminate(hFPM);  // Free the SGFPM object

    return 0;
}
