$exclude = @("venv", "projeto_intensivo.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "projeto_intensivo.zip" -Force