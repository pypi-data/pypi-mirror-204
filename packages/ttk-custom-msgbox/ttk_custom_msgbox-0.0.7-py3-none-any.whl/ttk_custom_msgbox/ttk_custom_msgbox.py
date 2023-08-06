from functools import partial
from tkinter import ttk
from ttkthemes import themed_tk
from tkinter import *

# Constants
INFO_MSGBOX = "INFO"
WARNING_MSGBOX = "WARNING"
ERROR_MSGBOX = "ERROR"
QUESTION_MSGBOX = "QUESTION"


class ThemedTkMsgBox:
    """
    ThemedTkMsgBox class creates a simple message box popup.
    The message box inherits the master window theme.

    The message box will appear in the middle of the window
    it was called from.
    """

    def __init__(self, master: themed_tk.ThemedTk, wait_response=True, _icon: str = None):
        # Create global variable for msgbox return.
        # The mainloop of the master window will wait for this variable
        # to change and only then will continue running.
        # This functionality can be turned off by
        # assigning wait_response = False on class initialization.
        self.icon = _icon
        self.msg_var = IntVar()
        self.wait = wait_response

        # Objects to be later used in msgbox
        self.msgbox = None

        # Get information for proper msgbox placement
        self.master = master
        self.master_x = master.winfo_x()
        self.master_y = master.winfo_y()
        self.master_width = master.winfo_width()
        self.master_height = master.winfo_height()

        # Dictionary for message types
        self.msg_meta = {INFO_MSGBOX: {"symbol": "i", "color": None},
                         WARNING_MSGBOX: {"symbol": "!", "color": 'yellow'},
                         ERROR_MSGBOX: {"symbol": "X", "color": 'red'},
                         QUESTION_MSGBOX: {"symbol": "?", "color": None}}

    def __button_funct(self, return_val: int):
        """
        Private method.
        Sets the return value of each button in the msgbox.
        """
        self.msg_var.set(return_val)
        self.msgbox.destroy()
        return None

    def __on_exit(self):
        """
        Private method.
        Manages msgbox behaviour and return value if 'X' button is pressed.
        """
        self.msg_var.set(-1)
        self.msgbox.destroy()
        return None

    def __msgbox_template(self,
                          msgbox_title: str,
                          msg_input: str,
                          buttons: list[str] = None,
                          msg_type: str = None):
        """
        Manages the main functionality of the msgbox.
        The number of buttons can be set by user.
        The text of each button is inputted as a list of strings.
        If the button

        Example:
            buttons = ['OK', 'CANCEL', 'RESET']
        """

        if buttons is None:
            buttons = ['OK']

        # Error handling
        for _temp_item in buttons:
            assert type(_temp_item) == str, \
                f"All items in buttons have to be strings.\n" \
                f"Faulty item: '{_temp_item}', of type: '{type(_temp_item)}'"

        assert msg_input != "", f"'msg_input' cannot be empty"

        # Constants
        _pad_y = 10
        _pad_x = 5
        _msgbox_min_width = 200
        _msgbox_min_height = 90

        # Create the msgbox window
        self.msgbox = Toplevel()
        # Set msgbox title
        self.msgbox.title(msgbox_title)
        # Set icon in case user set custom icon
        if self.icon is not None:
            self.msgbox.iconbitmap(self.icon)
        # Disable option to resize the msgbox
        self.msgbox.resizable(False, False)
        # Make msgbox show up over all other windows
        self.msgbox.attributes('-topmost', True)
        # Set msgbox minimum width and height
        self.msgbox.minsize(_msgbox_min_width, _msgbox_min_height)

        # create main frame of the msgbox window
        _main_frame = ttk.Frame(master=self.msgbox)
        _main_frame.pack(fill="both", expand=True)

        # Create frame for label to properly pack symbols for message types
        _msg_frame = ttk.Frame(master=_main_frame)

        # Check if message type was inputted
        _msg_color = None
        if msg_type is not None:
            if msg_type not in self.msg_meta.keys():
                raise KeyError(f"Invalid message type. "
                               f"Available options: '{self.msg_meta.keys()}'")

            # retrieve preset color for message type
            _msg_color = self.msg_meta[msg_type]["color"]

            # Create msg_sub_frame for symbols
            msg_sub_frame = ttk.Frame(master=_msg_frame)

            _encircle = "◯"
            _encircle_size = 30
            _symbol_text = self.msg_meta[msg_type]["symbol"]
            if msg_type == WARNING_MSGBOX:
                _encircle = "⚠"
                _symbol_text = ""
            circle_symbol = ttk.Label(master=msg_sub_frame,
                                      text=_encircle,
                                      anchor=W,
                                      justify=CENTER,
                                      font=("Arial", _encircle_size),
                                      foreground=_msg_color)

            _symbol = ttk.Label(master=msg_sub_frame,
                                text=_symbol_text,
                                anchor=W,
                                justify=CENTER,
                                font=("Arial Bold", 15),
                                foreground=_msg_color)

            circle_symbol.grid(column=0, row=0)
            if _symbol_text:
                _symbol.grid(column=0, row=0)

            msg_sub_frame.pack(anchor=W, side=LEFT, pady=5)

        # Create label that shows text in msgbox
        _msg_label = ttk.Label(_msg_frame,
                               text=msg_input,
                               anchor=E,
                               justify=CENTER,
                               foreground=_msg_color)

        # Pack the label into the msgbox
        _msg_label.pack(anchor=E, side=RIGHT, padx=_pad_x)

        # Pack label frame
        _msg_frame.pack(anchor=CENTER, pady=_pad_y, padx=_pad_x)

        # Create frame to pack buttons into
        _btn_frame = ttk.Frame(_main_frame)
        # Create buttons and pack them into frame
        for temp_nr in range(len(buttons)):
            _temp_button = ttk.Button(_btn_frame,
                                      text=buttons[temp_nr],
                                      takefocus=False,
                                      command=partial(self.__button_funct, temp_nr))
            _temp_button.pack(anchor=W, padx=_pad_x, side=LEFT)
        # Pack the button frame into the msgbox
        _btn_frame.pack(anchor=CENTER, pady=_pad_y, padx=_pad_x)

        # Update msgbox to correctly return dimensions of widgets
        self.msgbox.update()
        # Retrieve label frame dimensions in pixels for proper msgbox size
        _msg_width = _msg_frame.winfo_width()
        _msg_height = _msg_frame.winfo_height()
        # Retrieve button frame dimensions in pixels for proper msgbox size
        _btn_frame_width = _btn_frame.winfo_width()
        _btn_frame_height = _btn_frame.winfo_height()

        # Calculate msgbox width and height
        if _msg_width > _btn_frame_width:
            _msgbox_width = _msg_width + (_pad_x * 2)
        else:
            _msgbox_width = _btn_frame_width + (_pad_x * 2)

        _msgbox_height = _msg_height + _btn_frame_height + (_pad_y * 4)

        # Properly size and place msgbox
        self.master.update()
        self.msgbox.geometry \
            (f"{_msgbox_width}x"
             f"{_msgbox_height}+"
             f"{int(self.master_x + (self.master_width / 2) - (_msgbox_width / 2))}+"
             f"{int(self.master_y + (self.master_height / 2) - (_msgbox_height / 2))}")

        # Bind the click on 'X' button to the __on_exit() method
        self.msgbox.protocol('WM_DELETE_WINDOW', self.__on_exit)

        # Ask master window to wait till a button has been pushed and the
        # global variable has been changed
        self.master.wait_variable(self.msg_var)

        return self.msg_var.get() if self.msg_var.get() != -1 else None

    def info(self,
             msgbox_title: str = INFO_MSGBOX,
             msg_input: str = None,
             buttons=None):
        """
        Predefined INFO messagebox.\n
        Has one default button: 'OK'.\n
        The number of buttons can be customized.\n
        The text of each button is inputted as a list of strings.

        Example: buttons = ['OK', 'CANCEL', 'EXIT']

        :return: value for 'OK' button = 0 |
                 value for 'X' button = None
        """

        _info_msgbox = self.__msgbox_template(msgbox_title=msgbox_title,
                                              msg_input=msg_input,
                                              buttons=buttons,
                                              msg_type=INFO_MSGBOX)

        return _info_msgbox

    def warning(self,
                msgbox_title: str = WARNING_MSGBOX,
                msg_input: str = None,
                buttons=None):
        """
        Predefined WARNING messagebox.\n
        Has two default button: 'OK', 'CANCEL'.\n
        The number of buttons can be customized.\n
        The text of each button is inputted as a list of strings.

        Example: buttons = ['OK', 'CANCEL', 'EXIT']

        :return: value for 'OK' button = 0 |
                 value for 'CANCEL' button = 1 |
                 value for 'X' button = None
        """

        if buttons is None:
            buttons = ["OK", "CANCEL"]

        _warning_msgbox = self.__msgbox_template(msgbox_title=msgbox_title,
                                                 msg_input=msg_input,
                                                 buttons=buttons,
                                                 msg_type=WARNING_MSGBOX)

        return _warning_msgbox

    def question(self,
                 msgbox_title: str = QUESTION_MSGBOX,
                 msg_input: str = None,
                 buttons=None):
        """
        Predefined QUESTION messagebox.\n
        Has three default button: 'YES', 'NO, 'CANCEL'.\n
        The number of buttons can be customized.\n
        The text of each button is inputted as a list of strings.

        Example: buttons = ['Continue', 'Cancel', 'EXIT']

        :return: value for 'YES' button = 0 |
                 value for 'NO' button = 1 |
                 value for 'CANCEL' button = 2 |
                 value for 'X' button = None
        """

        if buttons is None:
            buttons = ["YES", "NO", "CANCEL"]

        _question_msgbox = self.__msgbox_template(msgbox_title=msgbox_title,
                                                  msg_input=msg_input,
                                                  buttons=buttons,
                                                  msg_type=QUESTION_MSGBOX)

        return _question_msgbox

    def error(self,
              msgbox_title: str = ERROR_MSGBOX,
              msg_input: str = None,
              buttons=None):
        """
        Predefined ERROR messagebox.\n
        Has one default button: 'OK'.\n
        The number of buttons can be customized.\n
        The text of each button is inputted as a list of strings.

        Example: buttons = ['OK', 'CANCEL', 'EXIT']

        :return: value for 'OK' button = 0 |
                 value for 'X' button = None
        """

        _error_msgbox = self.__msgbox_template(msgbox_title=msgbox_title,
                                               msg_input=msg_input,
                                               buttons=buttons,
                                               msg_type=ERROR_MSGBOX)

        return _error_msgbox

    def custom(self,
               msgbox_title: str = 'Your title here',
               msg_input: str = 'Your message here',
               buttons: list[str] = None):
        """
        Custom messagebox without info, error or warning symbols.
        The number of buttons can be set by user.
        If no custom buttons are inputted, the default button is 'OK'.
        The text of each button is inputted as a list of strings.

        Example:
            buttons = ['OK', 'CANCEL', 'RESET']
        """

        _custom_msgbox = self.__msgbox_template(msgbox_title=msgbox_title,
                                                msg_input=msg_input,
                                                buttons=buttons,
                                                msg_type=None)

        return _custom_msgbox
