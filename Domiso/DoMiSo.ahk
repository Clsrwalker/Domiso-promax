
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
live_playhead_ms:=0
live_last_tick_ms:=0
live_speed_offset_target_percent:=0
live_speed_offset_current_percent:=0
live_speed_step_percent:=2
live_speed_max_offset_percent:=50
live_speed_smoothing_ms:=120
live_target_offset_ms:=0
live_applied_offset_ms:=0
live_phase_rate:=0
live_phase_kp:=0.45
live_phase_max_rate:=0.05
live_phase_held_max_rate:=0.10
live_phase_smoothing_ms:=60
live_phase_deadband_ms:=1.5
live_phase_hold_delay_ms:=300
live_phase_held_interval_ms:=140
live_phase_hold_key:=""
live_phase_hold_direction:=0
live_phase_hold_started_ms:=0
live_phase_jog_rate:=0
live_control_status_until_ms:=0
live_control_status_last_ms:=0
live_control_status_kind:=""
beat_time_markers:=Array()
sky_play_hold_min_ms:=100
sky_play_same_key_gap_ms:=75
sky_play_key_delay_ms:=8
sky_play_press_ms:=40
sky_play_release_lead_min_ms:=20
sky_play_release_lead_max_ms:=50
sky_play_release_lead_ratio:=0.25
txt_list_paths:=Array()
txt_list_index:=0
hTxtListGui:=0
hTxtListBox:=0
txt_list_main_hidden:=0

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
txt_list_load_settings()

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
		statusTxt .= " | hold min " play_hold_min_ms() "ms"
		if(genshin_play_report.merged > 0) {
			statusTxt .= " | merge " genshin_play_report.merged
		}
	}
	statubar_txt(statusTxt)
}

score_speed_format(value)
{
	value += 0
	rounded := Round(value, 1)
	if(Abs(rounded - Round(rounded)) < 0.05) {
		return Round(rounded)
	}
	return rounded
}

score_speed_apply(value, update_control := 0)
{
	global yihuan_play_speed_percent, yihuan_play_time_scale
	text := Trim(value)
	if(!RegExMatch(text, "O)^\d+(?:\.\d+)?$")) {
		text := "100"
	}
	speed := text + 0.0
	if(speed < 50) {
		speed := 50
	} else if(speed > 150) {
		speed := 150
	}
	yihuan_play_speed_percent := Round(speed, 1)
	yihuan_play_time_scale := 100.0 / yihuan_play_speed_percent
	if(update_control) {
		GuiControl, main:, score_speed_input, % score_speed_format(yihuan_play_speed_percent)
	}
}

score_speed_reset()
{
	score_speed_apply(100, 1)
	live_speed_reset()
	live_phase_reset()
}

live_speed_reset()
{
	global live_speed_offset_target_percent, live_speed_offset_current_percent
	live_speed_offset_target_percent := 0
	live_speed_offset_current_percent := 0
}

live_phase_reset()
{
	global live_target_offset_ms, live_applied_offset_ms, live_phase_rate
	global live_phase_jog_rate, live_phase_hold_key, live_phase_hold_direction, live_phase_hold_started_ms
	live_target_offset_ms := 0
	live_applied_offset_ms := 0
	live_phase_rate := 0
	live_phase_jog_rate := 0
	live_phase_hold_key := ""
	live_phase_hold_direction := 0
	live_phase_hold_started_ms := 0
	SetTimer, live_phase_hold_tick, Off
}

live_clock_start(positionMs, resetSpeed := 1, startDelayMs := 0)
{
	global live_playhead_ms, live_last_tick_ms
	live_playhead_ms := playback_clamp_ms(positionMs)
	live_last_tick_ms := genshin_now_ms() + startDelayMs
	if(resetSpeed) {
		live_speed_reset()
		live_phase_reset()
	}
}

