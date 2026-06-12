game_profile_init()
{
	global current_game, current_game_name, genshin_note_map
	IniRead, current_game, setting.ini, game, current, yihuan
	if(!game_profile_valid(current_game))
		current_game := "yihuan"
	game_profile_apply(current_game)
}

game_profile_valid(gameId)
{
	return (gameId="yihuan" || gameId="genshin" || gameId="sky")
}

game_profile_apply(gameId)
{
	global current_game, current_game_name, genshin_note_map
	if(!game_profile_valid(gameId))
		gameId := "yihuan"
	current_game := gameId
	current_game_name := game_profile_name(gameId)
	genshin_note_map := game_profile_note_map(gameId)
	IniWrite, % current_game, setting.ini, game, current
}

game_profile_name(gameId := "")
{
	global current_game
	if(gameId="")
		gameId := current_game
	if(gameId="genshin")
		return "Genshin"
	if(gameId="sky")
		return "Sky"
	return "Yihuan"
}

game_profile_midi_target(gameId := "")
{
	global current_game
	if(gameId="")
		gameId := current_game
	if(gameId="genshin")
		return "genshin"
	if(gameId="sky")
		return "sky"
	return "yihuan"
}

game_profile_window_exist()
{
	global current_game
	if(current_game="genshin")
	{
		hwnd := WinExist("ahk_exe GenshinImpact.exe")
		if(!hwnd)
			hwnd := WinExist("ahk_exe YuanShen.exe")
		return hwnd
	}
	if(current_game="sky")
		return WinExist("ahk_exe Sky.exe")
	hwnd := WinExist("ahk_exe HTGame.exe")
	if(!hwnd)
		hwnd := WinExist("ahk_exe NTEGame.exe")
	return hwnd
}

game_profile_not_running_message()
{
	global current_game_name
	return current_game_name " is not running."
}

game_profile_folder_path(gameId := "")
{
	global current_game
	if(gameId="")
		gameId := current_game
	if(gameId="yihuan")
		return "D:\Neverness To Everness"
	if(gameId="sky")
		return "D:\sky"
	return ""
}

game_profile_open_folder()
{
	folderPath := game_profile_folder_path()
	if(folderPath!="" && InStr(FileExist(folderPath), "D"))
	{
		Run, %folderPath%
		return
	}
	MsgBox, 0x41040, Game Folder, No folder is configured for the selected game.
}

game_profile_note_map(gameId)
{
	if(gameId="genshin")
		return load_genshin_note_map()
	if(gameId="sky")
		return load_sky_note_map()
	return load_yihuan_note_map()
}

load_genshin_note_map()
{
	noteMap := {}
	noteMap[48] := "z"
	noteMap[50] := "x"
	noteMap[52] := "c"
	noteMap[53] := "v"
	noteMap[55] := "b"
	noteMap[57] := "n"
	noteMap[59] := "m"
	noteMap[60] := "a"
	noteMap[62] := "s"
	noteMap[64] := "d"
	noteMap[65] := "f"
	noteMap[67] := "g"
	noteMap[69] := "h"
	noteMap[71] := "j"
	noteMap[72] := "q"
	noteMap[74] := "w"
	noteMap[76] := "e"
	noteMap[77] := "r"
	noteMap[79] := "t"
	noteMap[81] := "y"
	noteMap[83] := "u"
	return noteMap
}

load_sky_note_map()
{
	defaultRows := ["y|u|i|o|p", "h|j|k|l|vkBA", "n|m|vkBC|vkBE|vkBF"]
	playablePitches := [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]
	rows := []
	Loop, 3
	{
		IniRead, rowValue, setting.ini, sky, % "row" A_Index, % defaultRows[A_Index]
		IniWrite, % rowValue, setting.ini, sky, % "row" A_Index
		rowTokens := normalize_sky_row(rowValue, defaultRows[A_Index])
		rows.Push(rowTokens)
	}
	noteMap := {}
	pitchIndex := 1
	Loop, 3
	{
		rowTokens := rows[A_Index]
		Loop, 5
		{
			noteMap[playablePitches[pitchIndex]] := rowTokens[A_Index]
			pitchIndex += 1
		}
	}
	return noteMap
}

normalize_sky_row(rowValue, fallback)
{
	tokens := StrSplit(rowValue, "|")
	if(tokens.Length() != 5)
		tokens := StrSplit(fallback, "|")
	Loop, % tokens.Length()
	{
		tokens[A_Index] := Trim(tokens[A_Index])
	}
	return tokens
}
