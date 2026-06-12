;~ guiDebug:=1
#Include lib/Gdip.ahk
pToken := Gdip_Startup()
FileCreateDir, % A_Temp "\domiso"
FileInstall, .\changes.md, % A_Temp "\domiso\changes.md", 1
sample_sheet=
(
Domiso
Select Game to switch playback mapping:
Yihuan: 36-key piano, Shift/Ctrl semitones
Genshin: 21-key lyre layout
Sky: 15-key layout

Paste a DoMiSo score here, or use File to open a txt / dms file.

Controls:
F7 pause auto play
F8 stop and reset
F9 start from beginning
F10 resume from pause

===============

1=C
bpm=84
( 1 3 5 )-- 0
5 6 5 3 2 1 0
1# 2 3b 3 4# 5 7b +1

)

ui:={}
ui_gap:=20
ui_section_gap:=20
ui.dpi_scale:=96/(A_ScreenDPI>0?A_ScreenDPI:96)
if(ui.dpi_scale>1)
	ui.dpi_scale:=1
if(ui.dpi_scale<0.72)
	ui.dpi_scale:=0.72
ui.font_title:=Max(14,Round(18*ui.dpi_scale))
ui.font_version:=Max(8,Round(9*ui.dpi_scale))
ui.font_section:=Max(9,Round(10*ui.dpi_scale))
ui.font_edit:=Max(9,Round(9*ui.dpi_scale))
ui.font_field:=Max(9,Round(9*ui.dpi_scale))
ui.font_time:=Max(9,Round(10*ui.dpi_scale))
ui.font_hint:=Max(8,Round(8*ui.dpi_scale))
ui.font_button:=Max(20,Round(26*ui.dpi_scale))
ui.font_status:=Max(11,Round(12*ui.dpi_scale))
ui.size:={w:740,h:1200}
ui.card_x:=20
ui.card_w:=ui.size.w-2*ui.card_x
ui.title_text_h:=80
ui.small_text_h:=46
ui.label_text_h:=56
ui.hint_text_h:=52
ui.header:={}
ui.header.pos:={x:0,y:0}
ui.header.size:={w:ui.size.w,h:108}

ui.statuBar:={}
ui.statuBar.pos:={x:4,y:ui.size.h-42-4}
ui.statuBar.size:={w:ui.size.w-8,h:42}

