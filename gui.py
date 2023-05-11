from tkinter import *
import csv
import os.path
import re


class GUI:
    def __init__(self, window):
        """Creates GUI"""
        self.window = window

        self.label_title = Label(self.window, text='CSV Writer', font=('Times New Roman', 12, 'bold'))
        self.label_title.pack(side='top')
        self.label_input = Label(self.window, text='Input File', font=('Times New Roman', 12, 'bold'))
        self.label_input.place(x=10, y=30)
        self.label_output = Label(self.window, text='Output File', font=('Times New Roman', 12, 'bold'))
        self.label_output.place(x=10, y=60)
        self.label_new_output = Label(self.window, text='New Output File', font=('Times New Roman', 12, 'bold'))

        self.entry_input_file = Entry(self.window, width=35, font=('Times New Roman', 12,))
        self.entry_input_file.place(x=100, y=30)
        self.entry_output_file = Entry(self.window, width=35, font=('Times New Roman', 12,))
        self.entry_output_file.place(x=100, y=60)
        self.entry_new_output_file = Entry(self.window, width=35, font=('Times New Roman', 12,))

        self.label_radio = Label(self.window, text='Overwrite Existing File?', font=('Times New Roman', 12, 'bold'))
        self.radio_1 = IntVar()
        self.radio_1.set(2)
        self.radio_yes = Radiobutton(self.window, text='YES', font=('Times New Roman', 12), variable=self.radio_1, value=0)
        self.radio_no = Radiobutton(self.window, text='NO', font=('Times New Roman', 12), variable=self.radio_1, value=1)

        self.button_submit = Button(self.window, text='SUBMIT', font=('Times New Roman', 12), command=self.submit).place(x=100, y=150)
        self.button_clear = Button(self.window, text='CLEAR', font=('Times New Roman', 12), command=self.clear).place(x=210, y=150)

        self.text_blank = Label(self.window, text='Please ensure both input and output fields are filled.', font=('Times New Roman', 12))
        self.text_fnf = Label(self.window, text='File not found! Please enter a valid file name.', font=('Times New Roman', 12))
        self.text_new_output = Label(self.window, text='Please enter a new output file name.', font=('Times New Roman', 12))
        self.text_stored = Label(self.window, text='Data Stored!', font=('Times New Roman', 12))

    def submit(self):
        """When submit button is clicked, the data is sorted and written to the appropriate CSV file."""
        input_file_name = self.entry_input_file.get()

        if len(input_file_name) == 0:
            self.text_fnf.place_forget()
            self.text_blank.place(x=200, y=200, anchor='center')
        else:
            while True:
                try:
                    file_name = input_file_name.strip()
                    complete_file_path = 'files/' + file_name
                    with open(complete_file_path, 'r') as input_file:
                         contents = input_file.readlines()
                    break
                except FileNotFoundError:
                    self.text_blank.place_forget()
                    self.text_fnf.place(x=200, y=200, anchor='center')
                    break

            output_file = self.entry_output_file.get()
            if len(output_file) == 0:
                self.text_fnf.place_forget()
                self.text_blank.place(x=200, y=200, anchor='center')
            elif os.path.isfile('files/' + output_file) is False or output_file == 'data.txt':
                self.text_blank.place_forget()
                self.text_fnf.place(x=200, y=200, anchor='center')
            else:
                if os.path.isfile('files/' + output_file):
                    self.text_fnf.place_forget()
                    self.text_blank.place_forget()
                    self.label_radio.place(x=10, y=100)
                    self.radio_yes.place(x=200, y=100)
                    self.radio_no.place(x=300, y=100)
                    choice = self.radio_1.get()

                    if choice == 1:
                        self.text_fnf.place_forget()
                        self.text_blank.place_forget()

                        self.label_output.place_forget()
                        self.entry_output_file.place_forget()

                        self.label_new_output.place(x=10, y=60)
                        self.entry_new_output_file.place(x=130, y=60, width=255)
                        self.text_new_output.place(x=200, y=200, anchor='center')

                        new_output_file = self.entry_new_output_file.get().strip()
                        if len(new_output_file) == 0:
                            self.text_stored.place_forget()
                            self.text_fnf.place_forget()
                            self.text_new_output.place(x=200, y=200, anchor='center')
                        else:
                            output_file = self.entry_new_output_file.get().strip()
                            self.write_data(contents, output_file)
                    if choice == 0:
                        output_file = self.entry_output_file.get().strip()
                        self.write_data(contents, output_file)

    def write_data(self, contents, output_file):
        """Function to write the input.txt data to the corresponding csv file
        :param contents: This stores the contents from the data.txt file. It is assumed that the input file is already
        stored in a folder called "files" that is in the same location as the code.
        :param output_file: The name of the output file the data is being written to. """
        emails = []
        subjects = []
        confidence = []

        with open(f'files/{output_file}', 'w', newline='') as final_output:
            writer = csv.DictWriter(final_output, fieldnames=['Email', 'Subject', 'Confidence'])
            writer.writeheader()

            for line in contents:
                email_names = re.findall('^From (\S+@\S+)', line)
                if len(email_names) == 1:
                    emails.append(email_names[0])
                subject_nums = re.findall('^Subject.*', line)
                if len(subject_nums) == 1:
                    subjects.append(subject_nums[0])
                x_confidence = re.findall('^X-DSPAM-Confidence.*', line)
                if len(x_confidence) == 1:
                    confidence.append(x_confidence[0])

            confidence_nums = []
            for i in confidence:
                confidence_nums.append(float(i.split()[1]))

            subjects_final = []
            for i in subjects:
                subjects_final.append(i.split()[4])

            for i in range(len(emails)):
                writer.writerow(
                    {'Email': emails[i], 'Subject': subjects_final[i], 'Confidence': confidence_nums[i]})

                self.text_stored.place(x=200, y=200, anchor='center')
                self.text_new_output.place_forget()
                self.text_fnf.place_forget()
                self.text_blank.place_forget()


    def clear(self):
        """Clears all entry boxes, hides radio buttons and respective labels, new output entry box and respective labels,
        and any text statements."""
        self.entry_input_file.delete(0, END)
        self.entry_output_file.delete(0, END)
        self.entry_new_output_file.place_forget()
        self.label_new_output.place_forget()
        self.label_output.place(x=10, y=60)
        self.entry_output_file.place(x=100, y=60)

        self.label_radio.place_forget()
        self.radio_yes.place_forget()
        self.radio_no.place_forget()

        self.text_blank.place_forget()
        self.text_new_output.place_forget()
        self.text_fnf.place_forget()
        self.text_stored.place_forget()
