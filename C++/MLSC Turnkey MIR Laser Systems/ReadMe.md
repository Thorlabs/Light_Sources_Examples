# Example Description
In the example the available MLSC lasers are found, a connection is established, device parameters are read, the laser is switched on and measurement values are printed on the screen.

The code is written for the following products: MLIF3400, MLQF4000, MLQF4550, MLQF10500, MLID3250, MLQD4500, MLQD9500

https://www.thorlabs.com/turnkey-mir-laser-systems


# Instructions for Use
Guides written for this example is written with Microsoft's Visual Studio in mind. Other IDEs can be used, but instructions are not provided in this repository.
1. Create a new VC++ project file or open the existed VC++ project file;
2. Under the Solution Explorer, right click the Source Files, then add the MLSC_example.cpp to the Source Files;
3. Set the path of the TLTKL header file according to the bit of the project you want to build:  
a. Open Project\Properties\Configuration Properties\C/C++\General  
b. Enter the path of the header files into Additional include Directories (C:\Program Files (x86)\IVI Foundation\VISA\WinNT\include or C:\Program Files\IVI Foundation\VISA\Win64\include)
4. Set the path of the TLTKL library according to the bit of the project you want to build:  
a. Open Project\Properties\Configuration Properties\Linker\General  
b. Enter the path of the library files into Additional Library Directories (C:\Program Files (x86)\IVI Foundation\VISA\WinNT\lib\msc or C:\Program Files\IVI Foundation\VISA\Win64\Lib_x64\msc)
5. Set the additional dependent library:  
a. Open Project\Properties\Configuration Properties\Linker\Input  
b. Add the additional depended libraries into Additional Dependencies (TLTKL_32.lib; or TLTKL_64.lib;).