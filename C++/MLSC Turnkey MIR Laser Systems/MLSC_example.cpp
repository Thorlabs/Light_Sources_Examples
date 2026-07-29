//Example Date of Creation(YYYY - MM - DD) 2026 - 07 - 29
//Example Date of Last Modification on Github 2026 - 07 - 29
//Version of C++ used for Testing and IDE: C++ 14, Visual Studio 2022
//Version of the Thorlabs SDK used : 1.0
//Example Description: The sample code shows how to control a MLSC laser in C++. 
//Tested with QD4500LH

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <conio.h>       

#include "TLTKL.h"

#ifndef VI_ERROR_RSRC_NFOUND
#define VI_ERROR_RSRC_NFOUND  (_VI_ERROR+0x3FFF007EL)
#endif



/*===========================================================================
 Defined
===========================================================================*/
#define COMM_TIMEOUT          			5000    	// communications timeout in ms

/*===========================================================================
 Prototypes
===========================================================================*/
ViStatus find_instruments(ViChar** resource);
ViStatus resetAndSelftest(ViSession handle);
ViStatus get_deviceId(ViSession handle);
ViStatus get_deviceParam(ViSession handle);
ViStatus switch_tecOn(ViSession instrHdl);
ViStatus switch_laserOn(ViSession instrHdl);
ViStatus get_measurementValues(ViSession handle);
void error_exit(ViSession handle, ViStatus err);
void waitKeypress(void);

/*===========================================================================
 Functions
===========================================================================*/
int main(int argc, char** argv)
{
	ViStatus    err;
	//ViBoolean   tecState, ldState;
	ViChar* rscPtr = NULL;
	ViSession   instrHdl = VI_NULL;

	printf("-----------------------------------------------------------\n");
	printf(" MLSC - Mid-IR Laser Source instrument driver sample       \n");
	printf("-----------------------------------------------------------\n\n");

	// Parameter checking / resource scanning
	if (argc < 2)
	{
		// Find resources (find_instruments allocates the returned string)
		err = find_instruments(&rscPtr);
		if (err) error_exit(instrHdl, err);  // something went wrong
		if (!rscPtr) exit(EXIT_SUCCESS);     // none found  
	}
	else
	{
		// Got resource in command line
		rscPtr = argv[1];
	}

	// Open session to instrument
	printf("Opening session to '%s' ... ", rscPtr);
	// device init with integrated device reset
	err = TLTKL_init(rscPtr, VI_ON, VI_OFF, &instrHdl);
	if (err) error_exit(instrHdl, err);  // can not open session to instrument
	printf("done\n\n");

	// free returned resource string if it was allocated by find_instruments
	if (argc < 2 && rscPtr != NULL)
	{
		free(rscPtr);
		rscPtr = NULL;
	}

	// Reset and selftest
	printf("Device selftest: ");
	err = resetAndSelftest(instrHdl);
	if (err) error_exit(instrHdl, err);
	printf("done\n");

	// Get instrument info
	err = get_deviceId(instrHdl);
	if (err) error_exit(instrHdl, err);

	// Get device parameter
	err = get_deviceParam(instrHdl);
	if (err) error_exit(instrHdl, err);

	// Switch TEC on
	err = switch_tecOn(instrHdl);
	if (err) error_exit(instrHdl, err);

	// Switch laser on
	err = switch_laserOn(instrHdl);
	if (err) error_exit(instrHdl, err);

	// Measure values continuously
	err = get_measurementValues(instrHdl);
	if (err) error_exit(instrHdl, err);

	// Switch laser and tec off  
	err = TLTKL_switchLdOutput(instrHdl, VI_OFF);
	err = TLTKL_switchTecOutput(instrHdl, VI_OFF);

	// Close session to instrument
	TLTKL_close(instrHdl);

	waitKeypress();
	return (EXIT_SUCCESS);
}


