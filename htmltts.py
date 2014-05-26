#!/usr/bin/python
# htmltts.py
# By Ben Newsome

# This program reads a commented html file, and creates audio files from the comments.

# It parses the html file for "<!--tts" to start the tts, and then tts--/> to end the tts.
# The first line after <!--tts should be the name of the slide.
import sys
import os
import urllib2

debug=True

def main(debug):
   # Get the file location from the sys arg
   if not os.path.exists(sys.argv[1]):
      sys.stderr.write('ERROR: Argument of the html file required')
      sys.exit(1)
   input_html_file=str(sys.argv[1])
   # Read the input html file
   html_file=open(input_html_file, 'rb')
   #parse the input file into paragraphs
   paragraphs=split_into_paragraphs(html_file,debug)
   #Create the mp3 from the paragraph
   create_mp3_tts(paragraphs,debug)
   return

def split_into_paragraphs(html_file, debug):
   read=False
   paragraph_text = ' '
   paragraph_first_line=True
   paragraphs={}
   paragraph_name = ' '
   for line in html_file:
      print line
      if line.startswith("/tts-->"):
         read=False   
         paragraphs[paragraph_name] = paragraph_text
         paragraph_first_line=True
      if read:
         if paragraph_first_line:
            paragraph_name=line[:-1]
            paragraph_first_line=False
            paragraph_text = ' '
         else:
            paragraph_text += line[:-1]
      if line.startswith("<!--tts"):
         read=True

   if debug:
      for item in paragraphs:
         print item
         print paragraphs[item]  
         print '\n'

   return paragraphs;

def create_mp3_tts(paragraphs,debug):
   tts_url = "http://translate.google.com/translate_tts?tl=en&q="

   for item in paragraphs:
      # replace space with html %20
#      tts_string=paragraphs[item].replace(' ','+')
#      url = tts_url + tts_string[1:]
      wav_file_location = "audio/" + item + ".wav"
      # Get around the tts engien not being able to understand '?'
      paragraphs[item] = paragraphs[item].replace('?','.')

      if debug:
         print wav_file_location
#         print tts_string
#         print url

#      request = urllib2.Request(url)
      # Lie to google saying we are firefox
#      request.add_header('User-agent', 'Mozilla/5.0')
#      opener = urllib2.build_opener()


#      mp3_file = open(mp3_file_location, "wb")
#      mp3_file.write(opener.open(request).read())
#      mp3_file.close
      cmd = 'pico2wave -w '+ wav_file_location + ' "' + paragraphs[item] + '"'
      print cmd
      os.system(cmd)


   return

main(debug)
