import can


class ClassicCanReceiver:
    def __init__(self, channel='can0', bitrate=500000):
        self.channel = channel
        self.bitrate = bitrate
        self.bus = can.interface.Bus(
            channel=self.channel, bustype='socketcan', bitrate=self.bitrate)

    def start_receiving(self):
        """Start receiving CAN messages."""
        print(f"Listening for messages on {self.channel}...")

        while True:
            try:
                # Wait for a message for 10 seconds
                msg = self.bus.recv(timeout=10)
                if msg:
                    data_hex_string = "".join("%02x" % b for b in msg.data)
                    print(
                        f"Received message on {self.channel}: ID={hex(msg.arbitration_id)}, Data={data_hex_string}")
                else:
                    print("No message received within timeout period.")
            except KeyboardInterrupt:
                print("\r")
                print("Reception interrupted by user.")
                break
            except can.CanError as e:
                print(f"CAN Error: {e}")
                break

    def close(self):
        """Close the CAN interface."""
        self.bus.shutdown()
        print(f"Closed {self.channel} interface.")


# Example Usage
if __name__ == "__main__":
    # Set up the receiver on can0
    can_receiver = ClassicCanReceiver(channel='can0', bitrate=500000)

    # Start receiving messages
    can_receiver.start_receiving()

    # Close the interface when done (can be done manually if needed)
    can_receiver.close()
