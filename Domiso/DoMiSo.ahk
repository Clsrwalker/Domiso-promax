
#Requires AutoHotkey v1.1.34
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance force
SetBatchLines, -1
SetWorkingDir %A_ScriptDir%
SetKeyDelay, -1, -1
SendMode Event
FileEncoding, UTF-8

#include meta.ahk

;@Ahk2Exe-IgnoreBegin
if A_Args.Length() > 0
{
	for n, param in A_Args
	{
		RegExMatch(param, "--out=(\w+)", outName)
		if(outName1=="version") {
			f := FileOpen(versionFilename,"w","UTF-8-RAW")
			f.Write(version)
			f.Close()
			ExitApp
		}
	}
}
;@Ahk2Exe-IgnoreEnd

;@Ahk2Exe-SetCompanyName HelloWorks
;@Ahk2Exe-SetName Domiso
;@Ahk2Exe-SetDescription Domiso Multi Game
;@Ahk2Exe-SetVersion version
;@Ahk2Exe-SetMainIcon domiso_game_music.ico
;@Ahk2Exe-ExeName Domiso

IniRead, nonAdmin, setting.ini, update, nonAdminMode, 0
if(!nonAdmin){
	UAC()
}
;@Ahk2Exe-IgnoreBegin
	gDebug:=1
	MsgBox, 0x41030,ATTENTION,You are running DEBUG version!!!`n注意，正在运行的是测试版本。
;@Ahk2Exe-IgnoreEnd
if(betaBuild=1) {
	MsgBox, 0x41030,ATTENTION,You are running BETA version`, the BETA version does not support automatic updates!!!`n注意，正在运行的是内测版本。内测版本不支持自动更新。
}

OnExit, TrueExit
#Include log.ahk
log_init()

#include update.ahk

#Include data/midi_data.ahk
#Include lib/Music.ahk
#include Encrypt.ahk

menu()

; 谱面模式normal or cipher
sheet_mode:="normal"
; 谱面内容
sheet_content:=""
; 显示内容
plain_content:=""


isBtn1Playing:=0
isBtn2Playing:=0
isBtn1Paused:=0
genshin_pause_offset:=0
genshin_resume_array:=Array()
playback_total_ms:=0
playback_seek_ms:=0
playback_pending_seek_ms:=0
playback_slider_internal:=0
playback_slider_dragging:=0
playback_mode:=""

_Instrument:=inst

DllCall("QueryPerformanceFrequency", "Int64P", freq)

baseOffset := [0,2,4,5,7,9,11]

; DONE: non admin & global mode display

Notes := new NotePlayer()
if(Notes.Device==0) {
	midi_device := False
} else {
	midi_device := True
}
IniRead, startup_music, setting.ini, update, startupMusic, 1
IniRead, global_mode, setting.ini, setup, globalMode, 0
load_yihuan_play_settings()
#Include GameProfiles.ahk
game_profile_init()

#Include gui.ahk
Gosub resolve
if(midi_device && startup_music){
	Notes.Start()
}
Return

#Include MidiConvert.ahk

titleMove:
PostMessage 0xA1, 2
Return

genshin_array_sort(ByRef array)
{
	array_string:=""
	For index, v in array
	{
		array_string .= v.delay "," v.note "," v.time "`n"
	}
	Sort, array_string, N
	array:={}
	Loop, Parse, array_string, `n
	{
		if(RegExMatch(A_LoopField, "O)(\d+),([^,]+),(\d+)", note))
		{
			array.Push({"delay":note[1], "note":note[2], "time":note[3]})
		}
	}
}

analyseNotes(Notes)
{
	global genshin_note_map, genshin_play_report, yihuan_play_speed_percent, yihuan_play_hold_min_ms, current_game_name
	notesCount:=0
	genshinNotesCount:=0
	For Key, Array in Notes.Timeline
	{
		For k, v in Array
		{
			if(v.Type=="NoteOn") {
				notesCount+=1
				if(genshin_note_map.HasKey(v.Index)){
					genshinNotesCount+=1
				}
			}
		}
	}
	fitPercent := notesCount > 0 ? Round(100*genshinNotesCount/notesCount, 2) : 0
	statusTxt := Round(Notes.total_beats,2) " beats | " genshinNotesCount "/" notesCount " Notes | " fitPercent "% fits " current_game_name
	if(IsObject(genshin_play_report) && genshin_play_report.HasKey("count")) {
		statusTxt .= " | Play " genshin_play_report.count
		statusTxt .= " | peak " genshin_play_report.peak "/s"
		if(genshin_play_report.minGap > 0) {
			statusTxt .= " | min " genshin_play_report.minGap "ms"
		}
		statusTxt .= " | " yihuan_play_speed_percent "% spd"
		statusTxt .= " | hold≥" yihuan_play_hold_min_ms "ms"
		if(genshin_play_report.merged > 0) {
			statusTxt .= " | merge " genshin_play_report.merged
		}
	}
	statubar_txt(statusTxt)
}

playback_clamp_ms(ms)
{
	global playback_total_ms
	ms := Round(ms)
	if(ms < 0) {
		ms := 0
	}
	if(playback_total_ms > 0 && ms > playback_total_ms) {
		ms := playback_total_ms
	}
	return ms
}

playback_format_ms(ms)
{
	ms := playback_clamp_ms(ms)
	totalSec := Floor(ms / 1000)
	hh := Floor(totalSec / 3600)
	mm := Floor(Mod(totalSec, 3600) / 60)
	ss := Mod(totalSec, 60)
	if(hh > 0) {
		return Format("{:02}:{:02}:{:02}", hh, mm, ss)
	}
	return Format("{:02}:{:02}", mm, ss)
}

playback_compute_total_ms()
{
	global Notes, genshin_play_array
	maxMs := 0
	For offset, _ in Notes.Timeline
	{
		offset += 0
		if(offset > maxMs) {
			maxMs := offset
		}
	}
	Loop, % genshin_play_array.Length()
	{
		ev := genshin_play_array[A_Index]
		evEnd := ev.delay + ev.time
		if(evEnd > maxMs) {
			maxMs := evEnd
		}
	}
	return Round(maxMs)
}

playback_ms_to_slider(ms)
{
	global playback_total_ms
	ms := playback_clamp_ms(ms)
	if(playback_total_ms <= 0) {
		return 0
	}
	return Round((ms * 1000.0) / playback_total_ms)
}

playback_slider_to_ms(sliderValue)
{
	global playback_total_ms
	sliderValue += 0
	if(sliderValue < 0) {
		sliderValue := 0
	}
	if(sliderValue > 1000) {
		sliderValue := 1000
	}
	if(playback_total_ms <= 0) {
		return 0
	}
	return Round((sliderValue * playback_total_ms) / 1000.0)
}

playback_get_current_ms()
{
	global isBtn1Playing, isBtn1Paused, isBtn2Playing, startTime, genshin_pause_offset, Notes, playback_seek_ms
	if(isBtn1Playing) {
		return playback_clamp_ms(genshin_now_ms() - startTime)
	}
	if(isBtn1Paused) {
		return playback_clamp_ms(genshin_pause_offset)
	}
	if(isBtn2Playing) {
		return playback_clamp_ms(Notes.GetPosition())
	}
	return playback_clamp_ms(playback_seek_ms)
}

playback_update_labels(currentMs := "", forceSlider := 0)
{
	global playback_total_ms, playback_seek_ms, playback_slider_dragging, playback_slider_internal
	if(currentMs = "") {
		currentMs := playback_get_current_ms()
	}
	currentMs := playback_clamp_ms(currentMs)
	playback_seek_ms := currentMs
	GuiControl,, playback_elapsed_label, % playback_format_ms(currentMs)
	GuiControl,, playback_total_label, % playback_format_ms(playback_total_ms)
	if(forceSlider || !playback_slider_dragging) {
		playback_slider_internal := 1
		GuiControl,, playback_slider, % playback_ms_to_slider(currentMs)
		playback_slider_internal := 0
	}
}

playback_refresh_after_resolve(resetSeek := 0)
{
	global playback_total_ms, playback_seek_ms, playback_pending_seek_ms
	playback_total_ms := playback_compute_total_ms()
	if(resetSeek) {
		playback_seek_ms := 0
	} else if(playback_seek_ms > playback_total_ms) {
		playback_seek_ms := 0
	}
	playback_pending_seek_ms := playback_seek_ms
	playback_update_labels(playback_seek_ms, 1)
}

playback_start_progress(mode := "")
{
	global playback_mode
	if(mode != "") {
		playback_mode := mode
	}
	SetTimer, playback_progress_tick, 100
}

playback_stop_progress()
{
	SetTimer, playback_progress_tick, Off
}

playback_apply_seek(targetMs)
{
	global isBtn1Playing, isBtn1Paused, isBtn2Playing, playback_pending_seek_ms
	global genshin_pause_offset, genshin_resume_array, Notes
	targetMs := playback_clamp_ms(targetMs)
	playback_pending_seek_ms := targetMs
	if(isBtn1Playing) {
		genshin_stop(0, 1)
		genshin_play(targetMs)
		return
	}
	if(isBtn1Paused) {
		genshin_pause_offset := targetMs
		genshin_resume_array := Array()
		playback_update_labels(targetMs, 1)
		return
	}
	if(isBtn2Playing) {
		Notes.Stop()
		Notes.Start(targetMs)
		playback_start_progress("listen")
		playback_update_labels(targetMs, 1)
		return
	}
	playback_update_labels(targetMs, 1)
}

load_yihuan_play_settings()
{
	global yihuan_play_speed_percent, yihuan_play_time_scale, yihuan_play_hold_min_ms
	global yihuan_play_same_key_gap_ms, yihuan_play_key_delay_ms, yihuan_play_press_ms

	IniRead, yihuan_play_speed_percent, setting.ini, yihuanplay, speedPercent, 95
	IniWrite, % yihuan_play_speed_percent, setting.ini, yihuanplay, speedPercent
	yihuan_play_speed_percent += 0
	if(yihuan_play_speed_percent < 70 || yihuan_play_speed_percent > 120) {
		yihuan_play_speed_percent := 95
	}
	yihuan_play_time_scale := 100.0 / yihuan_play_speed_percent

	IniRead, yihuan_play_hold_min_ms, setting.ini, yihuanplay, holdMinMs, 150
	IniWrite, % yihuan_play_hold_min_ms, setting.ini, yihuanplay, holdMinMs
	yihuan_play_hold_min_ms += 0
	if(yihuan_play_hold_min_ms < 80 || yihuan_play_hold_min_ms > 400) {
		yihuan_play_hold_min_ms := 150
	}

	IniRead, yihuan_play_same_key_gap_ms, setting.ini, yihuanplay, sameKeyMinGapMs, 110
	IniWrite, % yihuan_play_same_key_gap_ms, setting.ini, yihuanplay, sameKeyMinGapMs
	yihuan_play_same_key_gap_ms += 0
	if(yihuan_play_same_key_gap_ms < 20 || yihuan_play_same_key_gap_ms > 400) {
		yihuan_play_same_key_gap_ms := 110
	}

	IniRead, yihuan_play_key_delay_ms, setting.ini, yihuanplay, keyDelayMs, 8
	IniWrite, % yihuan_play_key_delay_ms, setting.ini, yihuanplay, keyDelayMs
	yihuan_play_key_delay_ms += 0
	if(yihuan_play_key_delay_ms < -1 || yihuan_play_key_delay_ms > 80) {
		yihuan_play_key_delay_ms := 8
	}

	IniRead, yihuan_play_press_ms, setting.ini, yihuanplay, keyPressMs, 14
	IniWrite, % yihuan_play_press_ms, setting.ini, yihuanplay, keyPressMs
	yihuan_play_press_ms += 0
	if(yihuan_play_press_ms < -1 || yihuan_play_press_ms > 120) {
		yihuan_play_press_ms := 14
	}
}

optimize_genshin_play_array(ByRef array)
{
	global yihuan_play_time_scale, yihuan_play_same_key_gap_ms
	out := Array()
	lastByKey := {}
	merged := 0

	Loop, % array.Length()
	{
		ev := array[A_Index]
		delay := Round(ev.delay * yihuan_play_time_scale)
		time := Round(ev.time * yihuan_play_time_scale)
		note := ev.note
		if(time < 1) {
			time := 1
		}
		if(lastByKey.HasKey(note))
		{
			prevIndex := lastByKey[note]
			prev := out[prevIndex]
			gap := delay - prev.delay
			if(gap >= 0 && gap < yihuan_play_same_key_gap_ms)
			{
				prevEnd := prev.delay + prev.time
				currEnd := delay + time
				if(currEnd > prevEnd) {
					prev.time := currEnd - prev.delay
				}
				out[prevIndex] := prev
				merged += 1
				Continue
			}
		}
		out.Push({"delay":delay, "time":time, "note":note})
		lastByKey[note] := out.Length()
	}
	array := out
	return build_genshin_play_report(array, merged)
}

build_genshin_play_report(array, merged := 0)
{
	report := {"count": array.Length(), "merged": merged, "peak": 0, "minGap": 0}
	if(array.Length() <= 0) {
		return report
	}
	windowStart := 1
	Loop, % array.Length()
	{
		curDelay := array[A_Index].delay
		while(windowStart < A_Index && curDelay - array[windowStart].delay > 1000)
		{
			windowStart += 1
		}
		curCount := A_Index - windowStart + 1
		if(curCount > report.peak) {
			report.peak := curCount
		}
		if(A_Index > 1)
		{
			gap := curDelay - array[A_Index-1].delay
			if(gap > 0 && (report.minGap = 0 || gap < report.minGap)) {
				report.minGap := gap
			}
		}
	}
	return report
}

load_yihuan_note_map()
{
	; 36-key piano: 3 chromatic octaves, C3-B5 / MIDI 48-83.
	noteMap := {}

	; Natural notes use the standard 21-key three-row layout.
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

	; Semitones follow the game's UI: Shift raises a natural key, Ctrl lowers a natural key.
	noteMap[49] := "Shift+z"  ; C#3
	noteMap[51] := "Ctrl+c"   ; Eb3
	noteMap[54] := "Shift+v"  ; F#3
	noteMap[56] := "Shift+b"  ; G#3
	noteMap[58] := "Ctrl+m"   ; Bb3
	noteMap[61] := "Shift+a"  ; C#4
	noteMap[63] := "Ctrl+d"   ; Eb4
	noteMap[66] := "Shift+f"  ; F#4
	noteMap[68] := "Shift+g"  ; G#4
	noteMap[70] := "Ctrl+j"   ; Bb4
	noteMap[73] := "Shift+q"  ; C#5
	noteMap[75] := "Ctrl+e"   ; Eb5
	noteMap[78] := "Shift+r"  ; F#5
	noteMap[80] := "Shift+t"  ; G#5
	noteMap[82] := "Ctrl+u"   ; Bb5

	return noteMap
}

queue_game_note(noteTune, noteTime)
{
	global genshin_note_map, genshin_delay, genshin_output, genshin_play_array
	if(!genshin_note_map.HasKey(noteTune)) {
		return
	}
	mappedKey := genshin_note_map[noteTune]
	genshin_output.="[" Round(genshin_delay) "]-(" mappedKey ")-{" Round(noteTime) "}`n"
	genshin_play_array.Push({"delay":Round(genshin_delay),"time":Round(noteTime),"note":mappedKey})
}

