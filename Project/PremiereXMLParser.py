import os

from bs4 import BeautifulSoup
import re
import subprocess
import uuid


class XMLParser:

    video_duration = 0
    xml_uuid = uuid.uuid4()
    name = ''
    base_duration = 5000
    base_name = 'Albert Einstein'
    body_sections = []
    images_xml_path = 'C:/Automated YouTube Project/FreeMoney/Project/images/'

    def write_header_xml(self):

        with open('Testing_XML_Writing/test.xml') as f:
            content = f.read()
            parsed_xml = BeautifulSoup(content, 'html.parser')
            parsed_xml.find(text='%%_uuid_%%').replace_with(str(self.xml_uuid))
            parsed_xml.find(text='%%_duration_%%').replace_with(str(self.base_duration))
            parsed_xml.find(text='%%_name_%%').replace_with(self.base_name)
            print(parsed_xml)

    def write_body_xml(self):

        directory = os.listdir('F:/Video_Resources/Albert_Ein/images/')
        clip_id = 1
        clip_start = 0

        with open('Testing_XML_Writing/track.xml') as f:
            content = f.read()
            parsed_xml = BeautifulSoup(content, 'html.parser')
            tag = parsed_xml.clipitem['id']
            #print(tag)
            #print(parsed_xml)
            if not os.path.exists(self.images_xml_path):
                os.makedirs(self.images_xml_path)
        for file in directory:

            file_xml = BeautifulSoup(content, 'html.parser')
            file_xml.find(text='%%_name_%%').replace_with(file)
            file_xml.find(text='%%_clip_duration_%%').replace_with(str(self.base_duration / len(directory)))

            clip_item_tag = file_xml.clipitem
            master_clip_id_tag = file_xml.masterclipid
            file_id_tag = file_xml.file
            print(file_id_tag)
            clip_item_tag['id'] = "clipitem-" + str(clip_id)
            master_clip_id_tag['id'] = "masterclip-" + str(clip_id)
            file_id_tag['id'] = "file-" + str(clip_id)

            file_xml.find(text='%%_clip_start_%%').replace_with(str(clip_start))
            clip_start += (self.base_duration / len(directory))
            file_xml.find(text='%%_clip_end_%%').replace_with(str(clip_start))
            

            f = open(self.images_xml_path + file[0:-4] + '.txt', 'w')
            f.write(str(file_xml))
            f.close()
            clip_id += 1


        #print(self.body_sections)

    def get_length(self, filename):
        """
        I'm going to need this eventually, but this is how I'll get the length of the video
        :return:
        """

        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        self.video_duration = result.stdout
        return float(result.stdout)

if __name__ == "__main__":
    c = XMLParser
    #c.write_header_xml(c)
    c.write_body_xml(c)

