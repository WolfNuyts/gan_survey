from tkinter import *
import pickle
import numpy as np
import random




class Display(object):
    def __init__(self):
        self.quality_q = 'Please rank the QUALITY from best(1) to worst(4):'
        self.cond_q = 'Please rank the RELEVANCE ACCORDING TO THE TEXT DESCRIPTION from best(1) to worst(4):'
        self.sample_size = 50
        self.i = 1
        self.results = np.zeros((self.sample_size*2, 4))
        with open('data/captions.pkl', 'rb') as fh:
            self.captions = pickle.load(fh)

        self.root = Tk()
        self.root.wm_title("survey")
        question_frame = Frame(self.root)
        question_frame.pack(side='top', pady=10, padx=20)
        self.question = Label(question_frame, text=self.quality_q, anchor='w', justify='left')
        self.question.pack(side='left')

        text_frame = Frame(self.root)
        text_frame.pack(side='top', pady=10, padx=20)
        self.text_descr = Label(text_frame, text='', wraplengt=1100)
        self.text_descr.config(font=("Courier", 18))
        self.text_descr.pack(side='top')

        image_frame0 = Frame(self.root)
        image_frame0.pack(side='left', pady=50, padx=20)
        canvas0 = Canvas(image_frame0, width=256, height=256)
        canvas0.pack()
        self.img0 = PhotoImage(file="data/0/0.png")
        canvas0.create_image(0, 0, anchor='nw', image=self.img0)
        self.user_input0 = StringVar(self.root)
        entry0 = Entry(image_frame0, textvariable=self.user_input0)
        entry0.pack()

        image_frame1 = Frame(self.root)
        image_frame1.pack(side=LEFT, pady=50, padx=20)
        canvas1 = Canvas(image_frame1, width=256, height=256)
        canvas1.pack()
        self.img1 = PhotoImage(file="data/0/1.png")
        canvas1.create_image(0, 0, anchor='nw', image=self.img1)
        self.user_input1 = StringVar(self.root)
        entry1 = Entry(image_frame1, textvariable=self.user_input1)
        entry1.pack()

        image_frame2 = Frame(self.root, pady=50, padx=20)
        image_frame2.pack(side='left')
        canvas2 = Canvas(image_frame2, width=256, height=256)
        canvas2.pack()
        self.img2 = PhotoImage(file="data/0/2.png")
        canvas2.create_image(0, 0, anchor='nw', image=self.img2)
        self.user_input2 = StringVar(self.root)
        entry2 = Entry(image_frame2, textvariable=self.user_input2)
        entry2.pack()

        image_frame3 = Frame(self.root, pady=50, padx=20)
        image_frame3.pack(side='left')
        canvas3 = Canvas(image_frame3, width=256, height=256)
        canvas3.pack()
        self.img3 = PhotoImage(file="data/0/3.png")
        canvas3.create_image(0, 0, anchor='nw', image=self.img3)
        self.user_input3 = StringVar(self.root)
        entry3 = Entry(image_frame3, textvariable=self.user_input3)
        entry3.pack()

        button_frame = Frame(self.root, pady=50, padx=20)
        button_frame.pack(side=BOTTOM)
        next_but = Button(button_frame, text="Next", fg="black", command=self.next_button)
        next_but.pack(side='bottom')
        self.error = Label(button_frame, text='', wraplengt=100, fg='red')
        self.error.pack(side='top')
        self.progress = Label(button_frame, text='progress: 1/' + str(self.sample_size))
        self.progress.pack(side='top')

        self.root.mainloop()

    def next_button(self):
        inputs = []
        self.error.configure(text='')
        for input in [self.user_input0.get(), self.user_input1.get(), self.user_input2.get(), self.user_input3.get()]:
            try:
                input = int(input)
                if input > 4 or input < 1:
                    self.error.configure(text='the inputs can only be: 1, 2, 3 or 4')
                    return
                inputs.append(input)
            except:
                self.error.configure(text='the inputs can only be: 1, 2, 3 or 4')
                return
        if len(set(inputs)) < 4:
            self.error.configure(text='make sure all the inputs are distinct')
            return

        if self.i == self.sample_size*2:

            self.results[self.i - 1] = np.array(inputs)
            with open('results/results_' + str(random.randint(0, int(1e15))) + '.pkl', 'wb') as fh:
                pickle.dump(self.results, fh)
            
            self.root.destroy()
            popup = Tk()
            popup.wm_title("survey")
            greeting = Label(popup,text="Bedankt voor het invullen van mijn survey!", width=100, height=10)
            greeting.pack()
            startBut = Button(popup, text="Close", fg="black", command=popup.destroy)
            startBut.pack()
            popup.mainloop()
        elif self.i % 2 == 1:
            self.results[self.i - 1] = np.array(inputs)
            self.user_input0.set('')
            self.user_input1.set('')
            self.user_input2.set('')
            self.user_input3.set('')

            self.question.configure(text=self.cond_q)
            self.text_descr.configure(text=self.captions[int(self.i/2)])
            self.i += 1
        else:
            self.results[self.i - 1] = np.array(inputs)
            self.user_input0.set('')
            self.user_input1.set('')
            self.user_input2.set('')
            self.user_input3.set('')

            self.question.configure(text=self.quality_q)
            self.text_descr.configure(text='')
            image_folder = 'data/' + str(int(self.i/2)) + '/'
            self.img0.configure(file=image_folder + '0.png')
            self.img1.configure(file=image_folder + '1.png')
            self.img2.configure(file=image_folder + '2.png')
            self.img3.configure(file=image_folder + '3.png')
            self.i += 1
            self.progress.configure(text='progress: ' + str(1 + int(self.i/2)) + '/' + str(self.sample_size))
        return


if __name__ == '__main__':
    popup = Tk()
    popup.wm_title("survey")
    greeting = Label(popup,
                     text="Hallo, "
                          "\n\nDeze survey onderzoekt hoe goed verschillende AI modellen realistische "
                          "afbeeldingen kunnen onderzoeken. Hiervoor krijgt u 50 reeksen van 4 afbeeldingen te zien"
                          "Deze zal u 2 keer moeten ranken van beste(1) tot slechtste(4)."
                          "\n\nDe eerst keer vragen we u om deze afbeelding te ranken op de kwaliteit van de "
                          "afbeeldingen. Dit wil zeggen dat u ze moeten ranken op hoe realistisch ze eruit zien."
                          "\n\nDe tweede keer vragen tonen we ook een tekst beschrijving van de afbeelding en "
                          "vragen we u om de afbeelding te ranken op hoe goed deze afbeeldingen afbeelden wat er in "
                          "de tekst beschrijving straat. De bedoeling is om deze keer de kwaliteit helemaal NIET in "
                          "rekening te brengen."
                          "\n\nalvast bedankt voor u medewerking,"
                          "\nWolf",
                     wraplengt=500, anchor='w', justify='left')
    greeting.pack()
    startBut = Button(popup, text="Start", fg="black", command=popup.destroy)
    startBut.pack()
    popup.mainloop()
    Display()
