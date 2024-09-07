import can
import argparse


class CanSender:
    def __init__(self, channel='can1', bitrate=500000, use_fd=False):
        self.channel = channel
        self.bitrate = bitrate
        self.use_fd = use_fd
        self.bus = can.interface.Bus(
            channel=self.channel, bustype='socketcan', bitrate=self.bitrate, fd=self.use_fd)

    def send_signal(self, can_id, data):
        """Send a CAN or CAN FD signal (message)."""
        # Payload length check
        max_len = 64 if self.use_fd else 8
        if len(data) > max_len:
            raise ValueError(
                f"Data length cannot exceed {max_len} bytes for {'CAN FD' if self.use_fd else 'classic CAN'}.")

        # Send the message
        msg = can.Message(arbitration_id=can_id, data=data,
                          is_fd=self.use_fd, is_extended_id=False)
        try:
            self.bus.send(msg)
            data_hex_string = "".join("%02x" % b for b in msg.data)
            print(
                f"Message sent on {self.channel}: ID={hex(can_id)}, Data={data_hex_string}, FD={msg.is_fd}, DLC={msg.dlc}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def close(self):
        """Close the CAN interface."""
        self.bus.shutdown()
        print(f"Closed {self.channel} interface.")


if __name__ == "__main__":
    # Argument parsing for FD mode
    parser = argparse.ArgumentParser(description="CAN Sender")
    parser.add_argument('fd', nargs='?', default='classic',
                        help="'fd' for CAN FD mode or nothing for classic CAN.")
    args = parser.parse_args()

    # Determine if CAN FD should be used
    use_fd = args.fd == 'fd'

    # Set up the sender
    can_sender = CanSender(channel='can1', bitrate=500000, use_fd=use_fd)

    # Send a CAN message with ID 0x123 and some data
    if not use_fd:
        can_sender.send_signal(
            0x123, [0x01, 0x02, 0x03, 0x04, 0xde, 0xad, 0xbe, 0xef])
    else:
        can_sender.send_signal(
            0x123, [0x01, 0x02, 0x03, 0x04, 0xde, 0xad, 0xbe, 0xef, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06])

    # Close the interface
    can_sender.close()
