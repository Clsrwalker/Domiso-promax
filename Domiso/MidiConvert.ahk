func_btn_midi:
midi_convert_show()
Return

midi_convert_show()
{
	global midi_convert_file, midi_convert_out_dir, midi_convert_target
	global hMidiConvertGui, midi_convert_pid, midi_convert_running
	global midi_convert_status, midi_convert_results, midi_convert_log
	global current_game
	IniRead, midi_convert_file, setting.ini, midiconvert, lastMidi, 
	defaultOutDir := "D:\domiso\txt"
	if(!InStr(FileExist(defaultOutDir), "D"))
		defaultOutDir := A_ScriptDir "\..\txt"
	IniRead, midi_convert_out_dir, setting.ini, midiconvert, outDir, %defaultOutDir%
	midi_convert_target := game_profile_midi_target(current_game)
	if(midi_convert_target="")
		midi_convert_target := "yihuan"
	midi_convert_running := 0
	midi_convert_pid := 0

	Gui, midi:Destroy
	Gui, midi:New, +AlwaysOnTop +Resize +HwndhMidiConvertGui, MIDI to TXT
	Gui, midi:Color, F7F1E6
	Gui, midi:Font, s10 c4B3827, Segoe UI
	Gui, midi:Add, Text, x18 y16 w560 h24, Select a MIDI file and generate DoMiSo txt files.
	Gui, midi:Add, Text, x18 y52 w90 h24, MIDI
	Gui, midi:Add, Edit, x112 y48 w440 h28 ReadOnly vmidi_convert_file, %midi_convert_file%
	Gui, midi:Add, Button, x562 y47 w90 h30 gmidi_select_file, Browse
	Gui, midi:Add, Text, x18 y88 w90 h24, Target
	Gui, midi:Add, DropDownList, x112 y84 w180 h140 vmidi_convert_target, yihuan|sky|genshin|all|other
	GuiControl, midi:ChooseString, midi_convert_target, %midi_convert_target%
	Gui, midi:Add, Text, x312 y88 w340 h24, Default follows the selected Game profile.
	Gui, midi:Add, Text, x18 y124 w90 h24, Out Dir
	Gui, midi:Add, Edit, x112 y120 w440 h28 vmidi_convert_out_dir, %midi_convert_out_dir%
	Gui, midi:Add, Button, x562 y119 w90 h30 gmidi_select_outdir, Browse
	Gui, midi:Add, Button, x112 y164 w120 h36 gmidi_start, Generate
	Gui, midi:Add, Button, x242 y164 w120 h36 gmidi_cancel, Cancel
	Gui, midi:Add, Button, x372 y164 w120 h36 gmidi_open_out, Open Folder
	Gui, midi:Add, Button, x502 y164 w150 h36 gmidi_load_selected, Load Selected
	Gui, midi:Add, Text, x18 y214 w634 h24 vmidi_convert_status, Ready.
	Gui, midi:Add, ListBox, x18 y246 w634 h164 vmidi_convert_results
	Gui, midi:Add, Edit, x18 y422 w634 h148 ReadOnly -Wrap vmidi_convert_log
	Gui, midi:Show, w670 h590
}

midi_select_file:
Gui, midi:+OwnDialogs
IniRead, lastMidi, setting.ini, midiconvert, lastMidi, 
SplitPath, lastMidi,, lastDir
if(lastDir="")
	lastDir := "D:\domiso\mid"
FileSelectFile, selectedMidi, 3, %lastDir%, Select MIDI, MIDI (*.mid; *.midi)
if(selectedMidi!="")
{
	GuiControl, midi:, midi_convert_file, %selectedMidi%
	IniWrite, %selectedMidi%, setting.ini, midiconvert, lastMidi
}
Return

midi_select_outdir:
Gui, midi:+OwnDialogs
GuiControlGet, outDir,, midi_convert_out_dir
if(outDir="")
	outDir := A_ScriptDir "\..\txt"