live_clock_tick(nowMs := "")
{
	global live_playhead_ms, live_last_tick_ms
	global live_speed_offset_target_percent, live_speed_offset_current_percent
	global live_speed_smoothing_ms, yihuan_play_speed_percent
	global live_target_offset_ms, live_applied_offset_ms, live_phase_rate
	global live_phase_kp, live_phase_max_rate, live_phase_held_max_rate
	global live_phase_smoothing_ms, live_phase_deadband_ms, live_phase_jog_rate
	global live_control_status_until_ms, live_control_status_last_ms, live_control_status_kind
	if(nowMs = "") {
		nowMs := genshin_now_ms()
	}
	if(live_last_tick_ms <= 0) {
		live_last_tick_ms := nowMs
	}
	dtMs := nowMs - live_last_tick_ms
	if(dtMs <= 0) {
		return playback_clamp_ms(live_playhead_ms)
	}
	smoothTau := Max(1, live_speed_smoothing_ms)
	alpha := 1 - Exp(-dtMs / smoothTau)
	live_speed_offset_current_percent += (live_speed_offset_target_percent - live_speed_offset_current_percent) * alpha
	baseSpeed := Max(1, yihuan_play_speed_percent + 0.0)
	phaseBeatMs := live_current_beat_ms(live_playhead_ms)
	if(live_phase_jog_rate != 0) {
		live_target_offset_ms += live_phase_jog_rate * dtMs
	}
	phaseErrorMs := live_target_offset_ms - live_applied_offset_ms
	desiredPhaseRate := live_phase_jog_rate + live_phase_kp * (phaseErrorMs / phaseBeatMs)
	phaseLimit := live_phase_jog_rate != 0 ? live_phase_held_max_rate : live_phase_max_rate
	if(desiredPhaseRate > phaseLimit) {
		desiredPhaseRate := phaseLimit
	} else if(desiredPhaseRate < -phaseLimit) {
		desiredPhaseRate := -phaseLimit
	}
	phaseTau := Max(1, live_phase_smoothing_ms)
	phaseAlpha := 1 - Exp(-dtMs / phaseTau)
	live_phase_rate += (desiredPhaseRate - live_phase_rate) * phaseAlpha
	live_applied_offset_ms += live_phase_rate * dtMs
	if(Abs(phaseErrorMs) < live_phase_deadband_ms && Abs(live_phase_rate) < 0.001) {
		live_applied_offset_ms := live_target_offset_ms
		live_phase_rate := 0
	}
	rate := (baseSpeed + live_speed_offset_current_percent) / baseSpeed + live_phase_rate
	if(rate < 0.1) {
		rate := 0.1
	}
	live_playhead_ms += dtMs * rate
	live_last_tick_ms := nowMs
	if(live_control_status_until_ms > nowMs && nowMs - live_control_status_last_ms >= 200) {
		live_control_status_last_ms := nowMs
		live_control_status(live_control_status_kind, 0)
	}
	return playback_clamp_ms(live_playhead_ms)
}

live_speed_adjust(direction)
{
	global live_speed_offset_target_percent, live_speed_step_percent, live_speed_max_offset_percent
	live_speed_offset_target_percent += direction * live_speed_step_percent
	if(live_speed_offset_target_percent > live_speed_max_offset_percent) {
		live_speed_offset_target_percent := live_speed_max_offset_percent
	} else if(live_speed_offset_target_percent < -live_speed_max_offset_percent) {
		live_speed_offset_target_percent := -live_speed_max_offset_percent
	}
	live_control_status("speed")
}

live_speed_home()
{
	global live_speed_offset_target_percent
	live_speed_offset_target_percent := 0
	live_control_status("speed")
}

live_format_signed(value, decimals := 1)
{
	value += 0
	rounded := Round(value, decimals)
	if(Abs(rounded - Round(rounded)) < 0.05) {
		rounded := Round(rounded)
	}
	return (rounded > 0 ? "+" : "") rounded
}

