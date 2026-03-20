import sys
import csv
import math
from datetime import datetime
import serial

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QListWidget
)

PORT = "COM10"   # change if your Arduino is on another COM port
BAUD = 9600


class SoundGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sound Level Monitor")
        self.resize(400, 300)

        # Quiet-room baseline from your sensor
        self.baseline = 46

        # To avoid logging repeated entries while threshold stays exceeded
        self.prev_over = 0

        self.title = QLabel("Live Sound Level")
        self.value_label = QLabel("Current Level: --- dB")
        self.status_label = QLabel("Threshold: ---")

        self.bar = QProgressBar()
        self.bar.setRange(30, 100)

        self.event_list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.value_label)
        layout.addWidget(self.status_label)
        layout.addWidget(self.bar)
        layout.addWidget(self.event_list)
        self.setLayout(layout)

        self.ser = serial.Serial(PORT, BAUD, timeout=0.1) #opens serial port

        self.csv_f = open("sound_events.csv", "a", newline="", encoding="utf-8")
        self.csv_w = csv.writer(self.csv_f)
        if self.csv_f.tell() == 0:
            self.csv_w.writerow(["timestamp", "raw_level", "estimated_db"])

        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial)
        self.timer.start(30) #every 30 ms it checks if new serial data has arrived

    def read_serial(self):
        while self.ser.in_waiting:
            line = self.ser.readline().decode(errors="ignore").strip()
            parts = line.split(",")

            if len(parts) != 3:
                continue

            try:
                arduino_ms = int(parts[0])
                sound_level = int(parts[1])
                over = int(parts[2])
            except ValueError:
                continue

            # Convert raw sensor value to estimated dB
            amplitude = max(sound_level - self.baseline, 0)
            estimated_db = 35 + 20 * math.log10(amplitude + 1)
            estimated_db = round(estimated_db, 1)

            self.value_label.setText(f"Current Level: {estimated_db} dB")

            bar_value = max(30, min(int(estimated_db), 100))
            self.bar.setValue(bar_value)

            if over == 1:
                self.status_label.setText("Threshold: EXCEEDED")
            else:
                self.status_label.setText("Threshold: NORMAL")

            # Log only when threshold changes from normal to exceeded
            if over == 1 and self.prev_over == 0:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.csv_w.writerow([ts, sound_level, estimated_db])
                self.csv_f.flush()
                self.event_list.insertItem(0, f"{ts}  |  {estimated_db} dB")

            self.prev_over = over

    def closeEvent(self, event):
        self.csv_f.close()
        self.ser.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = SoundGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
