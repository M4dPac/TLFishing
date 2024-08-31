# Указываем путь к виртуальному окружению
$PATH="D:\projects\TLFishing"

# Формируем команду для запуска скрипта
#$command = "-NoExit -Command "
#$command += "& '$PATH\.venv\Scripts\Activate.ps1'; "
#$command += "python '$PATH\create_filter.py'; "
#$command += "deactivate; "
#$command += "Exit"""

# Запускаем скрипт от администратора
Start-Process powershell.exe -Verb RunAs -ArgumentList "-NoExit -Command `"& '$PATH\.venv\Scripts\Activate.ps1'; python '$PATH\create_filter.py'; deactivate; Exit`""

# Запускаем скрипт от администратора с свернутым окном
#Start-Process powershell.exe -Verb RunAs -ArgumentList $command