note_release(elem)
{
	global sendHistory, deltaMS, genshin_pressed_array, gDebug
	note := elem.note
	newArray := Array()
	Loop, % genshin_pressed_array.Length()
	{
		if genshin_pressed_array[A_Index].note != note {
			newArray.Push(genshin_pressed_array[A_Index])
		}
	}
	if genshin_pressed_array.Length() != newArray.Length() {
		send_key := game_note_send_text(note, "up")
		genshin_pressed_array := newArray
		if(gDebug) {
			sendHistory.=Round(deltaMS) "ms " send_key "`n"
		}
		game_note_send(note, "up")
	}
}
note_play(elem)
{
	global sendHistory, deltaMS, genshin_pressed_array, gDebug, yihuan_play_hold_min_ms
	send_key:=""
	if (elem.HasKey("resume") || elem.time >= yihuan_play_hold_min_ms)
	{
		send_key:=game_note_send_text(elem.note, "down")
		game_note_send(elem.note, "down")
		genshin_pressed_array.Push(elem)
	} else {
		send_key:=game_note_send_text(elem.note, "tap")
		game_note_send(elem.note, "tap")
	}
	if(gDebug) {
		sendHistory.=Round(deltaMS) "ms " send_key " " elem.time "ms`n"
	}
}

game_note_parts(note, ByRef modKey, ByRef keyName)
{
	modKey := ""
	keyName := note
	if(RegExMatch(note, "iO)^(Shift|Ctrl)\+(.+)$", m)) {
		modKey := m.Value(1)
		keyName := m.Value(2)
	}
}

