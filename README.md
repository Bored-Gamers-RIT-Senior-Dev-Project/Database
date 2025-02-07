# Linux Users
1. Navagate to the Database repo `cd path/to/database/repo`
2. Run update_database.sh `./update_database.sh`

#Windows Users
1. Download Python https://www.python.org/downloads/
2. Make sure mysql bin is added to PATH. check by running `mysql --version` into a cmd window. If mysql is not found, follow the steps below.
   
    1. Find the MySQL bin Directory
  
    Open File Explorer.
    Navigate to the folder where MySQL is installed. By default, it’s usually in: `C:\Program Files\MySQL\MySQL Server X.X\` (Replace X.X with your MySQL version.)
    Locate the bin folder inside: `C:\Program Files\MySQL\MySQL Server X.X\bin`
    This folder contains mysql.exe, mysqldump.exe, and other MySQL command-line tools.
   
    2. Add MySQL bin to System PATH

    Press Win + R, type `sysdm.cpl`, and press Enter.
    Go to the Advanced tab.
    Click on Environment Variables.
    Edit the Path Variable
    In the System Variables section, scroll down and find Path.
    Select it and click Edit.
    Click New and paste the MySQL bin path:
    C:\Program Files\MySQL\MySQL Server X.X\bin
    Click OK to save.

3. navigate to your Database repo `cd path/to/database/repo`
4. run `python update_database.py`   
