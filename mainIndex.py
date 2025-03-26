from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from fpdf import FPDF
import csv
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

win1 = Tk()
win1.title("Student Analyse")
win1.geometry("600x700")
win1.maxsize(600, 700)
win1.minsize(600, 700)
win1.configure(bg="#33ffbd")

classtest_data = None
internal_data = None

def upload_classtest():
    global classtest_data
    file_path = askopenfilename(filetypes=[["CSV Files", "*.csv"]])
    if file_path:
        with open(file_path, "r") as file:
            classtest_data = list(csv.DictReader(file))
        messagebox.showinfo("File Uploaded", "Class Test file uploaded successfully.")

def upload_internal():
    global internal_data
    file_path = askopenfilename(filetypes=[["CSV Files", "*.csv"]])
    if file_path:
        with open(file_path, "r") as file:
            internal_data = list(csv.DictReader(file))
        messagebox.showinfo("File Uploaded", "Internal Marks file uploaded successfully.")

def Analyse():
    regno = Aregno.get().strip()
    accyear = Aaccyear.get().strip()
    dept = Adept.get().strip().lower()

    if not regno or not accyear or not dept:
        messagebox.showerror("Invalid Input", "RegNo, Academic Year, and Department are mandatory.")
        return

    if not classtest_data or not internal_data:
        messagebox.showerror("Missing Files", "Please upload Class Test and Internal Marks files.")
        return

    def find_record(data, regno, accyear, dept):
        for row in data:
            if row.get("Regno", "").strip() == regno and row.get("AccYear", row.get("Accyear", "")).strip() == accyear and row.get("Dept", "").strip().lower() == dept:
                return row
        return None

    classtest_scores = find_record(classtest_data, regno, accyear, dept)
    internal_scores = find_record(internal_data, regno, accyear, dept)

    if not classtest_scores:
        messagebox.showerror("Data Not Found", f"No Class Test record found for RegNo: {regno}")
        return
    if not internal_scores:
        messagebox.showerror("Data Not Found", f"No Internal Marks record found for RegNo: {regno}")
        return

    #=========================Gui=2nd_page===========================
    
    
    result_window = Toplevel()
    result_window.title(f"Analysis for RegNo: {regno}")
    result_window.geometry("600x800")
    result_window.maxsize(600, 800)
    result_window.minsize(600, 800)
    result_window.configure(bg="#33ffbd")

    # Add scrollbar
    scrollbar = Scrollbar(result_window)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas_frame = Canvas(result_window, bg="#33ffbd", yscrollcommand=scrollbar.set)
    canvas_frame.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar.config(command=canvas_frame.yview)

    frame = Frame(canvas_frame, bg="#33ffbd")
    canvas_frame.create_window((0, 0), window=frame, anchor="nw")

    def on_configure(event):
        canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))

    frame.bind("<Configure>", on_configure)

    # Display student details and scores
    Label(frame, text=f"Analysis for RegNo: {regno}", font=("Helvetica", 18, "bold"), bg="#33ffbd").pack(pady=10)

    Label(frame, text="Class Test Scores", font=("Helvetica", 16, "bold"), bg="#33ffbd").pack(pady=5)
    for k, v in classtest_scores.items():
        if k.lower() not in ["regno", "accyear", "dept"]:
            Label(frame, text=f"{k}: {v}", font=("Helvetica", 14), bg="#33ffbd", anchor="center", width=40).pack(pady=2)

    Label(frame, text="Internal Marks", font=("Helvetica", 16, "bold"), bg="#33ffbd").pack(pady=5)
    for k, v in internal_scores.items():
        if k.lower() not in ["regno", "accyear", "dept"]:
            Label(frame, text=f"{k}: {v}", font=("Helvetica", 14), bg="#33ffbd", anchor="center", width=40).pack(pady=2)

    # Combined graph analysis
    combined_scores = {
        "Class Test": {k: int(v) for k, v in classtest_scores.items() if k.lower() not in ["regno", "accyear", "dept"] and v.isdigit()},
        "Internal Marks": {k: int(v) for k, v in internal_scores.items() if k.lower() not in ["regno", "accyear", "dept"] and v.isdigit()}
    }

    graph_image_path = f"Graph_{regno}.png"

    if combined_scores["Class Test"] and combined_scores["Internal Marks"]:
        labels = list(combined_scores["Class Test"].keys())
        class_test_values = list(combined_scores["Class Test"].values())
        internal_values = [combined_scores["Internal Marks"].get(k, 0) for k in labels]

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(labels, class_test_values, label="Class Test", marker="o")
        ax.plot(labels, internal_values, label="Internal Marks", marker="o")
        ax.set_title("Exam Results Comparison")
        ax.set_ylabel("Scores")
        ax.set_xlabel("Subjects")
        ax.legend()

        canvas_plot = FigureCanvasTkAgg(fig, master=frame)
        canvas_plot.draw() 
        canvas_plot.get_tk_widget().pack(pady=10)

        # Save the graph as an image
        fig.savefig(graph_image_path)

    # Download results
    def Download():
        
        current_dir = os.getcwd()

        text_file_path = os.path.join(current_dir, f"Analysis_{regno}.txt")
        pdf_file_path = os.path.join(current_dir, f"Analysis_{regno}.pdf")

        # Save text content to a file
        with open(text_file_path, "w") as txt_file:
            txt_file.write(f"Analysis for RegNo: {regno}\n\n")
            txt_file.write("Class Test Scores:\n")
            for k, v in classtest_scores.items():
                if k.lower() not in ["regno", "accyear", "dept"]:
                    txt_file.write(f"{k}: {v}\n")
            txt_file.write("\nInternal Marks:\n")
            for k, v in internal_scores.items():
                if k.lower() not in ["regno", "accyear", "dept"]:
                    txt_file.write(f"{k}: {v}\n")

        # Generate the PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 10, txt=f"Analysis for RegNo: {regno}", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="Class Test Scores:", ln=True, align='C')
        for k, v in classtest_scores.items():
            if k.lower() not in ["regno", "accyear", "dept"]:
                pdf.cell(0, 10, txt=f"{k}: {v}", ln=True, align='C')

        pdf.ln(5)
        pdf.cell(0, 10, txt="Internal Marks:", ln=True, align='C')
        for k, v in internal_scores.items():
            if k.lower() not in ["regno", "accyear", "dept"]:
                pdf.cell(0, 10, txt=f"{k}: {v}", ln=True, align='C')

        pdf.ln(10)
        if os.path.exists(graph_image_path):
            pdf.image(graph_image_path, x=40, w=130,h=90)

        pdf.output(pdf_file_path)
        
        if os.path.exists(text_file_path):
            os.remove(text_file_path)
        if os.path.exists(graph_image_path):
            os.remove(graph_image_path)
        
        os.startfile(pdf_file_path)
        messagebox.showinfo("Download Complete", f"Analysis saved as PDF: {pdf_file_path}")

    Button(frame, text="Download PDF", font=("times new roman", 25, "bold"), bg="#fbe7a1", width=12, relief="groove", command=Download).pack(pady=10)



    #========================Gui=2nd_page=end========================
    
   
    