live_control_status(kind := "", pinMs := 1600)
{
	global live_speed_offset_target_percent, live_speed_offset_current_percent, live_target_offset_ms, live_applied_offset_ms
	global live_phase_rate, yihuan_play_speed_percent
	global live_control_status_until_ms, live_control_status_last_ms, live_control_status_kind
	if(pinMs > 0) {
		nowMs := genshin_now_ms()
		live_control_status_until_ms := nowMs + pinMs
		live_control_status_last_ms := nowMs
		live_control_status_kind := kind
	}
	if(kind="phase") {
		statubar_txt("Live phase target " live_format_signed(live_target_offset_ms, 0) "ms | current " live_format_signed(live_applied_offset_ms, 0) "ms | rate " live_format_signed(live_phase_rate * 100, 1) "%")
		return
	}
	baseSpeed := Max(1, yihuan_play_speed_percent + 0.0)
	totalRate := ((baseSpeed + live_speed_offset_current_percent) / baseSpeed + live_phase_rate) * 100
	statubar_txt("Live speed target " live_format_signed(live_speed_offset_target_percent, 1) "% | current " live_format_signed(live_speed_offset_current_percent, 1) "% | rate " Round(totalRate, 1) "%")
}

live_phase_step_ms(fine := 0)
{
	beatMs := live_current_beat_ms()
	if(fine) {
		stepMs := beatMs * 0.025
		if(stepMs < 8) {
			stepMs := 8
		} else if(stepMs > 18) {
			stepMs := 18
		}
	} else {
		stepMs := beatMs * 0.08
		if(stepMs < 20) {
			stepMs := 20
		} else if(stepMs > 50) {
			stepMs := 50
		}
	}
	return stepMs
}

live_current_beat_ms(positionMs := "")
{
	global beat_time_markers, yihuan_play_time_scale, live_playhead_ms
	if(positionMs = "") {
		positionMs := live_playhead_ms
	}
	scale := yihuan_play_time_scale + 0.0
	if(scale <= 0) {
		scale := 1.0
	}
	rawPositionMs := (positionMs + 0.0) / scale
	currentBeatMs := 750.0
	if(IsObject(beat_time_markers)) {
		Loop, % beat_time_markers.Length()
		{
			marker := beat_time_markers[A_Index]
			if(marker.delay <= rawPositionMs) {
				currentBeatMs := marker.beatMs
			}
		}
	}
	return Max(1, currentBeatMs * scale)
}

live_phase_nudge(direction, fine := 0)
{
	global live_target_offset_ms
	stepMs := live_phase_step_ms(fine)
	live_target_offset_ms += direction * stepMs
	live_control_status("phase")
}

live_phase_compute_jog_rate(direction)
{
	global live_phase_held_interval_ms, live_phase_held_max_rate
	rawRate := live_phase_step_ms(1) / Max(1, live_phase_held_interval_ms)
	if(rawRate > live_phase_held_max_rate) {
		rawRate := live_phase_held_max_rate
	}
	return direction * rawRate
}

live_phase_key_down(direction, fine, keyName)
{
	global live_phase_hold_key, live_phase_hold_direction, live_phase_hold_started_ms, live_phase_jog_rate
	if(live_phase_hold_key != "") {
		return
	}
	live_phase_nudge(direction, fine)
	live_phase_hold_key := keyName
	live_phase_hold_direction := direction
	live_phase_hold_started_ms := genshin_now_ms()
	live_phase_jog_rate := 0
	SetTimer, live_phase_hold_tick, 20
}

