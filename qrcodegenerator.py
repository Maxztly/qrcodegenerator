import sys
import qrcode
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PySide6.QtGui import QPixmap, Qt
from io import BytesIO

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(200, 200, 400, 200)

        self.label = QLabel("Link eingeben:")
        self.link_input = QLineEdit()
        self.convert_button = QPushButton("Konvertieren")
        self.convert_button.clicked.connect(self.generate_qr_code)

        self.save_button = QPushButton("QR Code speichern")
        self.save_button.clicked.connect(self.save_qr_code)

        self.qr_img_label = QLabel(self)  # Label zum Anzeigen des QR-Codes
        self.qr_img_label.setAlignment(Qt.AlignCenter)  # Zentrieren des QR-Codes im Label

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.link_input)
        self.layout.addWidget(self.convert_button)
        self.layout.addWidget(self.qr_img_label)  # Hinzufügen des Labels zum Layout
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def generate_qr_code(self):
        data = self.link_input.text()
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img_bytes = BytesIO()
            qr_img.save(qr_img_bytes, format="PNG")
            qr_img_pixmap = QPixmap()
            qr_img_pixmap.loadFromData(qr_img_bytes.getvalue())

            self.qr_img_label.setPixmap(qr_img_pixmap)  # QR-Code im vorhandenen Label aktualisieren

    def save_qr_code(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "QR Code speichern", "", "PNG Files (*.png)")
        if file_path:
            self.qr_img_label.pixmap().save(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec())