# PowerShell script to build Color Picker executable
Write-Host "Building Color Picker executable..." -ForegroundColor Cyan
Write-Host ""

try {
    # Run PyInstaller with the spec file
    & "D:/Python playfolder/colour picker/.venv/Scripts/python.exe" -m PyInstaller color_picker.spec --clean
    
    if (Test-Path "dist\ColorPicker.exe") {
        Write-Host "✓ Build successful! Executable created at: dist\ColorPicker.exe" -ForegroundColor Green
        Write-Host ""
        
        # Show file size
        $fileSize = (Get-Item "dist\ColorPicker.exe").Length
        $fileSizeMB = [Math]::Round($fileSize / 1MB, 2)
        Write-Host "File size: $fileSizeMB MB" -ForegroundColor Yellow
        Write-Host ""
        
        Write-Host "You can now run the executable from: dist\ColorPicker.exe" -ForegroundColor Green
        Write-Host "Or copy it to any Windows machine to run without Python installed." -ForegroundColor Green
    } else {
        Write-Host "✗ Build failed! Check the output above for errors." -ForegroundColor Red
    }
} catch {
    Write-Host "Error during build: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to continue"