game_note_send_text(note, action)
{
	local modKey, keyName
	game_note_parts(note, modKey, keyName)
	if(modKey != "") {
		if(action == "down")
			return "{" modKey " down}{" keyName " down}{" modKey " up}"
		if(action == "up")
			return "{" keyName " up}"
		return "{" modKey " down}{" keyName "}{" modKey " up}"
	}
	if(action == "down")
		return "{" keyName " down}"
	if(action == "up")
		return "{" keyName " up}"
	return "{" keyName "}"
}

game_note_send(note, action)
{
	send_key := game_note_send_text(note, action)
	Send, % send_key
}

genshin_now_ms()
{
	global freq
	DllCall("QueryPerformanceCounter", "Int64P", nowTime)
	Return nowTime//(freq/1000)
}

genshin_release_all_notes()
{
	global genshin_note_map, genshin_pressed_array
	genshin_pressed_array := Array()
	For k, v in genshin_note_map
	{
		game_note_send(v, "up")
	}
	Send, {Shift up}{Ctrl up}
}

genshin_build_resume_from_offset(targetMs)
{
	global genshin_play_array, genshin_resume_array, yihuan_play_hold_min_ms
	targetMs := playback_clamp_ms(targetMs)
	genshin_resume_array := Array()
	nextIndex := 1
	Loop, % genshin_play_array.Length()
	{
		ev := genshin_play_array[A_Index]
		if(ev.delay < targetMs)
		{
			remainingTime := Round(ev.delay + ev.time - targetMs)
			if(ev.time >= yihuan_play_hold_min_ms && remainingTime > 40)
			{
				genshin_resume_array.Push({"delay":Round(targetMs), "time":remainingTime, "note":ev.note, "resume":1})
			}
			nextIndex := A_Index + 1
			Continue
		}
		break
	}
	return nextIndex
}

