menu()
{
	global
	Menu, Tray, NoStandard
	Menu, Tray, Add, % "v" version,donothing
	Menu, Tray, Add
	Menu, Tray, Add, Setup, setup
	Menu, Tray, Add, Convert MIDI, func_btn_midi
	Menu, Tray, Add
	Menu, Tray, Add, Game Folder, gamefolder
	Menu, Tray, Add, Project Folder, projectfolder
	Menu, Tray, Add, History, changesfile
	Menu, Tray, Add, Exit, Exit
	Menu, Tray, Click, 1
}

_func_001()
{
	global
setup:
setup_gui_show()
Return
gamefolder:
game_profile_open_folder()
Return
projectfolder:
Run, %A_ScriptDir%
Return
donothing:
Return
changesfile:
Run, notepad.exe %A_Temp%\domiso\changes.md
Return
}
