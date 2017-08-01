; Example: This is a working script that writes some text to a file then reads it back into memory.
; It provides the same functionality as this DllCall-example.

FileSelectFile, FileName, S16,, Create a new file:
if (FileName = "")
	return
file := FileOpen(FileName, "w")
if !IsObject(file)
{
	MsgBox Can't open "%FileName%" for writing.
	return
}
TestString := "This is a test string.`r`n"  ; When writing a file this way, use `r`n rather than `n to start a new line.
file.Write(TestString)
file.Close()

; Now that the file was written, read its contents back into memory.
file := FileOpen(FileName, "r-d") ; read the file ("r"), share all access except for delete ("-d")
if !IsObject(file)
{
	MsgBox Can't open "%FileName%" for reading.
	return
}
CharsToRead := StrLen(TestString)
TestString := file.Read(CharsToRead)
file.Close()
MsgBox The following string was read from the file: %TestString%