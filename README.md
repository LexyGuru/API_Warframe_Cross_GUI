
<h1 align="center">
  <br>
  <a href="https://github.com/LexyGuru/API_Warframe_Cross_GUI"><img src="Icons/None.png" alt="Lekszikov" width="200"></a>
  <br>
  Lekszikov Miklos
  <br>
</h1>
<h4 align="center">Ez egy Warframe API asztali alkalmazas.</h4>
<p align="center">
  <a href="https://github.com/LexyGuru/API_Warframe_Cross_GUI/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/LexyGuru/API_Warframe_Cross_GUI" alt="Contributors">
  </a>
  <a href="https://github.com/LexyGuru/API_Warframe_Cross_GUI/issues">
    <img src="https://img.shields.io/github/commit-activity/t/LexyGuru/API_Warframe_Cross_GUI" alt="Commit Activity">
  </a>
  <a href="https://github.com/LexyGuru/API_Warframe_Cross_GUI/releases">
    <img src="https://img.shields.io/github/release-date/LexyGuru/API_Warframe_Cross_GUI" alt="Release Date">
  </a>
</p>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<picture>
   <img alt="Info" src="https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/Icons/git/info.svg">
</picture> <br>

> Cross platform 

|            | Support |
|------------|---------|
| Windows    | yes     |
| macOS      | yes     |
| Linux      | yes     | 


> Fontosabb API lekeresek 

|                   | Menü                  | Aktiv  |
|-------------------|-----------------------|--------|
| `Keresés`         |                       |        |
|                   | `Warframe Wiki`       | `Yes`  |
|                   | `Item Drop infok`     | `Yes`  |
|                   | `Warframe Drop infok` | `Yes`  |
| `Ciklusok`        |                       |        |
|                   |                       | `Yes`  |
|                   | `Void Fissures`       | `Yes`  |
|                   | `Sortie`              | `Yes`  |
|                   | `Nightwave`           | `Yes`  |
|                   | `Ciklusok`            | `Yes`  |
|                   | `Arbitration`         | `Yes`  |
|                   | `Archon Hunt`         | `Yes`  |
|                   | `Baro Ki'Teer`        | `Yes`  |
| `Események`       |                       | `Yes`  |
| `Git Update Info` |                       | `Yes`  |

<picture>
    <img alt="Info" src="https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/Icons/git/note.svg">
</picture> <br>

```bash
# Clone git 
$ git clone https://github.com/LexyGuru/API_Warframe_Cross_GUI.git

# Mappa megnyitas
$ cd API_Warframe_Cross_GUI

# Függöseg telepitese:
python install_update_packages.py
```
<picture>
    <img alt="Info" src="https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/Icons/git/tip.svg">
</picture> <br>

Windows rendszerre:
```bash
pyinstaller --onefile --windowed --add-data "gui:gui" --add-data "gui/Script:gui/Script" --add-data "gui/Styles:gui/Styles" --icon=Icons/AppIcon.ico main_qt6.py
```

macOS rendszerre:
```bash
pyinstaller --onefile --windowed --add-data "gui:gui" --add-data "gui/Script:gui/Script" --add-data "gui/Styles:gui/Styles" --icon=Icons/AppIcon.icns main_qt6.py
```

Linux rendszerre:
```bash
pyinstaller --onefile --windowed --add-data "gui:gui" --add-data "gui/Script:gui/Script" --add-data "gui/Styles:gui/Styles" --icon=Icons/AppIcon.png main_qt6.py
```

<picture>
   <img alt="Info" height="18" src="https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/Icons/git/note.svg">
</picture><br> 

If you're using Linux Bash for Windows, [see this guide](https://www.onlogic.com/blog/how-to-enable-bash-for-windows-10-and-11/) or use `node` from the command prompt.

<br>

 <picture>
   <img alt="Info" src="https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/Icons/git/warning.svg">
</picture>

