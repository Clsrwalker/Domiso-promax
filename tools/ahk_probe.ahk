#NoEnv
arr := [0,2,4,5,7,9,11]
FileDelete, d:\domiso\tools\ahk_probe_out.txt
FileAppend, % "arr0=" arr[0] "`narr1=" arr[1] "`narr2=" arr[2], d:\domiso\tools\ahk_probe_out.txt
ExitApp