/*---------------------------------------------------------------------------
  Find Instruments
---------------------------------------------------------------------------*/
ViStatus find_instruments(ViChar** resource)
{
	ViStatus       err;
	ViUInt32       instrIdx, cnt, resourceCount = 0;
	ViChar  	   rscTemp[TLTKL_BUFFER_SIZE], modelName[TLTKL_BUFFER_SIZE], serialNumber[TLTKL_BUFFER_SIZE], manufacturer[TLTKL_BUFFER_SIZE];
	int            i, idx, done;
	ViBoolean 	   resourceInUse = 0;

	printf("Scanning for instruments ...\n");
	err = TLTKL_findRsrc(0, &resourceCount);
	if (err) error_exit(0, err);
	if (!resourceCount)
	{
		printf("No matching instruments found\n\n");
		waitKeypress();
		exit(EXIT_SUCCESS);     // none found  
	}

	instrIdx = 0;
	if (resourceCount > 1) // more than 1 instrument found ?
	{
		// Display selection
		done = 0;
		do
		{
			printf("Found %d matching instruments:\n\n", resourceCount);

			for (cnt = 0; cnt < resourceCount; cnt++)
			{

				err = TLTKL_getRsrcName(0, cnt, rscTemp);
				if (err) error_exit(0, err);

				err = TLTKL_getRsrcInfo(0, cnt, modelName, serialNumber, manufacturer, &resourceInUse);
				if (err) error_exit(0, err);

				// Print out
				printf("% d: %s \tS/N: %s \tManufacturer: %s \tUsed: %d\n", cnt + 1, modelName, serialNumber, manufacturer, resourceInUse);
			}

			printf("\nPlease select (Enter): ");
			while ((idx = getchar()) == EOF);
			idx -= '0';
			/* Eingabepuffer bis Zeilenende sauber entfernen (portabel) */
			{
				int ch;
				while ((ch = getchar()) != '\n' && ch != EOF);
			}
			printf("\n");
			if ((idx < 1) || (idx > resourceCount))
			{
				printf("Invalid selection\n\n");
			}
			else
			{
				instrIdx = idx - 1;
				done = 1;
			}
		} while (!done);
	}
	else
	{
		// Single instrument: get its resource name
		err = TLTKL_getRsrcName(0, 0, rscTemp);
		if (err) error_exit(0, err);
	}

	// get information from selected instrument
	err = TLTKL_getRsrcName(0, instrIdx, rscTemp);
	if (err) error_exit(0, err);

	err = TLTKL_getRsrcInfo(0, instrIdx, modelName, serialNumber, manufacturer, &resourceInUse);
	if (err) error_exit(0, err);

	printf("Selected: %d   %s   S/N: %s   Manufacturer: %s   Used: %d\n\n", instrIdx + 1, modelName, serialNumber, manufacturer, resourceInUse);

	// Allocate persistent string and return it to caller (caller must free when appropriate)
	{
		size_t len = strlen(rscTemp) + 1;
		ViChar* out = (ViChar*)malloc(len);
		if (!out)
		{
			fprintf(stderr, "ERROR: memory allocation failed\n");
			return VI_ERROR_RSRC_NFOUND;
		}
		memcpy(out, rscTemp, len);
		*resource = out;
	}

	return (VI_SUCCESS);
}


/*---------------------------------------------------------------------------
 Reset device and selftest
---------------------------------------------------------------------------*/
ViStatus resetAndSelftest(ViSession instrHdl)
{
	ViStatus err;
	ViChar   errorMessage[TLTKL_BUFFER_SIZE];
	ViInt16  errNum;

	err = TLTKL_reset(instrHdl);
	if (err) return(err);

	err = TLTKL_selfTest(instrHdl, &errNum, errorMessage);
	if (err) return(err);
	if (errNum)
		printf("Error number: %ld Message: %s", errNum, errorMessage);

	return (EXIT_SUCCESS);
}


