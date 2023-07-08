# Important Information
### _The scripts are a little bit different because of some differences in path from linux to windows_

- Windows Path Example -> `C:\Users\exampleuser\Desktop\`
- Linux Path Example -> ` ~/Desktop/`

###### The differences in the files mainly occur due to Windows using `\` and Linux using `/`

---
# Usage Example

- Windows -> `main_windows.py C:\Testing\source C:\Testing\replica C:\Testing\logs\test.log 10`

- Linux -> `python main_linux.py ~/Desktop/Testing/source ~/Desktop/Testing/replica ~/Desktop/Testing/logs/test.log 10`

---
# Explanation
#### _Windows_

- `main.py` -> Main File To Run The Program (Always Run This One)

- `C:\Testing\source` -> Path To Source Folder

- `C:\Testing\replica` -> Path To Target Folder

- `C:\Testing\logs\test.log` -> Path To Log File (Program's Output)

- `10` -> Interval (In Seconds) Between Each Attempt Folder Synchronization



#### _Linux_

- `python` -> This Tells Linux That The Program We Will Run Is A Python Script

- `main.py` -> Main File To Run The Program (Always Run This One)

- `~/Desktop/Testing/source` -> Path To Source Folder

- `~/Desktop/Testing/replica` -> Path To Target Folder

- `~/Desktop/Testing/logs/test.log` -> Path To Log File (Program's Output)

- `10` -> Interval (In Seconds) Between Each Attempt Folder Synchronization
