#NoEnv

/*
Copyright 2011-2012 Anthony Zhang <azhang9@gmail.com>

this file is part of ProgressPlatformer. Source code is available at <https://github.com/Uberi/ProgressPlatformer>.

ProgressPlatformer is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

this program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

;wip: support different instruments for layers by storing it with every note and changing it when necessary

/*
#Persistent

n := new NotePlayer
n.Instrument(9)
n.Repeat := True

MusicStart := n.Offset

n.Note(48,1000).Delay(1000)
n.Note(47,1000).Delay(1000)
n.Note(48,1000).Delay(1000)
n.Note(45,1000).Delay(1000)

n.Offset := MusicStart

n.Note(55,500).Delay(500)
n.Note(55,500).Delay(500)
n.Note(56,500).Delay(500)
n.Note(55,500).Delay(500)

n.Start()
Return

Esc::ExitApp
*/

class NotePlayer
{
    __New()
    {
		try {
        	this.Device := new MIDIOutputDevice
        	this.Device.SetVolume(100)
		} catch {
			this.Device := 0
		}

        this.pCallback := RegisterCallback(this.SequenceCallback,"F","",&this)

        this.Offset := 0
        this.Timeline := []
        this.Playing := False
        this.Duration := 0
        this.Index := 0
        this.StartOffset := 0
        this.LastPosition := 0
        this.PlayStartTick := 0
        this.SequenceOffsets := []
    }

    Instrument(Sound)
    {
        Offset := Round(this.Offset)
        If !this.Timeline.HasKey(Offset)
            this.Timeline[Offset] := []
        this.Timeline[Offset].Insert(Object("Type","Instrument","Sound",Sound))
        Return, this
    }

    Delay(Length)
    {
        If (this.Offset + Length) < 0
            throw Exception("Invalid offset: " . (this.Offset + Length))
        this.Offset += Length
        Return, this
    }

    Note(Index,Length,DownVelocity = 60,UpVelocity = 60)
    {
        Offset := Round(this.Offset)
        If !this.Timeline.HasKey(Offset)
            this.Timeline[Offset] := []
        this.Timeline[Offset].Insert(Object("Type","NoteOn","Index",Index,"Velocity",DownVelocity))
        EndOffset := Round(this.Offset + Length)
        If !this.Timeline.HasKey(EndOffset)
            this.Timeline[EndOffset] := []
        this.Timeline[EndOffset].Insert(Object("Type","NoteOff","Index",Index,"Velocity",UpVelocity))
        Return, this
    }

    Play(Index,Length,Sound,DownVelocity = 60,UpVelocity = 60)
    {
        ;play the note with the given sound
        PreviousSound := this.Device.Sound
        this.Device.Sound := Sound
        this.Device.NoteOn(Index,DownVelocity)
        this.Device.Sound := PreviousSound

        ;set up the data the timer will need to do its task
        TimerData := Object()
        ObjAddRef(&TimerData)
        TimerData.Index := Index
        TimerData.Velocity := UpVelocity
        TimerData.Device := this.Device

        ;set up a timer to turn off the note
        pCallback := RegisterCallback(this.PlayCallback,"F","",&TimerData)
        hTimer := DllCall("SetTimer","UPtr",0,"UPtr",0,"UInt",Length,"UPtr",pCallback,"UPtr")
        If !hTimer
            throw Exception("Could not create update timer.")
        TimerData.pCallback := pCallback
        TimerData.hTimer := hTimer

        Return, this
    }

    BuildSequence()
    {
        ;insert the ending delay if necessary
        If !this.Timeline.HasKey(this.Offset)
            this.Timeline[this.Offset] := []

        ;convert the timeline into a set of actions
        this.Sequence := [], PreviousOffset := 0
        this.SequenceOffsets := []
        For Offset, Actions In this.Timeline
        {
            CurrentActions := ObjClone(Actions)
            CurrentActions.Insert(1,Offset - PreviousOffset)
            PreviousOffset := Offset
            this.Sequence.Insert(CurrentActions)
            this.SequenceOffsets.Insert(Offset)
        }
        this.Duration := PreviousOffset
        Return, this
    }

