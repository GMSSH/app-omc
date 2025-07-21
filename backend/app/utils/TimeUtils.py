import socket
import struct

from loguru import logger

from app.utils import helpers


class TimeUtils(object):
    @classmethod
    def get_localtime(cls):
        """
        Retrieves the current local time zone and area.

        Returns:
            A dictionary containing the time zone and area.

        Examples:
            >>> get_localtime()
            {'zone': 'America', 'area': 'New_York'}
        """
        result = helpers.exec_shell("ls -l /etc/localtime")
        if "->" not in result[0]:
            return {"zone": "", "area": ""}
        result = result[0]
        tmp = result[result.rfind("->") + 1:].replace("\n", "")
        area = tmp.strip().split("/")[-1]
        zone = tmp.strip().split("/")[-2]
        return {"zone": zone, "area": area}

    @classmethod
    def _unix_timestamp(cls, client):
        """
        Retrieves the Unix timestamp from an NTP server.

        Args:
            client: The client socket used for communication with the NTP server.

        Returns:
            A tuple containing a boolean indicating the success of the operation and the Unix timestamp.

        Examples:
            # Create a client socket and retrieve the Unix timestamp
            >>> client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            >>> success, timestamp = _unix_timestamp(client)
            >>> success
            True
            >>> timestamp
            1638451200.0
        """

        ntp_server = "time.windows.com"
        ntp_port = 123

        # NTP 数据包格式：48 字节（NTP v4 标准）
        ntp_packet = b"\x1b" + 47 * b"\0"
        # 发送请求到 NTP 服务器
        addr = socket.gethostbyname(ntp_server)
        client.sendto(ntp_packet, (addr, ntp_port))

        # 从服务器接收响应
        data, server_address = client.recvfrom(1024)
        # 从响应中提取传输时间戳（Transmit Timestamp）
        unpacked_data = struct.unpack("!12I", data)
        transmit_timestamp = unpacked_data[10] + float(unpacked_data[11]) / 2 ** 32

        # 添加 NTP 闰秒（闰秒从 1972 年开始增加）
        # transmit_timestamp += (37 - 10)
        # 转换为 Unix 时间戳
        unix_timestamp = transmit_timestamp - 2208988800
        # return time.ctime(unix_timestamp)
        return True, unix_timestamp

    @classmethod
    def get_ntp_time(cls):
        """
        Retrieves the current time from an NTP server.

        Returns:
            A tuple containing a boolean indicating the success of the operation and the Unix timestamp.

        Raises:
            socket.timeout: If a timeout occurs while communicating with the NTP server.
            socket.gaierror: If there is an error resolving the NTP server address.

        Examples:
            # Retrieve the current time from an NTP server
            >>> success, timestamp = get_ntp_time()
            >>> success
            True
            >>> timestamp
            1638451200.0
        """
        # 创建套接字并设置超时时间
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(5.0)
        try:
            res, unix_timestamp = cls._unix_timestamp(client)
            return res, unix_timestamp
        except (socket.timeout, socket.gaierror) as e:
            logger.error(e)
            return False, ""
        finally:
            client.close()