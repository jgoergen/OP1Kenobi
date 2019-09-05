class Config:

    DisplayWidth = 128
    DisplayHeight = 128

    FontFile = './Media/fonts/OpenSans-Bold.ttf'
    LargeFontSize = 16
    SmallFontSize = 10

    Key1Pin = 16
    Key2Pin = 20
    Key3Pin = 21
    KeyPressPin = 13
    KeyUpPin = 19
    KeyDownPin = 6
    KeyLeftPin = 26 
    KeyRightPin = 5

    OP1USBVendor = 0x2367
    OP1USBProduct = 0x0002

    OP1USBMountDir = '/media/op1'
    OP1USBId = '*Teenage_OP-1*'
    MediaDirectory = './Media'
    BackupDirectory = 'backups'
    BackupContext = 'default'

    PrimaryTextColor = (255, 255, 255)
    ErrorTextColor = (255, 0, 0)

    DisplayUpdateSpeed = 1000 / 30
    InputUpdateSpeed = 1000 / 30

    SoundVolume = 0.40
    MaxFilenameLength = 9
    ValidFilenameCharacters = [
        "-", "_", "+", "(", ")", "$",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", 
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
