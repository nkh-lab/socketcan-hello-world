import can
import argparse


class CanReceiver:
    def __init__(self, channel='can0', bitrate=500000, use_fd=False):
        self.channel = channel
        self.bitrate = bitrate
        self.use_fd = use_fd
        self.bus = can.interface.Bus(
            channel=self.channel, bustype='socketcan', bitrate=self.bitrate, fd=self.use_fd)

    def start_receiving(self):
        """Start receiving CAN or CAN FD messages."""
        print(
            f"Listening for messages on {self.channel} (FD={self.use_fd})...")

        while True:
            try:
                # Wait for a message for 10 seconds
                msg = self.bus.recv(timeout=10)
                if msg:
                    data_hex_string = "".join("%02x" % b for b in msg.data)
                    print(
                        f"Received message on {self.channel}: ID={hex(msg.arbitration_id)}, "
                        f"Data={data_hex_string}, FD={msg.is_fd}, DLC={msg.dlc}")
                else:
                    print("No message received within timeout period.")
            except KeyboardInterrupt:
                print("\rReception interrupted by user.")
                break
            except can.CanError as e:
                print(f"CAN Error: {e}")
                break

    def close(self):
        """Close the CAN interface."""
        self.bus.shutdown()
        print(f"Closed {self.channel} interface.")


if __name__ == "__main__":
    # Argument parsing for FD mode
    parser = argparse.ArgumentParser(description="CAN Receiver")
    parser.add_argument('fd', nargs='?', default='classic',
                        help="'fd' for CAN FD mode or nothing for classic CAN.")
    args = parser.parse_args()

    # Determine if CAN FD should be used
    use_fd = args.fd == 'fd'

    # Set up the receiver
    can_receiver = CanReceiver(channel='can0', bitrate=500000, use_fd=use_fd)

    # Start receiving messages
    can_receiver.start_receiving()

    # Close the interface when done
    can_receiver.close()