genshin_pause()
{
	global startTime, genshin_pressed_array, genshin_pause_offset, genshin_resume_array
	global isBtn1Playing, isBtn1Paused, yihuan_play_key_delay_ms, yihuan_play_press_ms
	if(!isBtn1Playing)
	{
		Return
	}
	genshin_pause_offset := genshin_now_ms() - startTime
	if(genshin_pause_offset < 0) {
		genshin_pause_offset := 0
	}
	genshin_resume_array := Array()
	For _, elem in genshin_pressed_array
	{
		remainingTime := Round(elem.delay + elem.time - genshin_pause_offset)
		if(remainingTime > 0)
		{
			genshin_resume_array.Push({"delay":Round(genshin_pause_offset), "time":remainingTime, "note":elem.note, "resume":1})
		}
	}
	isBtn1Playing:=0
	isBtn1Paused:=1
	btn1update()
	SetTimer, genshin_main, Off
	SetKeyDelay, -1, -1
	genshin_release_all_notes()
	playback_stop_progress()
	playback_update_labels(genshin_pause_offset, 1)
	statubar_txt("Paused @" Round(genshin_pause_offset) "ms | F10 Resume")
}

genshin_resume()
{
	global startTime, isBtn1Playing, isBtn1Paused, global_mode, domiso_active_hwnd, gui_id
	global yihuan_play_key_delay_ms, yihuan_play_press_ms, genshin_pause_offset, Notes
	if(!isBtn1Paused || isBtn1Playing)
	{
		Return
	}
	domiso_active_hwnd:=0
	if(global_mode) {
		domiso_active_hwnd:=WinExist("A")
		if(domiso_active_hwnd == gui_id) {
			Return
		}
	} else {
		genshin_hwnd := genshin_window_active(genshin_window_exist())
		WinWaitActive, ahk_id %genshin_hwnd%,, 0
		if(ErrorLevel==1)
		{
			MsgBox, 0x41010,,% game_profile_not_running_message()
			Return
		}
	}
	isBtn1Playing:=1
	isBtn1Paused:=0
	btn1update()
	startTime:=genshin_now_ms() + 250 - genshin_pause_offset
	SetKeyDelay, % yihuan_play_key_delay_ms, % yihuan_play_press_ms
	analyseNotes(Notes)
	SetTimer, genshin_main, 1
	playback_start_progress("auto")
}

