from Config import *

class PhraseInput:
    def __init__(self):
        self.phrase = ""
        self.cursorPosition = 0

    def ChangePhraseCharacter(self, delta):
        phraseList = list(self.phrase)
        char = phraseList[self.cursorPosition]
        charIndex = Config.ValidFilenameCharacters.index(char)
        charIndex += 1
        if charIndex >= len(Config.ValidFilenameCharacters):
            charIndex = 0
        phraseList[self.cursorPosition] = Config.ValidFilenameCharacters[charIndex]
        self.phrase = "".join(phraseList)

    def ChangePhraseCursorPosition(self, delta):
        self.cursorPosition += delta

        # cursor wrapping
        if (self.cursorPosition < 0):
            self.cursorPosition = Config.MaxFilenameLength

        elif (self.cursorPosition > Config.MaxFilenameLength):
            self.cursorPosition = 0

    def GetPhrase(self):
        phraseList = list(self.phrase)
        newPhraseList = []
        
        for index, char in enumerate(phraseList):
            if (index == self.cursorPosition):
                newPhraseList.append("[")
                newPhraseList.append(phraseList[index])
                newPhraseList.append("]")
            else:
                newPhraseList.append(phraseList[index])

        return "".join(newPhraseList)