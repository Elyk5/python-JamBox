from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()

root.title("MP3 Jambox") 
root.geometry("800x450")

#Initialize Pygame
pygame.mixer.init()

#Create Functon to deal with time of song
def play_time():
		#Check to see if song is stopped
		if stopped:
			return

		current_time = pygame.mixer.music.get_pos() / 1000
		converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

		song = playlist_box.get(ACTIVE)
		song = f'C:/mp3/audio/{song}.mp3'

		#Find current song length
		song_mut = MP3(song)
		global song_length
		song_length = song_mut.info.length
		#Convert to time format
		converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

		if int(song_slider.get()) == int(song_length):
			stop()

		elif paused:
			pass
		else:
			#Move slider along 1 second at a time
			next_time = int(song_slider.get()) + 1
			#Output 
			song_slider.config(to=song_length, value=next_time)

			#Convert slider poition to time format
			converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

			#Output slider
			status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

		#Add current time to slider bar
		if current_time >= 0:
			status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

		status_bar.after(1000, play_time)

#Functions created to add one or many songs to playlist.
def add_song():
		song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files","*.mp3"), ) )
		# Strip out directory structute and .mp3 from song title
		song = song.replace("C:/mp3/audio/", "")
		song = song.replace(".mp3", "")

		playlist_box.insert(END, song)

def add_multiple_songs():
		songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files","*.mp3"), ) )
		
		# Loop through song list and replace directory structure and mp3 from song name
		for song in songs:

				# Strip out directory structute and .mp3 from song title
				song = song.replace("C:/mp3/audio/", "")
				song = song.replace(".mp3", "")
				#Add to end to playlist
				playlist_box.insert(END, song)


#Create function to delete one song from playlist
def delete_song():
	playlist_box.delete(ANCHOR)

#Create function to delete all songs from playlist
def delete_all_songs():
	playlist_box.delete(0, END)

#Create play function
def play():
		#Set stopped to false because a song has started playing
		global stopped
		stopped = False

		#Reconstruct with dirextory structure
		song = playlist_box.get(ACTIVE)
		song = f'C:/mp3/audio/{song}.mp3'

		#Load song with pygame mixer
		pygame.mixer.music.load(song)

		#Play song with pygame mixer
		pygame.mixer.music.play(loops=0)

		#Get song time
		play_time()

#Create stopped variable
global stopped
stopped = False

#Create stop function
def stop():
		#Stop song
		pygame.mixer.music.stop()

		#Clear playlist bar
		playlist_box.selection_clear(ACTIVE)

		status_bar.config(text='')

		song_slider.config(value=0)

		global stopped
		stopped = True


#Create function to play the next song
def next_song():
		#Reset slider positio and status bar
		status_bar.config(text='')
		song_slider.config(value=0)
		#Get current song number
		next_one = playlist_box.curselection()
		#my_label.config(text=next_one)
		next_one = next_one[0] + 1

		#Grab the song title from the playlist, formats the song, loads song and then plays song
		song = playlist_box.get(next_one)
		song = f'C:/mp3/audio/{song}.mp3'
		pygame.mixer.music.load(song)
		pygame.mixer.music.play(loops=0)

		#Clear Active Bar in Playlist
		playlist_box.selection_clear(0, END)

		#Move active bar to next song
		playlist_box.activate(next_one)
		playlist_box.selection_set(next_one, last=None)

def song_before():
		#Reset slider positio and status bar
		status_bar.config(text='')
		song_slider.config(value=0)

		#Get current song number
		one_before = playlist_box.curselection()
		one_before = one_before[0] - 1

		#Grab the song title from the playlist, formats the song, loads song and then plays song
		song = playlist_box.get(one_before)
		song = f'C:/mp3/audio/{song}.mp3'
		pygame.mixer.music.load(song)
		pygame.mixer.music.play(loops=0)

		#Clear Active Bar in Playlist
		playlist_box.selection_clear(0, END)

		#Move active bar to song before
		playlist_box.activate(one_before)
		playlist_box.selection_set(one_before, last=None)

#Create paused variable
global paused
paused = False

#Create pause function
def pause(is_paused):
		global paused
		paused = is_paused

		if paused:
			#Unpause
			pygame.mixer.music.unpause()
			paused = False

		else:
			#Pause
			pygame.mixer.music.pause()
			paused = True

#Create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#Create slide function
def slide(x):
		#Reconstruct with dirextory structure
		song = playlist_box.get(ACTIVE)
		song = f'C:/mp3/audio/{song}.mp3'

		#Load song with pygame mixer
		pygame.mixer.music.load(song)

		#Play song with pygame mixer
		pygame.mixer.music.play(loops=0, start=song_slider.get())

#Create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#Create playlist Box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=70, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

#Create volume slider frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=10)

#Create volume slider
volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, length=125, value=.5, command=volume)
volume_slider.pack(pady=10)

#Create song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

#Define Button Images For Controls
pause_btn_img = PhotoImage(file='images/pause5.png')
back_btn_img = PhotoImage(file='images/back5.png')
forward_btn_img = PhotoImage(file='images/forward5.png')
play_btn_img = PhotoImage(file='images/play5.png')
stop_btn_img = PhotoImage(file='images/stop5.png')

#Create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

#Create Play/Stop.... Buttons
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=song_before)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)


pause_button.grid(row=0, column=0, padx=10)
back_button.grid(row=0, column=1, padx=10) 
forward_button.grid(row=0, column=2, padx=10)
play_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)



# Create menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create add song menu dropdown
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)

# Add one or multiple songs to playlist.
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
add_song_menu.add_command(label="Add Multiple Songs To Playlist", command=add_multiple_songs)


#Create delete song menu dropdowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu = remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command= delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command= delete_all_songs)

#Create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# Temporary Label
my_label = Label(root, text ='')
my_label.pack(pady=30)


root.mainloop()