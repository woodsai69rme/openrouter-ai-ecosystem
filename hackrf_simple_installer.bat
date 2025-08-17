@echo off
echo ================================================
echo HackRF Simple Windows Installer
echo ================================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [ADMIN] Running with Administrator privileges
) else (
    echo [WARNING] Not running as Administrator
    echo Some operations may fail
)

echo.
echo Step 1: Creating HackRF directory...
mkdir "C:\hackrf-tools" 2>nul
cd /d "C:\hackrf-tools"

echo.
echo Step 2: Downloading HackRF tools...
echo Please wait...

REM Download using PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/greatscottgadgets/hackrf/releases/download/v2024.02.1/hackrf-tools-win64.zip' -OutFile 'hackrf-tools.zip'}"

if exist "hackrf-tools.zip" (
    echo [SUCCESS] Download completed
) else (
    echo [ERROR] Download failed
    echo Please download manually from: https://github.com/greatscottgadgets/hackrf/releases
    pause
    exit /b 1
)

echo.
echo Step 3: Extracting tools...
powershell -Command "Expand-Archive -Path 'hackrf-tools.zip' -DestinationPath '.' -Force"

REM Find and move tools to root directory
for /d %%i in (hackrf-*) do (
    move "%%i\*" . >nul 2>&1
    rmdir "%%i" 2>nul
)

REM Clean up
del "hackrf-tools.zip" 2>nul

echo.
echo Step 4: Adding to PATH...
setx PATH "%PATH%;C:\hackrf-tools" /M >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] Added to system PATH
) else (
    echo [WARNING] Could not update system PATH automatically
    echo Please add C:\hackrf-tools to your PATH manually
)

echo.
echo Step 5: Testing installation...
set PATH=%PATH%;C:\hackrf-tools
hackrf_info.exe >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] hackrf_info found and working
    echo Running device test...
    hackrf_info.exe
) else (
    echo [INFO] hackrf_info installed but no device detected
    echo This is normal if HackRF is not connected or drivers not installed
)

echo.
echo Step 6: Driver installation...
echo Downloading Zadig driver installer...

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/pbatard/libwdi/releases/download/b730/zadig-2.5.exe' -OutFile 'zadig.exe'}"

if exist "zadig.exe" (
    echo [SUCCESS] Zadig downloaded
    echo.
    echo DRIVER INSTALLATION INSTRUCTIONS:
    echo ==================================
    echo 1. Connect your HackRF device to USB
    echo 2. The Zadig driver installer will open
    echo 3. Select "HackRF One" from the device list
    echo 4. Ensure "WinUSB" is selected as driver
    echo 5. Click "Install Driver"
    echo.
    echo Press any key to launch Zadig...
    pause >nul
    start zadig.exe
) else (
    echo [WARNING] Could not download Zadig
    echo Please download manually from: https://zadig.akeo.ie/
)

echo.
echo ================================================
echo Installation Summary
echo ================================================
echo Tools installed to: C:\hackrf-tools
echo.
echo NEXT STEPS:
echo 1. Install USB driver using Zadig (if not done)
echo 2. Connect HackRF device
echo 3. Open new Command Prompt and run: hackrf_info
echo 4. Restart HackRF Enhanced Platform
echo.
echo Press any key to exit...
pause >nul