live_phase_hold_tick:
if(!isBtn1Playing || live_phase_hold_key = "")
{
	live_phase_jog_rate := 0
	live_phase_hold_key := ""
	live_phase_hold_direction := 0
	live_phase_hold_started_ms := 0
	SetTimer, live_phase_hold_tick, Off
	Return
}
if(!GetKeyState(live_phase_hold_key, "P"))
{
	live_phase_jog_rate := 0
	live_phase_hold_key := ""
	live_phase_hold_direction := 0
	live_phase_hold_started_ms := 0
	SetTimer, live_phase_hold_tick, Off
	Return
}
if(genshin_now_ms() - live_phase_hold_started_ms >= live_phase_hold_delay_ms)
{
	if(live_phase_jog_rate = 0) {
		live_phase_jog_rate := live_phase_compute_jog_rate(live_phase_hold_direction)
		live_control_status("phase")
	} else {
		live_phase_jog_rate := live_phase_compute_jog_rate(live_phase_hold_direction)
	}
}
Return

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
	global isBtn1Playing, isBtn1Paused, isBtn2Playing, genshin_pause_offset, Notes, playback_seek_ms
	if(isBtn1Playing) {
		return playback_clamp_ms(live_clock_tick())
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
		genshin_play(targetMs, 0)
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

load_yihuan_play_settings(update_speed_control := 0)
{
	global score_speed_input, yihuan_play_speed_percent, yihuan_play_time_scale, yihuan_play_hold_min_ms
	global yihuan_play_same_key_gap_ms, yihuan_play_key_delay_ms, yihuan_play_press_ms

	if(score_speed_input != "") {
		score_speed_apply(score_speed_input, update_speed_control)
	} else {
		score_speed_apply(100, update_speed_control)
	}

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

play_hold_min_ms()
{
	global current_game, yihuan_play_hold_min_ms, sky_play_hold_min_ms
	if(current_game="sky")
		return sky_play_hold_min_ms
	return yihuan_play_hold_min_ms
}

play_same_key_gap_ms()
{
	global current_game, yihuan_play_same_key_gap_ms, sky_play_same_key_gap_ms
	if(current_game="sky")
		return sky_play_same_key_gap_ms
	return yihuan_play_same_key_gap_ms
}

play_key_delay_ms()
{
	global current_game, yihuan_play_key_delay_ms, sky_play_key_delay_ms
	if(current_game="sky")
		return sky_play_key_delay_ms
	return yihuan_play_key_delay_ms
}

play_key_press_ms()
{
	global current_game, yihuan_play_press_ms, sky_play_press_ms
	if(current_game="sky")
		return sky_play_press_ms
	return yihuan_play_press_ms
}

play_release_lead_ms(noteTime)
{
	global current_game, sky_play_release_lead_min_ms, sky_play_release_lead_max_ms, sky_play_release_lead_ratio
	if(current_game!="sky")
		return 80
	lead := Round(noteTime * sky_play_release_lead_ratio)
	if(lead < sky_play_release_lead_min_ms)
		lead := sky_play_release_lead_min_ms
	if(lead > sky_play_release_lead_max_ms)
		lead := sky_play_release_lead_max_ms
	if(noteTime > 30 && lead > noteTime - 20)
		lead := Max(0, noteTime - 20)
	return lead
}

optimize_genshin_play_array(ByRef array)
{
	global yihuan_play_time_scale
	out := Array()
	lastByKey := {}
	merged := 0
	sameKeyGapMs := play_same_key_gap_ms()

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
			if(gap >= 0 && gap < sameKeyGapMs)
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
	global sendHistory, deltaMS, genshin_pressed_array, gDebug
	send_key:=""
	holdMinMs := play_hold_min_ms()
	if (elem.HasKey("resume") || elem.time >= holdMinMs)
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
	global genshin_play_array, genshin_resume_array
	targetMs := playback_clamp_ms(targetMs)
	genshin_resume_array := Array()
	nextIndex := 1
	holdMinMs := play_hold_min_ms()
	Loop, % genshin_play_array.Length()
	{
		ev := genshin_play_array[A_Index]
		if(ev.delay < targetMs)
		{
			remainingTime := Round(ev.delay + ev.time - targetMs)
			if(ev.time >= holdMinMs && remainingTime > 40)
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
	genshin_pause_offset := playback_get_current_ms()
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
	global genshin_pause_offset, Notes
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
	live_clock_start(genshin_pause_offset, 0, 250)
	keyDelayMs := play_key_delay_ms()
	keyPressMs := play_key_press_ms()
	SetKeyDelay, %keyDelayMs%, %keyPressMs%
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
deltaMS:=live_clock_tick(nowTime//(freq/1000))
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
	releaseLeadMs := play_release_lead_ms(elem.time)
	if(deltaMS >= elem.delay+elem.time - releaseLeadMs) {
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
	global hEdit1, hTxtListGui, hTxtListBox
	if CtrlHwnd+0=hEdit1+0
	{
		if FileArray.MaxIndex() > 1
		{
			MsgBox, 0x41010, ERROR, More than 1 file detected.
			Return
		}
		score_load_file(FileArray[1])
		Return
	}
	if((hTxtListGui && GuiHwnd+0=hTxtListGui+0) || (hTxtListBox && CtrlHwnd+0=hTxtListBox+0))
	{
		added := txt_list_add_dropped(FileArray)
		statubar_txt("TXT List: added " added)
		Return
	}
}

score_load_file(path)
{
	global hEdit1, editer, sheet_mode, plain_content, sheet_content, playback_seek_ms, playback_pending_seek_ms
	if(!FileExist(path))
	{
		MsgBox, 0x41010, ERROR, Sheet file not found.
		Return 0
	}
	FileGetSize, size, %path%, K
	if size >= 256
	{
		MsgBox, 0x41010, ERROR, The file is too LARGE.
		Return 0
	}
	f:=FileOpen(path, "r")
	if(!IsObject(f))
	{
		MsgBox, 0x41010, ERROR, Can not open sheet file.
		Return 0
	}
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
	score_speed_reset()
	playback_seek_ms := 0
	playback_pending_seek_ms := 0
	Gosub, resolve
	Return 1
}

txt_list_load_settings()
{
	global txt_list_paths, txt_list_index
	txt_list_paths:=Array()
	IniRead, count, setting.ini, txtlist, count, 0
	count += 0
	Loop, %count%
	{
		key := "item" A_Index
		IniRead, p, setting.ini, txtlist, %key%,
		if(p!="" && FileExist(p))
			txt_list_add_path(p, 0)
	}
	IniRead, idx, setting.ini, txtlist, index, 0
	txt_list_index := idx + 0
	if(txt_list_index < 1 || txt_list_index > txt_list_paths.Length())
		txt_list_index := txt_list_paths.Length() ? 1 : 0
}

txt_list_save_settings()
{
	global txt_list_paths, txt_list_index
	IniDelete, setting.ini, txtlist
	IniWrite, % txt_list_paths.Length(), setting.ini, txtlist, count
	IniWrite, % txt_list_index, setting.ini, txtlist, index
	Loop, % txt_list_paths.Length()
	{
		key := "item" A_Index
		IniWrite, % txt_list_paths[A_Index], setting.ini, txtlist, %key%
	}
}

txt_list_show()
{
	global hTxtListGui, hTxtListBox, txt_list_box, txt_list_status
	txt_list_hide_main()
	if(hTxtListGui)
	{
		Gui, txtlist:Show
		txt_list_refresh(0)
		Return
	}
	Gui, txtlist:New, +Resize +MinSize700x460 +HwndhTxtListGui, TXT List
	Gui, txtlist:+Delimiter|
	Gui, txtlist:Color, F7F1E6
	Gui, txtlist:Font, s9 c4B3827, Segoe UI
	Gui, txtlist:Add, Text, x18 y14 w180 h32 +0x200, TXT List
	Gui, txtlist:Add, Text, x220 y14 w462 h32 Right +0x200 vtxt_list_status
	Gui, txtlist:Font, s9 c163746, Segoe UI
	Gui, txtlist:Add, ListBox, x18 y56 w664 h284 AltSubmit vtxt_list_box gtxt_list_select hwndhTxtListBox
	Gui, txtlist:Add, Button, x18 y358 w108 h42 gtxt_list_add_files, Add
	Gui, txtlist:Add, Button, x136 y358 w108 h42 gtxt_list_add_folder, Folder
	Gui, txtlist:Add, Button, x254 y358 w108 h42 gtxt_list_prev, Prev
	Gui, txtlist:Add, Button, x372 y358 w108 h42 gtxt_list_next, Next
	Gui, txtlist:Add, Button, x490 y358 w108 h42 gtxt_list_load, Load
	Gui, txtlist:Add, Button, x18 y410 w108 h42 gtxt_list_remove, Remove
	Gui, txtlist:Add, Button, x136 y410 w108 h42 gtxt_list_clear, Clear
	Gui, txtlist:Add, Button, x574 y410 w108 h42 gtxt_list_close, Close
	txt_list_refresh(0)
	Gui, txtlist:Show, w700 h470 Center
}

txt_list_hide_main()
{
	global gui_id, txt_list_main_hidden
	if(!gui_id)
		Return
	WinSet, AlwaysOnTop, Off, ahk_id %gui_id%
	Gui, main:Hide
	txt_list_main_hidden := 1
}

txt_list_restore_main(restoreTopmost := 1, activateGame := 0)
{
	global gui_id, txt_list_main_hidden
	if(!txt_list_main_hidden)
		Return
	Gui, main:Show, NoActivate
	if(gui_id)
	{
		mode := restoreTopmost ? "On" : "Off"
		WinSet, AlwaysOnTop, %mode%, ahk_id %gui_id%
	}
	txt_list_main_hidden := 0
	if(activateGame)
	{
		gameHwnd := game_profile_window_exist()
		if(gameHwnd)
			WinActivate, ahk_id %gameHwnd%
	}
}

main_show()
{
	global gui_id, txt_list_main_hidden
	Gui, main:Show
	if(gui_id)
		WinSet, AlwaysOnTop, On, ahk_id %gui_id%
	txt_list_main_hidden := 0
}

txt_list_hide()
{
	Gui, txtlist:Hide
	txt_list_restore_main(0, 1)
}

txt_list_current_dir()
{
	IniRead, lastDir, setting.ini, txtlist, lastDir, % A_ScriptDir "\..\txt"
	if(!InStr(FileExist(lastDir), "D"))
		lastDir := "D:\domiso\txt"
	if(!InStr(FileExist(lastDir), "D"))
		lastDir := A_ScriptDir
	Return lastDir
}

txt_list_add_path(path, save := 1)
{
	global txt_list_paths, txt_list_index
	if(path="" || !FileExist(path))
		Return 0
	SplitPath, path,,, ext
	StringLower, ext, ext
	if(ext!="txt" && ext!="dms")
		Return 0
	pathKey := path
	StringLower, pathKey, pathKey
	Loop, % txt_list_paths.Length()
	{
		existing := txt_list_paths[A_Index]
		StringLower, existing, existing
		if(existing=pathKey)
			Return 0
	}
	txt_list_paths.Push(path)
	if(txt_list_index=0)
		txt_list_index := 1
	if(save)
		txt_list_save_settings()
	Return 1
}

txt_list_add_paths(paths)
{
	added := 0
	for _, p in paths
		added += txt_list_add_path(p, 0)
	txt_list_save_settings()
	txt_list_refresh(0)
	Return added
}

txt_list_add_dropped(fileArray)
{
	added := 0
	Loop, % fileArray.MaxIndex()
	{
		p := fileArray[A_Index]
		if(InStr(FileExist(p), "D"))
			added += txt_list_add_folder_path(p)
		else
			added += txt_list_add_path(p, 0)
	}
	txt_list_save_settings()
	txt_list_refresh(0)
	Return added
}

txt_list_parse_file_selection(selected)
{
	files:=Array()
	lines:=Array()
	Loop, Parse, selected, `n, `r
	{
		if(A_LoopField!="")
			lines.Push(A_LoopField)
	}
	if(lines.Length()=0)
		Return files
	if(lines.Length()>1 && InStr(FileExist(lines[1]), "D"))
	{
		baseDir := lines[1]
		Loop, % lines.Length()-1
			files.Push(baseDir "\" lines[A_Index+1])
	}
	Else
	{
		Loop, % lines.Length()
			files.Push(lines[A_Index])
	}
	Return files
}

txt_list_add_folder_path(folder)
{
	paths := ""
	pattern := folder "\*.txt"
	Loop, Files, %pattern%, F
		paths .= A_LoopFileFullPath "`n"
	pattern := folder "\*.dms"
	Loop, Files, %pattern%, F
		paths .= A_LoopFileFullPath "`n"
	Sort, paths
	files:=Array()
	Loop, Parse, paths, `n, `r
	{
		if(A_LoopField!="")
			files.Push(A_LoopField)
	}
	Return txt_list_add_paths(files)
}

txt_list_display_name(path, index)
{
	SplitPath, path, name
	if(name="")
		name := path
	prefix := FileExist(path) ? "" : "[missing] "
	line := index ". " prefix name
	StringReplace, line, line, |, /, All
	Return line
}

txt_list_refresh(save := 1)
{
	global txt_list_paths, txt_list_index, hTxtListGui
	if(txt_list_index < 1 || txt_list_index > txt_list_paths.Length())
		txt_list_index := txt_list_paths.Length() ? 1 : 0
	if(hTxtListGui)
	{
		items := "|"
		Loop, % txt_list_paths.Length()
			items .= txt_list_display_name(txt_list_paths[A_Index], A_Index) "|"
		GuiControl, txtlist:, txt_list_box, %items%
		if(txt_list_index>0)
			GuiControl, txtlist:Choose, txt_list_box, %txt_list_index%
		txt_list_update_status()
	}
	if(save)
		txt_list_save_settings()
}

txt_list_update_status()
{
	global txt_list_paths, txt_list_index, hTxtListGui
	if(!hTxtListGui)
		Return
	count := txt_list_paths.Length()
	if(count=0)
		txt := "No files"
	else
		txt := txt_list_index "/" count
	GuiControl, txtlist:, txt_list_status, %txt%
}

txt_list_get_selected_index()
{
	global txt_list_paths, txt_list_index, hTxtListGui
	idx := 0
	if(hTxtListGui && WinExist("ahk_id " hTxtListGui))
	{
		GuiControlGet, idx, txtlist:, txt_list_box
		idx += 0
	}
	if(idx < 1)
		idx := txt_list_index + 0
	if(idx < 1 && txt_list_paths.Length())
		idx := 1
	if(idx > txt_list_paths.Length())
		idx := txt_list_paths.Length()
	Return idx
}

txt_list_stop_for_load()
{
	global isBtn1Playing, isBtn1Paused, isBtn2Playing, Notes, playback_seek_ms, playback_pending_seek_ms
	if(isBtn1Playing || isBtn1Paused)
		genshin_stop(1, 0)
	if(isBtn2Playing)
	{
		Notes.Stop()
		isBtn2Playing:=0
		btn2update()
		SetTimer, midi_playing_check, Off
		playback_stop_progress()
	}
	playback_seek_ms := 0
	playback_pending_seek_ms := 0
}

txt_list_load_index(idx)
{
	global txt_list_paths, txt_list_index
	if(idx < 1 || idx > txt_list_paths.Length())
	{
		statubar_txt("TXT List: no file selected")
		Return 0
	}
	path := txt_list_paths[idx]
	if(!FileExist(path))
	{
		statubar_txt("TXT List: missing file")
		Return 0
	}
	txt_list_index := idx
	txt_list_save_settings()
	txt_list_refresh(0)
	txt_list_stop_for_load()
	if(score_load_file(path))
	{
		SplitPath, path, name
		statubar_txt("Loaded: " name)
		Return 1
	}
	Return 0
}

txt_list_step(direction)
{
	global txt_list_paths
	count := txt_list_paths.Length()
	if(count=0)
	{
		statubar_txt("TXT List is empty")
		Return
	}
	idx := txt_list_get_selected_index()
	if(idx < 1)
		idx := 1
	idx += direction
	if(idx > count)
		idx := 1
	else if(idx < 1)
		idx := count
	txt_list_load_index(idx)
}

genshin_play(targetMs := 0, resetLive := 1)
{
	global sendHistory, gDebug, startTime, freq, genshin_pressed_p, genshin_pressed_array
	global isBtn1Playing, global_mode, domiso_active_hwnd, gui_id
	global isBtn1Paused, genshin_pause_offset, genshin_resume_array
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
	live_clock_start(targetMs, resetLive, 500)
	playback_seek_ms := targetMs
	playback_pending_seek_ms := targetMs
	keyDelayMs := play_key_delay_ms()
	keyPressMs := play_key_press_ms()
	SetKeyDelay, %keyDelayMs%, %keyPressMs%
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
		live_speed_reset()
		live_phase_reset()
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

func_btn_list:
txt_list_show()
Return

txt_list_select:
GuiControlGet, idx, txtlist:, txt_list_box
if(idx)
{
	txt_list_index := idx + 0
	txt_list_save_settings()
	txt_list_update_status()
}
Return

txt_list_add_files:
Thread, NoTimers
lastDir := txt_list_current_dir()
FileSelectFile, selectedFiles, M3, %lastDir%, Add TXT/DMS, DoMiSo Sheet (*.txt; *.dms)
Thread, NoTimers, false
if(selectedFiles!="")
{
	files := txt_list_parse_file_selection(selectedFiles)
	added := txt_list_add_paths(files)
	if(files.Length())
	{
		firstFile := files[1]
		SplitPath, firstFile,, lastDir
		if(lastDir!="")
			IniWrite, %lastDir%, setting.ini, txtlist, lastDir
	}
	statubar_txt("TXT List: added " added)
}
Return

txt_list_add_folder:
Thread, NoTimers
lastDir := txt_list_current_dir()
FileSelectFolder, selectedDir, *%lastDir%, 3, Add TXT/DMS Folder
Thread, NoTimers, false
if(selectedDir!="")
{
	added := txt_list_add_folder_path(selectedDir)
	IniWrite, %selectedDir%, setting.ini, txtlist, lastDir
	statubar_txt("TXT List: added " added)
}
Return

txt_list_load:
txt_list_load_index(txt_list_get_selected_index())
Return

txt_list_prev:
txt_list_step(-1)
Return

txt_list_next:
txt_list_step(1)
Return

txt_list_remove:
idx := txt_list_get_selected_index()
if(idx > 0 && idx <= txt_list_paths.Length())
{
	txt_list_paths.RemoveAt(idx)
	if(txt_list_index > txt_list_paths.Length())
		txt_list_index := txt_list_paths.Length()
	if(txt_list_index < 1 && txt_list_paths.Length())
		txt_list_index := 1
	txt_list_refresh()
}
Return

txt_list_clear:
txt_list_paths:=Array()
txt_list_index:=0
txt_list_refresh()
Return

txt_list_close:
txtlistGuiClose:
txtlistGuiEscape:
txt_list_hide()
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
load_yihuan_play_settings(1)
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
beat_time_markers:=Array()

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
beat_time_markers.Push({"delay":0, "beatMs":beatTime})
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
	{
		beatTime:=Round(60000/o.Value(1), 2)
		beat_time_markers.Push({"delay":Round(genshin_delay), "beatMs":beatTime})
	}
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

#UseHook On
#If (isBtn1Playing)
Up::
live_speed_adjust(1)
Return

NumpadUp::
live_speed_adjust(1)
Return

Numpad8::
live_speed_adjust(1)
Return

Down::
live_speed_adjust(-1)
Return

NumpadDown::
live_speed_adjust(-1)
Return

Numpad2::
live_speed_adjust(-1)
Return

Home::
live_speed_home()
Return

NumpadHome::
live_speed_home()
Return

Left::
live_phase_key_down(-1, 0, "Left")
Return

NumpadLeft::
live_phase_key_down(-1, 0, "NumpadLeft")
Return

Numpad4::
live_phase_key_down(-1, 0, "Numpad4")
Return

Right::
live_phase_key_down(1, 0, "Right")
Return

NumpadRight::
live_phase_key_down(1, 0, "NumpadRight")
Return

Numpad6::
live_phase_key_down(1, 0, "Numpad6")
Return

+Left::
live_phase_key_down(-1, 1, "Left")
Return

+NumpadLeft::
live_phase_key_down(-1, 1, "NumpadLeft")
Return

+Numpad4::
live_phase_key_down(-1, 1, "Numpad4")
Return

+Right::
live_phase_key_down(1, 1, "Right")
Return

+NumpadRight::
live_phase_key_down(1, 1, "NumpadRight")
Return

+Numpad6::
live_phase_key_down(1, 1, "Numpad6")
Return

#If
#UseHook Off

#include menu.ahk
