from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract
import tkinter as tk
import speech_recognition as sr

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



# Create the main Tkinter window
root = tk.Tk()
root.title("ImTex")
root.geometry("1250x800")
root.configure(bg='lightblue')




def open_window1():
    root.withdraw()
    def upload_and_extract_text():
        try:
            # Open a file dialog to select the image
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
            )
            if not file_path:
                return  # User canceled file selection

            # Open and process the image
            image = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(image)

            # Normalize the text: clean up newlines and extra spaces
            normalized_text = " ".join(line.strip() for line in extracted_text.splitlines() if line.strip())

            # Display the extracted text in the text widget
            text_display.delete(1.0, tk.END)
            text_display.insert(tk.END, extracted_text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def back_go():
        root.deiconify()
        window1.destroy()


    window1=tk.Tk()
    window1.geometry("1250x800")
    window1.config(bg="lightblue")
    window1.title("Image Text Extractor")

    text_label = tk.Label(window1, text="Extracted Text:",font=("Consolas",16,"bold"),bg="lightblue")
    text_label.pack(pady=5)
    text_label.place(x=200,y=150)

    text_display = tk.Text(window1, wrap=tk.WORD, width=61, height=18, font=("Timesnewroman",18,"bold"))
    text_display.pack(pady=10)
    text_display.place(x=200,y=200)

    upload_button = tk.Button(window1, text="Upload Image", command=upload_and_extract_text, font=("Consolas",14,"bold"),fg="white",bg="darkblue")
    upload_button.pack(pady=10)
    upload_button.place(x=870, y=150)

    back_button1=tk.Button(window1, text="Back", command=back_go, font=("Consolas",14,"bold"),fg="white",bg="darkblue")
    back_button1.pack(pady=10)
    back_button1.place(x=30,y=30)




# Function for Audio Text Extraction
def open_window2():
    root.withdraw()
    recognizer = sr.Recognizer()
    recorded_audio = None


    def start_recording():
        nonlocal recorded_audio

        recorded_audio = []
        # Start recording using the microphone for 10 seconds
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source, timeout=15)  # Record for 10 seconds

            # Append the recorded audio to the list
            recorded_audio.append(audio_data)
            window2.after(2000, lambda: status_label.config(text="Click 'Record' to begin recording."))

        # Automatically extract text after 10 seconds of recording
        extract_text()

    def extract_text():
        nonlocal recorded_audio

        if recorded_audio:
            # Combine recorded audio pieces into one
            audio_data = sr.AudioData(b''.join([audio.get_wav_data() for audio in recorded_audio]),
                                      recorded_audio[0].sample_rate, recorded_audio[0].sample_width)
            try:
                # Extract text using Google Speech API
                extracted_text = recognizer.recognize_google(audio_data)
                text_display.insert(tk.END,extracted_text)
            except sr.UnknownValueError:
                text_display.insert(tk.END, "Sorry, could not understand the audio\n")

            except sr.RequestError as e:
                text_display.insert(tk.END, f"Request error: {e}\n")
        else:
            messagebox.showinfo("Info", "No audio recorded to extract text from!")

    def back_go():
        root.deiconify()
        window2.destroy()


    # Set up the window
    window2 = tk.Tk()
    window2.config(bg="lightblue")
    window2.geometry("1250x800")
    window2.title("Audio Text Extractor")



    text_display = tk.Text(window2, wrap=tk.WORD, width=61, height=18, font=("Timesnewroman",18,"bold"))
    text_display.pack(pady=15)

    status_label = tk.Label(window2, text="Click 'Record' to begin recording.", bg="lightblue")
    status_label.pack(pady=10)

    # Button to start recording
    record_button = tk.Button(window2, text="Start Record", command=start_recording,font=("Consolas", 14, "bold"), fg="white", bg="darkblue")
    record_button.pack(pady=10)

    back_button1 = tk.Button(window2, text="Back", command=back_go, font=("Consolas", 14, "bold"), fg="white", bg="darkblue")
    back_button1.pack(pady=10)
    back_button1.place(x=30, y=30)






# Create and place widgets
imTex = tk.Button(root, text="Extract text from image", command=open_window1, width=30, height=2, font=("Consolas",16,"bold"),fg="white")
imTex.pack(pady=10)
imTex.config(bg="darkblue")
imTex.place(x=170, y=610)
recTex = tk.Button(root, text="Extract text from recording", command=open_window2, width=30, height=2, font=("Consolas",16,"bold"),fg="white")
recTex.pack(pady=15)
recTex.config(bg="darkblue")
recTex.place(x=770, y=610)

image1=tk.PhotoImage(file="imtex.png")
image2=tk.PhotoImage(file="recTex.png")
imgim=tk.Label(root, image=image1, width=400, height=400)
imgim.pack(pady=20)
imgim.place(x=150,y=190)
imgrec=tk.Label(root, image=image2, width=400, height=400)
imgrec.pack(pady=27)
imgrec.place(x=750, y=190)



root.mainloop()