@echo off
setlocal

cd /d "%~dp0"

set IMAGE_NAME=gui

:: Set VcXsrv Installer URL and expected install path
set "VCXSRV_URL=https://github.com/marchaesen/vcxsrv/releases/download/21.1.16.1/vcxsrv-64.21.1.16.1.installer.exe"
set "VCXSRV_PATH=C:\Program Files\VcXsrv\vcxsrv.exe"
set "VCXSRV_CONFIG_PATH=%USERPROFILE%\vcxsrv.config"
set "INSTALLER_PATH=vcxsrv_installer.exe"

:: Check if VcXsrv is installed
if exist "%VCXSRV_PATH%" (
    echo Path exists
) else (
    echo VcXsrv is not installed, downloading now...

    :: Download the VcXsrv installer
    powershell -Command "& {Invoke-WebRequest -Uri '%VCXSRV_URL%' -OutFile 'vcxsrv_installer.exe'}"

    echo VcXsrv is required for X11 forwarding on Windows, please wait...
    start /wait vcxsrv_installer.exe /S

    echo VcXsrv installation complete!
)

echo.

:: Set DISPLAY environment variable
setx DISPLAY host.docker.internal:0.0
set DISPLAY=host.docker.internal:0.0

:: Check if VcXsrv is already running
tasklist | find /i "vcxsrv.exe" >nul
if %errorlevel% neq 0 (
    echo Starting VcXsrv server...

    :: Create a default config file if it doesn’t exist
    if not exist "%VCXSRV_CONFIG_PATH%" (
        echo -multiwindow -clipboard -wgl -ac > "%VCXSRV_CONFIG_PATH%"
    )

    :: Start VcXsrv with required settings
    start "" "%VCXSRV_PATH%" -multiwindow -clipboard -wgl -ac
    echo VcXsrv started successfully
) else (
    echo VcXsrv is already running
)

:: Function to check if a command exists
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing Docker, please wait...

    :: Download Docker Installer
    powershell -Command "& {Invoke-WebRequest -Uri 'https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe' -OutFile 'DockerInstaller.exe'}"

    :: Install Docker silently
    echo Installing Docker...
    start /wait DockerInstaller.exe install --quiet

    echo Docker installed. Please restart your computer.
    pause
    exit /b
)

:: Check if Docker is running
tasklist | find /i "docker desktop.exe" >nul
if %errorlevel% neq 0 (
    echo Starting Docker...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    timeout /t 10 >nul
)

:: Check if the Docker image exists
docker inspect --type=image %IMAGE_NAME% >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing docker image, please wait...
    docker load -i vm.tar
)

:: Running the program
echo Running Program...
docker run --rm ^
    -e DISPLAY=%DISPLAY% ^
    -v "%CD%\output:/app/excel" ^
    -v "%CD%\config:/app/config" ^
    -v "%CD%\images:/app/images" ^
    -v "%CD%\images:/app/annotations/" ^
    %IMAGE_NAME%

echo Shutting down...
taskkill /IM vcxsrv.exe /F >nul 2>&1

shutdown -a >nul 2>&1
del "%INSTALLER_PATH%"
del DockerInstaller.exe

pause