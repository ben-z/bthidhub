# Copyright (c) 2020 ruundii. All rights reserved.


from hid_message_filter import HIDMessageFilter

MODIFIER_MASK_A1314_FN = 0x10
MODIFIER_MASK_A1314_EJECT = 0x08
MODIFIER_MASK_LEFT_CONTROL = 0x01
MODIFIER_MASK_LEFT_SHIFT = 0x02
MODIFIER_MASK_LEFT_ALT = 0x04
MODIFIER_MASK_LEFT_GUI_OR_CMD = 0x08
MODIFIER_MASK_A1314_RIGHT_CMD = 0x80
MODIFIER_MASK_RIGHT_ALT = 0x40
MODIFIER_MASK_RIGHT_SHIFT = 0x20

KEY_APPLICATION = 0x65

KEY_DELETE_FORWARD = 0x4c
KEY_LEFT_ARROW = 0x50
KEY_RIGHT_ARROW = 0x4f
KEY_DOWN_ARROW = 0x51
KEY_UP_ARROW = 0x52
KEY_HOME = 0x4a
KEY_END = 0x4d
KEY_PGUP = 0x4b
KEY_PGDN = 0x4e
KEY_PRINT_SCREEN = 0x46

FN_SUBSTITUTES = {
    KEY_LEFT_ARROW:KEY_HOME,
    KEY_RIGHT_ARROW: KEY_END,
    KEY_DOWN_ARROW: KEY_PGDN,
    KEY_UP_ARROW: KEY_PGUP,
}

class KeyboardWinToMacMessageFilter(HIDMessageFilter):
    #LeftControl: 0 | LeftShift: 0 | LeftAlt: 0 | Left GUI: 0 | RightControl: 0 | RightShift: 0 | RightAlt: 0 | Right GUI: 0 | # |Keyboard ['00', '00', '00', '00', '00', '00']


    def __init__(self):
        self.last_regular_report = bytearray(b'\x01\x00\x00\x00\x00\x00\x00\x00\x00')

    def filter_message_to_host(self, msg):
        #print(f"msglen: {len(msg)} msg {msg}")

        result_report = bytearray(msg)
        modifiers = result_report[0]
        
        if(modifiers & MODIFIER_MASK_LEFT_ALT): # left alt is pressed
            result_report[0] = result_report[0] & ~MODIFIER_MASK_LEFT_ALT | MODIFIER_MASK_LEFT_GUI_OR_CMD

        if(modifiers & MODIFIER_MASK_LEFT_GUI_OR_CMD): # left cmd is pressed
            result_report[0] = result_report[0] & ~MODIFIER_MASK_LEFT_GUI_OR_CMD | MODIFIER_MASK_LEFT_ALT

        final_msg = bytes(result_report)

        #print(f"msglen: {len(msg)} msg {msg} (final)")

        return super().filter_message_to_host(final_msg)

    def filter_message_from_host(self, msg):
        return msg[1:]

