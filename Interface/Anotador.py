"""Module Main"""
import os.path
import sys

# Implemented visual classes
from Main_Window_ui import *
from Enhance_Buttons import *
from Enhance_Sliders import *
from Edge_Detection_Buttons import *
from Manual_Detection_Buttons import *

# Include access to logic layer classes (Display, Explore, Process)
sys.path.append("C:/Users/YANIBIS/Anotador/Logic")
from Explore import *
from Display import *
from Process import *

# MAIN WINDOW
class MainWindow(QtWidgets.QMainWindow):
    """class Mainwindow implements functionalities related with the Anotador view layer"""

    # FLAGS
    btnExp_flg = 0  # used for hide/show next and previous widgets in the form
    # Enhance related flags
    enhance_buttons_flg = 0  # used for hide/show enhance buttons in the form
    enhance_sliders_flg = 0  # used for hide/show enhance sliders in the form
    gray_flg = 0  # image has been converted to gray scale
    black_white_flg = 0  # image has been converted to monocromatic
    white_black_flg = 0  # image has been converted to monocromatic inverse
    # Edge detection related flags
    gray_roi_flg = 0  # roi image has been converted to gray scale
    bw_roi_flg = 0  # roi image has been converted to monocromatic
    wb_roi_flg = 0  # roi image has been converted to monocromatic inverse
    edge_manual_flg = 0  # used for hide/show edge manual buttons in the form
    edge_detc_flg = 0  # used for hide/show edge detection buttons in the form
    edge_sobel_flg = 0  # roi image has been sobel mask filtered
    edge_laplacian_flg = 0  # roi image has been  laplacian mask filtered
    edge_canny_flg = 0  # roi image has been canny mask filtered
    edge_prewitt_flg = 0  # roi image has been prewitt mask filtered
    edge_robert_flg = 0  # roi image has been robert mask filtered
    activate_pen_flg = 0  # VERRRRRRRRRRRRRRRRRRRRRRRRRRR si es necesario

    # DATA MEMBERS
    img_index = 0  # register image index in path directory list when multiple selection
    mapped_coordinates = QtCore.QRect()  # mapped mouse click coordinates
    image_edge_rect = []  # [roi images edgeds , mapped coordinates]
    x_ini_coord = 0  # global x initial coordinantes for ROI (mouse press event)
    y_ini_coord = 0  # global y initial coordinantes for ROI (mouse press event)
    x_fin_coord = 0  # global x final coordinantes for ROI (mouse press event)
    y_fin_coord = 0  # global y final coordinantes for ROI (mouse press event)
    brightness_alpha = 1.00  # brightness enhance multiply factor
    contrast_beta = 0.00  # contrast enhance sumation factor
    b_w_threshold = 127  # contrast threshold for 8 bit gray scale images

    # Member functions
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Create class instance variables
        self.enhance_btn_inst = Enhance_Buttons()
        self.enhance_sld_inst = Enhance_Sliders()
        self.edge_detc_btn_inst = Edge_Detection_Buttons()
        self.manual_detc_btn_inst = Manual_Detection_Buttons()
        self.explore_inst = Explore()
        self.display_inst = Display()
        self.process_inst = Process()
        # HIDE/SHOW WIDGETS
        # Left frame (working over loaded original image)
        self.ui.Enhance_btn.setVisible(False)
        self.ui.Equalize_btn.setVisible(False)
        self.ui.Gray_btn.setVisible(False)
        self.ui.Black_white_btn.setVisible(False)
        self.ui.White_black_btn.setVisible(False)
        self.ui.Undo_btn.setVisible(False)
        self.ui.Label_btn.setVisible(False)
        # ROI options frame
        self.ui.single_ROI_btn.setVisible(False)
        self.ui.edge_ROI_btn.setVisible(False)
        self.ui.image_ROI_btn.setVisible(False)
        self.ui.multiple_ROI_btn.setVisible(False)
        self.ui.Undo_ROI_actions.setVisible(False)
        self.ui.ROI_color.setVisible(False)
        self.ui.ROI_width_up.setVisible(False)
        self.ui.ROI_width_down.setVisible(False)
        # Right frame (working over ROI image)
        self.ui.Edge_manual.setVisible(False)
        self.ui.Edge_detection.setVisible(False)
        self.ui.Edge_gray_btn.setVisible(False)
        self.ui.Edge_black_white_btn.setVisible(False)
        self.ui.Edge_white_black_btn.setVisible(False)
        self.ui.Undo_btn_edge.setVisible(False)
        self.ui.Mask_btn.setVisible(False)
        self.ui.Save_mask_btn.setVisible(False)
        # MENU
        self.ui.action_Open_file.triggered.connect(self.open_file_action)
        self.ui.action_Open_folder.triggered.connect(self.open_folder_action)
        self.ui.action_Enhance_buttons.triggered.connect(self.create_enhance_buttons)
        self.ui.action_Enhance_sliders.triggered.connect(self.create_enhance_sliders)
        self.ui.action_Convertir_escala_grises.triggered.connect(self.convert_to_gray)
        self.ui.action_Imagen_binaria.triggered.connect(self.convert_to_bw)
        self.ui.action_Imagen_binaria_invertida.triggered.connect(self.convert_to_wb)
        self.ui.action_Deshacer_imagen.triggered.connect(self.undo_enhance_changes)
        self.ui.action_ROI_simple.triggered.connect(self.activate_ROI_rect)
        self.ui.action_ROI_contornos.triggered.connect(self.activate_ROI_rect_edge)
        self.ui.action_ROI_multiple.triggered.connect(self.activate_multiple_ROI)
        self.ui.action_Deshacer_ROI.triggered.connect(self.undo_ROI_multiple)
        self.ui.action_Seleccionar_color.triggered.connect(self.select_ROI_color)
        self.ui.action_Aumentar_trazo.triggered.connect(self.select_ROI_width_up)
        self.ui.action_Disminuir_trazo.triggered.connect(self.select_ROI_width_down)
        self.ui.action_Crear_imagen_etiquetada.triggered.connect(
            self.create_label_image
        )
        self.ui.action_Herramientas_pintura.triggered.connect(
            self.create_edge_manual_buttons
        )
        self.ui.action_Deteccion_bordes.triggered.connect(
            self.create_edge_detection_buttons
        )
        self.ui.action_ROI_escala_grises.triggered.connect(self.edge_convert_to_gray)
        self.ui.action_ROI_binario.triggered.connect(self.edge_convert_to_bw)
        self.ui.action_ROI_binario_invertido.triggered.connect(self.edge_convert_to_wb)
        self.ui.action_Deshacer_area.triggered.connect(self.undo_edge_changes)
        self.ui.action_Ver_mascara.triggered.connect(self.create_mask_image_action)
        self.ui.action_Salvar_mascara.triggered.connect(self.save_mask_image_action)
        # BUTTONS
        self.ui.Next_file_btn.clicked.connect(self.show_next_file_action)  # next files
        self.ui.Previous_file_btn.clicked.connect(
            self.show_previous_file_action
        )  # previous files
        # Created widgets dynamically
        # Enhance menu (left frame)
        self.ui.Enhance_btn.clicked.connect(self.create_enhance_buttons)
        self.ui.Equalize_btn.clicked.connect(self.create_enhance_sliders)
        self.ui.Gray_btn.clicked.connect(self.convert_to_gray)
        self.ui.Black_white_btn.clicked.connect(self.convert_to_bw)
        self.ui.White_black_btn.clicked.connect(self.convert_to_wb)
        self.ui.Undo_btn.clicked.connect(self.undo_enhance_changes)
        self.ui.Label_btn.clicked.connect(self.create_label_image)
        # Edge detection menu (right frame)
        self.ui.Edge_manual.clicked.connect(self.create_edge_manual_buttons)
        self.ui.Edge_detection.clicked.connect(self.create_edge_detection_buttons)
        self.ui.Edge_gray_btn.clicked.connect(self.edge_convert_to_gray)
        self.ui.Edge_black_white_btn.clicked.connect(self.edge_convert_to_bw)
        self.ui.Edge_white_black_btn.clicked.connect(self.edge_convert_to_wb)
        self.ui.Undo_btn_edge.clicked.connect(self.undo_edge_changes)
        self.ui.Mask_btn.clicked.connect(self.create_mask_image_action)
        self.ui.Save_mask_btn.clicked.connect(self.save_mask_image_action)
        # ROI functionalities related buttons (vertical frame)
        self.ui.single_ROI_btn.clicked.connect(self.activate_ROI_rect)
        self.ui.edge_ROI_btn.clicked.connect(self.activate_ROI_rect_edge)
        self.ui.multiple_ROI_btn.clicked.connect(self.activate_multiple_ROI)
        self.ui.image_ROI_btn.clicked.connect(self.activate_all_image_ROI)
        self.ui.Undo_ROI_actions.clicked.connect(self.undo_ROI_multiple)
        self.ui.ROI_color.clicked.connect(self.select_ROI_color)
        self.ui.ROI_width_up.clicked.connect(self.select_ROI_width_up)
        self.ui.ROI_width_down.clicked.connect(self.select_ROI_width_down)
        # Capture mouse events with customize signals
        self.ui.Source_File.mouse_released_sig.connect(self.handle_released)
        # Show MainWindow form
        self.show()

    def handle_released(self):
        """handle_released: gets emited customize signal from mouse release event"""

        # Map mouse clicked in Qlabel coordinates respect to real image size
        MainWindow.mapped_coordinates = self.process_inst.mapped_coordinates(
            QLabelplus.rect_roi.normalized(),
            self.ui.Source_File.pixmap().rect(),
            QtCore.QRectF(self.ui.Source_File.contentsRect()),
        )
        # Create ROI image
        (
            roi_opencv_image,
            MainWindow.roi_format_indicator,
        ) = self.process_inst.define_roi(
            MainWindow.path_source[MainWindow.img_index], MainWindow.mapped_coordinates
        )
        # Single/automatic ROI edge detection validation
        if (
            QLabelplus.activate_ROI_flg == 1
            or QLabelplus.activate_ROI_all_image_flg == 1
        ):
            # Call method to convert opencv roi to pixmap
            roi_pixmap = self.display_inst.convert_cv_qt(roi_opencv_image)
            # Show ROI image in QLabel Work_Area
            self.ui.Work_Area.delete_line_list()
            self.ui.Work_Area.clear()
            self.ui.Work_Area.setPixmap(roi_pixmap)
            # Work_Area pixmap validation: Manual and automatic edge detection buttons dyamically created
            if self.ui.Work_Area.pixmap():
                self.ui.Edge_manual.setVisible(True)
                # 0: black and white [0,255]; 1: binary [0,1]; 2: gray scale [0-255]; 3: color; 10: unknown format
                if MainWindow.roi_format_indicator == 0:
                    self.ui.Edge_manual.setEnabled(True)
                self.ui.Edge_detection.setVisible(True)
                self.ui.Edge_gray_btn.setVisible(True)
                self.ui.Edge_black_white_btn.setVisible(True)
                self.ui.Edge_white_black_btn.setVisible(True)
                self.ui.Undo_btn_edge.setVisible(True)
                self.ui.Undo_btn_edge.setEnabled(False)
                self.ui.Mask_btn.setVisible(True)
                self.ui.Save_mask_btn.setVisible(True)
                self.ui.Save_mask_btn.setEnabled(False)
        elif QLabelplus.activate_ROI_edge_flg == 1:
            if QLabelplus.undo_flg == 0:
                im_edge = self.display_inst.rectangle_edge_detection(
                    MainWindow.roi_format_indicator,
                    roi_opencv_image,
                    QLabelplus.selected_color,
                    QLabelplus.pen_width,
                )
                # [im_edge, rectangle coordinates]
                temp = [
                    im_edge,
                    MainWindow.mapped_coordinates,
                ]
                MainWindow.image_edge_rect.append(temp)
            elif QLabelplus.undo_flg == 1:
                MainWindow.image_edge_rect.pop(-1)
                QLabelplus.undo_flg = 0

            for edges in MainWindow.image_edge_rect:
                Process.im_opencv[
                    edges[1].y() : edges[1].y() + edges[1].height(),
                    edges[1].x() : edges[1].x() + edges[1].width(),
                ] = edges[0]
                # Call method to convert opencv image to pixmap
                roi_pixmap = self.display_inst.convert_cv_qt(Process.im_opencv)
                # Show image with automatic edges in QLabel Source_File
                self.ui.Source_File.setPixmap(roi_pixmap)
                self.ui.Source_File.deleteRect()

    # EXPLORER ASSOCIATED TASKS
    def open_file_action(self):
        """open_file_action: implements actions associated with image's file open"""

        (
            MainWindow.path_source,
            MainWindow.btnExp_flg,
        ) = self.explore_inst.win_explore_file()
        # Hide/show components if single/multiple selection
        if MainWindow.btnExp_flg == 0:
            self.ui.Previous_file_btn.setEnabled(False)
            self.ui.Next_file_btn.setEnabled(False)
        elif MainWindow.btnExp_flg == 1:
            self.ui.Previous_file_btn.setEnabled(False)
            self.ui.Next_file_btn.setEnabled(True)
        # path_source validation: if it is formed
        if MainWindow.path_source != []:
            # Converts to pixmap the first image in path list
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[0]
            )
            # Show first image in QLabel Source_File
            self.visualize(img_source_pixmap, MainWindow.path_source[0])
        # path_source validation: if it is empty (open file action discard)
        else:
            # case 1: image loaded previously in Source_File and open file action is discard
            if self.ui.Source_File.pixmap():
                self.ui.Source_File.deleteRect()
                MainWindow.image_edge_rect = []
                self.ui.Work_Area.delete_line_list()
                self.ui.Work_Area.clear()
                MainWindow.path_source = [
                    self.ui.Dir_name.text() + "/" + self.ui.File_name.text()
                ]
                # Deactivate painting tool in Work_Area if activated
                if self.activate_pen_flg == 1:
                    self.activate_pen_flg = QLabelplusplus.activate_painting(self)
            # case 2: no loaded image in QLabel and open file action is discard
            else:
                self.ui.File_name.setText("Select an image file")

    def open_folder_action(self):
        """open_folder_action: implements actions associated with image's folder open"""

        (
            MainWindow.path_source,
            MainWindow.btnExp_flg,
        ) = self.explore_inst.win_explore_folder()
        # Hide/show components if single/multiple selection
        if MainWindow.btnExp_flg == 0:
            self.ui.Previous_file_btn.setEnabled(False)
            self.ui.Next_file_btn.setEnabled(False)
        elif MainWindow.btnExp_flg == 1:
            self.ui.Previous_file_btn.setEnabled(False)
            self.ui.Next_file_btn.setEnabled(True)
        # path_source validation: if it is formed
        if MainWindow.path_source != []:
            # Converts to pixmap the first image in path list
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[0]
            )
            # Show first image in QLabel Source_File
            self.visualize(img_source_pixmap, MainWindow.path_source[0])
        # path_source validation: if it is empty (open file action discard)
        else:
            # case 1: image loaded previously in Source_File and open file action is discard
            if self.ui.Source_File.pixmap():
                self.ui.Source_File.deleteRect()
                MainWindow.image_edge_rect = []
                self.ui.Work_Area.delete_line_list()
                self.ui.Work_Area.clear()
                MainWindow.path_source = [
                    self.ui.Dir_name.text() + "/" + self.ui.File_name.text()
                ]
                # Deactivate painting tool in Work_Area if activated
                if self.activate_pen_flg == 1:
                    self.activate_pen_flg = QLabelplusplus.activate_painting(self)
            # case 2: no loaded image in QLabel and open folder action is discard
            else:
                self.ui.File_name.setText("Select an image file")

    def show_next_file_action(self):
        """show_next_file_action: implements actions associated with next image's file exploration"""

        # Icrement img_index to point to next file
        MainWindow.img_index += 1
        # file exploration validation: if last image file hide Next_file_btn and show Previous_file_btn
        if MainWindow.img_index == (len(MainWindow.path_source) - 1):
            self.ui.Next_file_btn.setEnabled(False)
            self.ui.Previous_file_btn.setEnabled(True)
        # file exploration validation: if not last image file show Next_file_btn and Previous_file_btn
        else:
            self.ui.Next_file_btn.setEnabled(True)
            self.ui.Previous_file_btn.setEnabled(True)

        # file exploration validation: if path list (btnExp_flg) and not last image file show image
        if MainWindow.btnExp_flg == 1 and MainWindow.img_index < (
            len(MainWindow.path_source)
        ):
            # Convert to pixmap
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.visualize(
                img_source_pixmap, MainWindow.path_source[MainWindow.img_index]
            )
            # Display the image file name
            file_name = os.path.basename(MainWindow.path_source[MainWindow.img_index])
            directory_name = os.path.dirname(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.ui.File_name.setText(file_name)
            self.ui.Dir_name.setText(directory_name)

    def show_previous_file_action(self):
        """show_previous_file_action: implements actions associated with previous image's file exploration"""

        # Decrement img_index
        MainWindow.img_index -= 1
        # file exploration validation: if first image file show Next_file_btn and hide Previous_file_btn
        if MainWindow.img_index == 0:
            self.ui.Previous_file_btn.setEnabled(False)
            self.ui.Next_file_btn.setEnabled(True)
        # file exploration validation: if not first image file show Next_file_btn and Previous_file_btn
        else:
            self.ui.Next_file_btn.setEnabled(True)
            self.ui.Previous_file_btn.setEnabled(True)

        # file exploration validation: if path list (btnExp_flg) and not first image file
        if MainWindow.btnExp_flg == 1 and MainWindow.img_index >= 0:
            # Convert t pixmap
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.visualize(
                img_source_pixmap, MainWindow.path_source[MainWindow.img_index]
            )
            # Display the image file name
            file_name = os.path.basename(MainWindow.path_source[MainWindow.img_index])
            directory_name = os.path.dirname(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.ui.File_name.setText(file_name)
            self.ui.Dir_name.setText(directory_name)

    def visualize(self, pixmap_m, filename_m):
        """Manage basic actions associated with image file visualization and exploration in QLabel"""

        # pixmap_m validation: if QLabel pixmap is null (pixmap load error)
        if pixmap_m.isNull():
            self.ui.Source_File.deleteRect()
            MainWindow.image_edge_rect = []
            self.ui.Source_File.clear()
            self.ui.Source_File.setCursor(QtCore.Qt.WhatsThisCursor)
            self.ui.Work_Area.delete_line_list()
            self.ui.Work_Area.clear()
            self.ui.File_name.setText("Wrong image format")
            # Hide enhance and ROI selection buttons
            # Left frame
            self.ui.Enhance_btn.setVisible(False)
            self.ui.Equalize_btn.setVisible(False)
            self.ui.Gray_btn.setVisible(False)
            self.ui.Black_white_btn.setVisible(False)
            self.ui.White_black_btn.setVisible(False)
            self.ui.Undo_btn.setVisible(False)
            self.ui.Label_btn.setVisible(False)
            # ROI options frame
            self.ui.single_ROI_btn.setVisible(False)
            self.ui.edge_ROI_btn.setVisible(False)
            self.ui.image_ROI_btn.setVisible(False)
            self.ui.multiple_ROI_btn.setVisible(False)
            self.ui.Undo_ROI_actions.setVisible(False)
            self.ui.ROI_color.setVisible(False)
            self.ui.ROI_width_up.setVisible(False)
            self.ui.ROI_width_down.setVisible(False)
            # Destroy enhance widgets
            if MainWindow.enhance_buttons_flg == 1:
                self.deleteItemsOfLayout(Enhance_Buttons.enhancehorizontallayout)
                Enhance_Buttons.enhancehorizontallayout.deleteLater()
                MainWindow.enhance_buttons_flg = 0
            if MainWindow.enhance_sliders_flg == 1:
                self.deleteItemsOfLayout(Enhance_Sliders.enhancehorizontallayout)
                Enhance_Sliders.enhancehorizontallayout.deleteLater()
                MainWindow.enhance_sliders_flg = 0
            self.ui.left_label_indicator.setPixmap(QtGui.QPixmap("icons/no_ok.png"))
            timer = QtCore.QTimer(self)
            timer.singleShot(1000, self.clear_save_icon)
        # pixmap_m validation: if QLabel pixmap
        else:
            # Display image in QLabel widget
            self.ui.Source_File.deleteRect()
            MainWindow.image_edge_rect = []
            self.ui.Source_File.setPixmap(pixmap_m)
            self.ui.Source_File.setCursor(QtCore.Qt.ArrowCursor)
            self.ui.Work_Area.delete_line_list()
            self.ui.Work_Area.clear()
            # Display the image file name
            file_name = os.path.basename(filename_m)
            directory_name = os.path.dirname(filename_m)
            self.ui.File_name.setText(file_name)
            self.ui.Dir_name.setText(directory_name)
            # Show enhance and ROI selection buttons
            # Left frame
            self.ui.Enhance_btn.setVisible(True)
            self.ui.Equalize_btn.setVisible(True)
            self.ui.Gray_btn.setVisible(True)
            self.ui.Black_white_btn.setVisible(True)
            self.ui.White_black_btn.setVisible(True)
            self.ui.Undo_btn.setVisible(True)
            self.ui.Undo_btn.setEnabled(False)
            self.ui.Label_btn.setVisible(True)
            self.ui.Label_btn.setEnabled(False)
            # ROI options frame
            self.ui.single_ROI_btn.setVisible(True)
            self.ui.edge_ROI_btn.setVisible(True)
            self.ui.image_ROI_btn.setVisible(True)
            self.ui.multiple_ROI_btn.setVisible(True)
            self.ui.Undo_ROI_actions.setVisible(True)
            self.ui.Undo_ROI_actions.setEnabled(False)
            self.ui.ROI_color.setVisible(True)
            self.ui.ROI_width_up.setVisible(True)
            self.ui.ROI_width_down.setVisible(True)
            # Define cursor shape if related flags still activated
            if (
                QLabelplus.activate_ROI_flg == 1
                or QLabelplus.activate_ROI_edge_flg == 1
                or QLabelplus.activate_ROI_multiple_flg == 1
                or QLabelplus.activate_ROI_all_image_flg == 1
            ):
                self.ui.Source_File.setCursor(QtCore.Qt.CrossCursor)
                self.ui.Label_btn.setEnabled(True)
        # Enable Undo_btn_edge button
        self.ui.Undo_btn_edge.setEnabled(False)
        # Desable edge manual painting
        self.ui.Edge_manual.setEnabled(False)
        # Desable mask creation
        self.ui.Mask_btn.setEnabled(False)
        # Desable mask save
        self.ui.Save_mask_btn.setEnabled(False)
        # Restart ROI rectangle variables
        MainWindow.mapped_coordinates = QtCore.QRect()
        # Restart enhancement variables
        MainWindow.brightness_alpha = 1.00
        MainWindow.contrast_beta = 0.00
        # Take enhancement sliders to original position
        if MainWindow.enhance_sliders_flg == 1:
            self.enhance_sld_inst.brightnessSlider.setSliderPosition(50)
            self.enhance_sld_inst.contrastSlider.setSliderPosition(50)
        # Restart image format convertion flags
        MainWindow.gray_flg = 0
        MainWindow.black_white_flg = 0
        MainWindow.white_black_flg = 0

    # LEFT FRAME ASSOCIATED TASKS
    def create_enhance_buttons(self):
        """create_enhance_buttons: creates the sets of buttons used for source image enhancement"""

        # enhance widgets validation: if sliders set is activated when buttons set clicked, then destroy
        # sliders set
        if MainWindow.enhance_sliders_flg == 1 and MainWindow.enhance_buttons_flg == 0:
            self.delete_layout_items(Enhance_Sliders.hLayout_dynamic_left)
            Enhance_Sliders.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_sliders_flg = 0
            MainWindow.enhance_buttons_flg = 0
        # enhance widgets validation: neither sliders or buttons set when buttons set clicked, then create buttons set
        elif (
            MainWindow.enhance_buttons_flg == 0 and MainWindow.enhance_sliders_flg == 0
        ):
            # Create enhance buttons
            self.enhance_btn_inst.setupUi(self)

            self.enhance_btn_inst.Brightness_btn_plus.clicked.connect(
                self.enhance_brightness_plus_action
            )
            self.enhance_btn_inst.Brightness_btn_minus.clicked.connect(
                self.enhance_brightness_minus_action
            )
            self.enhance_btn_inst.Contrast_btn_plus.clicked.connect(
                self.enhance_contrast_plus_action
            )
            self.enhance_btn_inst.Contrast_btn_minus.clicked.connect(
                self.enhance_contrast_minus_action
            )
            # Update related flags
            MainWindow.enhance_sliders_flg = 0
            MainWindow.enhance_buttons_flg = 1
        # enhance widgets validation: if buttons set when buttons set clicked, then destroy buttons set
        elif (
            MainWindow.enhance_buttons_flg == 1 and MainWindow.enhance_sliders_flg == 0
        ):
            self.delete_layout_items(Enhance_Buttons.hLayout_dynamic_left)
            Enhance_Buttons.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_sliders_flg = 0
            MainWindow.enhance_buttons_flg = 0

    def create_enhance_sliders(self):
        """create_enhance_sliders: creates the sets of sliders used for source image enhancement"""

        # enhance widgets validation: if buttons set when sliders set clicked, then destroy buttons set
        if MainWindow.enhance_buttons_flg == 1 and MainWindow.enhance_sliders_flg == 0:
            self.delete_layout_items(Enhance_Buttons.hLayout_dynamic_left)
            Enhance_Buttons.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_buttons_flg = 0
            MainWindow.enhance_sliders_flg = 0
        # enhance widgets validation: neither sliders or buttons set when sliders set clicked, then create sliders set
        elif (
            MainWindow.enhance_sliders_flg == 0 and MainWindow.enhance_buttons_flg == 0
        ):
            # Instantiate Enhance_Sliders class and define sliders actions
            self.enhance_sld_inst.setupUi(self)

            self.enhance_sld_inst.brightnessSlider.valueChanged.connect(
                self.enhance_brightness_slider_action
            )
            self.enhance_sld_inst.contrastSlider.valueChanged.connect(
                self.enhance_contrast_slider_action
            )

            # Take sliders to position respect to buttons actions
            # enhance_sld_inst = Enhance_Sliders()
            self.enhance_sld_inst.brightnessSlider.setSliderPosition(
                int(MainWindow.brightness_alpha * 50)
            )
            self.enhance_sld_inst.contrastSlider.setSliderPosition(
                int((MainWindow.contrast_beta + 100) / 2)
            )

            # Update related flags
            MainWindow.enhance_buttons_flg = 0
            MainWindow.enhance_sliders_flg = 1
        # enhance widgets validation: if sliders set when sliders set clicked, then destroy sliders set
        elif (
            MainWindow.enhance_sliders_flg == 1 and MainWindow.enhance_buttons_flg == 0
        ):
            self.delete_layout_items(Enhance_Sliders.hLayout_dynamic_left)
            Enhance_Sliders.hLayout_dynamic_left.deleteLater()
            # Update related flags
            MainWindow.enhance_buttons_flg = 0
            MainWindow.enhance_sliders_flg = 0

    def delete_layout_items(self, layout):
        """delete_layout_items: deletes the dinamically created QHBoxLayout and its widgets"""

        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    delete_layout_items(item.layout())

    def enhance_brightness_plus_action(self, value):
        """enhance_brightness_plus_action: increments source image brightness trhough buttons"""

        # Buttons widgets. Increments alpha using a rate value for brightness of 0.05
        MainWindow.brightness_alpha += 0.05

        # Call method brightness_contrast for modify brighness
        img_enhance = self.display_inst.brightness_contrast(
            MainWindow.brightness_alpha,
            MainWindow.contrast_beta,
            MainWindow.path_source[MainWindow.img_index],
        )
        # Show the image with its brightness modify
        self.ui.Source_File.setPixmap(img_enhance)
        # Enable Undo_btn
        self.ui.Undo_btn.setEnabled(True)

    def enhance_brightness_minus_action(self, value):
        """enhance_brightness_minus_action: decrements source image brightness trhough buttons"""

        # Buttons widgets. Decrements alpha using a rate value for brightness of 0.05
        MainWindow.brightness_alpha -= 0.05

        # Call method brightness_contrast for modify brighness
        img_enhance = self.display_inst.brightness_contrast(
            MainWindow.brightness_alpha,
            MainWindow.contrast_beta,
            MainWindow.path_source[MainWindow.img_index],
        )
        # Show the image with its brightness modify
        self.ui.Source_File.setPixmap(img_enhance)
        # Enable Undo_btn
        self.ui.Undo_btn.setEnabled(True)

    def enhance_contrast_plus_action(self, value):
        """enhance_contrast_plus_action: increments source image contrast trhough buttons"""
        # Sliders widgets. Normalize alpha value beetwen -99 - 99
        if value:
            MainWindow.contrast_beta = (value * 2) - 99
            print(MainWindow.contrast_beta)
        # Buttons widgets. Increments beta using a rate value for contrast of 10
        else:
            MainWindow.contrast_beta += 10

        # Call method brightness_contrast for modify contrast
        img_enhance = self.display_inst.brightness_contrast(
            MainWindow.brightness_alpha,
            MainWindow.contrast_beta,
            MainWindow.path_source[MainWindow.img_index],
        )
        # Show the image with its contrast modify
        self.ui.Source_File.setPixmap(img_enhance)
        # Enable Undo_btn
        self.ui.Undo_btn.setEnabled(True)

    def enhance_contrast_minus_action(self, value):
        """enhance_contrast_minus_action: decrements source image contrast trhough buttons"""

        # Buttons widgets. Decrements beta using a rate value for contrast of 10
        MainWindow.contrast_beta -= 10

        # Call method brightness_contrast for modify contrast
        img_enhance = self.display_inst.brightness_contrast(
            MainWindow.brightness_alpha,
            MainWindow.contrast_beta,
            MainWindow.path_source[MainWindow.img_index],
        )
        # Show the image with its contrast modify
        self.ui.Source_File.setPixmap(img_enhance)  # Enable Undo_btn
        self.ui.Undo_btn.setEnabled(True)

    def enhance_brightness_slider_action(self, value):
        """enhance_brightness_slider_action: increments source image brightness trhough sliders"""

        # Sliders widgets. Normalize alpha value beetwen 0 - 2
        MainWindow.brightness_alpha = value / 50
        # Call method brightness_contrast for modify brightness
        img_enhance = self.display_inst.brightness_contrast(
            MainWindow.brightness_alpha,
            MainWindow.contrast_beta,
            MainWindow.path_source[MainWindow.img_index],
        )
        # Show the image with its brightness modify
        self.ui.Source_File.setPixmap(img_enhance)
        # Enable Undo_btn
        if MainWindow.brightness_alpha != 1.0 or MainWindow.contrast_beta != 0.0:
            self.ui.Undo_btn.setEnabled(True)

    def enhance_contrast_slider_action(self, value):
        """enhance_contrast_slider_action: increments source image contrast trhough sliders"""

        # Sliders widgets. Normalize alpha value beetwen -99 - 99
        MainWindow.contrast_beta = (value * 2) - 100
        # Call method brightness_contrast for modify contrast
        img_enhance = self.display_inst.brightness_contrast(
            MainWindow.brightness_alpha,
            MainWindow.contrast_beta,
            MainWindow.path_source[MainWindow.img_index],
        )
        # Show the image with its contrast modify
        self.ui.Source_File.setPixmap(img_enhance)
        # Enable Undo_btn
        if MainWindow.brightness_alpha != 1.0 or MainWindow.contrast_beta != 0.0:
            self.ui.Undo_btn.setEnabled(True)

    def convert_to_gray(self):
        """convert_to_gray: converts loaded image to gray scale"""

        # Deactivate brightness and contrast options
        if MainWindow.enhance_sliders_flg == 1:
            self.delete_layout_items(Enhance_Sliders.hLayout_dynamic_left)
            Enhance_Sliders.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_sliders_flg = 0
        if MainWindow.enhance_buttons_flg == 1:
            self.delete_layout_items(Enhance_Buttons.hLayout_dynamic_left)
            Enhance_Buttons.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_buttons_flg = 0
        # Call method convert_to_gray_scale for modify image
        gray_img, MainWindow.gray_flg = self.display_inst.convert_to_gray_scale(
            MainWindow.path_source[MainWindow.img_index]
        )
        self.ui.Source_File.setPixmap(gray_img)
        # Enable Undo_btn
        self.ui.Undo_btn.setEnabled(True)

    def convert_to_bw(self):
        """converto_to_bw: converts loaded image to monocromatic image"""

        # Deactivate brightness and contrast options
        if MainWindow.enhance_sliders_flg == 1:
            self.delete_layout_items(Enhance_Sliders.hLayout_dynamic_left)
            Enhance_Sliders.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_sliders_flg = 0
        if MainWindow.enhance_buttons_flg == 1:
            self.delete_layout_items(Enhance_Buttons.hLayout_dynamic_left)
            Enhance_Buttons.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_buttons_flg = 0
        # Call method convert_to_black_white for modify image
        bw_img, MainWindow.black_white_flg = self.display_inst.convert_to_black_white(
            MainWindow.path_source[MainWindow.img_index]
        )
        self.ui.Source_File.setPixmap(bw_img)
        # Enable Undo_btn
        self.ui.Undo_btn.setEnabled(True)

    def convert_to_wb(self):
        """convert_to_wb: converts loaded image to monocromatic image"""

        # Deactivate brightness and contrast options
        if MainWindow.enhance_sliders_flg == 1:
            self.delete_layout_items(Enhance_Sliders.hLayout_dynamic_left)
            Enhance_Sliders.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_sliders_flg = 0
        if MainWindow.enhance_buttons_flg == 1:
            self.delete_layout_items(Enhance_Buttons.hLayout_dynamic_left)
            Enhance_Buttons.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_buttons_flg = 0
        # Call method convert_to_black_white_inv for modify image
        (
            wb_img,
            MainWindow.white_black_flg,
        ) = self.display_inst.convert_to_black_white_inv(
            MainWindow.path_source[MainWindow.img_index]
        )
        self.ui.Source_File.setPixmap(wb_img)
        # Enable Undo_btn
        self.ui.Undo_btn.setEnabled(True)

    def create_label_image(self):
        """create_label_image: creates a label image based on original loaded image"""

        # temp_text = self.ui.Dir_name.text()
        self.ui.Dir_name.setText("¡Image file labeled save!")

        # Deactivate brightness and contrast options
        if MainWindow.enhance_sliders_flg == 1:
            self.delete_layout_items(Enhance_Sliders.hLayout_dynamic_left)
            Enhance_Sliders.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_sliders_flg = 0
        if MainWindow.enhance_buttons_flg == 1:
            self.delete_layout_items(Enhance_Buttons.hLayout_dynamic_left)
            Enhance_Buttons.hLayout_dynamic_left.deleteLater()
            # Reset related flags
            MainWindow.enhance_buttons_flg = 0
        # Save single ROI rectangle labeled image
        if (
            QLabelplus.rect_roi
            and len(QLabelplus.rect_roi_multiple) == 0
            and len(MainWindow.image_edge_rect) == 0
        ):
            try:
                self.ui.Source_File.single_label_img(
                    self.process_inst.im_opencv,
                    MainWindow.path_source[MainWindow.img_index],
                    MainWindow.mapped_coordinates,
                )
                self.ui.left_label_indicator.setPixmap(QtGui.QPixmap("icons/ok.png"))
                timer = QtCore.QTimer(self)
                timer.singleShot(1000, self.clear_save_icon)
            except Exception:
                self.ui.left_label_indicator.setPixmap(QtGui.QPixmap("icons/no_ok.png"))
                timer = QtCore.QTimer(self)
                timer.singleShot(1000, self.clear_save_icon)
        # Save multiple ROI rectangles labeled image
        elif (
            QLabelplus.rect_roi
            and len(QLabelplus.rect_roi_multiple) > 0
            and len(MainWindow.image_edge_rect) == 0
        ):
            # [rectangle mapped coordinates, rectangle color, rectangle width]
            mapped_roi = []
            for rectangles in QLabelplus.rect_roi_multiple:
                mapped_coordinates = [
                    self.process_inst.mapped_coordinates(
                        rectangles[0].normalized(),
                        self.ui.Source_File.pixmap().rect(),
                        QtCore.QRectF(self.ui.Source_File.contentsRect()),
                    ),
                    rectangles[1],
                    rectangles[2],
                ]
                mapped_roi.append(mapped_coordinates)
            try:
                self.ui.Source_File.multiple_label_img(
                    self.process_inst.im_opencv,
                    MainWindow.path_source[MainWindow.img_index],
                    mapped_roi,
                )
                self.ui.left_label_indicator.setPixmap(QtGui.QPixmap("icons/ok.png"))
                timer = QtCore.QTimer(self)
                timer.singleShot(1000, self.clear_save_icon)
            except Exception:
                self.ui.left_label_indicator.setPixmap(QtGui.QPixmap("icons/no_ok.png"))
                timer = QtCore.QTimer(self)
                timer.singleShot(1000, self.clear_save_icon)
        # Save automatic ROI rectangle contoured image
        elif len(MainWindow.image_edge_rect) > 0:
            img_name = os.path.basename(MainWindow.path_source[MainWindow.img_index])
            img_directory = os.path.dirname(
                MainWindow.path_source[MainWindow.img_index]
            )
            try:
                cv2.imwrite(
                    img_directory + "/" + "contoured_" + img_name, Process.im_opencv
                )
                self.ui.left_label_indicator.setPixmap(QtGui.QPixmap("icons/ok.png"))
                timer = QtCore.QTimer(self)
                timer.singleShot(1000, self.clear_save_icon)
            except Exception:
                self.ui.left_label_indicator.setPixmap(QtGui.QPixmap("icons/no_ok.png"))
                timer = QtCore.QTimer(self)
                timer.singleShot(1000, self.clear_save_icon)

    def clear_save_icon(self):
        if self.ui.left_label_indicator.pixmap():
            self.ui.left_label_indicator.clear()
        elif self.ui.right_label_indicator.pixmap():
            self.ui.right_label_indicator.clear()

    def undo_enhance_changes(self):
        """undo_enhance_changes: undo all enhance changes made to image"""

        # Modify if changes related to enhancement needs to be manage
        modify_enhancement_flg = 0
        if (
            MainWindow.gray_flg == 1
            or MainWindow.black_white_flg == 1
            or MainWindow.white_black_flg == 1
        ):
            modify_enhancement_flg = 1

        # enhance validation: if alpha or beta are the default values
        if (
            MainWindow.brightness_alpha != 1.0
            or MainWindow.contrast_beta != 0.0
            or modify_enhancement_flg == 1
        ):
            # Call method for show the original source image
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.visualize(
                img_source_pixmap, MainWindow.path_source[MainWindow.img_index]
            )
            # Display the image file name
            file_name = os.path.basename(MainWindow.path_source[MainWindow.img_index])
            directory_name = os.path.dirname(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.ui.File_name.setText(file_name)
            self.ui.Dir_name.setText(directory_name)

    # ROI VERTICAL FRAME
    def activate_ROI_rect(self):
        """activate_ROI_rect: aditional functionalities related with ROI area selection"""

        # ROI selection area validation: if selection deactivated and pixmap, then delete rectangle
        if (
            QLabelplus.activate_ROI_flg == 1
            or QLabelplus.activate_ROI_edge_flg == 1
            or QLabelplus.activate_ROI_multiple_flg == 1
            or QLabelplus.activate_ROI_all_image_flg == 1
        ) and self.ui.Source_File.pixmap():
            QLabelplus.activate_ROI_edge_flg = 0
            QLabelplus.activate_ROI_multiple_flg = 0
            QLabelplus.activate_ROI_all_image_flg = 0
            # Clear not involve lists
            self.ui.Source_File.deleteRect()
            MainWindow.image_edge_rect = []
            # Call method for show the original source image
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.visualize(
                img_source_pixmap, MainWindow.path_source[MainWindow.img_index]
            )
        # activate_ROI_flg activates/deactivates the selection area
        QLabelplus.activate_ROI(self)
        if QLabelplus.activate_ROI_flg == 1:
            self.ui.Source_File.setCursor(QtCore.Qt.CrossCursor)
            self.ui.Undo_ROI_actions.setEnabled(False)
            self.ui.Label_btn.setEnabled(True)
        elif QLabelplus.activate_ROI_flg == 0:
            self.ui.Source_File.setCursor(QtCore.Qt.ArrowCursor)
            self.ui.Label_btn.setEnabled(False)

    def activate_ROI_rect_edge(self):

        # Clear Work_Area qlabel, free painting and qrect in Source_File qlabel
        self.ui.Work_Area.delete_line_list()
        self.ui.Work_Area.clear()
        # ROI selection area validation: if selection deactivated and pixmap, then delete rectangle
        if (
            QLabelplus.activate_ROI_flg == 1
            or QLabelplus.activate_ROI_edge_flg == 1
            or QLabelplus.activate_ROI_multiple_flg == 1
            or QLabelplus.activate_ROI_all_image_flg == 1
        ) and self.ui.Source_File.pixmap():
            QLabelplus.activate_ROI_flg = 0
            QLabelplus.activate_ROI_multiple_flg = 0
            QLabelplus.activate_ROI_all_image_flg = 0
            # Clear not involve lists
            self.ui.Source_File.deleteRect()
            MainWindow.image_edge_rect = []
            # Call method for show the original source image
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.visualize(
                img_source_pixmap, MainWindow.path_source[MainWindow.img_index]
            )
        # activate_ROI_edge_flg activates/deactivates the edge rectangle selection
        QLabelplus.activate_ROI_edge(self)
        if QLabelplus.activate_ROI_edge_flg == 1:
            self.ui.Source_File.setCursor(QtCore.Qt.CrossCursor)
            self.ui.Undo_ROI_actions.setEnabled(True)
            self.ui.Label_btn.setEnabled(True)
        elif QLabelplus.activate_ROI_edge_flg == 0:
            self.ui.Source_File.setCursor(QtCore.Qt.ArrowCursor)
            self.ui.Label_btn.setEnabled(False)

    def activate_multiple_ROI(self):
        """activate_multiple_ROI: aditional functionalities related with multiple ROI area selection"""

        # Clear Work_Area qlabel, free painting and qrect in Source_File qlabel
        self.ui.Work_Area.delete_line_list()
        self.ui.Work_Area.clear()
        # ROI selection area validation: if selection deactivated and pixmap, then delete rectangle
        if (
            QLabelplus.activate_ROI_flg == 1
            or QLabelplus.activate_ROI_edge_flg == 1
            or QLabelplus.activate_ROI_multiple_flg == 1
            or QLabelplus.activate_ROI_all_image_flg == 1
        ) and self.ui.Source_File.pixmap():
            QLabelplus.activate_ROI_flg = 0
            QLabelplus.activate_ROI_edge_flg = 0
            QLabelplus.activate_ROI_all_image_flg = 0
            # Clear not involve lists
            self.ui.Source_File.deleteRect()
            MainWindow.image_edge_rect = []
            # Call method for show the original source image
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.visualize(
                img_source_pixmap, MainWindow.path_source[MainWindow.img_index]
            )
        # activate_multiple_ROI_flg activates/deactivates the multiple selection area
        QLabelplus.activate_ROI_multiple(self)
        if QLabelplus.activate_ROI_multiple_flg == 1:
            self.ui.Source_File.setCursor(QtCore.Qt.CrossCursor)
            self.ui.Undo_ROI_actions.setEnabled(True)
            self.ui.Label_btn.setEnabled(True)
        elif QLabelplus.activate_ROI_multiple_flg == 0:
            self.ui.Source_File.setCursor(QtCore.Qt.ArrowCursor)
            self.ui.Label_btn.setEnabled(False)

    def undo_ROI_multiple(self):

        if (QLabelplus.activate_ROI_multiple_flg == 1) and len(
            QLabelplus.rect_roi_multiple
        ) > 0:
            QLabelplus.undo_ROI_multiple_roi(self)
        elif (
            QLabelplus.activate_ROI_edge_flg == 1
            and len(MainWindow.image_edge_rect) > 0
        ):
            QLabelplus.undo_ROI_multiple_roi(self)

    def select_ROI_color(self):
        col = QtWidgets.QColorDialog.getColor()
        if col.isValid():
            QLabelplus.ROI_color(col.name())

    def select_ROI_width_up(self):
        QLabelplus.ROI_width(self, 1)

    def select_ROI_width_down(self):
        QLabelplus.ROI_width(self, 0)

    def activate_all_image_ROI(self):
        # Clear Work_Area qlabel, free painting and qrect in Source_File qlabel
        self.ui.Work_Area.delete_line_list()
        self.ui.Work_Area.clear()
        # ROI selection area validation: if selection deactivated and pixmap, then delete rectangle
        if (
            QLabelplus.activate_ROI_flg == 1
            or QLabelplus.activate_ROI_edge_flg == 1
            or QLabelplus.activate_ROI_multiple_flg == 1
            or QLabelplus.activate_ROI_all_image_flg == 1
        ) and self.ui.Source_File.pixmap():
            QLabelplus.activate_ROI_flg = 0
            QLabelplus.activate_ROI_edge_flg = 0
            QLabelplus.activate_ROI_multiple_flg = 0
            # Clear not involve lists
            self.ui.Source_File.deleteRect()
            MainWindow.image_edge_rect = []
            # Call method for show the original source image
            img_source_pixmap = self.display_inst.convert_to_pixmap(
                MainWindow.path_source[MainWindow.img_index]
            )
            self.visualize(
                img_source_pixmap, MainWindow.path_source[MainWindow.img_index]
            )
        # activate_multiple_ROI_flg activates/deactivates the multiple selection area
        QLabelplus.activate_ROI_all_image(self)
        if QLabelplus.activate_ROI_all_image_flg == 1:
            self.ui.Source_File.setCursor(QtCore.Qt.CrossCursor)
            self.ui.Undo_ROI_actions.setEnabled(False)
        elif QLabelplus.activate_ROI_all_image_flg == 0:
            self.ui.Source_File.setCursor(QtCore.Qt.ArrowCursor)

    # RIGHT FRAME ASSOCIATED TASKS
    def create_edge_manual_buttons(self):
        """create_edge_manual_buttons: creates the sets of buttons used for manual detection methods"""

        # manual edge widgets validation: if detection edge set when manual edge set clicked, then destroy detection edge set
        if MainWindow.edge_detc_flg == 1 and MainWindow.edge_manual_flg == 0:
            self.delete_layout_items(Edge_Detection_Buttons.hLayout_dynamic_right)
            Edge_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_manual_flg = 0
            MainWindow.edge_detc_flg = 0
        # manual edge widgets validation: neither detction or manual edge buttons set, then create manual edge buttons set
        elif MainWindow.edge_detc_flg == 0 and MainWindow.edge_manual_flg == 0:
            # Instantiate Manual_Edge_Buttons class and define manual detection buttons actions
            # manual_detc_btn_inst = Manual_Detection_Buttons()
            self.manual_detc_btn_inst.setupUi(self)

            self.manual_detc_btn_inst.Pen_b_btn.clicked.connect(
                self.manual_detection_pen_b_action
            )
            self.manual_detc_btn_inst.Pen_w_btn.clicked.connect(
                self.manual_detection_pen_w_action
            )
            self.manual_detc_btn_inst.Paint_width_up.clicked.connect(
                self.manual_detection_width_up_action
            )
            self.manual_detc_btn_inst.Paint_width_down.clicked.connect(
                self.manual_detection_width_down_action
            )
            self.manual_detc_btn_inst.Undo_paint_btn.clicked.connect(
                self.manual_detection_undo_paint_action
            )

            # Update related flags
            MainWindow.edge_detc_flg = 0
            MainWindow.edge_manual_flg = 1
        # manual edge widgets validation: if manual edge set when manual edge set clicked, then destroy manual edge set
        elif MainWindow.edge_detc_flg == 0 and MainWindow.edge_manual_flg == 1:
            self.delete_layout_items(Manual_Detection_Buttons.hLayout_dynamic_right)
            Manual_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_manual_flg = 0
            MainWindow.edge_detc_flg = 0

    def create_edge_detection_buttons(self):
        """create_edge_detection_buttons: creates the sets of buttons used for automatic detection methods"""

        # detection edge widgets validation: if manual edge set when detection edge set clicked, then destroy manual edge set
        if MainWindow.edge_manual_flg == 1 and MainWindow.edge_detc_flg == 0:
            self.delete_layout_items(Manual_Detection_Buttons.hLayout_dynamic_right)
            Manual_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_manual_flg = 0
            MainWindow.edge_detc_flg = 0
        # detection edge widgets validation: neither manual or detection edge buttons set, then create detection edge buttons set
        elif MainWindow.edge_manual_flg == 0 and MainWindow.edge_detc_flg == 0:
            # Instantiate Detection_Edge_Buttons class and define edges detection buttons actions
            # edge_detc_btn_inst = Edge_Detection_Buttons()
            self.edge_detc_btn_inst.setupUi(self)

            self.edge_detc_btn_inst.Sobel_btn.clicked.connect(
                self.edge_detection_sobel_action
            )
            self.edge_detc_btn_inst.Laplacian_btn.clicked.connect(
                self.edge_detection_laplacian_action
            )
            self.edge_detc_btn_inst.Canny_btn.clicked.connect(
                self.edge_detection_canny_action
            )
            self.edge_detc_btn_inst.Prewitt_btn.clicked.connect(
                self.edge_detection_prewitt_action
            )
            self.edge_detc_btn_inst.Robert_btn.clicked.connect(
                self.edge_detection_robert_action
            )
            self.edge_detc_btn_inst.Thresh_bw_slider.valueChanged.connect(
                self.edge_bw_threshold_action
            )

            # Update related flags
            MainWindow.edge_manual_flg = 0
            MainWindow.edge_detc_flg = 1
        # detection edge widgets validation: if detection edge set when detection edge set clicked, then destroy detection edge set
        elif MainWindow.edge_manual_flg == 0 and MainWindow.edge_detc_flg == 1:
            self.delete_layout_items(Edge_Detection_Buttons.hLayout_dynamic_right)
            Edge_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_manual_flg = 0
            MainWindow.edge_detc_flg = 0
        # Desable edge manual painting
        self.ui.Edge_manual.setEnabled(False)

    def edge_convert_to_gray(self):
        """edge_convert_to_gray:"""

        # Deactivate automatic edge and manual detection options
        if MainWindow.edge_detc_flg == 1:
            self.delete_layout_items(Edge_Detection_Buttons.hLayout_dynamic_right)
            Edge_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_detc_flg = 0
        if MainWindow.edge_manual_flg == 1:
            self.delete_layout_items(Manual_Detection_Buttons.hLayout_dynamic_right)
            Manual_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_manual_flg = 0

        if self.ui.Work_Area.pixmap():
            # Call method for convert to gray
            gray_roi, MainWindow.gray_roi_flg = self.process_inst.convert_to_gray()
            gray_roi_pixmap = self.display_inst.convert_cv_qt(gray_roi)
            # Show gray ROI image
            self.ui.Work_Area.setPixmap(gray_roi_pixmap)
            # Enable Undo_btn_edge button
            self.ui.Undo_btn_edge.setEnabled(True)
            # Desable edge manual painting
            self.ui.Edge_manual.setEnabled(False)
            # Desable mask creation
            self.ui.Mask_btn.setEnabled(False)
            # Desable mask save
            self.ui.Save_mask_btn.setEnabled(False)
            # Reset flags
            MainWindow.bw_roi_flg = 0
            MainWindow.wb_roi_flg = 0

    def edge_convert_to_bw(self):
        """edge_convert_to_bw: convert to black and white ROI image related actions"""

        # Deactivate automatic edge and manual detection options
        if MainWindow.edge_detc_flg == 1:
            self.delete_layout_items(Edge_Detection_Buttons.hLayout_dynamic_right)
            Edge_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_detc_flg = 0
        if MainWindow.edge_manual_flg == 1:
            self.delete_layout_items(Manual_Detection_Buttons.hLayout_dynamic_right)
            Manual_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_manual_flg = 0

        if MainWindow.mapped_coordinates:
            # Call method for convert to black and white
            (
                bw_roi,
                MainWindow.bw_roi_flg,
            ) = self.process_inst.convert_to_black_white()
            # Instantiate Display class and call method to convert opencv to pixmap
            bw_roi_pixmap = self.display_inst.convert_cv_qt(bw_roi)
            # Show black and white ROI image
            self.ui.Work_Area.setPixmap(bw_roi_pixmap)
            # Enable Undo_btn_edge button
            self.ui.Undo_btn_edge.setEnabled(True)
            # Enable edge manual painting
            self.ui.Edge_manual.setEnabled(True)
            # Enable mask creation
            self.ui.Mask_btn.setEnabled(True)
            # Reset flags
            MainWindow.gray_roi_flg = 0
            MainWindow.wb_roi_flg = 0

    def edge_convert_to_wb(self):
        """edge_convert_to_wb: convert to white and black ROI image related actions"""

        # Deactivate automatic edge and manual detection options
        if MainWindow.edge_detc_flg == 1:
            self.delete_layout_items(Edge_Detection_Buttons.hLayout_dynamic_right)
            Edge_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_detc_flg = 0
        if MainWindow.edge_manual_flg == 1:
            self.delete_layout_items(Manual_Detection_Buttons.hLayout_dynamic_right)
            Manual_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_manual_flg = 0

        if MainWindow.mapped_coordinates:
            # Call method for convert to black and white inv
            (
                wb_roi,
                MainWindow.wb_roi_flg,
            ) = self.process_inst.convert_to_white_black()
            wb_roi_pixmap = self.display_inst.convert_cv_qt(wb_roi)
            # Show white and black ROI image
            self.ui.Work_Area.setPixmap(wb_roi_pixmap)
            # Enable Undo_btn_edge button
            self.ui.Undo_btn_edge.setEnabled(True)
            # Enable edge manual painting
            self.ui.Edge_manual.setEnabled(True)
            # Enable mask creation
            self.ui.Mask_btn.setEnabled(True)
            # Reset flags
            MainWindow.gray_roi_flg = 0
            MainWindow.bw_roi_flg = 0

    def undo_edge_changes(self):
        """undo_edge_changes: undo made changes in ROI image"""

        # Modify if changes related to enhancement needs to be manage
        modify_roi_enhancement_flg = 0
        if (
            MainWindow.gray_roi_flg == 1
            or MainWindow.bw_roi_flg == 1
            or MainWindow.wb_roi_flg == 1
        ):
            modify_roi_enhancement_flg = 1

        # enhance validation: if alpha or beta are the default values
        if modify_roi_enhancement_flg == 1:

            # Call methods for adecuate ROI formation
            # Create ROI image
            (
                roi_opencv_image,
                MainWindow.roi_format_indicator,
            ) = self.process_inst.define_roi(
                MainWindow.path_source[MainWindow.img_index],
                MainWindow.mapped_coordinates,
            )
            # Instantiate Display class and call method to convert defined_roi_opencv_image to pixmap
            display_inst_process = Display()
            roi_pixmap = display_inst_process.convert_cv_qt(roi_opencv_image)
            # Show ROI image in QLabel Work_Area
            self.ui.Work_Area.setPixmap(roi_pixmap)
            # Reset flags
            MainWindow.gray_roi_flg = 0
            MainWindow.bw_roi_flg = 0
            MainWindow.wb_roi_flg = 0
            modify_roi_enhancement_flg = 0
            self.ui.Undo_btn_edge.setEnabled(False)
            self.ui.Edge_manual.setEnabled(False)
            self.ui.Mask_btn.setEnabled(False)

    def create_mask_image_action(self):
        """create_mask_image: creates black/white image mask based on ROI selected area"""

        # Deactivate automatic edge and manual detection options
        if MainWindow.edge_detc_flg == 1:
            self.delete_layout_items(Edge_Detection_Buttons.hLayout_dynamic_right)
            Edge_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_detc_flg = 0
        if MainWindow.edge_manual_flg == 1:
            self.delete_layout_items(Manual_Detection_Buttons.hLayout_dynamic_right)
            Manual_Detection_Buttons.hLayout_dynamic_right.deleteLater()
            # Reset related flags
            MainWindow.edge_manual_flg = 0

        # Transformation validation
        if MainWindow.roi_format_indicator == 0:
            roi_img = Process.im_opencv_roi
        elif MainWindow.bw_roi_flg == 1:
            roi_img, _ = self.process_inst.convert_to_black_white()
        elif MainWindow.wb_roi_flg == 1:
            roi_img, _ = self.process_inst.convert_to_white_black()
        elif MainWindow.edge_sobel_flg == 1:
            roi_img = self.process_inst.sobel_detection(MainWindow.b_w_threshold)
        elif MainWindow.edge_laplacian_flg == 1:
            roi_img = self.process_inst.laplacian_detection(MainWindow.b_w_threshold)
        elif MainWindow.edge_canny_flg == 1:
            roi_img = self.process_inst.canny_detection(MainWindow.b_w_threshold)
        elif MainWindow.edge_prewitt_flg == 1:
            roi_img = self.process_inst.prewitt_detection(MainWindow.b_w_threshold)
        elif MainWindow.edge_robert_flg == 1:
            roi_img = self.process_inst.robert_detection(MainWindow.b_w_threshold)
        else:
            self.ui.right_label_indicator.setPixmap(QtGui.QPixmap("icons/no_ok.png"))
            timer = QtCore.QTimer(self)
            timer.singleShot(1000, self.clear_save_icon)
            self.ui.Dir_name.setText("Image must be in binary format(black and white)")
            return
        # Painting validation
        if len(QLabelplusplus.segment_line_list) > 0:
            roi_img = self.ui.Work_Area.painting_mask(roi_img)
        # img_size: size of original image
        img_size = [
            self.ui.Source_File.pixmap().rect().height(),
            self.ui.Source_File.pixmap().rect().width(),
        ]
        # Black background
        MainWindow.img_output = np.zeros(img_size, dtype=np.uint8)
        # White background
        if MainWindow.bw_roi_flg == 1:
            MainWindow.img_output[:, :] = 255
        # elif MainWindow.wb_

        MainWindow.img_output[
            MainWindow.mapped_coordinates.y() : (
                MainWindow.mapped_coordinates.y()
                + MainWindow.mapped_coordinates.height()
            ),
            MainWindow.mapped_coordinates.x() : (
                MainWindow.mapped_coordinates.x()
                + MainWindow.mapped_coordinates.width()
            ),
        ] = roi_img
        # Call method to convert opencv to pixmap
        img_output_pixmap = self.display_inst.convert_cv_qt(MainWindow.img_output)

        self.ui.Work_Area.delete_line_list()
        self.ui.Work_Area.clear()
        self.ui.Work_Area.setPixmap(img_output_pixmap)
        self.ui.Save_mask_btn.setEnabled(True)

    def save_mask_image_action(self):
        """save_mask_image_action: save created image mask based on ROI selected area"""

        img_name = os.path.basename(MainWindow.path_source[MainWindow.img_index])
        img_directory = os.path.dirname(MainWindow.path_source[MainWindow.img_index])
        try:
            cv2.imwrite(
                img_directory + "/" + "masked_" + img_name, MainWindow.img_output
            )
            self.ui.right_label_indicator.setPixmap(QtGui.QPixmap("icons/ok.png"))
            timer = QtCore.QTimer(self)
            timer.singleShot(1000, self.clear_save_icon)
        except Exception:
            self.ui.right_label_indicator.setPixmap(QtGui.QPixmap("icons/no_ok.png"))
            timer = QtCore.QTimer(self)
            timer.singleShot(1000, self.clear_save_icon)
        self.ui.Save_mask_btn.setEnabled(False)

    # Automatic edge detection related actions
    def edge_detection_sobel_action(self):
        """edge_detection_sobel_action: implements sobel edge detection method into ROI selected region"""

        if MainWindow.mapped_coordinates:
            # Call methods for sobel detection method
            img_sobel = self.process_inst.sobel_detection(MainWindow.b_w_threshold)
            # Call method to convert numpy array to pixmap
            pixmap_sobel = self.display_inst.convert_cv_qt(img_sobel)
            # Show sobel image
            self.ui.Work_Area.setPixmap(pixmap_sobel)
            # Activate edge_sobel_flg and deactivate rest implied flags
            MainWindow.edge_sobel_flg = 1
            MainWindow.edge_laplacian_flg = 0
            MainWindow.edge_canny_flg = 0
            MainWindow.edge_prewitt_flg = 0
            MainWindow.edge_robert_flg = 0
            MainWindow.bw_roi_flg = 0
            MainWindow.wb_roi_flg = 0
            # Enable Thresh_bw_slider for threshold definition
            Edge_Detection_Buttons.Thresh_bw_slider.setEnabled(True)
            # Enable edge manual painting
            self.ui.Edge_manual.setEnabled(True)
            # Enable mask creation
            self.ui.Mask_btn.setEnabled(True)

    def edge_detection_laplacian_action(self):
        """edge_detection_laplacian_action: implements laplacian edge detection method into ROI selected region"""

        if MainWindow.mapped_coordinates:
            # Call methods for sobel detection method
            img_laplacian = self.process_inst.laplacian_detection(
                MainWindow.b_w_threshold
            )
            # Call method to convert numpy array to pixmap
            pixmap_laplacian = self.display_inst.convert_cv_qt(img_laplacian)
            # Show laplacian image
            self.ui.Work_Area.setPixmap(pixmap_laplacian)
            # Activate edge_laplacian_flg and deactivate rest of implied flags
            MainWindow.edge_sobel_flg = 0
            MainWindow.edge_laplacian_flg = 1
            MainWindow.edge_canny_flg = 0
            MainWindow.edge_prewitt_flg = 0
            MainWindow.edge_robert_flg = 0
            MainWindow.bw_roi_flg = 0
            MainWindow.wb_roi_flg = 0
            # Enable Thresh_bw_slider for threshold definition
            Edge_Detection_Buttons.Thresh_bw_slider.setEnabled(True)
            # Enable edge manual painting
            self.ui.Edge_manual.setEnabled(True)
            # Enable mask creation
            self.ui.Mask_btn.setEnabled(True)

    def edge_detection_canny_action(self):
        """edge_detection_canny_action: implements canny edge detection method into ROI selected region"""

        if MainWindow.mapped_coordinates:
            # Call methods for sobel detection method
            img_canny = self.process_inst.canny_detection(MainWindow.b_w_threshold)
            # Call method to convert numpy array to pixmap
            pixmap_canny = self.display_inst.convert_cv_qt(img_canny)
            # Show Canny image
            self.ui.Work_Area.setPixmap(pixmap_canny)
            # Activate edge_canny_flg and deactivate rest of implied flags
            MainWindow.edge_sobel_flg = 0
            MainWindow.edge_laplacian_flg = 0
            MainWindow.edge_canny_flg = 1
            MainWindow.edge_prewitt_flg = 0
            MainWindow.edge_robert_flg = 0
            MainWindow.bw_roi_flg = 0
            MainWindow.wb_roi_flg = 0
            # Enable Thresh_bw_slider for threshold definition
            Edge_Detection_Buttons.Thresh_bw_slider.setEnabled(True)
            # Enable edge manual painting
            self.ui.Edge_manual.setEnabled(True)
            # Enable mask creation
            self.ui.Mask_btn.setEnabled(True)

    def edge_detection_prewitt_action(self):
        """edge_detection_prewitt_action: implements prewitt edge detection method into ROI selected region"""

        if MainWindow.mapped_coordinates:
            # Call methods for sobel detection method
            img_prewitt = self.process_inst.prewitt_detection(MainWindow.b_w_threshold)
            # Call method to convert numpy array to pixmap
            pixmap_prewitt = self.display_inst.convert_cv_qt(img_prewitt)
            # Show Prewitt image
            self.ui.Work_Area.setPixmap(pixmap_prewitt)
            # Activate edge_prewitt_flg and deactivate rest of implied flags
            MainWindow.edge_sobel_flg = 0
            MainWindow.edge_laplacian_flg = 0
            MainWindow.edge_canny_flg = 0
            MainWindow.edge_prewitt_flg = 1
            MainWindow.edge_robert_flg = 0
            MainWindow.bw_roi_flg = 0
            MainWindow.wb_roi_flg = 0
            # Enable Thresh_bw_slider for threshold definition
            Edge_Detection_Buttons.Thresh_bw_slider.setEnabled(True)
            # Enable edge manual painting
            self.ui.Edge_manual.setEnabled(True)
            # Enable mask creation
            self.ui.Mask_btn.setEnabled(True)

    def edge_detection_robert_action(self):
        """edge_detection_robert_action: implements prewitt edge detection method into ROI selected region"""

        if MainWindow.mapped_coordinates:
            # Call methods for sobel detection method
            img_robert = self.process_inst.robert_detection(MainWindow.b_w_threshold)
            # Call method to convert numpy array to pixmap
            pixmap_robert = self.display_inst.convert_cv_qt(img_robert)
            # Show Robert image
            self.ui.Work_Area.setPixmap(pixmap_robert)
            # Activate edge_robert_flg and deactivate rest of implied flags
            MainWindow.edge_sobel_flg = 0
            MainWindow.edge_laplacian_flg = 0
            MainWindow.edge_canny_flg = 0
            MainWindow.edge_prewitt_flg = 0
            MainWindow.edge_robert_flg = 1
            MainWindow.bw_roi_flg = 0
            MainWindow.wb_roi_flg = 0
            # Enable Thresh_bw_slider for threshold definition
            Edge_Detection_Buttons.Thresh_bw_slider.setEnabled(True)
            # Enable edge manual painting
            self.ui.Edge_manual.setEnabled(True)
            # Enable mask creation
            self.ui.Mask_btn.setEnabled(True)

    def edge_bw_threshold_action(self, value):
        """edge_bw_threshold_action: method called on black and white threshold slider value changed"""

        # Call actual edge detection method
        if MainWindow.edge_sobel_flg == 1:
            MainWindow.b_w_threshold = value
            self.edge_detection_sobel_action()
        elif MainWindow.edge_laplacian_flg == 1:
            MainWindow.b_w_threshold = value
            self.edge_detection_laplacian_action()
        elif MainWindow.edge_canny_flg == 1:
            MainWindow.b_w_threshold = value
            self.edge_detection_canny_action()
        elif MainWindow.edge_prewitt_flg == 1:
            MainWindow.b_w_threshold = value
            self.edge_detection_prewitt_action()
        elif MainWindow.edge_robert_flg == 1:
            MainWindow.b_w_threshold = value
            self.edge_detection_robert_action()

    # Manual edge detection related actions
    def manual_detection_pen_b_action(self):
        """manual_detection_pen_b_action: activates pen tool for manual detection actions, color black"""

        # activate_pen_flg activates/deactivates the pen tool
        QLabelplusplus.activate_painting(self, "#000000")

    def manual_detection_pen_w_action(self):
        """manual_detection_pen_w_action: activates pen tool for manual detection actions, color white"""

        # activate_pen_flg activates/deactivates the pen tool
        QLabelplusplus.activate_painting(self, "#ffffff")

    def manual_detection_width_up_action(self):
        """manual_detection_eraser_w_action: activates eraser tool for manual detection actions, color white"""

        QLabelplusplus.paint_width(self, 1)

    def manual_detection_width_down_action(self):
        """manual_detection_eraser_b_action: activates eraser tool for manual detection actions, color black"""

        QLabelplusplus.paint_width(self, 0)

    def manual_detection_undo_paint_action(self):
        """manual_detection_eraser_b_action: activates eraser tool for manual detection actions, color black"""
        if len(QLabelplusplus.segment_line_list) > 0:
            QLabelplusplus.undo_paint(self)


# Main Program
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
