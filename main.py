from menu import mainMenu, subtitlesMenu
import subprocess, os, glob
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pydub import AudioSegment

class mp4:

    def __init__(self, baseVideo):

        self.video = baseVideo
        if os.path.isfile('myContainer.mp4'):
            self.createdContainer = "myContainer.mp4"
        

    def createContainer(self, subtitles):

        #os.system("ffmpeg -i {} -ss 00:00:00 -t 00:01:00 BBB_1m.mp4".format(self.video))
        ffmpeg_extract_subclip(self.video, 0, 60, targetname='BBB_1m.mp4')
        proc = subprocess.Popen(["ffprobe -v error -show_entries stream=index,codec_name,codec_type BBB_1m.mp4"], stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT) 
        output, err = proc.communicate()
        splitted = str(output).split("[STREAM]")
        
        cont = 0
        for s in splitted:
            print(s)
            if s.find("audio") != -1:
                print('a', cont)
                os.system("ffmpeg -i BBB_1m.mp4 -map 0:{} -c copy streams/audio_{}.mp3".format(cont, cont))
                cont += 1
            elif s.find("video") != -1:
                print('v')
                os.system("ffmpeg -i BBB_1m.mp4 -map 0:{} -c copy streams/video.mp4".format(cont, cont))
                cont += 1
            elif s.find("subtitle") != -1:
                print('s')
                os.system("ffmpeg -i BBB_1m.mp4 -map 0:{} -c copy streams/subs_{}.mp3".format(cont, cont))
                cont += 1
        

        audio = glob.glob("streams/*.mp3")[0]
        os.system("ffmpeg -i {} -ac 1 streams/mono.mp3".format(audio))
        
        s = AudioSegment.from_file(audio)
        low_sample_rate = s.set_frame_rate(24000)
        low_sample_rate.export("streams/lowBitrate.mp3", bitrate="16k", format="mp3")

        os.system("ffmpeg -i streams/video.mp4 -i streams/mono.mp3 -i streams/lowBitrate.mp3 -i {} -map 0:v -map 1:a -map 2:a -map 3:s -c:v copy -c:a mp3 -c:s mov_text myContainer.mp4".format(subtitles))

        self.createdContainer = "myContainer.mp4"

    def bradcastingStandard(self):

        proc = subprocess.Popen(["ffprobe -v error -show_entries stream=index,codec_name,codec_type {}".format(self.createdContainer)], stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT) 
        output, err = proc.communicate()
        splitted = str(output).split("[STREAM]")

        codecs = []

        for s in splitted:
            codec = {}
            if s.find("codec_name") != -1:
                s_splitted = s.split("\\")
                for s_s in s_splitted:
                    if s_s.find("codec_type") != -1:
                        s_s_splitted = s_s.split("=")
                        codec["type"] = s_s_splitted[1]
                    elif s_s.find("codec_name") != -1:
                        s_s_splitted = s_s.split("=")
                        codec["name"] = s_s_splitted[1]
            if codec != {}:
                codecs.append(codec)

        possibleStandardsAudio = []
        possibleStandardsVideo = []

        for codec in codecs:
            if codec['type'] == "audio":
                if codec['name'] == "aac":
                    possibleStandardsAudio.append("DVB")
                    possibleStandardsAudio.append("ISDB")
                    possibleStandardsAudio.append("DTMB")
                elif codec['name'] == "mp3":
                    possibleStandardsAudio.append("DVB")
                    possibleStandardsAudio.append("DTMB")
                elif codec['name'] == "dolby":
                    possibleStandardsAudio.append("DVB")
                elif codec['name'] == "ac3":
                    possibleStandardsAudio.append("ATSC")
                    possibleStandardsAudio.append("DTMB")
                elif codec['name'] == "dra" or codec['name'] == "mp2":
                    possibleStandardsAudio.append("DTMB")
                else:
                    possibleStandardsAudio.append(None)
            elif codec['type'] == "video":
                if codec['name'] == "mpeg2":
                    possibleStandardsVideo.append("DVB")
                    possibleStandardsVideo.append("ISDB")
                    possibleStandardsVideo.append("ATSC")
                    possibleStandardsVideo.append("DTMB")
                elif codec['name'] == "h264":
                    possibleStandardsVideo.append("DVB")
                    possibleStandardsVideo.append("ISDB")
                    possibleStandardsVideo.append("ATSC")
                    possibleStandardsVideo.append("DTMB")
                elif codec['name'] == "avs" or codec['name'] == "avs+":
                    possibleStandardsVideo.append("DTMB")
                else:
                    possibleStandardsVideo.append(None)
        
        coincidences = [i for i, j in zip(possibleStandardsAudio, possibleStandardsVideo) if i == j]

        if len(coincidences) != 0:
            print("Possible Standards with this configuration: ", coincidences)
        else:
            print("There are no possible standards with this configuration!")

    def createContainerAndCheck(self, subtitles):

        self.createContainer(subtitles)
        self.bradcastingStandard()



if __name__ == "__main__":

    menu = mainMenu()
    action = menu['Action menu']
    video = menu['video file']
    container = mp4(video)

    if action == "Create container":
        subs = subtitlesMenu()['subtitles file']
        container.createContainer(subs)
    elif action == 'Check standard':
        if os.path.isfile('myContainer.mp4'):
            container.bradcastingStandard()
        else: 
            print("A created container must be created to check. Name: myContainer.mp4")
    elif action == 'Create and check standards':
        subs = subtitlesMenu()['subtitles file']
        container.createContainerAndCheck(subs)
    
