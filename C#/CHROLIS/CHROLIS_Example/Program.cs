using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Thorlabs.TL6WL_64.Interop;

namespace CHROLIS_Example
{
    class Program
    {
        static void Main(string[] args)
        {
            TL6WL chrolis = new TL6WL(IntPtr.Zero);

            uint numAvailableDevices = 0;
            chrolis.findRsrc(out numAvailableDevices);

            if (numAvailableDevices == 0)
            {
                Console.WriteLine("No devices found, closing app...");
                return;
            }

            Console.WriteLine("{0} device(s) found, connecting to first available...");

            StringBuilder resourceString = new StringBuilder(256);
            chrolis.getRsrcName(0, resourceString);

            chrolis = new TL6WL(resourceString.ToString(), false, false);

            //Change these array values to adjust state of the source
            //Brightness values are from 0-1000 for percentage of max brightness
            bool[] ledEnableStates = { false, false, true, false, false, false };
            short[] ledBrightnessVals = { 0, 0, 500, 0, 0, 0};

            Console.WriteLine("Press Enter to enable the source");
            while (Console.ReadKey().Key != ConsoleKey.Enter)
            { }

            //Set the states of the led's from arrays
            chrolis.setLED_HeadPowerStates(ledEnableStates[0], ledEnableStates[1], ledEnableStates[2], ledEnableStates[3], ledEnableStates[4], ledEnableStates[5]);
            chrolis.setLED_HeadBrightness(ledBrightnessVals[0], ledBrightnessVals[1], ledBrightnessVals[2], ledBrightnessVals[3], ledBrightnessVals[4], ledBrightnessVals[5]);

            Console.WriteLine("Press Enter to disable the source");
            while (Console.ReadKey().Key != ConsoleKey.Enter)
            { }

            //disable led's
            chrolis.setLED_HeadPowerStates(false, false, false, false, false, false);

            chrolis.Dispose();
            Console.WriteLine("Device closed. Press any key to exit...");
            Console.ReadKey();
        }
    }
}
