#NoEnv
arr := [0,2,4,5,7,9,11]
base := 60
x := base + arr[0]
y := base + arr[1]
FileAppend, % "x=" x "`ny=" y, *
ExitApp
