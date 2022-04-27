## Included Examples

### Initialize and Enable: 
This example shows the basic initialization and use of the KLS101 laser source. This includes opening the source, initializing the settings, enabling the laser, setting the power, and closing the open resourses. 

## Build Instructions
1. Set the desired startup file. 
2. Set Project Platform under Project -> Properties -> Build. This should be selected to match the bit-version of the dll's you plan to use (e.g. x64 for 64-bit dll's). 
3. Copy the following dll's from the Kinesis installation folder to the bin of the startup project e.g \Light_Sources_Examples\C#\KLS101\Initialize_and_Enable\bin\Debug:
   * Thorlabs.MotionControl.DeviceManager.dll
   * Thorlabs.MotionControl.DeviceManagerCLI.dll
   * Thorlabs.MotionControl.KCube.LaserSource.dll
   * Thorlabs.MotionControl.KCube.LaserSourceCLI.dll
   * Thorlabs.MotionControl.PrivateInternal.dll

4. The References are already added to the project, but in the event they need to be re-added you will need the following: 
   * Thorlabs.MotionControl.DeviceManagerCLI
   * Thorlabs.MotionControl.KCube.LaserSourceCLI