FileSelectFolder, selectedDir, *%outDir%, 3, Select output folder
if(selectedDir!="")
{
	GuiControl, midi:, midi_convert_out_dir, %selectedDir%
	IniWrite, %selectedDir%, setting.ini, midiconvert, outDir
}
Return

midi_start:
midi_convert_start()
Return

midi_cancel:
midi_convert_cancel()
Return

midi_open_out:
GuiControlGet, outDir,, midi_convert_out_dir
if(outDir!="")
	Run, %outDir%
Return

midi_load_selected:
midi_convert_load_selected()
Return

midiGuiClose:
midiGuiEscape:
midi_convert_cancel(0)
Gui, midi:Destroy
Return

midi_convert_tick:
midi_convert_update()
Return

midi_convert_start()
{
	global midi_convert_pid, midi_convert_running, midi_convert_progress_file, midi_convert_log_file
	global midi_convert_manifest_file, midi_convert_started_tick

	if(midi_convert_running)
		return
	Gui, midi:Submit, NoHide
	GuiControlGet, midiFile,, midi_convert_file
	GuiControlGet, target,, midi_convert_target
	GuiControlGet, outDir,, midi_convert_out_dir
	if(!FileExist(midiFile))
	{
		MsgBox, 0x41010, ERROR, MIDI file not found.
		return
	}
	if(outDir="")
		outDir := A_ScriptDir "\..\txt"
	FileCreateDir, %outDir%
	if(ErrorLevel)
	{
		MsgBox, 0x41010, ERROR, Can not create output folder.
		return
	}
	IniWrite, %midiFile%, setting.ini, midiconvert, lastMidi
	IniWrite, %target%, setting.ini, midiconvert, target
	IniWrite, %outDir%, setting.ini, midiconvert, outDir

	tempDir := A_Temp "\domiso_yihuan_convert"
	FileCreateDir, %tempDir%
	FormatTime, stamp,, yyyyMMdd_HHmmss
	SplitPath, midiFile,,,, midiStem
	midi_convert_progress_file := tempDir "\" midiStem "_" stamp "_progress.json"
	midi_convert_manifest_file := tempDir "\" midiStem "_" stamp "_manifest.json"
	midi_convert_log_file := tempDir "\" midiStem "_" stamp ".log"
	FileDelete, %midi_convert_progress_file%
	FileDelete, %midi_convert_manifest_file%
	FileDelete, %midi_convert_log_file%

	toolScript := midi_find_generate_script()
	if(!FileExist(toolScript))
	{
		MsgBox, 0x41010, ERROR, domiso_generate_select.py not found.
		return
	}
	cmd := A_ComSpec " /c " Chr(34) "python " midi_q(toolScript) " " midi_q(midiFile) " --target " target " --out-dir " midi_q(outDir) " --report-dir " midi_q(outDir) " --progress-file " midi_q(midi_convert_progress_file) " --manifest-file " midi_q(midi_convert_manifest_file) " > " midi_q(midi_convert_log_file) " 2>&1" Chr(34)
	GuiControl, midi:, midi_convert_status, % "Running " target "..."
	GuiControl, midi:, midi_convert_log, 
	GuiControl, midi:, midi_convert_results, |
	Run, %cmd%,, Hide, midi_convert_pid
	if(ErrorLevel)
	{
		MsgBox, 0x41010, ERROR, Failed to start Python.
		return
	}
	midi_convert_running := 1
	midi_convert_started_tick := A_TickCount
	SetTimer, midi_convert_tick, 700
}

midi_convert_update()
{
	global midi_convert_pid, midi_convert_running, midi_convert_progress_file, midi_convert_log_file
	if(!midi_convert_running)
		return
	status := midi_progress_summary(midi_convert_progress_file)
	if(status!="")
		GuiControl, midi:, midi_convert_status, %status%
	logText := midi_read_tail(midi_convert_log_file, 6000)
	if(logText!="")
		GuiControl, midi:, midi_convert_log, %logText%
	Process, Exist, %midi_convert_pid%
	if(ErrorLevel)
		return
	SetTimer, midi_convert_tick, Off
	midi_convert_running := 0
	midi_convert_finish()
}

