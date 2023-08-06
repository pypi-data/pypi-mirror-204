# MIT License

# Copyright (c) 2023 Postek Electronics Co., Ltd

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# For the functions that only have pass in this file, please refer to the ox script development manual for details
# The functions are marked with pass only because they are meanted to be executed on the printer and will not function
# correctly on your device. Please use the runtime environment on Postek printers for most accurate results


# --coding: utf-8 --
import string

def debuglog(info: str):
    """
    Log the information to the debug log file stored inside the printer

    Parameters:
        info (str): The information to be logged
    """
    pass


MM = 0
DOTS = 1


def PTK_SetUnit(unit=MM):
    """
    PTK_SetUnit is used to set the unit of measurement for the printer. The default unit is mm.

    Parameters:
        unit (int): The unit of measurement to be used. 0 -> mm, 1 -> dots
    """
    pass


def PTK_GetErrorInfo():
    """
    PTK_GetErrorInfo is used to get the error information from the printer

    """
    pass


# ===========================================================#
# Functions related to ports of the printer
# ===========================================================#

PORT_SERIAL = 0
PORT_USBDEVICE = 1
PORT_ETHERNET = 2
PORT_BLUETOOTH = 3
PORT_WIFI = 4
PORT_PARALLEL = 5
PORT_WEBSOCK = 6
PORT_USBHOST = 7
PORT_SCRIPT = 8


def PTK_GetPortData(port, dataLen=1024, timeout=5000) -> bytes:
    """
    PTK_GetPortData is used to get the data from the printer

    Parameters:
        port: The port to get the data from
            PORT_SERIAL: Serial port
            PORT_USBDEVICE: USB Device port
            PORT_ETHERNET: Ethernet port
            PORT_BLUETOOTH: Bluetooth port
            PORT_WIFI: Wifi port
            PORT_PARALLEL: Parallel port
            PORT_WEBSOCK: Websocket port
            PORT_USBHOST: USB Host port
            PORT_SCRIPT: Script port
        dataLen (int): The length of the data to be read
        timeout (int): The timeout for the operation

    Returns:
        bytes: The data read from the printer
    """
    pass


def PTK_SendCmdToPrinter(cmd: str) -> bool:
    """
    PTK_SendCmdToPrinter is used to send commands loadded from Forms to the printer

    Parameters:
        cmd (str): The command to be sent to the printer

    Returns:
        bool: The command was sent successfully
        String: The error message if the command was not sent successfully
    """
    return True

# ===========================================================#
# Functions related to the printer settings
# ===========================================================#


BOTTOM_RIGHT = "T"
TOP_LEFT = "B"


def PTK_SetPrintDirection(direction: string) -> bool:
    """
    PTK_SetPrintDirection is used to set the print direction of the printer. The default direction starts at bottom right.

    Parameters:
        direction (string): The direction to be used. "T" -> Top Left, "B" -> Bottom Right

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_CutPage(number_of_labels=1, save_in_flash=False) -> bool:
    """
    PTK_CutPage is used to cut the page after printing the number of labels specified

    Parameters:
        number_of_labels (int): The number of labels to be printed before cutting the page
        save_in_flash (bool): Save the command in flash so that the value can be restored when the printer powers up again

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_Reset() -> bool:
    """
    PTK_Reset is used to reset the printer

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


# ===========================================================#
# Functions for print job related settings
# ===========================================================#

def PTK_SetDarkness(darkness: int) -> bool:
    """
    PTK_SetDarkness is used to set the darkness of the print. The default darkness is 8.

    Parameters:
        darkness (int): The darkness to be used. The range is 0 to 20.

    Returns:
        int: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_SetLabelHeight(height: int, gapH=1) -> bool:
    """
    PTK_SetLabelHeight is used to set the height of the label.

    Parameters:
        height (int): The height of the label in mm
        gapH (int): The gap between the labels in mm

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_SetLabelWidth(width: int) -> bool:
    """
    PTK_SetLabelWidth is used to set the width of the label.

    Parameters:
        width (int): The width of the label in mm

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_SetCoordinateOrigin(x=0, y=0) -> bool:
    """
    PTK_SetCoordinateOrigin is used to set the origin of the coordinates. The default origin is (0,0).

    Parameters:
        x (int): The x coordinate of the origin
        y (int): The y coordinate of the origin

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_SetPrintSpeed(speed) -> bool:
    """
    PTK_SetPrintSpeed is used to set the print speed of the printer. The default speed depends on the model of the printer.

    Parameters:
        speed (float): The speed to be used in inches per second. The range depends upon the model of the printer.

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


# ===========================================================#
# Text related functions
# ===========================================================#

NORMAL = "N"
REVERSE = "R"
SDRAM = 0
FLASH = 1