/*---------------------------------------------------------------------------
 Read out device ID and print it to screen
---------------------------------------------------------------------------*/
ViStatus get_deviceId(ViSession instrHdl)
{
	ViStatus err;
	ViChar   nameBuf[TLTKL_BUFFER_SIZE];
	ViChar   snBuf[TLTKL_BUFFER_SIZE];
	ViChar   fwRevBuf[TLTKL_BUFFER_SIZE];
	ViChar   manufMsgBuf[TLTKL_BUFFER_SIZE];
	ViChar   calMsgBuf[TLTKL_BUFFER_SIZE];

	ViChar   nameBufHead[TLTKL_BUFFER_SIZE];
	ViChar   snBufHead[TLTKL_BUFFER_SIZE];
	ViChar   fwRevBufHead[TLTKL_BUFFER_SIZE];
	ViChar   manufMsgBufHead[TLTKL_BUFFER_SIZE];
	ViChar   calMsgBufHead[TLTKL_BUFFER_SIZE];

	ViChar   drvRevBuf[TLTKL_BUFFER_SIZE];

	// reading controller information
	err = TLTKL_identificationQuery(instrHdl, VI_NULL, nameBuf, snBuf, fwRevBuf);
	if (err) return(err);
	printf("Controller:      %s\n", nameBuf);
	printf("Serial number:   %s\n", snBuf);
	printf("Firmware:        %s\n", fwRevBuf);

	err = TLTKL_manufacturerMessage(instrHdl, manufMsgBuf);
	if (err) return(err);
	printf("Manufactured:    %s\n", manufMsgBuf);

	err = TLTKL_calibrationMessage(instrHdl, calMsgBuf);
	if (err) return(err);
	printf("Calibrated:      %s\n\n", calMsgBuf);

	// reading laser head information
	err = TLTKL_identificationQueryHead(instrHdl, VI_NULL, nameBufHead, snBufHead, fwRevBufHead);
	if (err) return(err);
	printf("Laser Head:      %s\n", nameBufHead);
	printf("Serial number:   %s\n", snBufHead);
	printf("Firmware:        %s\n", fwRevBufHead);

	err = TLTKL_manufacturerMessageHead(instrHdl, manufMsgBufHead);
	if (err) return(err);
	printf("Manufactured:    %s\n", manufMsgBufHead);

	err = TLTKL_calibrationMessageHead(instrHdl, calMsgBufHead);
	if (err) return(err);
	printf("Calibrated:      %s\n\n", calMsgBufHead);

	// reading driver version
	err = TLTKL_revisionQuery(instrHdl, drvRevBuf, VI_NULL);
	if (err) return(err);
	printf("Driver Version:  %s\n\n", drvRevBuf);

	return(VI_SUCCESS);
}


/*---------------------------------------------------------------------------
 Get device parameter
---------------------------------------------------------------------------*/
ViStatus get_deviceParam(ViSession instrHdl)
{
	ViStatus err;
	ViInt16	ldType;
	ViReal64 ldWave, ldPow, ldVolt, ldCurr, tecCurr;

	// query laser type
	err = TLTKL_getLdType(instrHdl, &ldType);
	if (err) return(err);
	printf("Laser Type is                  %d (%d-DFB, %d-FP)\n\n", ldType, TLTKL_LASER_TYPE_DFB, TLTKL_LASER_TYPE_FP);

	// get laser nominal wavelength 
	err = TLTKL_getLdWaveNom(instrHdl, TLTKL_ATTR_SET_VAL, &ldWave);
	if (err) return(err);
	printf("Laser Nominal Wavelength is    %.1f nm\n", ldWave * 1e9); // convert m -> nm

	// get laser nominal optical power 
	err = TLTKL_getLdPowOptNom(instrHdl, TLTKL_ATTR_SET_VAL, &ldPow);
	if (err) return(err);
	printf("Laser Nominal Optical Power is %.1f mW\n", ldPow * 1000); // convert W to mW

	// get laser maximum voltage 
	err = TLTKL_getLdVoltLimMax(instrHdl, TLTKL_ATTR_SET_VAL, &ldVolt);
	if (err) return(err);
	printf("Laser maximum Voltage is       %.1f V\n", ldVolt);

	// get laser maximum current limit
	err = TLTKL_getLdCurrLimMax(instrHdl, TLTKL_ATTR_SET_VAL, &ldCurr);
	if (err) return(err);
	printf("Laser maximum Current Limit is %.3f A\n", ldCurr);

	// get tec current limit
	err = TLTKL_getTecCurrLimit(instrHdl, TLTKL_ATTR_SET_VAL, &tecCurr);
	if (err) return(err);
	err = TLTKL_setTecCurrLimit(instrHdl, tecCurr);
	if (err) return(err);
	printf("Tec Current Limit is           %.3f A\n\n", tecCurr);

	return(VI_SUCCESS);
}


/*---------------------------------------------------------------------------
 Switch tec on
---------------------------------------------------------------------------*/
ViStatus switch_tecOn(ViSession instrHdl)
{
	ViStatus 	err;
	ViBoolean   tecState;

	err = TLTKL_switchTecOutput(instrHdl, VI_ON);
	if (err) error_exit(instrHdl, err);
	err = TLTKL_getTecOutputState(instrHdl, &tecState);
	if (err) error_exit(instrHdl, err);
	if (tecState == VI_ON)
	{
		printf("Tec switched on.\n");
	}
	else
	{
		printf("Tec did not switch on!!!\n");
		err = TLTKL_beep(instrHdl);
		if (err) error_exit(instrHdl, err);
	}

	return(VI_SUCCESS);
}


