from tkinter import ttk

# Color Palet Ref https://www.figma.com/colors/steel-blue/

def configure_styles(root):
    style = ttk.Style()
    bg_standard = "#366899"
    fg_standard = "white"
    btn_bg = "#B4C3D2"
    btn_fg = "black"

    # Set DEFAULT backgrounds for ALL ttk widgets
    style.theme_use('clam')
    style.configure("TFrame", background=bg_standard)
    style.configure("TLabel", background=bg_standard, foreground=fg_standard)
    style.configure("TCheckbutton", background=bg_standard, foreground=fg_standard)
    style.map("TCheckbutton", background=[('active', bg_standard)],
              indicatorbackground=[('selected', 'green'), ('!selected', "white")],
              indicatorforeground=[('selected', 'green'), ('!selected', "white")])
    style.configure("TRadiobutton", background=bg_standard)
    style.configure("TButton", background=btn_bg, foreground=btn_fg)
    style.configure("TEntry", fieldbackground=btn_bg, foreground="black")
    style.configure("TCombobox", fieldbackground=btn_bg, foreground="black")


    # Custom Configs for override
    style.configure("Title.TLabel", font=("Arial", 12, "bold"), foreground=fg_standard, background=bg_standard, padding=(0, 5))

    style.configure( "Sublabel.TLabel", font=("Arial", 10, "bold"), foreground=fg_standard, background=bg_standard, justify="center")

    style.configure( "Subframe.TFrame", background=bg_standard, relief="solid", borderwidth=0)