def PTK_CreatFont(location, fontname, downloadfontname) -> bool:
    """
    PTK_CreatFont is used to create a font in the printer

    Parameters:
        location (int): The location to store the font. 0 -> SDRAM, 1 -> Flash
        fontname (str): The name of the font to be created, the name should be in a single capital letters between A to Z
        downloadfontname (str): The name of the font to be downloaded

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_DrawText(
    x_coordinate: int,
    y_coordinate: int,
    fonts: string,
    font_size: int,
    data: string,
    text_style="N",
    rotation=0,
    horizontal_multiplier=-1,
) -> bool:
    """
    PTK_DrawText is used to print text on the label

    Parameters:
        x_coordinate (int): The x coordinate of the text
        y_coordinate (int): The y coordinate of the text
        fonts (string): The font to be used. i.e "Inter", the Font should be stored in the fonts folder on the printer
        font_size (int): The size of the font
        data (string): The text to be printed
        text_style (string): The style of the text. "N" -> Normal, "R" -> Reverse
        rotation (int): The rotation of the text. The range is 0 to 360
        horizontal_multiplier (int): The horizontal multiplier of the text. The range is 1 to 10

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True

# ===========================================================#
# 2D Barcode related functions
# ===========================================================#


def PTK_DrawBar2D_DATAMATRIX(
    x_coordinate: int, y_coordinate: int, multiplier: int, data: string, rotation=0
) -> bool:
    """
    PTK_DrawBar2D_DATAMATRIX is used to print a DataMatrix barcode on the label

    Parameters:
        x_coordinate (int): The x coordinate of the barcode
        y_coordinate (int): The y coordinate of the barcode
        multiplier (int): The multiplier of the barcode. The range is 1 to 9
        data (string): The data to be printed in the barcode
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_DrawBar2D_QR(
    x_coordinate: int,
    y_coordinate: int,
    qr_version=0,
    rotation=0,
    multiplier=1,
    encode_mode=0,
    correction_level=0,
    masking=8,
    data='string',
) -> bool:
    """
    PTK_DrawBar2D_QR is used to print a QR barcode on the label

    Parameters:
        x_coordinate (int): The x coordinate of the barcode
        y_coordinate (int): The y coordinate of the barcode
        qr_version (int): The version of the QR code. The range is 0 to 40
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree
        multiplier (int): The multiplier of the barcode. The range is 1 to 99
        encode_mode (int): The encoding mode of the barcode. The range is 0 to 4 where
            0 = Numeric, 1 = Alphanumeric, 2 = Byte, 3 = chinese, 4 = auto
        correction_level (int): The correction level of the barcode. The range is 0 to 3
        masking (int): The masking of the barcode. The range is 0 to 8
        data (string): The data to be printed in the barcode

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


UPS = 1
NOT_UPS = 0