midi_convert_finish()
{
	global midi_convert_log_file, midi_convert_progress_file
	outputs := midi_parse_outputs(midi_convert_log_file)
	GuiControl, midi:, midi_convert_results, |
	count := 0
	for _, p in outputs
	{
		SplitPath, p,,, ext
		if(FileExist(p) && ext="txt")
		{
			GuiControl, midi:, midi_convert_results, %p%
			count += 1
		}
	}
	status := midi_progress_summary(midi_convert_progress_file)
	if(count > 0)
		GuiControl, midi:, midi_convert_status, % "Done. " count " output files found. " status
	else
		GuiControl, midi:, midi_convert_status, % "Finished, but no output files were detected. Check log."
	logText := midi_read_tail(midi_convert_log_file, 12000)
	GuiControl, midi:, midi_convert_log, %logText%
}

midi_convert_cancel(closeMsg := 1)
{
	global midi_convert_pid, midi_convert_running
	if(!midi_convert_running)
		return
	RunWait, % A_ComSpec " /c taskkill /PID " midi_convert_pid " /T /F",, Hide
	SetTimer, midi_convert_tick, Off
	midi_convert_running := 0
	if(closeMsg)
		GuiControl, midi:, midi_convert_status, Cancelled.
}

midi_convert_load_selected()
{
	global hEdit1
	GuiControlGet, selected,, midi_convert_results
	if(selected="")
	{
		MsgBox, 0x41040, MIDI, Select a generated txt first.
		return
	}
	if(!FileExist(selected))
	{
		MsgBox, 0x41010, ERROR, Selected file does not exist.
		return
	}
	GuiDropFiles(0, [selected], hEdit1, 0, 0)
	Gui, midi:Destroy
}

midi_q(s)
{
	return Chr(34) s Chr(34)
}

midi_find_generate_script()
{
	local p
	p := A_ScriptDir "\tools\domiso_generate_select.py"
	if(FileExist(p))
		return p
	p := A_ScriptDir "\..\tools\domiso_generate_select.py"
	if(FileExist(p))
		return p
	p := "D:\domiso\tools\domiso_generate_select.py"
	if(FileExist(p))
		return p
	return ""
}

midi_read_tail(path, maxChars := 4000)
{
	if(!FileExist(path))
		return ""
	f := FileOpen(path, "r", "UTF-8")
	if(!IsObject(f))
		return ""
	txt := f.Read()
	f.Close()
	if(StrLen(txt) > maxChars)
		txt := SubStr(txt, StrLen(txt)-maxChars+1)
	return txt
}

midi_progress_summary(path)
{
	if(!FileExist(path))
		return ""
	f := FileOpen(path, "r", "UTF-8")
	if(!IsObject(f))
		return ""
	txt := f.Read()
	f.Close()
	status := midi_json_value(txt, "status")
	current := midi_json_value(txt, "current")
	total := midi_json_value(txt, "total")
	name := midi_json_value(txt, "current_name")
	if(status="")
		return ""
	if(current!="" && total!="")
		return status " [" current "/" total "] " name
	return status
}

midi_json_value(txt, key)
{
	pat := Chr(34) key Chr(34) "\s*:\s*(?:" Chr(34) "([^" Chr(34) "]*)" Chr(34) "|([0-9]+))"
	if(RegExMatch(txt, "O)" pat, m))
	{
		if(m.Value(1)!="")
			return m.Value(1)
		return m.Value(2)
	}
	return ""
}

midi_parse_outputs(path)
{
	outputs := []
	if(!FileExist(path))
		return outputs
	f := FileOpen(path, "r", "UTF-8")
	if(!IsObject(f))
		return outputs
	txt := f.Read()
	f.Close()
	Loop, Parse, txt, `n, `r
	{
		if(RegExMatch(A_LoopField, "O)^OUTPUT=(.+)$", m))
			outputs.Push(m.Value(1))
	}
	return outputs
}
