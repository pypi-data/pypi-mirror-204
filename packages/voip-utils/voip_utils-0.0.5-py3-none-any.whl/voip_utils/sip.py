"""Implementation of SIP (Session Initiation Protocol)."""
import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from .error import VoipError
from .util import is_ipv4_address

SIP_PORT = 5060

_LOGGER = logging.getLogger(__name__)
_CRLF = "\r\n"
_OPUS_PAYLOAD = "123"


@dataclass
class SdpInfo:
    """Information for Session Description Protocol (SDP)."""

    username: str
    id: int
    session_name: str
    version: str


@dataclass
class CallInfo:
    """Information gathered from an INVITE message."""

    caller_ip: str
    caller_sip_port: int
    caller_rtp_port: int
    server_ip: str
    headers: dict[str, str]


class SipDatagramProtocol(asyncio.DatagramProtocol, ABC):
    """UDP server for the Session Initiation Protocol (SIP)."""

    def __init__(self, sdp_info: SdpInfo) -> None:
        """Set up SIP server."""
        self.sdp_info = sdp_info
        self.transport = None

    def connection_made(self, transport):
        """Server ready."""
        self.transport = transport

    def datagram_received(self, data: bytes, addr):
        """Handle INVITE SIP messages."""
        try:
            message = data.decode()
            method, headers, body = self._parse_sip(message)

            if method and (method.lower() != "invite"):
                # Not an INVITE message
                return

            caller_ip, caller_sip_port = addr
            _LOGGER.debug(
                "Incoming call from ip=%s, port=%s",
                caller_ip,
                caller_sip_port,
            )

            # Extract caller's RTP port from SDP.
            # See: https://datatracker.ietf.org/doc/html/rfc2327
            caller_rtp_port: Optional[int] = None
            body_lines = body.splitlines()
            for line in body_lines:
                line = line.strip()
                if line:
                    key, value = line.split("=", maxsplit=1)
                    if key == "m":
                        parts = value.split()
                        if parts[0] == "audio":
                            caller_rtp_port = int(parts[1])

            if caller_rtp_port is None:
                raise VoipError("No caller RTP port")

            # Extract our visible IP from SIP header.
            # <sip:123.123.123.123:1234>;tag=...
            sip_ip_str = headers["to"].partition(";")[0]
            sip_ip_str = sip_ip_str[1:-1]
            _sip, server_ip, _port = sip_ip_str.split(":", maxsplit=2)
            if not is_ipv4_address(server_ip):
                raise VoipError(f"Invalid IPv4 address in {sip_ip_str}")

            self.on_call(
                CallInfo(
                    caller_ip=caller_ip,
                    caller_sip_port=caller_sip_port,
                    caller_rtp_port=caller_rtp_port,
                    server_ip=server_ip,
                    headers=headers,
                )
            )
        except Exception:
            _LOGGER.exception("Unexpected error handling SIP INVITE")

    @abstractmethod
    def on_call(self, call_info: CallInfo):
        """Handle incoming calls."""

    def answer(
        self,
        call_info: CallInfo,
        server_rtp_port: int,
    ):
        """Send OK message to caller with our IP and RTP port."""
        if self.transport is None:
            return

        # SDP = Session Description Protocol
        # See: https://datatracker.ietf.org/doc/html/rfc2327
        body_lines = [
            "v=0",
            f"o={self.sdp_info.username} {self.sdp_info.id} 1 IN IP4 {call_info.server_ip}",
            f"s={self.sdp_info.session_name}",
            f"c=IN IP4 {call_info.server_ip}",
            "t=0 0",
            f"m=audio {server_rtp_port} RTP/AVP {_OPUS_PAYLOAD}",
            f"a=rtpmap:{_OPUS_PAYLOAD} opus/48000/2",
            "a=ptime:20",
            "a=maxptime:150",
            "a=sendrecv",
            _CRLF,
        ]
        body = _CRLF.join(body_lines)

        response_headers = {
            "Via": call_info.headers["via"],
            "From": call_info.headers["from"],
            "To": call_info.headers["to"],
            "Call-ID": call_info.headers["call-id"],
            "Content-Type": "application/sdp",
            "Content-Length": len(body),
            "CSeq": call_info.headers["cseq"],
            "Contact": call_info.headers["contact"],
            "User-Agent": f"{self.sdp_info.username} {self.sdp_info.id} {self.sdp_info.version}",
            "Allow": "INVITE, ACK, BYE, CANCEL, OPTIONS",
        }
        response_lines = ["SIP/2.0 200 OK"]

        for key, value in response_headers.items():
            response_lines.append(f"{key}: {value}")

        response_lines.append(_CRLF)
        response_str = _CRLF.join(response_lines) + body
        response_bytes = response_str.encode()

        self.transport.sendto(
            response_bytes,
            (call_info.caller_ip, call_info.caller_sip_port),
        )
        _LOGGER.debug(
            "Sent OK to ip=%s, port=%s with rtp_port=%s",
            call_info.caller_ip,
            call_info.caller_sip_port,
            server_rtp_port,
        )

    def _parse_sip(self, message: str) -> Tuple[Optional[str], Dict[str, str], str]:
        """Parse SIP message and return method, headers, and body."""
        lines = message.splitlines()

        method: Optional[str] = None
        headers: dict[str, str] = {}
        offset: int = 0

        # See: https://datatracker.ietf.org/doc/html/rfc3261
        for i, line in enumerate(lines):
            if line:
                offset += len(line) + len(_CRLF)

            if i == 0:
                method = line.split()[0]
            elif not line:
                break
            else:
                key, value = line.split(":", maxsplit=1)
                headers[key.lower()] = value.strip()

        body = message[offset:]

        return method, headers, body
