
FileEncoding, UTF-8

; 是否内测版本
betaBuild:=0

name_en:="Domiso"
name_zh:="Domiso"
version:="0.99.9"
versionFilename:="version.txt"
ahkFilename:="DoMiSo.ahk"
binaryFilename:="Domiso.exe"
downloadFilename:="Domiso.zip"
downloadUrl:=""

if(betaBuild=1) {
	version:=version . " BETA"
}
