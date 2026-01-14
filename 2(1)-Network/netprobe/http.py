from __future__ import annotations

from typing import Optional


def build_request(host: str, path: str) -> bytes:
    """
    HTTP GET 요청 메시지를 바이트 형태로 생성합니다.
    """
    if not path.startswith("/"):
        path = "/" + path

    ###########################################################
    # TODO: HTTP/1.1 규격에 맞게 요청 문자열(GET, Host, Connection 헤더 포함)을 완성하세요.
    # HINT: 각 줄의 끝은 \r\n이며, 헤더의 끝에는 빈 줄(\r\n)이 하나 더 필요합니다.
    
    req = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}\r\n"
    "Connection: close\r\n"
    "\r\n"
    )

    
    ###########################################################

    return req.encode("utf-8")


def send_and_recv(sock, request: bytes, max_bytes: int) -> bytes:
    
    sock.sendall(request)

    chunks: list[bytes] = []
    total = 0
    while True:
        data = sock.recv(4096)
        if not data:
            break
        chunks.append(data)
        total += len(data)
        if total > max_bytes:
            break
    return b"".join(chunks)


def parse_status_and_preview(raw: bytes, max_preview: int = 200) -> tuple[Optional[int], str, Optional[str]]:
    """
    서버의 Raw 응답 데이터를 분석하여 상태 코드와 본문 미리보기를 추출합니다. 
    
    요구사항:
    1. 헤더와 바디를 구분하는 CRLF 2번(b"\\r\\n\\r\\n")의 위치를 찾으세요. 
    2. 헤더 영역을 decode한 뒤, Status Line(첫 줄)에서 상태 코드를 추출하세요. 
    3. 바디 영역에서 max_preview 만큼의 데이터를 decode하여 반환하세요. 
    4. 규격에 맞지 않는 데이터가 들어올 경우 적절한 에러 메시지를 반환하세요. 
    """
    
    boundary = raw.find(b"\r\n\r\n")
    if boundary == -1:
      return None, "", "Invalid HTTP response: missing header/body separator"

    header_bytes = raw[:boundary]
    body_bytes = raw[boundary + 4:]

    header_text = header_bytes.decode("utf-8", errors="replace")
    lines = header_text.split("\r\n")
    if not lines or not lines[0].strip():
        return None, "", "Invalid HTTP response: empty status line"

    status_line = lines[0]
    parts = status_line.split()
    if len(parts) < 2:
        return None, "", f"Invalid HTTP status line: {status_line}"

    try:
        status_code = int(parts[1])
    except ValueError:
        return None, "", f"Invalid status code: {parts[1]}"

    preview = body_bytes[:max_preview].decode("utf-8", errors="replace")
    error = None

    return status_code, preview, error