genshin_main:
if(!global_mode) {
	genshin_win_hwnd:=genshin_window_exist()
}
if(genshin_pressed_p > genshin_play_array.Length() and genshin_pressed_array.Length() == 0 or (!global_mode && !genshin_win_hwnd))
{
	playback_seek_ms := playback_get_current_ms()
	if(playback_total_ms > 0 && playback_seek_ms >= playback_total_ms - 50) {
		playback_seek_ms := playback_total_ms
	}
	genshin_stop(1, 1)
	Return
}
DllCall("QueryPerformanceCounter", "Int64P",  nowTime)
; genshin_window_active(genshin_window_exist())
deltaMS:=nowTime//(freq/1000)-startTime
if(genshin_resume_array.Length() > 0 and deltaMS >= genshin_pause_offset)
{
	For _, elem in genshin_resume_array
	{
		if(global_mode) {
			if WinActive("ahk_id " domiso_active_hwnd)
			{
				note_play(elem)
			}
		} else {
			if WinActive("ahk_id " genshin_win_hwnd)
			{
				note_play(elem)
			}
		}
	}
	genshin_resume_array := Array()
}
Loop, % genshin_pressed_array.Length()
{
	elem := genshin_pressed_array[A_Index]
	if(deltaMS >= elem.delay+elem.time - 80) {
		if(global_mode) {
			if WinActive("ahk_id " domiso_active_hwnd)
			{
				note_release(elem)
			}
		} else {
			if WinActive("ahk_id " genshin_win_hwnd)
			{
				note_release(elem)
			}
		}
	}
}

genshin_prepare_p:=genshin_pressed_p
While(genshin_prepare_p <= genshin_play_array.Length() and deltaMS + 40 >= genshin_play_array[genshin_prepare_p].delay)
{
	note_release(genshin_play_array[genshin_prepare_p])
	genshin_prepare_p += 1
}
While(genshin_pressed_p <= genshin_play_array.Length() and deltaMS >= genshin_play_array[genshin_pressed_p].delay)
{
	if not genshin_play_array[genshin_pressed_p].note
	{
		genshin_pressed_p += 1
		Break
	}
	if(global_mode) {
		if WinActive("ahk_id " domiso_active_hwnd)
		{
			note_play(genshin_play_array[genshin_pressed_p])
		}
	} else {
		if WinActive("ahk_id " genshin_win_hwnd)
		{
			note_play(genshin_play_array[genshin_pressed_p])
		}
	}
	genshin_pressed_p += 1
}
Return

; 管理员权限下，无法直接使用拖入文件的功能，改由文件选择器调用此方法
GuiDropFiles(GuiHwnd, FileArray, CtrlHwnd, X, Y) {
	global hEdit1, editer, sheet_mode, plain_content, sheet_content, playback_seek_ms, playback_pending_seek_ms
	if FileArray.MaxIndex() > 1
	{
		MsgBox, 0x41010, ERROR, More than 1 file detected.
		Return
	}
	if CtrlHwnd+0=hEdit1+0
	{
		FileGetSize, size, % FileArray[1], K
		if size >= 256
		{
			MsgBox, 0x41010, ERROR, The file is too LARGE.
			Return
		}
		f:=FileOpen(FileArray[1], "r")
		if(is_dms_file(f))
		{
			sheet_mode:="cipher"
			GuiControl, +ReadOnly +Disabled, editer
			f.Seek(0)
			_temp:=Decrypt_file(f)
			plain_content:=_temp[1]
			sheet_content:=_temp[2]
		}
		Else
		{
			sheet_mode:="normal"
			GuiControl, -ReadOnly -Disabled, editer
			f.Seek(0)
			plain_content:=f.Read()
			sheet_content:=plain_content
		}
		f.Close()
		ControlSetText,, % plain_content, ahk_id %hEdit1%
		playback_seek_ms := 0
		playback_pending_seek_ms := 0
		Gosub, resolve
	}
}

genshin_play(targetMs := 0)
{
	global sendHistory, gDebug, startTime, freq, genshin_pressed_p, genshin_pressed_array
	global isBtn1Playing, global_mode, domiso_active_hwnd, gui_id
	global yihuan_play_key_delay_ms, yihuan_play_press_ms, isBtn1Paused, genshin_pause_offset, genshin_resume_array
	global playback_seek_ms, playback_pending_seek_ms
	targetMs := playback_clamp_ms(targetMs)
	genshin_pressed_array := Array()
	genshin_pressed_p := genshin_build_resume_from_offset(targetMs)
	genshin_pause_offset := targetMs
	isBtn1Paused := 0
	DllCall("QueryPerformanceCounter", "Int64P",  nowTime)
	domiso_active_hwnd:=0
	if(global_mode) {
		domiso_active_hwnd:=WinExist("A")
		if(domiso_active_hwnd == gui_id) {
			Return
		}
	} else {
		genshin_hwnd := genshin_window_active(genshin_window_exist())
		WinWaitActive, ahk_id %genshin_hwnd%,, 0
		if(ErrorLevel==1)
		{
			MsgBox, 0x41010,,% game_profile_not_running_message()
			Return
		}
	}
	isBtn1Playing:=1
	btn1update()
	startTime:=nowTime//(freq/1000) + 500 - targetMs
	playback_seek_ms := targetMs
	playback_pending_seek_ms := targetMs
	SetKeyDelay, % yihuan_play_key_delay_ms, % yihuan_play_press_ms
	if(gDebug) {
		sendHistory:=""
	}
	SetTimer, genshin_main, 1
	playback_start_progress("auto")
	playback_update_labels(targetMs, 1)
}

