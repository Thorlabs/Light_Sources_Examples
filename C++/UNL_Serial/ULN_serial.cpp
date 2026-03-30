// Title: ULN_serial.cpp
// Created Date: 2025-09-24
// Last modified date: 2026-03-24
// Visual Studio 2022, C++ 14
// 
// Notes:
// Example for the ULN lasers using serial commands. Sets TEC mode to auto
// and briefly turns laser on.
//

#include <windows.h>
#include <stdio.h>
#include <string.h>

#define PORT "COM3"
#define BAUD CBR_115200

HANDLE openPort(const char* port)
{
    char path[32];
    snprintf(path, sizeof(path), "\\\\.\\%s", port);

    HANDLE h = CreateFileA(path, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (h == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Failed to open %s (error %lu)\n", port, GetLastError());
        return INVALID_HANDLE_VALUE;
    }

    DCB dcb;
    memset(&dcb, 0, sizeof(DCB));
    dcb.DCBlength = sizeof(DCB);
    GetCommState(h, &dcb);
    dcb.BaudRate = BAUD;
    dcb.ByteSize = 8;
    dcb.Parity = NOPARITY;
    dcb.StopBits = ONESTOPBIT;
    SetCommState(h, &dcb);

    COMMTIMEOUTS to = { 0 };
    SetCommTimeouts(h, &to);

    return h;
}

int readLine(HANDLE h, char* buf, int bufLen)
{
    int pos = 0;
    while (pos < bufLen - 1) {
        char c;
        DWORD n;
        if (!ReadFile(h, &c, 1, &n, NULL) || n == 0) break;
        if (c == '\n') break;
        buf[pos++] = c;
    }
    // Strip \r
    if (pos > 0 && buf[pos - 1] == '\r') pos--;
    buf[pos] = '\0';
    return pos;
}

// Send command parse response
void sendCmd(HANDLE h, const char* cmd)
{
    char line[256];
    int  len = snprintf(line, sizeof(line), "%s\r\n", cmd);
    DWORD written;
    WriteFile(h, line, len, &written, NULL);

    char resp[256];
    readLine(h, resp, sizeof(resp));

    // Parse return code E.G. 000: OK:response, etc.
    char* colon = strchr(resp, ':');
    if (colon) {
        *colon = '\0';
        const char* code = resp;
        const char* text = colon + 1;

        if (strcmp(code, "000") == 0)
            printf("OK  %-20s - %s\n", cmd, text);
        else
            printf("ERR %-20s - %s: %s\n", cmd, code, text);
    } else {
        printf("??? %-20s - %s\n", cmd, resp);
    }
}

int main(void)
{
    HANDLE h = openPort(PORT);
    if (h == INVALID_HANDLE_VALUE) return 1;

    sendCmd(h, "nop");
    Sleep(500);

    sendCmd(h, "laser_tec_ctrl_mode auto");
    Sleep(500);

    sendCmd(h, "laser on");
    Sleep(3000);

    sendCmd(h, "laser off");
    Sleep(500);

    CloseHandle(h);
    puts("Done - port closed.");
    return 0;
}
