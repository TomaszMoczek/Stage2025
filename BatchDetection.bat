set repo=Captures\raw


REM -------------------- SNAP ----------------------------------

call SamplesAudioWM\Sample_reader.exe -i KantarCertificationMeters.wav -type SNAP -profile P5T
ren CompactDetectionLog.txt CompactDetectionLog-KantarCertificationMeters.wav.txt
ren flog.txt flog-KantarCertificationMeters.wav.txt
del *.dat

for %%i in (%repo%\*.wav) do (
call SamplesAudioWM\Sample_reader.exe -i %%i -type SNAP -profile P5T
ren CompactDetectionLog.txt CompactDetectionLog-%%~nxi.txt
ren flog.txt flog-%%~nxi.txt
del *.dat
)

mkdir LogsSNAP
move *.txt LogsSNAP
