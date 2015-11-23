# COC-postresults
Python utility to create results content ready for posting at cascadeoc.org as part of the WIOL and Winter O season.

## Start the GUI
Nothing special if python is installed. From the repository, run ```python .\meetresultsGUI.py```

If python is not installed, keep reading.

## Packaging for computers without python
We'll use [PyInstaller](http://www.pyinstaller.org/) for packaging the app and all dependencies including python itself. For the COC download computer, which runs windows, you'll need to use a windows machine for this task as PyInstaller can only build packages for the current host OS. After instaling pyInstaller (via pip or your favorite python package manager) simply run ```pyinstaller .\meetresultsGUI.py```

This will evaluate the python file to determine all the necessary dependencies and create a couple new folders in the current working directory. You want the **dist** directory, which should contain a folder called ```meetresultsGUI```. 

**Important!** There are a couple more external files the script needs in order to create the ouput html. Copy these from the repository into the ```meetresultsGUI``` folder:
 - ```ClubCodes.csv```
 - ```ResultURLs.csv```
 - ```OutilsJs.js```
 - ```OutilsStyle.css```

Now that all those extra files are included, copy the ```meetresultsGUI``` folder to a USB stick or other transfer mechanism. 

On the second computer, it is safe to run ```meetresultsGUI.exe``` from the USB stick, or copy the entire folder to any location on the machine.