button_count:=3
ui.button_h:=72
ui.button1:={}
ui.button1.size:={w:(ui.card_w-(button_count-1)*ui_gap)//button_count,h:ui.button_h}
ui.button1.pos:={x:ui.card_x,y:ui.size.h-ui.statuBar.size.h-2*(ui.button_h+ui_gap)-18}
ui.button2:={}
ui.button2.pos:={x:ui.button1.pos.x+ui.button1.size.w+ui_gap,y:ui.button1.pos.y}
ui.button2.size:={w:ui.button1.size.w,h:ui.button1.size.h}
ui.button3:={}
ui.button3.pos:={x:ui.button2.pos.x+ui.button2.size.w+ui_gap,y:ui.button2.pos.y}
ui.button3.size:={w:ui.button1.size.w,h:ui.button1.size.h}

ui.buttonFile:={}
ui.buttonFile.pos:={x:ui.button1.pos.x,y:ui.button1.pos.y+ui.button_h+ui_gap}
ui.buttonFile.size:={w:ui.button1.size.w,h:ui.button1.size.h}
ui.buttonMidi:={}
ui.buttonMidi.pos:={x:ui.buttonFile.pos.x+ui.buttonFile.size.w+ui_gap,y:ui.buttonFile.pos.y}
ui.buttonMidi.size:={w:ui.button1.size.w,h:ui.button1.size.h}
ui.buttonPub:={}
ui.buttonPub.pos:={x:ui.buttonMidi.pos.x+ui.buttonMidi.size.w+ui_gap,y:ui.buttonFile.pos.y}
ui.buttonPub.size:={w:ui.button1.size.w,h:ui.button1.size.h}

ui.instrument:={}
ui.instrument.label:={x:ui.card_x,y:ui.button1.pos.y-132,w:220,h:Round(ui.label_text_h*1.33)}
ui.instrument.pos:={x:ui.card_x,y:ui.instrument.label.y+80}
ui.instrument.size:={w:ui.card_w,h:46}

ui.progress:={}
ui.game:={}
ui.game.label:={x:ui.card_x,y:ui.instrument.label.y-156,w:180,h:ui.label_text_h}
ui.game.pos:={x:ui.card_x,y:ui.game.label.y+62}
ui.game.size:={w:ui.card_w,h:46}

ui.progress.label:={x:ui.card_x,y:ui.game.label.y-156,w:220,h:ui.label_text_h}
ui.progress.time_y:=ui.progress.label.y+62
ui.progress.pos:={x:ui.card_x,y:ui.progress.label.y+98}
ui.progress.size:={w:ui.card_w,h:46}
ui.hotkey:={}
ui.hotkey.pos:={x:ui.card_x,y:ui.buttonFile.pos.y+ui.buttonFile.size.h+4}
ui.hotkey.size:={w:ui.card_w,h:28}

ui.edit:={}
ui.edit.label:={x:ui.card_x,y:ui.header.size.h+32,w:220,h:ui.label_text_h}
ui.edit.pos:={x:ui.card_x,y:ui.edit.label.y+66}
ui.edit.size:={w:ui.card_w,h:ui.progress.label.y-ui_section_gap-ui.edit.pos.y}

ui.hatch:=0
ui.bgcolor:=0xffeaf6f8
ui.fgcolor:=0xffffffff
ui.headercolor:=0xffc9edf2
ui.bordercolor:=0xff2a8c9f
playback_hint=
(
F7 Pause   F8 Stop   F9 Start   F10 Resume
)
Gui, main:New, -Caption -DPIScale -AlwaysOnTop -Owner +OwnDialogs hwndgui_id
Gui, Color, % ui.fgcolor, % ui.bgcolor
Gui, Add, pic, x0 y0 w1 h1 0xE hwndhBg, 
Gui, Add, pic, % "x" ui.header.pos.x " y" ui.header.pos.y " w" ui.header.size.w " h" ui.header.size.h " gtitleMove 0xE hwndhHeaderBar", 
Gui, Font, % "s" ui.font_title " w600 c174B5C", Segoe UI
Gui, Add, Text, % "x20 y20 w440 h" ui.title_text_h " +0x200 BackgroundTrans gtitleMove", Domiso
Gui, Font, % "s" ui.font_version " c2A7B8D", Segoe UI
Gui, Add, Text, % "x" ui.size.w-170 " y30 w150 h" ui.small_text_h " Right +0x200 BackgroundTrans gtitleMove", % "v" version
Gui, Add, Text, % "x" ui.card_x " y" ui.header.size.h " w" ui.card_w " h1 0x10"
Gui, Font, % "s" ui.font_section " w600 c174B5C", Segoe UI
Gui, Add, Text, % "x" ui.edit.label.x " y" ui.edit.label.y " w" ui.edit.label.w " h" ui.edit.label.h " +0x200 BackgroundTrans", Score
Gui, Add, Text, % "x" ui.progress.label.x " y" ui.progress.label.y " w" ui.progress.label.w " h" ui.progress.label.h " +0x200 BackgroundTrans", Playback
Gui, Add, Text, % "x" ui.game.label.x " y" ui.game.label.y " w" ui.game.label.w " h" ui.game.label.h " +0x200 BackgroundTrans", Game
Gui, Add, Text, % "x" ui.instrument.label.x " y" ui.instrument.label.y " w" ui.instrument.label.w " h" ui.instrument.label.h " +0x200 BackgroundTrans", Instrument
Gui, Font, % "s" ui.font_edit " c163746", Consolas
Gui, Add, Edit, % "x" ui.edit.pos.x " y" ui.edit.pos.y " w" ui.edit.size.w " h" ui.edit.size.h " vediter hwndhEdit1", % sample_sheet
Gui, Font, % "s" ui.font_field " c163746", Segoe UI
gameChoose := current_game="genshin" ? 2 : current_game="sky" ? 3 : 1
Gui, Add, DDL, % "x" ui.game.pos.x " y" ui.game.pos.y " AltSubmit r3 vgame_select gfunc_game_select w" ui.game.size.w " h" ui.game.size.h " Choose" gameChoose, Yihuan|Genshin|Sky
Gui, Add, DDL, % "x" ui.instrument.pos.x " y" ui.instrument.pos.y " AltSubmit r13 vinstrument_select w" ui.instrument.size.w " h" ui.instrument.size.h " Choose" _Instrument+1, %Instruments%
Gui, Font, % "s" ui.font_time " c163746", Consolas
Gui, Add, Text, % "x" ui.progress.pos.x " y" ui.progress.time_y " w112 h48 +0x200 BackgroundTrans vplayback_elapsed_label", 00:00
Gui, Add, Text, % "x" ui.progress.pos.x+ui.progress.size.w-112 " y" ui.progress.time_y " w112 h48 Right +0x200 BackgroundTrans vplayback_total_label", 00:00
Gui, Add, Slider, % "x" ui.progress.pos.x " y" ui.progress.pos.y " w" ui.progress.size.w " h46 Range0-1000 AltSubmit vplayback_slider gfunc_playback_slider hwndhPlaybackSlider ToolTip", 0
Gui, Font, % "s" ui.font_hint " c3F6C79", Segoe UI
Gui, Add, Text, % "x" ui.hotkey.pos.x " y" ui.hotkey.pos.y " w" ui.hotkey.size.w " h" ui.hotkey.size.h " Center +0x200 BackgroundTrans", % playback_hint
Gui, +Delimiter`n

Gui, Add, pic, % "x" ui.button1.pos.x " y" ui.button1.pos.y " w" ui.button1.size.w " h" ui.button1.size.h " 0xE hwndhBtn1 gfunc_btn_play", 
Gui, Add, pic, % "x" ui.button2.pos.x " y" ui.button2.pos.y " w" ui.button2.size.w " h" ui.button2.size.h " 0xE hwndhBtn2 gfunc_btn_listen", 
Gui, Add, pic, % "x" ui.button3.pos.x " y" ui.button3.pos.y " w" ui.button3.size.w " h" ui.button3.size.h " 0xE hwndhBtn3 gfunc_btn_exit", 

Gui, Add, pic, % "x" ui.buttonFile.pos.x " y" ui.buttonFile.pos.y " w" ui.buttonFile.size.w " h" ui.buttonFile.size.h " 0xE hwndhBtnFile gfunc_btn_file", 
Gui, Add, pic, % "x" ui.buttonMidi.pos.x " y" ui.buttonMidi.pos.y " w" ui.buttonMidi.size.w " h" ui.buttonMidi.size.h " 0xE hwndhBtnMidi gfunc_btn_midi", 
Gui, Add, pic, % "x" ui.buttonPub.pos.x " y" ui.buttonPub.pos.y " w" ui.buttonPub.size.w " h" ui.buttonPub.size.h " 0xE hwndhBtnPub gfunc_btn_publish", 

Gui, Add, pic, % "x" ui.statuBar.pos.x " y" ui.statuBar.pos.y " w" ui.statuBar.size.w " h" ui.statuBar.size.h " 0xE hwndhStatuBar", 


hBitmap:={}
hBitmap.headerBar:=hBitmapByBorderHatchAndText(ui.header.size.w,ui.header.size.h,ui.bordercolor,0,ui.headercolor,ui.headercolor,0)
hBitmap.button1:=hBitmapByBorderHatchAndText(ui.button1.size.w,ui.button1.size.h, 0xff2a8c9f,1,0xffeffcff,0xffeffcff,0,"Play")
hBitmap.button1Hover:=hBitmapByBorderHatchAndText(ui.button1.size.w,ui.button1.size.h, 0xff197b8e,2,0xffe1f7fb,0xffe1f7fb,0,"Play")
hBitmap.button1Playing:=hBitmapByBorderHatchAndText(ui.button1.size.w,ui.button1.size.h, 0xff236f80,1,0xff236f80,0xff236f80,0,"Stop","cFFFFF8ED S" ui.font_button " Center vCenter")
hBitmap.button1PlayingHover:=hBitmapByBorderHatchAndText(ui.button1.size.w,ui.button1.size.h, 0xff174f5c,2,0xff174f5c,0xff174f5c,0,"Stop","cFFFFF8ED S" ui.font_button " Center vCenter")

hBitmap.button2:=hBitmapByBorderHatchAndText(ui.button2.size.w,ui.button2.size.h, 0xff567bb2,1,0xfff2f6ff,0xfff2f6ff,0,"Listen")
hBitmap.button2Hover:=hBitmapByBorderHatchAndText(ui.button2.size.w,ui.button2.size.h, 0xff416aa5,2,0xffe9f0ff,0xffe9f0ff,0,"Listen")
hBitmap.button2Playing:=hBitmapByBorderHatchAndText(ui.button2.size.w,ui.button2.size.h, 0xff236f80,1,0xff236f80,0xff236f80,0,"Stop","cFFFFF8ED S" ui.font_button " Center vCenter")
hBitmap.button2PlayingHover:=hBitmapByBorderHatchAndText(ui.button2.size.w,ui.button2.size.h, 0xff174f5c,2,0xff174f5c,0xff174f5c,0,"Stop","cFFFFF8ED S" ui.font_button " Center vCenter")

hBitmap.button3:=hBitmapByBorderHatchAndText(ui.button3.size.w,ui.button3.size.h, 0xff7d91a1,1,0xfff7fbff,0xfff7fbff,0,"Exit")
hBitmap.button3Hover:=hBitmapByBorderHatchAndText(ui.button3.size.w,ui.button3.size.h, 0xff667b8b,2,0xffeef6fb,0xffeef6fb,0,"Exit")

hBitmap.buttonFile:=hBitmapByBorderHatchAndText(ui.buttonFile.size.w,ui.buttonFile.size.h, 0xff2a8c9f,1,0xffeffcff,0xffeffcff,0,"File")
hBitmap.buttonFileHover:=hBitmapByBorderHatchAndText(ui.buttonFile.size.w,ui.buttonFile.size.h, 0xff197b8e,2,0xffe1f7fb,0xffe1f7fb,0,"File")

hBitmap.buttonMidi:=hBitmapByBorderHatchAndText(ui.buttonMidi.size.w,ui.buttonMidi.size.h, 0xff6d73c9,1,0xfff4f5ff,0xfff4f5ff,0,"MIDI")
hBitmap.buttonMidiHover:=hBitmapByBorderHatchAndText(ui.buttonMidi.size.w,ui.buttonMidi.size.h, 0xff575eb3,2,0xffeceeff,0xffeceeff,0,"MIDI")

hBitmap.buttonPub:=hBitmapByBorderHatchAndText(ui.buttonPub.size.w,ui.buttonPub.size.h, 0xff5a9b85,1,0xfff0fbf8,0xfff0fbf8,0,"Encrypt")
hBitmap.buttonPubHover:=hBitmapByBorderHatchAndText(ui.buttonPub.size.w,ui.buttonPub.size.h, 0xff43856e,2,0xffe5f7f1,0xffe5f7f1,0,"Encrypt")

hBitmap.bg:=hBitmapByBorderHatchAndText(ui.size.w,ui.size.h, ui.bgcolor,0,ui.bgcolor,ui.bgcolor,0)

SetImage(hBg,hBitmap.bg)
SetImage(hHeaderBar,hBitmap.headerBar)
SetImage(hBtn1,hBitmap.button1)
SetImage(hBtn2,hBitmap.button2)
SetImage(hBtn3,hBitmap.button3)
SetImage(hBtnFile,hBitmap.buttonFile)
SetImage(hBtnMidi,hBitmap.buttonMidi)
SetImage(hBtnPub,hBitmap.buttonPub)
statubar_txt("v" version)
Gui, main:Show, % "w" ui.size.w " h" ui.size.h

OnMessage(0x200, "MouseMove")
OnMessage(0x201, "MouseDown")
OnMessage(0x203, "MouseDown")
OnMessage(0x202, "MouseUp")

#include setup_gui.ahk

MouseUp(wParam, lParam, msg, hwnd)
{
	global
	local mhwnd
	MouseGetPos,,,,mhwnd,2
	if(playback_slider_dragging)
	{
		playback_slider_dragging := 0
		playback_apply_seek(playback_pending_seek_ms)
	}
}

MouseDown(wParam, lParam, msg, hwnd)
{
	global
	local xPos, sw, sh, sliderValue, ratio, thumbLen, usableWidth, currentValue, currentThumbX
	if(hwnd==hPlaybackSlider)
	{
		xPos := lParam & 0xFFFF
		if(xPos > 0x7FFF)
			xPos -= 0x10000
		WinGetPos, , , sw, sh, ahk_id %hPlaybackSlider%
		if(sw > 0)
		{
			SendMessage, 0x041C, 0, 0,, ahk_id %hPlaybackSlider%
			thumbLen := ErrorLevel
			if(thumbLen <= 0 || thumbLen >= sw)
				thumbLen := 18
			usableWidth := sw - thumbLen
			if(usableWidth <= 0)
			{
				usableWidth := sw
				thumbLen := 0
			}

			GuiControlGet, currentValue,, playback_slider
			currentValue += 0
			currentThumbX := thumbLen / 2 + (currentValue / 1000.0) * usableWidth

			if(Abs(xPos - currentThumbX) <= Max(6, thumbLen / 2))
			{
				playback_slider_dragging := 1
				return
			}

			ratio := (xPos - thumbLen / 2) / usableWidth
			if(ratio < 0)
				ratio := 0
			else if(ratio > 1)
				ratio := 1
			sliderValue := Round(ratio * 1000)
			playback_slider_internal := 1
			GuiControl,, playback_slider, % sliderValue
			playback_slider_internal := 0
			playback_pending_seek_ms := playback_slider_to_ms(sliderValue)
			GuiControl,, playback_elapsed_label, % playback_format_ms(playback_pending_seek_ms)
			GuiControl,, playback_total_label, % playback_format_ms(playback_total_ms)
			playback_slider_dragging := 0
			playback_apply_seek(playback_pending_seek_ms)
			return 0
		}
	}
}

statubar_txt(txt)
{
	global hStatuBar, ui
	_hBitmap := hBitmapByColorAndText(ui.statuBar.size.w,ui.statuBar.size.h,0xff236f80,txt,"bold cFFFFF8ED S" ui.font_status " Right vCenter")
	SetImage(hStatuBar,_hBitmap)
	DeleteObject(_hBitmap)
}

btn1update()
{
	global
	btn_release(hBtn1)
}
btn2update()
{
	global
	btn_release(hBtn2)
	if(isBtn2Playing)
	{
		GuiControl, disable, instrument_select
	} else {
		GuiControl, enable, instrument_select
	}
}

btn_release(hwnd)
{
	global
	if(hwnd==hBtn1)
	{
		if(isBtn1Playing)
		{
			SetImage(hBtn1,hBitmap.button1Playing)
		}
		Else
		{
			SetImage(hBtn1,hBitmap.button1)
		}
	}
	if(hwnd==hBtn2)
	{
		if(isBtn2Playing)
		{
			SetImage(hBtn2,hBitmap.button2Playing)
		}
		Else
		{
			SetImage(hBtn2,hBitmap.button2)
		}
	}
	if(hwnd==hBtn3)
	{
		SetImage(hBtn3,hBitmap.button3)
	}
	if(hwnd==hBtnPub)
	{
		SetImage(hBtnPub,hBitmap.buttonPub)
	}
	if(hwnd==hBtnFile)
	{
		SetImage(hBtnFile,hBitmap.buttonFile)
	}
	if(hwnd==hBtnMidi)
	{
		SetImage(hBtnMidi,hBitmap.buttonMidi)
	}
}

MouseMove(wParam, lParam, msg, hwnd)
{
	Global
	local mhwnd
	If(WinExist("A")!=gui_id)
	Return
	MouseGetPos,,,,mhwnd,2
	Static _LastButtonData = true
	If(mhwnd != _LastButtonData)	;光标移动到新控件
	{
		btn_release(_LastButtonData)
		if(mhwnd==hBtn1)
		{
			if(isBtn1Playing)
			{
				SetImage(hBtn1,hBitmap.button1PlayingHover)
			}
			Else
			{
				SetImage(hBtn1,hBitmap.button1Hover)
			}
		}
		if(mhwnd==hBtn2)
		{
			if(isBtn2Playing)
			{
				SetImage(hBtn2,hBitmap.button2PlayingHover)
			}
			Else
			{
				SetImage(hBtn2,hBitmap.button2Hover)
			}
		}
		if(mhwnd==hBtn3)
		{
			SetImage(hBtn3,hBitmap.button3Hover)
		}
		if(mhwnd==hBtnPub)
		{
			SetImage(hBtnPub,hBitmap.buttonPubHover)
		}
		if(mhwnd==hBtnFile)
		{
			SetImage(hBtnFile,hBitmap.buttonFileHover)
		}
		if(mhwnd==hBtnMidi)
		{
			SetImage(hBtnMidi,hBitmap.buttonMidiHover)
		}
	}
	_LastButtonData := mhwnd
	Return
}


hBitmapHatch(w,h,bgcolor:=0xffff0000,fgcolor:=0xff00ff00,hatch:=0)
{
	pBitmap := Gdip_CreateBitmap(w, h)
	G := Gdip_GraphicsFromImage(pBitmap)
	Gdip_SetSmoothingMode(G, 4)
	pBrush := Gdip_BrushCreateHatch(fgcolor,bgcolor,hatch)
	Gdip_FillRectangle(G, pBrush, -1, -1, w+1, h+1)
	hBitmap := Gdip_CreateHBITMAPFromBitmap(pBitmap)
	Gdip_DeleteBrush(pBrush)
	Gdip_DeleteGraphics(G)
	Gdip_DisposeImage(pBitmap)
	Return hBitmap
}
hBitmapByBorderHatchAndText(w,h,bdcolor:=0xffffffff,bdwidth:=1,fgcolor:=0xff00ff00,bgcolor:=0xff00ff00,hatch:=1,text:="",option:="")
{
	global ui
	pBitmap := Gdip_CreateBitmap(w, h)
	G := Gdip_GraphicsFromImage(pBitmap)
	Gdip_SetSmoothingMode(G, 4)
	if(hatch<=0)
		pBrush := Gdip_BrushCreateSolid(bgcolor)
	else
		pBrush := Gdip_BrushCreateHatch(fgcolor,bgcolor,hatch)
	Gdip_FillRectangle(G, pBrush, -1, -1, w+1, h+1)
	if(text!=""){
		if(option="")
			Gdip_TextToGraphics(G, text,"cFF444444 S" ui.font_button " Center vCenter","Segoe UI",w,h)
		Else
			Gdip_TextToGraphics(G, text,option,"Segoe UI",w,h)
	}
	Gdip_DeleteBrush(pBrush)
	if(bdwidth>0){
		pBrush := Gdip_BrushCreateSolid(bdcolor)
		Gdip_FillRectangle(G, pBrush, -1, -1, w, bdwidth+1)
		Gdip_FillRectangle(G, pBrush, 1, h-bdwidth-1, w, h)
		Gdip_FillRectangle(G, pBrush, -1, -1, bdwidth+1, h)
		Gdip_FillRectangle(G, pBrush, w-bdwidth-1, 1, w-1, h)
	}
	hBitmap := Gdip_CreateHBITMAPFromBitmap(pBitmap)
	Gdip_DeleteBrush(pBrush)
	Gdip_DeleteGraphics(G)
	Gdip_DisposeImage(pBitmap)
	Return hBitmap
}
hBitmapBy2ColorAndText(w,h,fgcolor:=0xff00ff00,text:="",option:="")
{
	global ui
	Return hBitmapByBorderHatchAndText(w,h,,0,fgcolor,ui.bgcolor,ui.hatch,text,option)
}
hBitmapByColorAndText(w,h,bgcolor:=0xffff0000,text:="",option:="")
{
	pBitmap := Gdip_CreateBitmap(w, h)
	G := Gdip_GraphicsFromImage(pBitmap)
	Gdip_SetSmoothingMode(G, 4)
	pBrush := Gdip_BrushCreateSolid(bgcolor)
	Gdip_FillRectangle(G, pBrush, -1, -1, w+1, h+1)
	if(text!=""){
		if(option="")
			Gdip_TextToGraphics(G, text,"cFFf1f1f1 S" ui.font_status " Center vCenter","Segoe UI",w,h)
		Else
			Gdip_TextToGraphics(G, text,option,"Segoe UI",w,h)
	}
	hBitmap := Gdip_CreateHBITMAPFromBitmap(pBitmap)
	Gdip_DeleteBrush(pBrush)
	Gdip_DeleteGraphics(G)
	Gdip_DisposeImage(pBitmap)
	Return hBitmap
}