    ApplyStateAt(Offset)
    {
        this.ActiveNotes := []
        currentSound := this.Device.Sound
        Loop, % this.SequenceOffsets.MaxIndex()
        {
            absOffset := this.SequenceOffsets[A_Index]
            if absOffset > Offset
                break
            For Index, Action In this.Sequence[A_Index]
            {
                If Index != 1
                {
                    If Action.Type = "Instrument"
                        currentSound := Action.Sound
                    Else If Action.Type = "NoteOn"
                        this.ActiveNotes[Action.Index] := Action.Velocity
                    Else If Action.Type = "NoteOff"
                        this.ActiveNotes.Remove(Action.Index, "")
                }
            }
        }
        this.Device.Sound := currentSound
        For Index, Velocity in this.ActiveNotes
        {
            this.Device.NoteOn(Index, Velocity)
            this.ActiveNotes[Index] := 1
        }
        Return, this
    }

    FindNextIndex(Offset)
    {
        Loop, % this.SequenceOffsets.MaxIndex()
        {
            if this.SequenceOffsets[A_Index] > Offset
                return A_Index
        }
        return this.SequenceOffsets.MaxIndex() + 1
    }

    ScheduleNext(ReferenceOffset)
    {
        if (this.Index <= ObjMaxIndex(this.Sequence))
        {
            delay := this.SequenceOffsets[this.Index] - ReferenceOffset
            if (delay < 1)
                delay := 1
            this.hTimer := DllCall("SetTimer","UPtr",0,"UPtr",0,"UInt",delay,"UPtr",this.pCallback,"UPtr")
            If !this.hTimer
                throw Exception("Could not create update timer.")
        }
        Else
        {
            this.Playing := False
            this.LastPosition := this.Duration
        }
        Return, this
    }

    Start(Offset = 0)
    {
        If this.Playing ;note player is already playing
            Return, this

        this.BuildSequence()
        if (Offset < 0)
            Offset := 0
        if (Offset > this.Duration)
            Offset := this.Duration

        this.StartOffset := Offset
        this.LastPosition := Offset
        this.Index := this.FindNextIndex(Offset)
        this.ApplyStateAt(Offset)

        ;activate the first set of actions if it is present
        If this.Sequence.MaxIndex()
        {
            this.Playing := True
            this.PlayStartTick := A_TickCount
            this.ScheduleNext(Offset)
        }
        Return, this
    }

    Stop()
    {
        If !this.Playing
            Return, this

        this.LastPosition := this.GetPosition()

        ;clean up timers
        If !DllCall("KillTimer","UPtr",0,"UPtr",this.hTimer)
            throw Exception("Could not destroy update timer.")

        ;turn off any active notes
        For Index In this.ActiveNotes
            this.Device.NoteOff(Index,100)
        this.Playing := False
        Return, this
    }

    GetPosition()
    {
        if this.Playing
        {
            pos := this.StartOffset + (A_TickCount - this.PlayStartTick)
            if (pos > this.Duration)
                pos := this.Duration
            return pos
        }
        return this.LastPosition
    }

    Reset()
    {
        this.Stop()
        this.Offset := 0
        this.Timeline := []
        this.Sequence := []
        this.SequenceOffsets := []
        this.Duration := 0
        this.Index := 0
        this.StartOffset := 0
        this.LastPosition := 0
        this.PlayStartTick := 0
        Return, this
    }