In case of problems, file a [report](https://github.com/LexyGuru/API_Warframe_Cross_GUI/issues).
<br><br><br>

<picture>
    <img alt="Info" height="60" src="https://raw.githubusercontent.com/LexyGuru/API_Warframe_Cross_GUI/main/Icons/git/tip.svg">
</picture>

> # UPX Telepítési Útmutató 
> optimize_build.py futtatása esetén
## macOS

1. Homebrew segítségével (ajánlott):
   - Nyisson meg egy Terminal ablakot.
   - Ha még nincs telepítve a Homebrew, telepítse ezt a paranccsal:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Telepítse az UPX-et:
     ```
     brew install upx
     ```

2. Manuális telepítés:
   - Látogasson el az [UPX letöltési oldalára](https://github.com/upx/upx/releases/latest).
   - Töltse le a macOS-hez való legújabb verziót (pl. `upx-4.0.2-darwin_x86_64.tar.xz`).
   - Csomagolja ki a letöltött fájlt.
   - Másolja az `upx` bináris fájlt egy PATH-ban lévő könyvtárba, például:
     ```
     sudo cp upx /usr/local/bin/
     ```

## Windows

1. Chocolatey segítségével (ajánlott):
   - Nyisson meg egy PowerShell ablakot adminisztrátorként.
   - Ha még nincs telepítve a Chocolatey, telepítse ezt a paranccsal:
     ```
     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
     ```
   - Telepítse az UPX-et:
     ```
     choco install upx
     ```

2. Manuális telepítés:
   - Látogasson el az [UPX letöltési oldalára](https://github.com/upx/upx/releases/latest).
   - Töltse le a Windows-hoz való legújabb verziót (pl. `upx-4.0.2-win64.zip`).
   - Csomagolja ki a letöltött fájlt.
   - Másolja az `upx.exe` fájlt egy PATH-ban lévő könyvtárba, vagy adja hozzá az UPX könyvtárát a PATH-hoz:
     - Nyissa meg a Rendszer tulajdonságait.
     - Kattintson a "Speciális rendszerbeállítások"-ra.
     - Kattintson a "Környezeti változók"-ra.
     - A "Rendszerváltozók" alatt keresse meg a "Path" változót és kattintson a "Szerkesztés"-re.
     - Kattintson az "Új"-ra és adja hozzá az UPX könyvtárának teljes elérési útját.

## Linux

1. Csomagkezelő segítségével:
   - Ubuntu/Debian:
     ```
     sudo apt-get update
     sudo apt-get install upx-ucl
     ```
   - Fedora:
     ```
     sudo dnf install upx
     ```
   - Arch Linux:
     ```
     sudo pacman -S upx
     ```

2. Manuális telepítés:
   - Látogasson el az [UPX letöltési oldalára](https://github.com/upx/upx/releases/latest).
   - Töltse le a Linux-hoz való legújabb verziót (pl. `upx-4.0.2-amd64_linux.tar.xz`).
   - Csomagolja ki a letöltött fájlt.
   - Másolja az `upx` bináris fájlt egy PATH-ban lévő könyvtárba, például:
     ```
     sudo cp upx /usr/local/bin/
     ```

## Ellenőrzés

A telepítés után ellenőrizze, hogy az UPX megfelelően működik-e:

1. Nyisson meg egy új terminál/parancssor ablakot.
2. Írja be:
   ```
   upx --version
   ```

Ha a parancs kiírja az UPX verzióját, a telepítés sikeres volt.






<!---
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/check.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/complete.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/danger.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/error.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/example.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/info.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/issue.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/note.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/solution.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/tip.svg
https://github.com/LexyGuru/API_Warframe_Cross_GUI/blob/main/Icons/git/warning.svg




hdiutil create -volname WarframeInfoHub -srcfolder dist/WarframeInfoHub.app -ov -format UDZO WarframeInfoHub.dmg--->


    

