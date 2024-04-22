
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, \
    QVBoxLayout, QTextEdit, QFileDialog, QComboBox, QLineEdit, QLabel
from PIL import Image, ExifTags
import piexif
import sys
import os


class ImageMetaEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.img = None
        self.metadata = None
        self.initUI()
        
    def initUI(self):
        """
        Initializes the user interface of the application. This method sets up the layout,
        widgets (buttons, combo box, text edit), and connects signals to the appropriate slots.
        It also configures the window settings such as title and size.

        Parameters:
        - None

        Effects:
        - Sets up the GUI components and layout of the application.
        """
        # Layout and button to open image file
        self.button = QPushButton('Open Image', self)
        self.button.clicked.connect(self.openImage)
        
        # ComboBox and LineEdit for editing metadata
        self.tagCombo = QComboBox(self)
        self.valueEdit = QLineEdit(self)
        self.saveButton = QPushButton('Save Changes', self)
        self.saveButton.clicked.connect(self.saveMetadata)

        # Text edit for displaying metadata
        self.textEdit = QTextEdit(self)
        self.textEdit.setReadOnly(True)

        # Label used as the app status.
        self.statusLabel = QLabel(self)

        # Layout configuration
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(self.tagCombo)
        layout.addWidget(self.valueEdit)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.statusLabel)
        
        self.setLayout(layout)
        self.setWindowTitle('Image Metadata Reader and Editor')
        self.setGeometry(300, 300, 350, 350)

    def openImage(self):
        """
        Opens a file dialog allowing the user to select an image file. Once a file is selected,
        it calls the loadImage method to load the image and its metadata.

        Parameters:
        - None

        Effects:
        - Opens a file dialog.
        - Loads the selected image file.
        """
        # File dialog to open an image file
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.jpg *.jpeg)', options=options)        
        if filename:
            self.loadImage(filename)
    
    def loadImage(self, filename):
        """
        Loads an image from the specified filename and retrieves its EXIF metadata.
        Calls displayMetadata to show the metadata in the GUI.

        Parameters:
        - filename (str): Path to the image file to be loaded.

        Effects:
        - Loads the image and its metadata.
        - Updates the GUI to display the loaded metadata.
        """
        # Load image from file.
        self.img = Image.open(filename)
        # Read metadata from image.
        self.metadata = self.img._getexif()
        # Display the metadata.
        self.displayMetadata()
    
    def displayMetadata(self):
        """
        Displays the metadata of the loaded image in the text edit widget. Metadata fields
        are also populated in a combo box to allow selection for editing.

        Parameters:
        - None

        Effects:
        - Updates the text edit and combo box widgets with metadata from the loaded image.
        """
        if self.metadata:
            self.textEdit.clear()
            self.tagCombo.clear()
            for tag_id, value in self.metadata.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                self.tagCombo.addItem(f"{tag}", tag_id)
                self.textEdit.append(f"{tag}: {value}")
        else:
            self.textEdit.setText('No metadata found.')
    
    def saveMetadata(self):
        """
        Saves the modified metadata to the image file. The method updates the selected metadata
        field with the new value provided by the user in the GUI. It then saves the image to a new
        file with "modified_" prefix to preserve the original image.

        The EXIF data is updated using the piexif library, which requires handling the data as a
        dictionary. Thumbnail data is safely removed to avoid complications during the save process.

        Parameters:
        - None directly, but utilizes class attributes such as self.img (current PIL Image object),
        self.tagCombo (contains the selected metadata tag), and self.valueEdit (contains the new value).

        Raises:
        - Exception: Catches and logs all exceptions related to the EXIF data handling and file operations,
        which are then displayed in the GUI.

        Effects:
        - Saves a new image file with updated metadata in the same directory as the original file.
        - Updates the GUI to display a confirmation message with the path to the saved file.
        """
        current_tag_id = self.tagCombo.currentData()
        new_value = self.valueEdit.text()

        if current_tag_id and new_value:
            try:
                # Extract the the metadata (EXIF data) from the image in a structured and editable form.
                exif_dict = piexif.load(self.img.info["exif"])

                # Remove thumbnail data to avoid issues
                exif_dict.pop("thumbnail", None)

                # Update the metadata
                for ifd_name in exif_dict:
                    if current_tag_id in exif_dict[ifd_name]:
                        # Assuming value is string
                        exif_dict[ifd_name][current_tag_id] = str(new_value).encode()  

                # Convert the modified metadata dictionary into the byte string format 
                # required by the image file.
                exif_bytes = piexif.dump(exif_dict)

                # Create a modified filename.
                new_file_name = self.create_modified_filename(self.img.filename)

                # Save the image with new metadata
                self.img.save(new_file_name, "jpeg", exif=exif_bytes)
                self.displayMetadata()
                self.statusLabel.setText(f'Metadata saved to {new_file_name}')
            except Exception as e:
                self.statusLabel.setText('Failed to save metadata: ' + str(e))

    def create_modified_filename(self, original_path):
        """
        Generates a new file path by prefixing the original filename with "modified_".

        Parameters:
        - original_path (str): The original file path of the image.

        Returns:
        - str: The new file path with "modified_" prefixed to the original filename.
        """
        dir_name = os.path.dirname(original_path)
        base_name = os.path.basename(original_path)
        return os.path.join(dir_name, "modified_" + base_name)


# Running the application
app = QApplication(sys.argv)
ex = ImageMetaEditor()
ex.show()
sys.exit(app.exec_())