    SequenceCallback(x,y,z)
    {
        NotePlayer := Object(A_EventInfo) ;retrieve the note player object

        ;remove the currently active timer
        If !DllCall("KillTimer","UPtr",0,"UPtr",NotePlayer.hTimer)
            throw Exception("Could not destroy update timer.")

        ;execute the set of actions
        NotePlayer.LastPosition := NotePlayer.SequenceOffsets[NotePlayer.Index]
        For Index, Action In NotePlayer.Sequence[NotePlayer.Index] ;perform the current action set
        {
            If Index != 1 ;skip over the first field, which is the time offset
            {
                If Action.Type = "Instrument" ;instrument change
                    NotePlayer.Device.Sound := Action.Sound
                Else If Action.Type = "NoteOn" ;note on action
                {
                    NotePlayer.Device.NoteOn(Action.Index,Action.Velocity)
                    NotePlayer.ActiveNotes[Action.Index] := 1
                }
                Else If Action.Type = "NoteOff" ;note off action
                {
                    NotePlayer.Device.NoteOff(Action.Index,Action.Velocity)
                    NotePlayer.ActiveNotes.Remove(Action.Index,"")
                }
            }
        }

        If (NotePlayer.Index < ObjMaxIndex(NotePlayer.Sequence)) ;set the next timer if available
        {
            NotePlayer.Index ++
            NotePlayer.ScheduleNext(NotePlayer.SequenceOffsets[NotePlayer.Index - 1])
        }
        Else If NotePlayer.Repeat ;repeat note sequence
        {
            NotePlayer.StartOffset := 0
            NotePlayer.PlayStartTick := A_TickCount
            NotePlayer.Index := 1
            NotePlayer.ScheduleNext(0)
        }
        Else ;stop playing
        {
            ;turn off any active notes
            For Index In NotePlayer.ActiveNotes
                NotePlayer.Device.NoteOff(Index,100)
            NotePlayer.Playing := False
            NotePlayer.LastPosition := NotePlayer.Duration
        }
    }

    PlayCallback(x,y,z)
    {
        TimerData := Object(A_EventInfo) ;retrieve the note player object
        ObjRelease(A_EventInfo) ;release the extra reference created before

        If !DllCall("KillTimer","UPtr",0,"UPtr",TimerData.hTimer)
            throw Exception("Could not destroy update timer.")
        DllCall("GlobalFree","UPtr",TimerData.pCallback) ;free callback

        TimerData.Device.NoteOff(TimerData.Index,TimerData.Velocity)
    }

    __Delete()
    {
        this.Stop()
        DllCall("GlobalFree","UPtr",this.pCallback) ;free callback
    }
}

class MIDIOutputDevice
{
    static DeviceCount := 0

    __New(DeviceID = 0)
    {
        If MIDIOutputDevice.DeviceCount = 0
        {
            this.hModule := DllCall("LoadLibrary","Str","winmm")
            If !this.hModule
                throw Exception("Could not load WinMM library.")
        }
        MIDIOutputDevice.DeviceCount ++

        ;open the MIDI output device
        hMIDIOutputDevice := 0
        this.hMIDIOutputDevice := hMIDIOutputDevice
        Status := DllCall("winmm\midiOutOpen","UInt*",hMIDIOutputDevice,"UInt",DeviceID,"UPtr",0,"UPtr",0,"UInt",0) ;CALLBACK_NULL
        If Status != 0 ;MMSYSERR_NOERROR
            throw Exception("Could not open MIDI output device: " . DeviceID . ".")
        this.hMIDIOutputDevice := hMIDIOutputDevice

        this.Channel := 0
        this.Sound := 0
        this.Pitch := 0
    }

    __Get(Key)
    {
        Return, this["_" . Key]
    }

    __Set(Key,Value)
    {
        If (Key = "Channel")
        {
            If Value Not Between 0 And 15
                throw Exception("Invalid channel: " . Value . ".",-1)
        }
        Else If (Key = "Sound")
        {
            If Value Not Between 0 And 127
                throw Exception("Invalid sound: " . Value . ".",-1)
            If DllCall("winmm\midiOutShortMsg","UInt",this.hMIDIOutputDevice,"UInt",0xC0 | this.Channel | (Value << 8)) ;"Program Change" event
                throw Exception("Could not send ""Program Change"" message.")
        }
        Else If (Key = "Pitch")
        {
            If (Value < -100)
                Value := -100
            If (Value > 100)
                Value := 100
            TempValue := Round(((Value + 100) / 200) * 0x4000)
            If DllCall("winmm\midiOutShortMsg","UInt",this.hMIDIOutputDevice,"UInt",0xE0 | this.Channel | ((TempValue & 0x7F) << 8) | (TempValue << 9)) ;"Pitch Bend" event
                throw Exception("Could not send ""Pitch Bend"" message.")
        }
        ObjInsert(this,"_" . Key,Value)
        Return, Value
    }

