# Linux Users
1. Navigate to the Database repo `cd path/to/database/repo`
2. add executable permissions to the script `chmod 755 update_database.py`
3. Run update_database.py `./update_database.py`

# Windows Users
1. Download Python https://www.python.org/downloads/
2. Make sure mysql bin is added to PATH. check by running `mysql --version` into a cmd window. If mysql is not found, follow the steps below.
   
    1. Find the MySQL bin Directory
  
       1. Open File Explorer.
       2. Navigate to the folder where MySQL is installed. By default, it’s usually in: `C:\Program Files\MySQL\MySQL Server X.X\` (Replace X.X with your MySQL version.)
       3. Locate the bin folder inside: `C:\Program Files\MySQL\MySQL Server X.X\bin`
       4. This folder contains mysql.exe, mysqldump.exe, and other MySQL command-line tools.
   
    2. Add MySQL bin to System PATH

       1. Press Win + R, type `sysdm.cpl`, and press Enter.
       2. Go to the Advanced tab.
       3. Click on Environment Variables.
       4. Edit the Path Variable
       5. In the System Variables section, scroll down and find Path.
       6. Select it and click Edit.
       7. Click New and paste the MySQL bin path: `C:\Program Files\MySQL\MySQL Server X.X\bin`
       8. Click OK to save.

3. navigate to your Database repo `cd path/to/database/repo`
4. run `python update_database.py`

# Inserting Test Data
1. Install dependencies: 
      1. Create and activate the virtual envrironment, following the instructions [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)
      2. Install the dependencies: `pip install .`
2. Run the script `python3 insert_data.py`
3. This script will insert
      1. 200 Users
      2. 20 Univeristies
      3. 3 Roles
      4. 50 Teams
      5. 20 Tournaments
      6. 100 Matches
      7. 80 Tickets
4. Deactivate the environment: `deactivate`
