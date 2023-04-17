using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO.Ports;
using System.Threading.Tasks;

namespace Benchtop_Laser_Diode_Example
{
    class Program
    {
        static SerialPort benchtopSource;

        static void Main(string[] args)
        {
            Console.WriteLine("Enter name of port to connect (e.g. COM3): ");
            String portName = Console.ReadLine().Trim();

            benchtopSource = new SerialPort();
            benchtopSource.PortName = portName;
            benchtopSource.DataBits = 8;
            benchtopSource.StopBits = StopBits.One;
            benchtopSource.BaudRate = 115200;
            benchtopSource.Parity = Parity.None;
            benchtopSource.Handshake = Handshake.None;
            benchtopSource.ReadTimeout = 1000;
            benchtopSource.WriteTimeout = 500;
            benchtopSource.RtsEnable = true;
            benchtopSource.NewLine = "\r"; //Returns from the benchtopSource are ended with a carriage return character
            benchtopSource.Open();

            //The "Enter" key needs to be sent to enable communication with the device. This is represented by a single carriage return
            benchtopSource.Write("\r");
            //The return from this character is ended differently than the others so a different method is used to read it out. This always prints "Command error CMD_NOT_DEFINED"
            WriteOutCharacters();

            //All commands will return an echo of the sent string before returning any other data. This is used to store that if needed
            string echo = "";

            //Read the ID of the port
            benchtopSource.Write("id?\r");
            echo = benchtopSource.ReadLine();
            Console.WriteLine("Device is a: " + benchtopSource.ReadLine());

            //Set the target temperature
            benchtopSource.Write("target=25\r");
            echo = benchtopSource.ReadLine();

            //Get the current temperature of the diode
            benchtopSource.Write("temp?\r");
            echo = benchtopSource.ReadLine();
            Console.WriteLine("Returned Temperature is: " + benchtopSource.ReadLine());

            //Set the diode current in mA
            benchtopSource.Write("current=100\r");
            echo = benchtopSource.ReadLine();

            //Wait for the enter key to enable the diode
            Console.WriteLine("Press Enter to enable the diode");
            while (Console.ReadKey().Key != ConsoleKey.Enter)
            { }

            //Enable the diode
            benchtopSource.Write("enable=1\r");
            echo = benchtopSource.ReadLine();

            //Wait for the enter key to disable the diode
            Console.WriteLine("Press Enter to disable the diode");
            while (Console.ReadKey().Key != ConsoleKey.Enter)
            { }

            //Disable the diode
            benchtopSource.Write("enable=0\r");
            echo = benchtopSource.ReadLine();

            //Close the port
            benchtopSource.Close();
            Console.WriteLine("Press Any Key to Exit");
            Console.ReadKey();
        }

        private static void WriteOutCharacters()
        {
            //Writes out all available characters until the buffer is empty. Characters are stored in a string to be read out at the end. 
            string output = "";
            bool bytesAvailable = true;
            while (bytesAvailable)
            {
                try
                {
                    char curChar = (char)benchtopSource.ReadChar();
                    //Ignore characters that would start or end the line 
                    if (curChar == '>' || curChar == '\n' || curChar == '\r')
                    { }
                    else
                    {
                        output += curChar;
                    }
                }
                catch (Exception)
                {
                    bytesAvailable = false;
                }
            }
            Console.WriteLine(output);
        }
    }
}