    __Delete()
    {
        this.Reset()
        If DllCall("winmm\midiOutClose","UInt",this.hMIDIOutputDevice)
            throw Exception("Could not close MIDI output device.")

        MIDIOutputDevice.DeviceCount --
        If MIDIOutputDevice.DeviceCount = 0
            DllCall("FreeLibrary","UPtr",this.hModule)
    }

    GetVolume(Channel = "")
    {
        Volume := 0
        If DllCall("winmm\midiOutGetVolume","UInt",this.hMIDIOutputDevice,"UInt*",Volume) ;retrieve the device volume
            throw Exception("Could not retrieve device volume.")
        If (Channel = "" || Channel = "Left")
            Return, ((Volume & 0xFFFF) / 0xFFFF) * 100
        Else If (Channel = "Right")
            Return, ((Volume >> 16) / 0xFFFF) * 100
        Else
            throw Exception("Invalid channel:" . Channel . ".",-1)
    }

    SetVolume(Volume,Channel = "")
    {
        If Volume Not Between 0 And 100
            throw Exception("Invalid volume: " . Volume . ".",-1)
        If (Channel = "")
            Volume := Round((Volume / 100) * 0xFFFF), Volume |= Volume << 16
        Else If (Channel = "Left")
            Volume := Round((Volume / 100) * 0xFFFF)
        Else If (Channel = "Right")
            Volume := Round((Volume / 100) * 0xFFFF) << 16
        Else
            throw Exception("Invalid channel: " . Channel . ".",-1)
        DllCall("winmm\midiOutSetVolume","UInt",this.hMIDIOutputDevice,"UInt",Volume) ;set the device volume
    }

    NoteOn(Note,Velocity)
    {
        If Note Is Not Integer
            throw Exception("Invalid note: " . Note . ".",-1)
        If Velocity Not Between 0 And 100
            throw Exception("Invalid velocity: " . Velocity . ".",-1)
        Velocity := Round((Velocity / 100) * 127)
        If DllCall("winmm\midiOutShortMsg","UInt",this.hMIDIOutputDevice,"UInt",0x90 | this.Channel | (Note << 8) | (Velocity << 16)) ;"Note On" event
            throw Exception("Could not send ""Note On"" message.")
    }

    NoteOff(Note,Velocity)
    {
        If Note Is Not Integer
            throw Exception("Invalid note: " . Note . ".",-1)
        If Velocity Not Between 0 And 100
            throw Exception("Invalid velocity: " . Velocity . ".",-1)
        Velocity := Round((Velocity / 100) * 127)
        If DllCall("winmm\midiOutShortMsg","UInt",this.hMIDIOutputDevice,"UInt",0x80 | this.Channel | (Note << 8) | (Velocity << 16)) ;"Note Off" event
            throw Exception("Could not send ""Note Off"" message.")
    }

    UpdateNotePressure(Note,Pressure)
    {
        If Note Is Not Integer
            throw Exception("Invalid note: " . Note . ".",-1)
        If Pressure Not Between 0 And 100
            throw Exception("Invalid pressure: " . Pressure . ".",-1)
        Pressure := Round((Pressure / 100) * 127)
        If DllCall("winmm\midiOutShortMsg","UInt",this.hMIDIOutputDevice,"UInt",0xA0 | this.Channel | (Note << 8) | (Pressure << 16)) ;"Polyphonic Aftertouch" event
            throw Exception("Could not send ""Polyphonic Aftertouch"" message.")
    }

    Reset()
    {
        If DllCall("winmm\midiOutReset","UInt",this.hMIDIOutputDevice)
            throw Exception("Could not reset MIDI output device.")
    }
}
