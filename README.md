# ShutdownTimer documentation
## What is it
A simple and minimal desktop app that allows you to set a timer for your pc to shutdown at.
## Build
### Requirements
- Python 3.10
- PyInstaller 5.2
- Local copy of [Shutdown-Timer repository](https://github.com/enricoferraiolo/Shutdown-Timer)
### Instruction
Open terminal, navigate to ShutdownTimer root directory and execute the following command: 
``` sh
pyinstaller --noconfirm --onefile --windowed --icon "./src/stopwatch.ico" --name "ShutdownTimer"  "./src/main.py"
```

Now, you will find your *ShutdownTimer.exe* file in: `./dist/`
