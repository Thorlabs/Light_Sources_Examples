# Included Examples

## CHROLIS Example
The sample code shows how you can initialize, set the intensity of each LED, and enable the output of the CHROLIS. User input is required for the source to be enabled in this example. 

## Instructions for Use

Before building and running this example. Please make sure you have downloaded the CHROLIS control app from here: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=CHROLIS

1) Set the project platform under the properties menu. This should be set to match the intended development platform e.g. x64 for deployment on 64-bit machines. 

2) Add the TLTSPB library as a reference by right clicking the References section of the Solution Explorer. Navigate to the appropriate folder for your platform target: 
    * 32-bit: C:\Program Files (x86)\IVI Foundation\VISA\VisaCom\Primary Interop Assemblies
    * 64-bit: C:\Program Files\IVI Foundation\VISA\VisaCom64\Primary Interop Assemblies
This solution is pre-built for 64-bit systems, so it may be needed to delete and re-add the reference to this dll. 