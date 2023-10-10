# win实用命令
- 定时关机
schtasks /create /tn "SHUTDOWN" /tr "shutdown /s" /sc ONCE /st 11:11



shutdown -s -t  600
shutdown -a 