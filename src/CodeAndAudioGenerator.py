import os

class CodeAndAudioGenerator():
    def __init__(self, fN, notesS):
        self.fileName = fN
        self.lilyFileName = self.fileName + ".lily"
        self.notesString = notesS

    def executeFileCreation(self):
        self.writeLilyPondFile()
        self.generatePDFandMidiFiles()
        self.generateWAVFile()
        self.generateMP3File()

    def writeLilyPondFile(self):
        file_object = open(self.lilyFileName, 'w')
        file_object.write("\\version \"2.20.0\" \n")
        file_object.write("\\score {\n")
        file_object.write("   \\absolute { \n")
        file_object.write("        \\tempo 4 = 120 \n")

        s = "         " + self.notesString + " \n"
        file_object.write(s)

        file_object.write("   } \n")
        file_object.write("   \\layout { } \n")
        file_object.write("   \\midi { } \n")
        file_object.write("}")
        file_object.close()

    def generatePDFandMidiFiles(self):
        print("----- GENERATING PDF AND MIDI FILES -----")
        lilyPondInstruction = "lilypond " + self.lilyFileName
        os.system(lilyPondInstruction)
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
