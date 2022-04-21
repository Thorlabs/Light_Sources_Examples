using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Thorlabs.MotionControl.DeviceManagerCLI;
using Thorlabs.MotionControl.KCube.LaserSourceCLI;

namespace Initialize_and_Enable
{
    internal class Program
    {
        static void Main(string[] args)
        {
            //Try building the device list. Close if this fails
            try
            {
                DeviceManagerCLI.BuildDeviceList();
            }
            catch (Exception)
            {
                Console.WriteLine("Device list failed to build");
                return;
            }

            //Get all available devices that are KLS controllers. These are identified by the first 2 digits of the serial number. 
            List<string> serialNumbers = DeviceManagerCLI.GetDeviceList(56);

            //Close if no KLS devices are connected. 
            if (serialNumbers.Count > 0)
            {
                Console.WriteLine(serialNumbers[0]);
            }
            else
            {
                Console.WriteLine("No connected devices");
                return;
            }

            //Connect to the first available KLS
            KCubeLaserSource kls = KCubeLaserSource.CreateKCubeLaserSource(serialNumbers[0]);

            //Check if created device is null
            if (kls != null)
            {
                kls.Connect(serialNumbers[0]);
                kls.WaitForSettingsInitialized(5000);
                kls.StartPolling(100);
                Thread.Sleep(500);

                // Call GetLaserSourceConfiguration on the device to initialize the settings
                LaserSourceConfiguration laserSourceConfiguration = kls.GetLaserSourceConfiguration(serialNumbers[0]);

                //Set control mode
                kls.SetControlSource(InputSourceSettings.LaserSourceInputSourceFlags.SoftwareOnly);

                //Get the current and power limits for the laser
                LaserLimits klsLimits = kls.GetLimits();
                Console.WriteLine("Laser Max Power: {0}", klsLimits.MaxPower);
                Console.WriteLine("Laser Max Current: {0}", klsLimits.MaxCurrent);

                //Set the power to 10% of max
                kls.SetPower(klsLimits.MaxPower*.1M);

                //Turn the laser on for 5 seconds the disconnect
                kls.SetOn();
                Thread.Sleep(5000);
                kls.SetOff();
                kls.StopPolling();
                kls.Disconnect(false);
            }
            else { Console.WriteLine("Error ocurred with device creation"); }

            Console.WriteLine("Press any key to continue");
            Console.ReadKey();
        }
    }
}
