using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO.Ports;
using System.Threading.Tasks;
using System.Threading;

namespace SPDC_Example
{
    internal class Program
    {
        static SerialPort spdc;
        static void Main(string[] args)
        {
            Console.WriteLine("Enter name of port to connect (e.g. COM3): ");
            String portName = Console.ReadLine().Trim();
            InitPort(portName);

            string id;
            GetSPDCID(out id);
            Console.WriteLine("SPDC ID: " + id);

            double[] limits;
            GetCurrentLimits(out limits);
            Console.WriteLine("Warning Limit: " + limits[0]);

            SetPumpPower(50); //Pump power in mW

            EnableSource();
            Thread.Sleep(5000);
            DisableSource();

            //Close the port
            spdc.Close();
            Console.WriteLine("Press Any Key to Exit");
            Console.ReadKey();
        }

        static int GetSPDCID(out string id)
        {
            string response = SendCommand("id\r");
            if (response.Equals("WRITE_ERROR") || response.Equals("READ_ERROR"))
            {
                id = "ERROR";
                return 1;
            }
            else {
                id = response;
                return 0;
            }
        }

        static int GetCurrentLimits(out double[] limits)
        {
            string response = SendCommand("sh limit\r");
            if (response.Equals("WRITE_ERROR") || response.Equals("READ_ERROR"))
            {
                limits = new double[]{0,0,0,0};
                return 1;
            }
            else
            {
                string[] segments = response.Split('\n');
                limits = new double[] {
                    Double.Parse(segments[0].Substring(segments[0].IndexOf(":") + 1, segments[0].IndexOf(" ") - segments[0].IndexOf(":"))),
                    Double.Parse(segments[0].Substring(segments[1].IndexOf(":") + 1, segments[1].IndexOf(" ") - segments[1].IndexOf(":"))),
                    Double.Parse(segments[0].Substring(segments[2].IndexOf(":") + 1, segments[2].IndexOf(" ") - segments[2].IndexOf(":"))),
                    Double.Parse(segments[0].Substring(segments[3].IndexOf(":") + 1, segments[3].IndexOf(" ") - segments[3].IndexOf(":")))
                };

                return 0;
            }
        }

        static int SetPumpPower(double power)
        {
            string response = SendCommand("ch 1 pow " + power.ToString() + "\r");
            if (response.Equals("WRITE_ERROR") || response.Equals("READ_ERROR"))
            {
                return 1;
            }
            else
            {
                return 0;
            }
        }

        static int EnableSource()
        {
            //Enable the driver and laser control
            string response = SendCommand("la on\r");
            response += SendCommand("en 1\r");
            if (response.Contains("WRITE_ERROR") || response.Contains("READ_ERROR"))
            {
                return 1;
            }
            else
            {
                return 0;
            }
        }

        static int DisableSource()
        {
            string response = SendCommand("la off\r");
            if (response.Equals("WRITE_ERROR") || response.Equals("READ_ERROR"))
            {
                return 1;
            }
            else
            {
                return 0;
            }
        }

        static string SendCommand(string command)
        {
            string response = "";
            try
            {
                spdc.Write(command);
            }
            catch (Exception ex)
            {
                return "WRITE_ERROR";
            }
            long startTime = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            long endTime = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            while (!response.Contains("CMD>"))
            {
                try
                {
                    response += spdc.ReadExisting();
                }
                catch (Exception)
                { }
                if (endTime - startTime > 2000)
                {
                    response = "READ_ERROR";
                    break;
                }
                endTime = DateTimeOffset.Now.ToUnixTimeMilliseconds();
            }

            string[] segments = response.Split('\n');

            string commandReturn = "";
            if (segments.Length >= 3) //response has a return echo + val + cmd>
            { 
                //The return from the spdc is split by CRLF. The requested data will be everything in betweem
                //the echo and the cmd> return
                for(int i = 1; i < segments.Length-1; i++)
                {
                    commandReturn += segments[i].Remove('\r'); // Remove carriage returns to clean output
                    if (segments.Length > 3 && i < segments.Length - 2)// only add if there are multiple lines
                    { commandReturn += '\n'; } // add a new line to make parsing easier on 
                }
            }
            else if (segments.Length == 2)//No response from controller. return is echo + cmd>
            { }
            else { commandReturn = response; }// error. return message in response string

            return commandReturn;
        }

        static void InitPort(string portName)
        {
            spdc = new SerialPort();
            spdc.PortName = portName;
            spdc.DataBits = 8;
            spdc.StopBits = StopBits.One;
            spdc.BaudRate = 115200;
            spdc.Parity = Parity.None;
            spdc.Handshake = Handshake.XOnXOff;
            spdc.ReadTimeout = 1000;
            spdc.WriteTimeout = 500;
            spdc.RtsEnable = true;
            spdc.NewLine = "\n"; //Returns from the spdc are ended with a carriage return character
            spdc.Open();
        }
    }
}