genshin_stop(clearPause := 1, keepPosition := 0)
{
	global isBtn1Playing, isBtn1Paused, genshin_pause_offset, genshin_resume_array, gDebug, sendHistory, Notes
	global playback_seek_ms, playback_pending_seek_ms
	isBtn1Playing:=0
	if(clearPause) {
		isBtn1Paused:=0
		genshin_pause_offset:=0
		genshin_resume_array:=Array()
	}
	if(!keepPosition) {
		playback_seek_ms := 0
		playback_pending_seek_ms := 0
	}
	btn1update()
	SetTimer, genshin_main, Off
	SetKeyDelay, -1, -1
	if(gDebug) {
		Clipboard:=sendHistory
	}
	genshin_release_all_notes()
	analyseNotes(Notes)
	playback_stop_progress()
	playback_update_labels(playback_seek_ms, 1)
}

genshin_window_exist()
{
	return game_profile_window_exist()
}

genshin_window_active(hwnd)
{
	WinActivate, ahk_id %hwnd%
	Return hwnd
}


func_btn_play:
play_request_from_current := 1
if(global_mode){
	MsgBox, 0x41010, ERROR, USE Hotkey to play in global mode`n`n全局模式请使用热键开始演奏
	Return
}
Goto, func_start_play_dispatch

func_hotkey_play:
play_request_from_current := 0
func_start_play_dispatch:
if(nonAdmin)
{
	MsgBox, 0x41010, ERROR, Can not play in non Admin Mode`n`n在非管理员模式下无法自动演奏
	Return
}
if(!isBtn1Playing)
{
	Gosub resolve
	genshin_array_sort(genshin_play_array)
	if(midi_device) {
		Gosub, func_btn_listen_stop
	}
	if(play_request_from_current) {
		genshin_play(playback_seek_ms)
	} else {
		playback_seek_ms := 0
		playback_pending_seek_ms := 0
		genshin_play(0)
	}
}
Return

no_midi_device_warning(){
	MsgBox, 0x41010, ERROR, Midi output Device not found`n`n没有找到可供试听的Midi设备
}

func_btn_listen_stop:
if(midi_device) {
	playback_seek_ms := playback_get_current_ms()
	playback_pending_seek_ms := playback_seek_ms
	Notes.Stop()
	isBtn2Playing:=0
	btn2update()
	playback_stop_progress()
	playback_update_labels(playback_seek_ms, 1)
} else {
	no_midi_device_warning()
}
Return

func_btn_listen:
if(midi_device) {
	if(!isBtn2Playing)
	{
		Gosub resolve
		; Clipboard:=output
		Notes.Start(playback_seek_ms)
		SetTimer, midi_playing_check, 1000
		isBtn2Playing:=1
		btn2update()
		playback_start_progress("listen")
		playback_update_labels(playback_seek_ms, 1)
	}
	Else
	{
		Gosub, func_btn_listen_stop
	}
} else {
	no_midi_device_warning()
}
Return

midi_playing_check:
if(isBtn2Playing){
	if(!Notes.Playing){
		playback_seek_ms := Notes.GetPosition()
		isBtn2Playing:=0
		btn2update()
		SetTimer, midi_playing_check, Off
		playback_stop_progress()
		playback_update_labels(playback_seek_ms, 1)
	}
} else {
	SetTimer, midi_playing_check, Off
}
Return

playback_progress_tick:
if(isBtn1Playing || isBtn2Playing)
{
	playback_update_labels(playback_get_current_ms())
}
else if(isBtn1Paused)
{
	playback_update_labels(genshin_pause_offset, 1)
	SetTimer, playback_progress_tick, Off
}
else
{
	playback_update_labels(playback_seek_ms, 1)
	SetTimer, playback_progress_tick, Off
}
Return

func_playback_slider:
if(playback_slider_internal)
{
	Return
}
GuiControlGet, sliderValue,, playback_slider
playback_slider_dragging := 1
playback_pending_seek_ms := playback_slider_to_ms(sliderValue)
GuiControl,, playback_elapsed_label, % playback_format_ms(playback_pending_seek_ms)
GuiControl,, playback_total_label, % playback_format_ms(playback_total_ms)
if !GetKeyState("LButton", "P")
{
	playback_slider_dragging := 0
	playback_apply_seek(playback_pending_seek_ms)
}
Return

func_game_select:
Gui, main:Submit, NoHide
newGame := game_select=2 ? "genshin" : game_select=3 ? "sky" : "yihuan"
if(newGame != current_game)
{
	if(isBtn1Playing)
		genshin_stop(1, 1)
	if(isBtn2Playing)
		Gosub, func_btn_listen_stop
	game_profile_apply(newGame)
	playback_seek_ms := 0
	playback_pending_seek_ms := 0
	Gosub, resolve
	statubar_txt("Game: " current_game_name)
}
Return

func_btn_file:
Thread, NoTimers
FileSelectFile, select_file, 1, , Title, DoMiSo Sheet (*.txt; *.dms)
Thread, NoTimers, false
if select_file
{
	GuiDropFiles(0, [select_file], hEdit1, 0, 0)
}
Return

func_btn_publish:
if(sheet_mode!="normal")
{
	Return
}
Gui, main:Submit, NoHide
pub_txt:=editer
If Encrypt_dms_valid(pub_txt)!=1
{
	MsgBox, 0x41010, Wrong, No Publish Mark detected.
	Return
}
pub_filename:=Encrypt_dms_enc(pub_txt)
MsgBox, 0x1040, Success, % "Published as 【" pub_filename "】"
Return

