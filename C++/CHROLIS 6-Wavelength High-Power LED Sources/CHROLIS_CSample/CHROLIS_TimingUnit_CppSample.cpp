// CHROLIS_CSample.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

/***
  * Additional Include Paths:
  *   "C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Include"    [32Bit]
  *   "C:\Program Files\IVI Foundation\VISA\Win64\Include"          [64Bit]
  *   "C:\Program Files\Thorlabs\upSERIES\Drivers\Instr\incl"       [No VXIPnP Folder]
  *
  * Additional Library Directories:
  *   "C:\Program Files (x86)\IVI Foundation\VISA\WinNT\lib\msc"    [32Bit]
  *   "C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc"      [64Bit]
  *   "C:\Program Files\Thorlabs\CHROLIS\Drivers\Instr\msvc"        [32Bit - No VXIPnP Folder]
  *   "C:\Program Files\Thorlabs\CHROLIS\Drivers\Instr\msvc64"      [64Bit - No VXIPnP Folder]
  *
  * Additional Dependencies:
  *   "TL6WL_32.lib"                                                [32Bit]
  *   "TL6WL_64.lib"                                                [64Bit]
  *
  * Library Locations:
  *   "C:\Program Files (x86)\IVI Foundation\VISA\WinNT\Bin"        [32Bit]
  *   "C:\Program Files\IVI Foundation\VISA\Win64\Bin"              [64Bit]
  *   "C:\Program Files\Thorlabs\CHROLIS\Drivers\Instr\bin"         [No VXIPnP Folder]
  *
  * Libraries:
  *   "TL6WL_32.dll"                                                [32Bit]
  *   "TL6WL_64.dll"                                                [64Bit]
 ***/

#include <stdio.h>
#include <string.h>
#include <windows.h>
#include "TL6WL.h"
#include <iostream>