def PTK_DrawBar2D_MaxiCode(
    x_coordinate: int, y_coordinate: int, mode: int, is_ups_data: int, data: string
) -> bool:
    """
    PTK_DrawBar2D_MaxiCode is used to print a MaxiCode barcode on the label

    Parameters:
        x_coordinate (int): The x coordinate of the barcode
        y_coordinate (int): The y coordinate of the barcode
        mode (int): The mode of the barcode. The range is 2 to 4
        is_ups_data (int): The ups data of the barcode. 0 -> Not UPS, 1 -> UPS
        data (string): The data to be printed in the barcode

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_DrawBar2D_Pdf417(
    x_coordinate: int,
    y_coordinate: int,
    correction_level: int,
    data_compression_level: int,
    px: int,
    py: int,
    maxrow: int,
    maxcolumn: int,
    t: int,
    data: string,
    rotation=0,
) -> bool:
    """
    PTK_DrawBar2D_Pdf417 is used to print a Pdf417 barcode on the label

    Parameters:
        x_coordinate (int): The x coordinate of the barcode
        y_coordinate (int): The y coordinate of the barcode
        correction_level (int): The correction level of the barcode. The range is 0 to 8
        data_compression_level (int): The data compression level of the barcode. The range is 0 to 1
        px (int): The px of the barcode. The range is 2 to 9
        py (int): The py of the barcode. The range is 4 to 99
        maxrow (int): The maxrow of the barcode. The range is 3 to 90
        maxcolumn (int): The maxcolumn of the barcode. The range is 1 to 30
        t (int): Truncation of the barcode. i.e 0 -> No truncation, 1 -> Truncation
        data (string): The data to be printed in the barcode
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_DrawBar2D_HANXIN(
    x_coordinate: int,
    y_coordinate: int,
    multiplier: int,
    data: string,
    encoding=0,
    correction_level=0,
    masking=0,
    rotation=0,
) -> bool:
    """
    PTK_DrawBar2D_HANXIN is used to print a Han Xin barcode on the label

    Parameters:
        x_coordinate (int): The x coordinate of the barcode
        y_coordinate (int): The y coordinate of the barcode
        multiplier (int): The multiplier of the barcode. The range is 1 to 30
        data (string): The data to be printed in the barcode
        encoding (int): The encoding of the barcode. The range is 0 to 6 where
            0 = Auto, 1 = Text, 2 = Binary, 3 = Numeric, 4 = Alphanumeric, 5 = GB 18030 binary, 6 = GB 18030 numeric
        correction_level (int): The correction level of the barcode. The range is 0 to 3
        masking (int): The masking of the barcode. The range is 0 to 3
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


# ===========================================================#
# 1D Barcodes
# ===========================================================#

NO_TEXT = "N"
TEXT = "B"


def PTK_DrawBarcode(
    x_coordinate: int,
    y_coordinate: int,
    barcode_type: string,
    narrow_unit_width: int,
    wide_unit_width: int,
    data: string,
    human_readable=TEXT,
    bar_height=10,
    rotation=0,
) -> bool:
    """
    PTK_DrawBarcode is used to print a 1D barcode on the label

    Parameters:
        x_coordinate (int): The x coordinate of the barcode
        y_coordinate (int): The y coordinate of the barcode
        barcode_type (string): The type of the barcode.
            0 = Code 128 UCC(shipping container code)
            1 = Code 128 auto
            1A = Code 128 subset A
            1B = Code 128 subset B
            1C = Code 128 subset C
            1E = UCC/EAN128
            2 = Interleaved 2 of 5 (wide_unit_width adjustable)
            2C = Interleaved 2 of 5 check sum digit (wide_unit_width adjustable)
            2D = Interleaved 2 of 5 with human readable check digit (wide_unit_width adjustable)
            2M = Matrix 2 of 5 (wide_unit_width adjustable)
            3 = Code 3 of 9 (wide_unit_width adjustable)
            3C = Code 3 of 9 check sum digit (wide_unit_width adjustable)
            3E = Extended Code 3 of 9 (wide_unit_width adjustable)
            3F = Extended Code 3 of 9 check sum digit (wide_unit_width adjustable)
            9 = Code 93
            E30 = EAN 13
            E32 = EAN 13 2 digit add on
            E35 = EAN 13 5 digit add on
            E80 = EAN 8
            E82 = EAN 8 2 digit add on
            E85 = EAN 8 5 digit add on
            K = Codabar (wide_unit_width adjustable)
            P = Postnet
            UA0 = UPC-A
            UA2 = UPC-A 2 digit add on
            UA5 = UPC-A 5 digit add on
            UE0 = UPC-E
            UE2 = UPC-E 2 digit add on
            UE5 = UPC-E 5 digit add on


            The range is 0 to 8 where
            0 = UPC-A, 1 = UPC-E, 2 = EAN13, 3 = EAN8, 4 = CODE39, 5 = ITF, 6 = CODABAR, 7 = CODE93, 8 = CODE128

        narrow_unit_width (int): The bar width of the narrow unit width of the barcode in mm
        wide_unit_width (int): The bar width of the narrow unit width of the barcode in mm. Not applicable for all barcode types
        data (string): The data to be printed in the barcode
        human_readable (string): The human readable of the barcode. The range is "N" or "B" where
            "N" = No text, "B" = Text
        bar_height (int): The bar height of the barcode. The range is 1 to 9999
        rotation (int): The rotation of the barcode. The range is 0 to 3 where
            0 = 0 degree, 1 = 90 degree, 2 = 180 degree, 3 = 270 degree

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


# ===========================================================#
# Printing graphics
# ===========================================================#

def PTK_DrawGraphics(x, y, graphic_name):
    """
    PTK_DrawGraphics is used to print a graphic on the label

    Parameters:
        x (int): The x coordinate of the graphic
        y (int): The y coordinate of the graphic
        graphic_name (string): The name of the graphic that is stored in the printer

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True

# ===========================================================#
# Printing lines
# ===========================================================#


def PTK_DrawDiagonal(
    x_coordinate: int,
    y_coordinate: int,
    thickness: int,
    end_point_x: int,
    end_point_y: int,
) -> bool:
    """
     PTK_DrawDiagonal is used to draw lines on the label

     Parameters:
        x_coordinate (int): The x coordinate of the line
        y_coordinate (int): The y coordinate of the line
        thickness (int): The thickness of the line in mm
        end_point_x (int): The x coordinate of the end point of the line
        end_point_y (int): The y coordinate of the end point of the line

     Returns:
         bool: The function executed successfully
         String: The error message in string if an error occured
     """
    return True


def PTK_DrawRectangle(
    x_coordinate: int,
    y_coordinate: int,
    thickness: int,
    end_point_x: int,
    end_point_y: int,
) -> bool:
    """
    PTK_DrawRectangle is used to draw a rectangle on the label

    Parameters:
        x_coordinate (int): The x coordinate of the rectangle
        y_coordinate (int): The y coordinate of the rectangle
        thickness (int): The thickness of the rectangle in mm
        end_point_x (int): The x coordinate of the end point of the rectangle
        end_point_y (int): The y coordinate of the end point of the rectangle

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True