func_btn_exit:
Exit:
ExitApp

winMove:
PostMessage, 0xA1, 2
Return

resolve:
Gui, main:Submit, NoHide
load_yihuan_play_settings()
_Instrument:=instrument_select-1
if(sheet_mode=="normal")
{
	sheet_content:=editer

}
parse_content:=sheet_content
if(sheet_mode="normal")
{
	If Encrypt_dms_valid(sheet_content)=1
	{
		parse_content:=dms_parser(sheet_content)[2]
	}
}

total_beats:=0
genshin_play_array:={}
genshin_output:=""
genshin_delay:=0
genshin_play_report := {"count": 0, "merged": 0, "peak": 0, "minGap": 0}

arpeggio_start:=0	;琶音起始
; NOTE: 由于存在变速的情况，无法简单的计算整首曲子的拍子数，此处处理了琶音产生的拍子计数错误
; TODO: 增加设定琶音延时的语法
arpeggio_delay_set:=40	;琶音递增延时
arpeggio_delay:=0	;琶音累计延时

output:=""
Notes.Reset()
if(_Instrument<0 or _Instrument>127){
	_Instrument:=0
}
Notes.Instrument(_Instrument)
base:=60
beatTime:=Round(60000/80, 2)
Loop, Parse, parse_content, `n,`r%A_Space%%A_Tab%	;逐行解析
{
	chord:=0	;重置和弦标记
	chordTime:=0	;重置和弦长度
	multiplet:=0	;重置多连音标记
	this_chord_beats:=0
	
	If(RegExMatch(A_LoopField,"iO)(?:b|B)(?:p|P)(?:m|M)=(\d+)",o))	;解析bpm标记
	{
		bpm_parser(o)
	}
;~ 	MsgBox, % NoteData
	If(RegExMatch(A_LoopField,"iO)1=([A-G]\d?\d?\#?|b?)",p))	;解析调号标记
	{
		tone_parser(p)
	}
	
	If(RegExMatch(A_LoopField,"iO)rollback=(\d+\.?\d*)",r))	;解析rollback标记
	{
		rollback_parser(r)
	}
	
	/*
	琶音 arpeggio
	音阶 scale
	音符 note
	升降调 semitone
	时值 notelen
	*/
	
	currentLine:=A_LoopField
	Loop, Parse, currentLine, %A_Space%%A_Tab%
	{
		If(RegExMatch(A_LoopField,"iSO)^(?P<arpeggio>\~)?(?P<scale>\-*|\+*)(?P<note>[0-7])(?P<semitone>\#|b)?(?P<notelen>(?:\/|\-|\.)*)\s?$",tune))	;解析音符
		{
			note_parser(tune)
		}
		If(RegExMatch(A_LoopField,"iSO)(\(|\{)",mark))	;解析左括号
		{
			bracket_start_parser(mark)
		}
		If(RegExMatch(A_LoopField,"iSO)(\)|\})((?:\/|\-|\.)*)\s?$",mark))	;解析右括号
		{
			bracket_end_parser(mark)
		}
	}
}
Notes.total_beats:=total_beats
genshin_array_sort(genshin_play_array)
genshin_play_report := optimize_genshin_play_array(genshin_play_array)
; Clipboard:=genshin_output
; 统计音符并显示到状态栏
analyseNotes(Notes)
playback_refresh_after_resolve()
Return

bpm_parser(obj)
{
	global
	If(o.Value(1)>30 And o.Value(1)<600)
	beatTime:=Round(60000/o.Value(1), 2)
}

tone_parser(obj)
{
	global
	If(RegExMatch(NoteData,"(\d\d?\d?)\s" obj.Value(1) "\s",q))
	base:=q1	
}

rollback_parser(obj)
{
	global
	If(obj.Value(1)*beatTime<=Notes.Offset)
	{
		Notes.Delay(-obj.Value(1)*beatTime)
		output.="Notes.Delay(" -obj.Value(1)*beatTime ")`n"
		genshin_delay -= obj.Value(1)*beatTime
	}
	Else
	{
		Notes.Offset:=0
		output.="Notes.Offset:=0`n"
		genshin_delay := 0
	}
}

