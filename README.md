# mitmproxy-lenovo-imm-uefi-decoder
Decodes UEFI Settings like iSCSI_InitiatorName sent to the IMM via OneCLI

Install Mitmproxy and EfiCompressor via pip 

`pip install EfiCompressor mitmproxy==11.0.0`


Run Mitmweb/mitmproxy like this

`mitmweb --mode reverse:https://imm-ip --listen-port 443      --no-web-open-browser --web-port 6509 --web-host 0.0.0.0 -v --ssl-insecure  -s ~/Documents/onecli/decoder.py`

Use Localhost in the OneCLI Target:

`onecli config batch --file ~/Documents/onecli/batch-commands  --imm USERID:pw@127.0.0.1`

before:
![image](https://github.com/user-attachments/assets/aad27154-f2cd-4c33-a6d9-4e173fa7955e)

![image](https://github.com/user-attachments/assets/4155ac3c-bf2e-43e1-adac-a86d4ab025a9)
after:
![image](https://github.com/user-attachments/assets/082b6ddb-f00a-44a7-879d-b7bda07e151b)

![image](https://github.com/user-attachments/assets/0f57ef0d-7ae0-495a-97f0-a6e15056dc3e)
