import can


class ClassicCanSender:
    def __init__(self, channel='can1', bitrate=500000):
        self.channel = channel
        self.bitrate = bitrate
        self.bus = can.interface.Bus(
            channel=self.channel, bustype='socketcan', bitrate=self.bitrate)

    def send_signal(self, can_id, data):
        """Send a classic CAN signal (message)."""
        msg = can.Message(arbitration_id=can_id, data=data,
                          is_extended_id=False, is_fd=False)
        try:
            self.bus.send(msg)
            data_hex_string = "".join("%02x" % b for b in msg.data)
            print(
                f"Message sent on {self.channel}: ID={hex(can_id)}, Data={data_hex_string}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def close(self):
        """Close the CAN interface."""
        self.bus.shutdown()
        print(f"Closed {self.channel} interface.")


# Example Usage
if __name__ == "__main__":
    # Set up the sender on can1
    can_sender = ClassicCanSender(channel='can1', bitrate=500000)

    # Send a CAN message with ID 0x123 and some data
    can_sender.send_signal(
        0x123, [0x01, 0x02, 0x03, 0x04, 0xde, 0xad, 0xbe, 0xef])

    # Close the interface
    can_sender.close()