note_parser(tune)
{
	global
	noteTime:=beatTime
	
	If(tune.Value("scale")!="")	;解析八度偏移量
	{
		If InStr(tune.Value("scale"), "-")
		offs:=-StrLen(tune.Value("scale"))
		Else If InStr(tune.Value("scale"), "+")
		offs:=StrLen(tune.Value("scale"))
		Else offs:=0
	}
	Else offs:=0
	
	noteTune:=base+baseOffset[tune.Value("note")+0]+offs*12	;解析基本音
	
	If(tune.Value("semitone")!="")	;解析升降调
	{
		If InStr(tune.Value("semitone"), "#"){
			noteTune+=1
		}
		Else If InStr(tune.Value("semitone"), "b"){
			noteTune-=1
		}
	}

;~ 			If(tune.Value(4)!="")	;解析基本音符长度
	If(1)
	{
		noteTime:=extra_length_parser(beatTime, tune.Value("notelen"))
		this_note_beats:=noteTime/beatTime
	}
	if(chord=1) {
		if(noteTune>0) {
			chord_cache.Push({"note":noteTune,"time":noteTime})
			chordTime:=noteTime>chordTime ? noteTime : chordTime
		}
	} else if(multiplet=1) {
		multiplet_cache.Push({"note":noteTune,"time":noteTime})
	} else {
		is_arpeggio := false
		If(tune.Value("arpeggio")!="")	;解析琶音标记
		{
			if(noteTime<=arpeggio_delay+20) {
				Return
			}
			is_arpeggio := true
			Notes.Delay(-last_noteTime)
			Notes.Delay(arpeggio_delay_set)
			genshin_delay+=arpeggio_delay_set-last_noteTime
			arpeggio_delay+=arpeggio_delay_set
			noteTime-=arpeggio_delay
		} else {
			arpeggio_start:=genshin_delay
			arpeggio_delay:=0
		}
		if(noteTune>0) {
			Notes.Note(noteTune,noteTime,50).Delay(noteTime)
			output.="Notes.Note(" noteTune "," noteTime ",50).Delay(" noteTime ")`n"
			queue_game_note(noteTune, noteTime)
		} else {
			Notes.Delay(noteTime)
			output.="Notes.Delay(" noteTime ")`n"
		}
		genshin_delay += noteTime
		if(!is_arpeggio) {
			total_beats += this_note_beats
		}
	}
	last_noteTime:=noteTime
}

bracket_start_parser(obj)
{
	global
	If(mark.Value(1)="(" And chord=0)
	{
		chord:=1
		chord_cache:={}
		chordTime:=0
		this_chord_beats:=0
	}
	If(mark.Value(1)="{" And multiplet=0)
	{
		multiplet:=1
		multiplet_cache:={}
	}
}
; 解析额外长度标记
extra_length_parser(basetime, src)
{
	global beatTime
	s := 1
	p := RegExMatch(src, "iO)(\/+|\-+|\.+)", obj, s)
	lastBase := beatTime
	while(p)
	{
		if(InStr(obj.Value(1), "/"))
		{
			_t := lastBase / 2**obj.Len(1)
			basetime := basetime - lastBase + _t
			lastBase := _t
		} else if(InStr(obj.Value(1), "-")) {
			basetime += beatTime*obj.Len(1)
			lastBase := beatTime
		} else {
			db:=lastBase
			Loop, % obj.Len(1)
			{
				db *= 0.5
				basetime += db
			}
		}
		s += obj.Len(1)
		p := RegExMatch(src, "iO)(\/+|\-+|\.+)", obj, s)
	}
	return basetime
}
bracket_end_parser(mark)
{
	global
	local d,p,s,obj,db,mlen,mk,mtime
	If(mark.Value(1)=")" And chord=1)
	{
		chord:=0
		if(mark.Value(2)!="")
		{
			chordTime := extra_length_parser(chordTime, mark.Value(2))
		}
		Loop, % chord_cache.Length()
		{
			Notes.Note(chord_cache[A_Index].note, chordTime, 50)
			; chord_cache[A_Index].time
			output.="Notes.Note(" chord_cache[A_Index].note "," chordTime ",50)`n"
			queue_game_note(chord_cache[A_Index].note, chordTime)
		}
		Notes.Delay(chordTime)
		chord:=0
		output.="Notes.Delay(" chordTime ")`n"
		genshin_delay += chordTime
		this_chord_beats := chordTime/beatTime
		total_beats += this_chord_beats
	}
	If(mark.Value(1)="}" And multiplet=1)
	{
		multiplet:=0
		mtime:=beatTime
		if(mark.Value(2)!="")
		{
			mtime := extra_length_parser(mtime, mark.Value(2))
		}
		mlen:=0
		Loop, % multiplet_cache.Length()
		{
			mlen+=multiplet_cache[A_Index].time
		}
		mk:=mtime/mlen
		Loop, % multiplet_cache.Length()
		{
			if(multiplet_cache[A_Index].note > 0) {
				Notes.Note(multiplet_cache[A_Index].note, mk*multiplet_cache[A_Index].time, 50)
				queue_game_note(multiplet_cache[A_Index].note, mk*multiplet_cache[A_Index].time)
			}
			Notes.Delay(mk*multiplet_cache[A_Index].time)
			output.="Notes.Note(" multiplet_cache[A_Index].note "," mk*multiplet_cache[A_Index].time ",50)`n"
			genshin_delay+=mk*multiplet_cache[A_Index].time
		}
		total_beats += mtime/beatTime
	}
}

UAC()
{
	full_command_line := DllCall("GetCommandLine", "str")
	if not (A_IsAdmin or RegExMatch(full_command_line, " /restart(?!\S)"))
	{
		try
		{
			if A_IsCompiled
				Run *RunAs "%A_ScriptFullPath%" /restart
			else
				Run *RunAs "%A_AhkPath%" /restart "%A_ScriptFullPath%"
		}
		ExitApp
	}
}

free(ByRef var)
{
	VarSetCapacity(var, 0)
}

GuiClose:
ExitApp

TrueExit:
IniWrite, % _Instrument, setting.ini, update, inst
IniWrite, % version, setting.ini, update, ver
log_flush()
ExitApp

;@Ahk2Exe-IgnoreBegin
F5::ExitApp
F6::Reload
;@Ahk2Exe-IgnoreEnd

F7::genshin_pause()
F8::genshin_stop()
F9::Gosub, func_hotkey_play
F10::genshin_resume()

#include menu.ahk
