from app import app

import os
  
from pydub import AudioSegment

path_chunks = "chunks/"


def pre_processing(path):
  
    dirlist = os.listdir(path)

    for i in dirlist:
      path = path + '/' + i

    sound_file = AudioSegment.from_wav(path)

    dir = path_chunks
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

  
    print(sound_file.duration_seconds)
   
    if sound_file.duration_seconds > 5.00:
              
        for i, chunk in enumerate(sound_file[::4000]):
        
            print(chunk.duration_seconds)    
            if chunk.duration_seconds > 3.00:         
                chunk_silent = AudioSegment.silent(duration = 500)
              
                audio_chunk = chunk_silent + chunk + chunk_silent
              
                  
                print('saving chunk'+str(i)+'.wav')

                
                audio_chunk.export( path_chunks+ '/chunk'+str(i)+'.wav', bitrate ='192k', format ="wav")
              
                    
                filename = 'chunk'+str(i)+'.wav'
              
                print("Processing chunk "+str(i))
          
    elif sound_file.duration_seconds < 3:
            chunk_silent = AudioSegment.silent(duration = 1000)
            audio_chunk = chunk_silent + sound_file + chunk_silent
            print('saving chunk.wav')
            # specify the bitrate to be 192 k

            

            audio_chunk.export(path_chunks+'/chunk.wav', bitrate ='192k', format="wav")
      
            # the name of the newly created chunk
            filename = 'chunk.wav'
      
            print("Processing chunk ")

    else: 
        sound_file.export(path_chunks+'/chunk.wav',
                          bitrate='192k', format="wav")