int main()
{
    //ViStatus err;
#ifdef WIN32
    ViChar bitness[TL6WL_LONG_STRING_SIZE] = "x86";
#else
    ViChar bitness[TL6WL_LONG_STRING_SIZE] = "x64";
#endif

    int inp;
    std::cout << "Choose one of the following options:        \n"
        "1. Internal trigger demonstration\n (will show a sequence of LED2 and LED4, with 3 repetitions, no external trigger needed)\n"
        "2. External direct trigger (connect trigger input to 'LED4')\n" 
        "3. Sequence will start after triggered (connect trigger input to 'AUX1')\n"
        "4. LED6 is triggered by LED4, after 3 pulses (connect trigger input to 'LED4')\n"; 
    std::cin >> inp; // Get user input from the keyboard


    ViSession instrHdl = NULL;

    ViStatus err = 0;

    ViUInt32 numDevices = 0;

    char rsrc[256];

     // find devices connected to host,

    err = TL6WL_findRsrc(VI_NULL, &numDevices);

    // get resource name of first connected device

    err = TL6WL_getRsrcName(VI_NULL, 0, rsrc);

    // open device, get instrument handle

    err = TL6WL_init(rsrc, VI_TRUE, VI_FALSE, &instrHdl);
    if (VI_SUCCESS == err)printf("Device connected");

    // configure LEDs according to your needs, selection of LEDs + amplitude

    printf("\nSet Master Brightness to 10.0%% \n");
    err = TL6WL_setLED_LinearModeValue(instrHdl, 100);
    if (VI_SUCCESS != err)
    {
        printf("  TL6WL_setLED_LinearModeValue() :\n    Error Code = %#.8lX\n", err);
        printf("\nSample Terminated\n");

        printf("\nClose Device\n");
        err = TL6WL_close(instrHdl);
        if (VI_SUCCESS != err)
        {
            printf("  TLUP_close() :\n    Error Code = %#.8lX\n", err);
        }

        return -4;
    }
    printf("Set LED Brightness to 100.0%% \n");
    err = TL6WL_setLED_HeadBrightness(instrHdl, 1000, 1000, 1000, 1000, 1000, 1000);
    if (VI_SUCCESS != err)
    {
        printf("  TL6WL_setLED_HeadBrightness() :\n    Error Code = %#.8lX\n", err);
        printf("\nSample Terminated\n");

        printf("\nClose Device\n");
        err = TL6WL_close(instrHdl);
        if (VI_SUCCESS != err)
        {
            printf("  TLUP_close() :\n    Error Code = %#.8lX\n", err);
        }

        return -5;
    }

    // always start with stopping an eventually running timing unit (TU)

    err = TL6WL_TU_StartStopGeneratorOutput_TU(instrHdl, false);

    // for a new sequence always clear the current sequence of the timing unit (TU)

    err = TL6WL_TU_ResetSequence(instrHdl);

    //parameters for sequence case 1:

    ViUInt8 sigNr1 = 2; //LED2
    ViBoolean activeLow1 = 0;        // this is positive logic (not active low)
    ViUInt32 startDelayus1 = 0;     // this is start delay of 0ms
    ViUInt32 activeTimeus1 = 500000;   // this is half a second
    ViUInt32 inactiveTimeus1 = 1000000;   // this is 1s
    ViUInt32 repetitionCount1 = 3;    //number of repetitions

    ViUInt8 sigNr2 = 4;  //LED4
    ViBoolean activeLow2 = 0;        // this is positive logic (not active low)
    ViUInt32 startDelayus2 = 500000;     // this is start delay of half a second
    ViUInt32 activeTimeus2 = 500000;   // this is half a second
    ViUInt32 inactiveTimeus2 = 1000000;   // this is 1s
    ViUInt32 repetitionCount2 = 3;   //number of repetitions

    // parameters for trigger condition case3
    ViUInt8 sigNr3 = 7;//input channel AUX1
    ViBoolean startsLow3 = 0;  
    ViUInt32 edgeCount3 = 1;
    ViInt16 affectedSignalBitmask3 = 0x000A;//output channels 2 and 4

    //parameters for case 4
    ViUInt8 sigNr4 = 4;//input channel
    ViBoolean startsLow4 = 0;
    ViUInt32 edgeCount4 = 3;//condition is met after 3 edges
    ViInt16 affectedSignalBitmask4 = 0x0020;//output channel 6

    switch (inp) {
        ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // Internal Trigger
        //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    case 1:

        // define sequence for LED2 and LED4

        TL6WL_TU_AddGeneratedSelfRunningSignal(instrHdl, sigNr1, activeLow1, startDelayus1, activeTimeus1, inactiveTimeus1, repetitionCount1);
        TL6WL_TU_AddGeneratedSelfRunningSignal(instrHdl, sigNr2, activeLow2, startDelayus2, activeTimeus2, inactiveTimeus2, repetitionCount2);


        // start the sequence (this is the software trigger)
        TL6WL_setLED_HeadPowerStates(instrHdl, VI_FALSE, VI_TRUE, VI_FALSE, VI_TRUE, VI_FALSE, VI_FALSE);

        err = TL6WL_TU_StartStopGeneratorOutput_TU(instrHdl, true);
        if (VI_SUCCESS != err)
        {
            printf(" TL6WL_TU_StartStopGeneratorOutput_TU  :\n    Error Code = %#.8lX\n", err);
            printf("\nSample Terminated\n");

            printf("\nClose Device\n");
            err = TL6WL_close(instrHdl);
            if (VI_SUCCESS != err)
            {
                printf("  TLUP_close() :\n    Error Code = %#.8lX\n", err);
            }

            return -6;
        }
        Sleep(5000);

        break;
        /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // Direct trigger
        // ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    case 2:

        //trigger input to LED 4 for direct trigger
        TL6WL_setLED_HeadPowerStates(instrHdl, VI_FALSE, VI_FALSE, VI_FALSE, VI_TRUE, VI_FALSE, VI_FALSE);
        Sleep(5000);
        TL6WL_setLED_HeadPowerStates(instrHdl, VI_FALSE, VI_FALSE, VI_FALSE, VI_FALSE, VI_FALSE, VI_FALSE);
        break;

        // /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // Generated triggerd signal
        // ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    case 3:
   
        TL6WL_TU_AddGeneratedTriggeredSignal(instrHdl, sigNr1, activeLow1, startDelayus1, activeTimeus1, inactiveTimeus1, repetitionCount1);
        TL6WL_TU_AddGeneratedTriggeredSignal(instrHdl, sigNr2, activeLow2, startDelayus2, activeTimeus2, inactiveTimeus2, repetitionCount2);
        TL6WL_setLED_HeadPowerStates(instrHdl, VI_FALSE, VI_TRUE, VI_FALSE, VI_TRUE, VI_FALSE, VI_FALSE);

        err = TL6WL_TU_AddTriggerPoint(instrHdl, sigNr3, startsLow3, edgeCount3, affectedSignalBitmask3);
        if (VI_SUCCESS != err)
        {
            printf("TU_AddTriggerPoint :\n    Error Code = %#.8lX\n", err);
            printf("\nSample Terminated\n");

            printf("\nClose Device\n");
            err = TL6WL_close(instrHdl);
            if (VI_SUCCESS != err)
            {
                printf("  TLUP_close() :\n    Error Code = %#.8lX\n", err);
            }

            return -6;
        }


        err = TL6WL_TU_StartStopGeneratorOutput_TU(instrHdl, true);
        if (VI_SUCCESS != err)
        {
            printf(" TL6WL_TU_StartStopGeneratorOutput_TU  :\n    Error Code = %#.8lX\n", err);
            printf("\nSample Terminated\n");

            printf("\nClose Device\n");
            err = TL6WL_close(instrHdl);
            if (VI_SUCCESS != err)
            {
                printf("  TLUP_close() :\n    Error Code = %#.8lX\n", err);
            }

            return -6;
        }
        Sleep(5000);
        break;


     ///////////////////////////////////////////////////////////////////////////////////////////////////
     // Directly triggered signal
     ///////////////////////////////////////////////////////////////////////////////////////////////////
    case 4:

        err = TL6WL_setLED_HeadPowerStates(instrHdl, VI_FALSE, VI_FALSE, VI_FALSE, VI_TRUE, VI_FALSE, VI_TRUE);


        TL6WL_TU_AddDirectlyTriggeredSignal(instrHdl, 6);

        err = TL6WL_TU_AddTriggerPoint(instrHdl, sigNr4, startsLow4, edgeCount4, affectedSignalBitmask4);
        if (VI_SUCCESS != err)
        {
            printf("  TU_AddTriggerPoint :\n    Error Code = %#.8lX\n", err);
            printf("\nSample Terminated\n");

            printf("\nClose Device\n");
            err = TL6WL_close(instrHdl);
            if (VI_SUCCESS != err)
            {
                printf("  TLUP_close() :\n    Error Code = %#.8lX\n", err);
            }

            return -6;
        }

        err = TL6WL_TU_StartStopGeneratorOutput_TU(instrHdl, true);
        if (VI_SUCCESS != err)
        {
            printf(" TL6WL_TU_StartStopGeneratorOutput_TU  :\n    Error Code = %#.8lX\n", err);
            printf("\nSample Terminated\n");

            printf("\nClose Device\n");
            err = TL6WL_close(instrHdl);
            if (VI_SUCCESS != err)
            {
                printf("  TLUP_close() :\n    Error Code = %#.8lX\n", err);
            }

            return -6;
        }
        Sleep(5000);
        break;
    default:
        printf("\ninvalid input\n");
        break;
    }

    // finally close the device
    err = TL6WL_setLED_HeadPowerStates(instrHdl, VI_FALSE, VI_FALSE, VI_FALSE, VI_FALSE, VI_FALSE, VI_FALSE);
    err = TL6WL_close(instrHdl);
    
    

   }

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
