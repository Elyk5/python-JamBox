from tkinter import *
from tkinter import filedialog
import pygame

root = Tk()

root.title("MP3 Jambox") 
root.geometry("600x500")

#Initialize Pygame
pygame.mixer.init()

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
		#Reconstruct with dirextory structure
		song = playlist_box.get(ACTIVE)
		song = f'C:/mp3/audio/{song}.mp3'

		#Load song with pygame mixer
		pygame.mixer.music.load(song)

		#Play song with pygame mixer
		pygame.mixer.music.play(loops=0)

#Create stop function
def stop():
		#Stop song
		pygame.mixer.music.stop()

		#Clear playlist bar
		playlist_box.selection_clear(ACTIVE)

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

#Create playlist Box
playlist_box = Listbox(root, bg="black", fg="green", width=70, selectbackground="green", selectforeground="black")

playlist_box.pack(pady=20)

#Define Button Images For Controls
back_btn_img = PhotoImage(file='images/back5.png')
forward_btn_img = PhotoImage(file='images/forward5.png')
play_btn_img = PhotoImage(file='images/play5.png')
pause_btn_img = PhotoImage(file='images/pause5.png')
stop_btn_img = PhotoImage(file='images/stop5.png')

#Create Button Frame
control_frame = Frame(root)
control_frame.pack(pady=20)

#Create Play/Stop.... Buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)


back_button.grid(row=0, column=0, padx=10) 
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
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

# Temporary Label
my_label = Label(root, text ='')
my_label.pack(pady=30)


root.mainloop()