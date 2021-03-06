import os
import sys


class CodeAndAudioGenerator():
    def __init__(self, fN, notesS, temp, keyS, compasS):
        self.fileName = fN
        self.lilyFileName = self.fileName + ".lily"
        self.notesString = notesS
        self.tempo = str(temp)
        self.key = keyS
        self.compas = compasS

    def executeFileCreation(self):
        self.writeLilyPondFile()
        self.generatePDFandMidiFiles()
        self.generateWAVFile()
        self.generateMP3File()

    def writeLilyPondFile(self):
        keyS = ""
        compasS = ""
        if self.key != "":
            keyS = "        \\key " + self.key[0].lower() + " \\" + self.key[1:] + "\n"
        if self.compas != "":
            compasS = "        \\time " + self.compas + "\n"

        file_object = open(self.lilyFileName, 'w')
        s = "\\version \"2.20.0\" \n"
        s += "\\score {\n"
        s += "   \\absolute { \n"
        s += "        \\tempo 4 = " + self.tempo + "\n"
        s += keyS
        s += compasS
        s += "         " + self.notesString + "\n"
        s += "   } \n"
        s += "   \\layout { } \n"
        s += "   \\midi { } \n"
        s += "}"
        file_object.write(s)
        file_object.close()

    def generatePDFandMidiFiles(self):
        print("----- GENERATING PDF AND MIDI FILES -----")
        lilyPondInstruction = "lilypond " + self.lilyFileName
        ret = os.system(lilyPondInstruction)
        if ret != 0:
            print("ERROR: something went wrong compiling the lilypond file, did you write something weird?")
            sys.exit()
        print("----- SUCCESSFULLY GENERATED PDF AND MIDI FILES ----- \n")

    def generateWAVFile(self):
        print("----- GENERATING WAV FILE -----")
        wavInstruction = "timidity -Ow -o " + self.fileName + ".wav " + self.fileName + ".midi"
        os.system(wavInstruction)
        print("----- SUCCESSFULLY GENERATED WAV FILE ----- \n")

    def generateMP3File(self):
        mp3FilePath = "./" + self.fileName + ".mp3"
        if os.path.exists(mp3FilePath):
            os.remove(mp3FilePath)
        print("----- GENERATING MP3 FILE -----")
        wavInstruction = "ffmpeg -i " + self.fileName + ".wav -codec:a libmp3lame -qscale:a 2 " + self.fileName + ".mp3"
        os.system(wavInstruction)
        print("----- SUCCESSFULLY GENERATED MP3 FILE -----")
