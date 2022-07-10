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
            f.close()

        with open('images/heading.xml', 'w') as f:
            f.write(str(parsed_xml))
            f.close()

    def write_body_xml(self):
        directory_path = 'F:/Video_Resources/Albert_Ein/images/'
        directory = os.listdir('F:/Video_Resources/Albert_Ein/images/')
        directory.sort(key=lambda f: int(re.sub('\D', '', f)))
        clip_id = 1
        clip_start = 0

        with open('Testing_XML_Writing/track.xml') as f:
            content = f.read()
            parsed_xml = BeautifulSoup(content, 'html.parser')

            #print(tag)
            #print(parsed_xml)
            if not os.path.exists(self.images_xml_path):
                os.makedirs(self.images_xml_path)

        for file in directory:
            print(file)
            duration = self.base_duration / len(directory)
            file_xml = BeautifulSoup(content, 'html.parser')
            names = file_xml.find_all(text='%%_name_%%')
            for name in names:
                name.replace_with(file)
            file_xml.find(text='%%_clip_duration_%%').replace_with(str(duration))
            file_xml.find(text='masterclip-%%_master_clip_id_%%').replace_with("masterclip-" + str(clip_id))
            file_xml.find(text='%%_path_%%').replace_with('file://localhost/F%3a/Video_Resources/Albert_Ein/images/' + file)

            clip_item_tag = file_xml.clipitem
            file_id_tag = file_xml.file
            #print(file_id_tag)
            clip_item_tag['id'] = "clipitem-" + str(clip_id)

            file_id_tag['id'] = "file-" + str(clip_id)

            file_xml.find(text='_clip_start_').replace_with(str(clip_start))
            #print(file_xml.start)
            clip_start += duration
            #print(str(clip_start))
            file_xml.find(text='_clip_end_').replace_with(str(clip_start))
            #print(file_xml.end)
            #print(str(clip_start))

            with open(self.images_xml_path + 'initial' + '.xml', 'a') as f:
                f.write(str(file_xml))
                f.close()
            clip_id += 1

    def write_the_whole_thing(self):
        with open('images/heading.xml') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

        print(soup)
        with open('images/initial.xml') as g:
            initial = g.read()
            #print(initial)
            soup.find('tra').replace_with(initial)
            g.close()
        with open('images/final.xml', 'w') as r:
            r.write(str(soup))
            print('should be written')

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
    c.write_header_xml(c)
    c.write_body_xml(c)
    c.write_the_whole_thing(c)

