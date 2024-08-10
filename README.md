<h1 align="center">
  <br>
  <a href="http://www.amitmerchant.com/electron-markdownify"><img src="Icons/None.png" alt="Markdownify" width="200"></a>
  <br>
  Lekszikov Miklos
  <br>
</h1>

<h4 align="center">Ez egy Warframe API asztali alkalmazas.</h4>


<p align="center">

</p>



## Jelenlegi 

* Cross platform
  - Windows, macOS és Linux ready.
* Fontosabb API lekeresek
  * Keresés 
    - ITEM 
    - DROP 
  * Ciklusok 
  * Események 
  * Void Fissures 
  * Sortie 
  * Nightwave 
  * Arbitration 
  * Baro Ki'Teer 


## Letöltés
```bash
# Clone this repository
$ git clone https://github.com/LexyGuru/API_Warframe_Cross_GUI.git

# Go into the repository
$ cd API_Warframe_Cross_GUI

```

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

> **Note**
> If you're using Linux Bash for Windows, [see this guide](https://www.onlogic.com/blog/how-to-enable-bash-for-windows-10-and-11/) or use `node` from the command prompt.





    