/*---------------------------------------------------------------------------
 Switch laser on
---------------------------------------------------------------------------*/
ViStatus switch_laserOn(ViSession instrHdl)
{
	ViStatus 	err;
	ViBoolean   ldState;

	err = TLTKL_beep(instrHdl);
	if (err) error_exit(instrHdl, err);
	printf("\nATTENTION: Laser will be switched on by pressing <ENTER>.");
	while (getchar() == EOF);
	err = TLTKL_switchLdOutput(instrHdl, VI_ON);
	if (err) error_exit(instrHdl, err);
	err = TLTKL_getLdOutputState(instrHdl, &ldState);
	if (err) error_exit(instrHdl, err);
	if (ldState == VI_ON)
	{
		printf("Laser switched on.\n");
	}
	else
	{
		printf("Laser did not switch on!!!\n");
		err = TLTKL_beep(instrHdl);
		if (err) error_exit(instrHdl, err);
	}

	return(VI_SUCCESS);
}


/*---------------------------------------------------------------------------
 Get measurement values continuously
---------------------------------------------------------------------------*/
ViStatus get_measurementValues(ViSession instrHdl)
{
	ViStatus 	e, err;
	ViInt16		intpMode;
	ViInt32		key;
	ViReal64		val, ldVolt, ldCurr, thermRes, ldTemp, tecCurr;

	printf("Start continuous measurements if laser is ON by pressing <Enter>\n");
	while (getchar() == EOF);

	printf("Press <ESC> to exit\n");

	// write out (interpolated) laser setpoints
	// query laser interpolation mode 
	err = TLTKL_getLdIntpolType(instrHdl, &intpMode);
	if (err) return(err);
	printf("Current laser setpoint:");

	// get laser current setpoint 
	err = TLTKL_getLdCurrSetpoint(instrHdl, TLTKL_ATTR_SET_VAL, &val);
	printf("Current: %.4f A ", val);
	if (err) error_exit(instrHdl, err);

	// get temperature setpoint
	err = TLTKL_getTempSetpoint(instrHdl, TLTKL_ATTR_SET_VAL, &val);
	printf("Temperature: %.3f C\n\n", val);
	if (err) error_exit(instrHdl, err);

	printf("Laser Current [A]   Volt [V]   Temp. Sensor [Ohm]   Temp. [C]   Tec Current [A]\n");
	/* fflush(stdin) entfernt, da undefiniertes Verhalten; Eingaben werden nicht benötigt */
	err = 0;
	do
	{
		// measure all values
		e = TLTKL_measMultiple(instrHdl, &ldCurr, &ldVolt, &ldTemp, &thermRes, &tecCurr);
		if (e)
		{
			TLTKL_beep(instrHdl);
			printf("\nError %d 0x%x at TLTKL_measMultiple() !!!\n", e, e);
			if (!err) err = e;
		}
		else
		{
			printf("    %5.3lf           %6.3lf        %7.1lf            %6.3lf        %6.3lf\n", ldCurr, ldVolt, thermRes, ldTemp, tecCurr);
		}

		if (_kbhit())
		{
			key = _getch();
			if (key == 27) // ESC
				err = 999999;
		}
	} while (err == 0);

	if (err == 999999)
		return(VI_SUCCESS);
	else
		return(err);
}


/*---------------------------------------------------------------------------
  Exit with error message
---------------------------------------------------------------------------*/
void error_exit(ViSession instrHdl, ViStatus err)
{
	ViChar   buf[TLTKL_ERR_DESCR_BUFFER_SIZE];

	// switch off laser and tec
	TLTKL_switchLdOutput(instrHdl, VI_OFF);
	TLTKL_switchTecOutput(instrHdl, VI_OFF);

	// Get error description and print out error
	TLTKL_errorMessage(instrHdl, err, buf);
	fprintf(stderr, "ERROR: %s\n", buf);

	// close session to instrument if open
	if (instrHdl != VI_NULL)
	{
		TLTKL_close(instrHdl);
	}

	// exit program
	waitKeypress();
	exit(EXIT_FAILURE);
}


/*---------------------------------------------------------------------------
  Print keypress message and wait
---------------------------------------------------------------------------*/
void waitKeypress(void)
{
	printf("Press <ENTER> to exit\n");
	while (getchar() == EOF);
}


/****************************************************************************
  End of Source file
****************************************************************************/