# Reset Function
def Reset():
    Aregno.delete(0, END)
    Aaccyear.delete(0, END)
    Adept.delete(0, END)
    global classtest_data, internal_data
    classtest_data = None
    internal_data = None
    messagebox.showinfo("Reset", "All inputs and uploaded files have been cleared.")

def Exit():
    win1.destroy()

def Student_Login():
    pass
# ==========================Gui= main_page==========================


Label(win1, text="Student Data Analysis", font=("Helvetica", 25, "bold"), bg="#fbe7a1", width=30, relief="groove").place(x=0, y=0, height=74)

Label(win1, text="RegNo:", font=("times new roman", 20, "bold"), bg=win1['bg'], width=8, relief="groove").place(x=40, y=100)
Aregno = Entry(win1, font=("Helvetica", 14, "bold"), bg="white", width=33, relief="groove")
Aregno.place(x=190, y=100, height=35)

Label(win1, text="Acc Year:", font=("times new roman", 20, "bold"), bg=win1['bg'], width=8, relief="groove").place(x=40, y=150)
Aaccyear = Entry(win1, font=("Helvetica", 14, "bold"), bg="white", width=33, relief="groove")
Aaccyear.place(x=190, y=150, height=35)

Label(win1, text="Dept:", font=("times new roman", 20, "bold"), bg=win1['bg'], width=8, relief="groove").place(x=40, y=200)
Adept = Entry(win1, font=("Helvetica", 14, "bold"), bg="white", width=33, relief="groove")
Adept.place(x=190, y=200, height=35)

Label(win1, text="Class Test:", font=("times new roman", 20, "bold"), bg=win1['bg'], width=12, relief="groove").place(x=40, y=250)
Button(win1, text="Upload File", font=("times new roman", 14, "bold"), bg="white", relief="groove", command=upload_classtest).place(x=260, y=250)

Label(win1, text="Internal Marks:", font=("times new roman", 20, "bold"), bg=win1['bg'], width=12, relief="groove").place(x=40, y=300)
Button(win1, text="Upload File", font=("times new roman", 14, "bold"), bg="white", relief="groove", command=upload_internal).place(x=260, y=300)


Button(win1, text="Analyse", font=("times new roman", 25, "bold"), bg="#fbe7a1", width=8, relief="groove",command=Student_Login).place(x=40, y=400, height=60,width=530)


Button(win1, text="Analyse", font=("times new roman", 25, "bold"), bg="#fbe7a1", width=8, relief="groove", command=Analyse).place(x=40, y=500, height=60)
Button(win1, text="Reset", font=("times new roman", 25, "bold"), bg="#fbe7a1", width=8, relief="groove", command=Reset).place(x=220, y=500, height=60)
Button(win1, text="Exit", font=("times new roman", 25, "bold"), bg="#fbe7a1", width=8, relief="groove", command=Exit).place(x=400, y=500, height=60)

win1.mainloop()
