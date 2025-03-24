@echo off
chcp 65001 > nul
:: BAT-файл для сброса изменений и обновления из репозитория (UTF-8)
echo [✓] Выполняем сброс изменений и обновление репозитория...
echo.

:: Проверка наличия Git
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [×] Ошибка: Git не установлен или не добавлен в PATH
    pause
    exit /b 1
)

:: Переход в корень репозитория (если нужно)
:: cd /d "C:\путь\к\репозиторию"

:: 1. Выполняем git reset --hard
echo [→] Выполняем git reset --hard...
git reset --hard
if %errorlevel% neq 0 (
    echo [×] Ошибка при выполнении git reset --hard
    pause
    exit /b 1
)

:: 2. Выполняем git pull
echo.
echo [→] Выполняем git pull...
git pull
if %errorlevel% neq 0 (
    echo [×] Ошибка при выполнении git pull
    pause
    exit /b 1
)

echo.
echo [✓] Операции успешно завершены!
pause