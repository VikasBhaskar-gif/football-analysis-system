"""
video_streaming.py
==================
HTTP Range-request video streaming helper for smooth seeking and scrubber dragging.
Supports 206 Partial Content responses according to RFC 7233.
"""

import os
from typing import Generator
from fastapi import Request, HTTPException, status
from starlette.responses import StreamingResponse, Response


def parse_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    """Parse HTTP Range header: 'bytes=start-end'."""
    try:
        units, range_str = range_header.strip().split("=")
        if units != "bytes":
            raise ValueError("Unsupported unit")
        parts = range_str.split("-")
        start = int(parts[0]) if parts[0] else 0
        end = int(parts[1]) if len(parts) > 1 and parts[1] else file_size - 1
        start = max(0, min(start, file_size - 1))
        end = max(start, min(end, file_size - 1))
        return start, end
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
            detail=f"Invalid range request: {e}",
            headers={"Content-Range": f"bytes */{file_size}"},
        )


def file_iterator(file_path: str, start: int, end: int, chunk_size: int = 1024 * 1024) -> Generator[bytes, None, None]:
    """Yield file chunks from byte `start` to `end` inclusive."""
    with open(file_path, "rb") as f:
        f.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            read_size = min(chunk_size, remaining)
            data = f.read(read_size)
            if not data:
                break
            remaining -= len(data)
            yield data


def stream_video_file(request: Request, file_path: str, content_type: str = "video/mp4") -> Response:
    """Generate appropriate 200 or 206 Partial Content streaming response for video."""
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video file not found")

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("range") or request.headers.get("Range")

    if not range_header:
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
            "Content-Type": content_type,
        }
        return StreamingResponse(
            file_iterator(file_path, 0, file_size - 1),
            status_code=status.HTTP_200_OK,
            headers=headers,
            media_type=content_type,
        )

    start, end = parse_range_header(range_header, file_size)
    content_length = end - start + 1

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Content-Length": str(content_length),
        "Content-Type": content_type,
    }

    return StreamingResponse(
        file_iterator(file_path, start, end),
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        headers=headers,
        media_type=content_type,
    )
