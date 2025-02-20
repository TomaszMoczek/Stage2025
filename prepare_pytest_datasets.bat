set repo=Captures\raw

call SamplesAudioWM\Sample_reader.exe -i KantarCertificationMeters.wav -type SNAP -profile P5T
ren CompactDetectionLog.txt CompactDetectionLog-KantarCertificationMeters.wav.txt
del flog.txt
del *.dat

for %%i in (%repo%\*.wav) do (
call SamplesAudioWM\Sample_reader.exe -i %%i -type SNAP -profile P5T
ren CompactDetectionLog.txt CompactDetectionLog-%%~nxi.txt
del flog.txt
del *.dat
)

mkdir LogsSNAP
move *.txt LogsSNAP