# ===========================================================#
# Printjob settings
# ===========================================================#


def PTK_PrintLabel(number_of_label=1, number_of_copy=1) -> bool:
    """
    PTK_PrintLabel is used to print the label

    Parameters:
        number_of_label (int): The number of label to be printed.
        number_of_copy (int): The number of copies to be printed.

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_PrintConfigunation() -> bool:
    """
    PTK_PrintConfigunation is used to print the current configuration of the printer onto the label.
    Usually only used for debugging purposes

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True


def PTK_FeedMedia() -> bool:
    """
    PTK_FeedMedia is used to feed one label

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True

def PTK_MediaCalibration() -> bool:
    """
    PTK_MediaCalibration is used to calibrate the media. If the calibration is successful the
    media size information will be stored and used for the next printjob unless specificed through
    PTK_SetLabelHeight or specificed through print job configuration

    Returns:
        bool: The function executed successfully
        String: The error message in string if an error occured
    """
    return True

# ===========================================================#
# Functions to display information on the printer screen
# ===========================================================#

# Parent class of all UI elements
# This shouldn't be used directly
class UIWidgets:
    def __init__(self, name, value, Onpressed):
        pass

# Button class used for creating a button on the printer screen
# To create UI Elements use UIInit and UIPage
class UIButton(UIWidgets):
    def __init__(self, Onpressed, name="测试按钮", visible=True):
        pass


# Text class used for just displaying text on the printer screen
# To create UI Elements use UIInit and UIPage
class UIText(UIWidgets):
    def __init__(self, value="--", name="测试文本", visible=True):
        pass

# List class that can be used to create a drop down list on the printer screen
# To create UI Elements use UIInit and UIPage
class UIList(UIWidgets):
    def __init__(
        self,
        Onpressed,
        items,
        name="testing list",
        value="0",
        valueType="int",
        valueMax="1",
        valueMin="0",
        visible=True,
    ):
        pass

# Input class that can be used to create a input box on the printer screen
# To create UI Elements use UIInit and UIPage
class UIInput(UIWidgets):
    def __init__(
        self,
        Onpressed,
        name="测试输入",
        value="0",
        valueType="double",
        valueMax="10.0",
        valueMin="-10.0",
        dotNum=1,
        visible=True,
    ):
        pass

# Checkbox class that can be used to create a checkbox on the printer screen
# To create UI Elements use UIInit and UIPage
class UICheckbox(UIWidgets):
    def __init__(
        self,
        Onpressed,
        name="测试复选框",
        value="0",
        valueType="bool",
        valueMax="1",
        valueMin="0",
        visible=True,
    ):
        pass


def UIchangePage(pagenum):
    """
    UIchangePage can be used to change the page on the printer screen as
        a ox script can be used to create multiple pages

    Parameters:
        pagenum (int): The page number to be displayed
    """
    pass

def UIPage(*args) -> dict:
    """
    UIPage is used to create a page on the printer screen. A page is used to
        group UI elements together. UI elements have to be added to a page to be displayed
        on the printer screen. UI elements needs to be added in the following way

    controller = UIInit(
        UIPage(
            UIText(name="Barcode One:", value="--"),
            UIText(name="Barcode Two:", value="--"),
        ),
    )

    Parameters:
        *args (UIWidgets): The UI elements to be added to the page

    Returns:
        dict: The page in dictionary format, it is meanted to be used with UIInit and not
            used directly by the user

    """
    return {}

# UI初始化
def UIInit(*params, require_execute_confirmation=True) -> dict:
    """
    UIInit is used to initialize the UI elements on the printer screen. 

    Parameters:
        *params (dict): The pages to be displayed on the printer screen, it should be used in the
            way shown below. The user can create multiple pages and add UI elements to each page
        require_execute_confirmation (bool, optional): If the printer screen should require
            confirmation before executing the script. Defaults to True.

    controller = UIInit(
        UIPage(
            UIText(name="Barcode One:", value="--"),
            UIText(name="Barcode Two:", value="--"),
        ),
        UIPage(
            UIText(name="Barcode Three:", value="--"),
            UIText(name="Barcode Four:", value="--"),
        ),
    )
            
    Returns:
        controller (dict): The controller for the UI elements. The user can use the controllers
            to change the values of the UI elements on the printer screen

    """
    return {}