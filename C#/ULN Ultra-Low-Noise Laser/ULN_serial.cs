// Title: ULN_serial.cs
// Created Date: 2025-09-22
// Last modified date: 2026-03-23
//
// Notes:
// Example for the ULN lasers using serial commands. Sets TEC mode to auto
// and briefly turns laser on.
//


using System;
using System.IO.Ports;
using System.Threading;

class ULN
{
    const string PORT = "COM3";
    const int BAUD = 115200;
    const int TIMEOUT = 5000;

    static void Main()
    {
        using var port = new SerialPort(PORT, BAUD, Parity.None, 8, StopBits.One)
        {
            NewLine = "\r\n",
            ReadTimeout = TIMEOUT,
            WriteTimeout = TIMEOUT
        };

        port.Open();

        SendCmd(port, "nop");
        Thread.Sleep(500);

        SendCmd(port, "laser_tec_ctrl_mode auto");
        Thread.Sleep(500);

        SendCmd(port, "laser on");
        Thread.Sleep(3000);

        SendCmd(port, "laser off");
        Thread.Sleep(500);

        Console.WriteLine("Done - port closed.");
    }

    // Send command parse response
    static void SendCmd(SerialPort port, string cmd)
    {
        port.WriteLine(cmd);

        // Parse return code E.G. 000: OK:response, etc.
        string raw = port.ReadLine(); 
        string[] parts = raw.Split(':', 2);
        string code = parts[0].Trim();
        string text = parts.Length > 1 ? parts[1] : "";

        if (code == "000")
            Console.WriteLine($"[OK]  {cmd,-20} - {text}");
        else
            Console.WriteLine($"[ERR] {cmd,-20} - {code}: {text}");
    }
}
