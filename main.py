# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 12:00:02 2025

@author: MIALON alexis
"""

#%% [1] Import
import mysql.connector
from dbcredentials import db
import tkinter as tk
from enum import Enum
from PIL import Image, ImageTk
from tkinter import filedialog
from collections import deque
#%% [2] OOP

class Mode(Enum):
    UPDATE = 1
    ADD = 2
    DELETE = 3
    
class App:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pokedex")
        self.root.geometry("1300x900")
        self.root.state('zoomed')
        try:
            self.root.iconphoto(False, ImageTk.PhotoImage(Image.open("Pictures/icon.png")))
        except:
            pass
        self.mydb = mysql.connector.connect(
            host=db["host"], 
            user=db["user"],
            password=db["password"],
            database="pokedex"
        )
        self.mycursor = self.mydb.cursor()
        self.id = 0
        
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.last_frame = deque()
        self.frame_dict = dict()
        self.frame_dict["Login"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["Choose"] = tk.Frame(self.container, bg="lightgreen")
        self.frame_dict["Research"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["Contribution"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["SelectContribution"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribPokemonChoose"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribPokemonEvolution"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribPokemonMove"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribPokemonAbility"]= tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribPokemon"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribAbility"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribCategory"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribMove"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribType"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["ContribTiers"] = tk.Frame(self.container, bg="lightblue")
        
        for frame in self.frame_dict.values():
            frame.place(relwidth=1, relheight=1)
            
        #%%% [2.1.1] Login page
        self.login_dict = dict()
        
        try:
            im = Image.open("Pictures/background_login.jpg").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.frame_dict["Background"] = tk.Label(self.frame_dict["Login"], image=im)
            self.frame_dict["Background"].image = im
            self.frame_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        
        self.login_dict["Title"] = tk.Label(self.frame_dict["Login"], text="Welcome to the Pokedex", font=("Arial",36, "bold"), fg="black", bg="#FF6347", borderwidth=2, relief="solid")
        self.login_dict["Title"].pack(pady=20)
        
        self.login_dict["Account"] = tk.Label(self.frame_dict["Login"], text="Connect to your account", font=("Arial", 16, "bold"), fg="black", bg="lightgreen", borderwidth=2, relief="solid")
        self.login_dict["Account"].place(relx=0.77, rely=0.3, anchor="center")
        self.login_dict["NewAccount"] = tk.Label(self.frame_dict["Login"], text="Create your account", font=("Arial", 16, "bold"), fg="black", bg="white", borderwidth=2, relief="solid")
        self.login_dict["NewAccount"].place(relx=0.22, rely=0.3, anchor="center")
        
        self.login_dict["Connection"] = tk.Button(self.frame_dict["Login"], text="Connection", bg="lightgreen", command=self.connection)
        self.login_dict["Connection"].place(relx=0.72, rely=0.75, relwidth=0.1, relheight=0.04)
        self.login_dict["Creation"] = tk.Button(self.frame_dict["Login"], text="Creation", bg="white", command=self.creation_account)
        self.login_dict["Creation"].place(relx=0.17, rely=0.75, relwidth=0.1, relheight=0.04)
        
        
        self.login_dict["Login"] = tk.Entry(self.frame_dict["Login"], width=35, fg="gray", bg="lightgreen")
        self.login_dict["Login"].place(relx=0.72, rely=0.6, relwidth=0.1, relheight=0.04)
        self.login_dict["Login"].insert(0, "Enter your login")
        self.login_dict["Login"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.login_dict["Login"],"Enter your login", False))
        self.login_dict["Login"].bind("<FocusOut>", lambda event: self.clear_entry(event, self.login_dict["Login"],"Enter your login"))
        
        self.login_dict["Password"] = tk.Entry(self.frame_dict["Login"], width=35, fg="gray", bg="lightgreen")
        self.login_dict["Password"].place(relx=0.72, rely=0.65, relwidth=0.1, relheight=0.04)
        self.login_dict["Password"].insert(0, "Enter your password")
        self.login_dict["Password"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.login_dict["Password"],"Enter your password", True))
        self.login_dict["Password"].bind("<FocusOut>", lambda event: self.clear_entry(event, self.login_dict["Password"],"Enter your password"))
        
        self.login_dict["LoginNew"] = tk.Entry(self.frame_dict["Login"], width=35, fg="gray")
        self.login_dict["LoginNew"].place(relx=0.17, rely=0.6, relwidth=0.1, relheight=0.04)
        self.login_dict["LoginNew"].insert(0, "Enter your login")
        self.login_dict["LoginNew"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.login_dict["LoginNew"],"Enter your login", False))
        self.login_dict["LoginNew"].bind("<FocusOut>", lambda event: self.clear_entry(event, self.login_dict["LoginNew"],"Enter your login"))
        
        self.login_dict["PasswordNew"] = tk.Entry(self.frame_dict["Login"], width=35, fg="gray")
        self.login_dict["PasswordNew"].place(relx=0.17, rely=0.65, relwidth=0.1, relheight=0.04)
        self.login_dict["PasswordNew"].insert(0, "Enter your password")
        self.login_dict["PasswordNew"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.login_dict["PasswordNew"],"Enter your password", True))
        self.login_dict["PasswordNew"].bind("<FocusOut>", lambda event: self.clear_entry(event, self.login_dict["PasswordNew"],"Enter your password"))
        
        self.login_dict["PasswordNew2"] = tk.Entry(self.frame_dict["Login"], width=35, fg="gray")
        self.login_dict["PasswordNew2"].place(relx=0.17, rely=0.70, relwidth=0.1, relheight=0.04)
        self.login_dict["PasswordNew2"].insert(0, "Confirm your password")
        self.login_dict["PasswordNew2"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.login_dict["PasswordNew2"],"Confirm your password", True))
        self.login_dict["PasswordNew2"].bind("<FocusOut>", lambda event: self.clear_entry(event, self.login_dict["PasswordNew2"],"Confirm your password"))
        
        
        #%%% [2.1.2] Choose page
        self.choose_dict = dict()
        
        
        try:
            im = Image.open("Pictures/choose.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.frame_dict["Background"] = tk.Label(self.frame_dict["Choose"], image=im)
            self.frame_dict["Background"].image = im
            self.frame_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        
        self.choose_dict["Title"] = tk.Label(self.frame_dict["Choose"], text="Choose your mode", font=("Arial",36, "bold"), fg="black", bg="lightgreen", borderwidth=2, relief="solid")
        self.choose_dict["Title"].pack(pady=20)

        self.choose_dict["Research"] = tk.Button(self.frame_dict["Choose"], text="Research", compound="top", width=20, height=1, bg="lightblue", command= lambda: self.change_frame(self.frame_dict["Choose"], self.frame_dict["Research"]))
        self.choose_dict["Research"].place(relx=0.75, rely=0.9, anchor="center")
        self.choose_dict["Contribute"] = tk.Button(self.frame_dict["Choose"], text="Contribution", compound="top", width=20, height=1, bg="#dd7b40", command= lambda: self.change_frame(self.frame_dict["Choose"], self.frame_dict["Contribution"]))
        self.choose_dict["Contribute"].place(relx=0.25, rely=0.9, anchor="center")
        self.choose_dict["Deconnection"] = tk.Button(self.frame_dict["Choose"], text="Deconnection", compound="top", bg="#FF6347", command=self.return_back)
        self.choose_dict["Deconnection"].place(relx=0.95, rely=0.05, anchor="center")
        
        
        #%%% [2.1.3] Contribute page
        self.contribute_dict = dict()
        
        self.contribute_dict["Title"] = tk.Label(self.frame_dict["Contribution"], text="Choose your type of contribution", font=("Arial, 16"))
        self.contribute_dict["Title"].pack(pady=20)
        
        self.contribute_dict["Update"] = tk.Button(self.frame_dict["Contribution"], text="Update", compound="top", command= lambda: self.selection_mode(Mode.UPDATE))
        self.contribute_dict["Update"].place(relx=0.33, rely=0.33, anchor="center")
        
        self.contribute_dict["Add"] = tk.Button(self.frame_dict["Contribution"], text="Create", compound="top", command= lambda: self.selection_mode(Mode.ADD))
        self.contribute_dict["Add"].place(relx=0.66, rely=0.33, anchor="center")
        
        self.contribute_dict["Delete"] = tk.Button(self.frame_dict["Contribution"], text="Delete", compound="top", command= lambda: self.selection_mode(Mode.DELETE))
        self.contribute_dict["Delete"].place(relx=0.5, rely=0.66, anchor="center")
        
        self.mode = 0
        self.contribute_dict["Deconnection"] = tk.Button(self.frame_dict["Contribution"], text="Return", compound="top", command=self.return_back)
        self.contribute_dict["Deconnection"].place(relx=0.5, rely=0.9, anchor="center")
        
        #%%% [2.1.4] Select Contribution
        
        self.select_contribute_dict = dict()
        
        self.category_contribute_dict = dict()
        self.type_contribute_dict = dict()
        self.tier_contribute_dict = dict()
        self.ability_contribute_dict = dict()
        
        self.select_contribute_dict["Title"] = tk.Label(self.frame_dict["SelectContribution"], text="Choose your field of contribution", font=("Arial, 16"))
        self.select_contribute_dict["Title"].pack(pady=20)
        
        self.select_contribute_dict["Pokemon"] = tk.Button(self.frame_dict["SelectContribution"], text="Pokemon", compound="top", command= lambda: self.change_frame(self.frame_dict["SelectContribution"], self.frame_dict["ContribPokemonChoose"]))
        self.select_contribute_dict["Pokemon"].place(relx=0.25, rely=0.33, anchor="center")
        
        self.select_contribute_dict["Abilities"] = tk.Button(self.frame_dict["SelectContribution"], text="Abilities", compound="top", command= lambda: self.change_frame_binary(self.frame_dict["ContribAbility"], self.ability_contribute_dict, "Ability", desc=True))
        self.select_contribute_dict["Abilities"].place(relx=0.5, rely=0.33, anchor="center")
        
        self.select_contribute_dict["Categories"] = tk.Button(self.frame_dict["SelectContribution"], text="Attack categories", compound="top", command= lambda: self.change_frame_binary(self.frame_dict["ContribCategory"], self.category_contribute_dict, "Category"))
        self.select_contribute_dict["Categories"].place(relx=0.75, rely=0.33, anchor="center")
        
        self.select_contribute_dict["Moves"] = tk.Button(self.frame_dict["SelectContribution"], text="Moves", compound="top", command= lambda: self.change_frame_move())
        self.select_contribute_dict["Moves"].place(relx=0.25, rely=0.66, anchor="center")
        
        self.select_contribute_dict["Types"] = tk.Button(self.frame_dict["SelectContribution"], text="Types", compound="top", command= lambda: self.change_frame_binary(self.frame_dict["ContribType"], self.type_contribute_dict, "Type"))
        self.select_contribute_dict["Types"].place(relx=0.5, rely=0.66, anchor="center")
        
        self.select_contribute_dict["Tiers"] = tk.Button(self.frame_dict["SelectContribution"], text="Tiers", compound="top", command= lambda: self.change_frame_binary(self.frame_dict["ContribTiers"], self.tier_contribute_dict, "Tier"))
        self.select_contribute_dict["Tiers"].place(relx=0.75, rely=0.66, anchor="center")
        
        self.select_contribute_dict["Deconnection"] = tk.Button(self.frame_dict["SelectContribution"], text="Return", compound="top", command=self.return_back)
        self.select_contribute_dict["Deconnection"].place(relx=0.5, rely=0.9, anchor="center")
        
        self.create_binary(self.category_contribute_dict, self.frame_dict["ContribCategory"], "Category", "Categories")
        self.create_binary(self.type_contribute_dict, self.frame_dict["ContribType"], "Type", "Types")
        self.create_binary(self.tier_contribute_dict, self.frame_dict["ContribTiers"], "Tier", "Tiers")
        self.create_binary(self.ability_contribute_dict, self.frame_dict["ContribAbility"], "Ability", "Abilities", description=True)
        
        
        #%%% [2.1.4]
        self.pokemon_select_contribute_dict = dict()
        self.pokemon_select_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribPokemonChoose"], text="Choose the type of modification", font=("Arial, 16"))
        self.pokemon_select_contribute_dict["Title"].pack(pady=20)
        
        self.pokemon_select_contribute_dict["Pokemon"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Pokemon", compound="top", command=self.change_frame_pokemon_pokemon)
        self.pokemon_select_contribute_dict["Pokemon"].place(relx=0.25, rely=0.33, anchor="center")
        
        self.pokemon_select_contribute_dict["Moves"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Pokemon moves", compound="top", command= lambda: self.change_frame(self.frame_dict["ContribPokemonChoose"], self.frame_dict["ContribPokemonMove"]))
        self.pokemon_select_contribute_dict["Moves"].place(relx=0.75, rely=0.33, anchor="center")
        
        self.pokemon_select_contribute_dict["Evolutions"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Pokemon evolution", compound="top", command= lambda: self.change_frame(self.frame_dict["ContribPokemonChoose"], self.frame_dict["ContribPokemonEvolution"]))
        self.pokemon_select_contribute_dict["Evolutions"].place(relx=0.25, rely=0.66, anchor="center")
        
        self.pokemon_select_contribute_dict["Abilities"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Pokemon abilities", compound="top", command= lambda: self.change_frame(self.frame_dict["ContribPokemonChoose"], self.frame_dict["ContribPokemonAbility"]))
        self.pokemon_select_contribute_dict["Abilities"].place(relx=0.75, rely=0.66, anchor="center")
        
        self.pokemon_select_contribute_dict["Deconnection"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Return", compound="top", command=self.return_back)
        self.pokemon_select_contribute_dict["Deconnection"].place(relx=0.5, rely=0.9, anchor="center")
        #%%% [2.1.4.1] Pokemon change
        
        self.pokemon_contribute_dict = dict()

        self.pokemon_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribPokemon"], text=self.title_contribute("Pokemon"), font=("Arial, 16"))
        self.pokemon_contribute_dict["Title"].pack(pady=20)
        
        self.pokemon_contribute_dict["Select"] = self.get_binary("Pokemons", True)
        self.pokemon_contribute_dict["Select"].insert(0, "None")
        
        self.pokemon_contribute_dict["SelectUse"] = self.get_binary("Pokemons", False)
        self.pokemon_contribute_dict["SelectUse"].insert(0, "None")
        #%%% [2.1.4.2]
        
        self.pokemon_add = dict()
        
        self.pokemon_add["NID"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_add["NID"].place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_add["NID"].insert(0, "Enter the national id")
        self.pokemon_add["NID"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.pokemon_add["NID"],"Enter the national id", False))
        self.pokemon_add["NID"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.pokemon_add["NID"],"Enter the national id"))
        
        self.pokemon_add["Name"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_add["Name"].place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Name"].insert(0, "Enter the name")
        self.pokemon_add["Name"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.pokemon_add["Name"],"Enter the name", False))
        self.pokemon_add["Name"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.pokemon_add["Name"],"Enter the name"))
        
        
        self.pokemon_add["ImageLabel"] = tk.Label(self.frame_dict["ContribPokemon"], text="Type 1")
        self.pokemon_add["ImageLabel"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Image"] = tk.Button(self.frame_dict["ContribPokemon"], text="Image selection", compound="top", command=lambda: self.get_image_path(self.pokemon_add["ImageLabel"], self.pokemon_add["Image"]))
        self.pokemon_add["Image"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["SelectType1"] =  tk.StringVar()
        self.pokemon_add["SelectType2"] =  tk.StringVar()
        self.pokemon_add["SelectTier"] =  tk.StringVar()
        
        
        
        self.pokemon_add["Type1Label"] = tk.Label(self.frame_dict["ContribPokemon"], text="Type 1")
        self.pokemon_add["Type1Label"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType1"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_add["Type1Label"].config(text=x))
        self.pokemon_add["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Type2Label"] = tk.Label(self.frame_dict["ContribPokemon"], text="Type 2")
        self.pokemon_add["Type2Label"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType2"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_add["Type2Label"].config(text=x))
        self.pokemon_add["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        

        self.pokemon_add["TierLabel"] = tk.Label(self.frame_dict["ContribPokemon"], text="Tier")
        self.pokemon_add["TierLabel"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectTier"], *self.tier_contribute_dict["Select"], command=lambda x: self.pokemon_add["TierLabel"].config(text=x))
        self.pokemon_add["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["HP"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_add["HP"].place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_add["HP"].insert(0, "Enter the HP")
        self.pokemon_add["HP"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.pokemon_add["HP"],"Enter the HP", False))
        self.pokemon_add["HP"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.pokemon_add["HP"],"Enter the HP"))
        
        self.pokemon_add["Attack"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_add["Attack"].place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Attack"].insert(0, "Enter the attack")
        self.pokemon_add["Attack"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.pokemon_add["Attack"],"Enter the attack", False))
        self.pokemon_add["Attack"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.pokemon_add["Attack"],"Enter the attack"))
        
        self.pokemon_add["Defense"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_add["Defense"].place(relx=0.6, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Defense"].insert(0, "Enter the defense")
        self.pokemon_add["Defense"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.pokemon_add["Defense"],"Enter the defense", False))
        self.pokemon_add["Defense"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.pokemon_add["Defense"],"Enter the defense"))
        
        self.pokemon_add["Speed"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_add["Speed"].place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Speed"].insert(0, "Enter the speed")
        self.pokemon_add["Speed"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.pokemon_add["Speed"],"Enter the speed", False))
        self.pokemon_add["Speed"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.pokemon_add["Speed"],"Enter the speed"))
        
        self.pokemon_add["SpAt"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_add["SpAt"].place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_add["SpAt"].insert(0, "Enter the special attack")
        self.pokemon_add["SpAt"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.pokemon_add["SpAt"],"Enter the special attack", False))
        self.pokemon_add["SpAt"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.pokemon_add["SpAt"],"Enter the special attack"))
        
        self.pokemon_add["SpDef"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_add["SpDef"].place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_add["SpDef"].insert(0, "Enter the special defense")
        self.pokemon_add["SpDef"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.pokemon_add["SpDef"],"Enter the special defense", False))
        self.pokemon_add["SpDef"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.pokemon_add["SpDef"],"Enter the special defense"))
        
        
        self.pokemon_add["Create"] = tk.Button(self.frame_dict["ContribPokemon"], text="Create", command=self.create_pokemon)
        self.pokemon_add["Create"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        self.pokemon_contribute_dict["Deconnection"] = tk.Button(self.frame_dict["ContribPokemon"], text="Return", compound="top", command=self.return_back)
        self.pokemon_contribute_dict["Deconnection"].place(relx=0.9, rely=0.9, anchor="center")
        
        self.pokemon_delete = dict()
        self.pokemon_delete["SelectPokemon"] = tk.StringVar()
        self.pokemon_delete["ChooseLabel"] = tk.Label(self.frame_dict["ContribPokemon"], text="Pokemon")
        self.pokemon_delete["ChooseLabel"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_delete["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_delete["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"], command=lambda x: self.pokemon_delete["ChooseLabel"].config(text=x))
        self.pokemon_delete["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_delete["Delete"] = tk.Button(self.frame_dict["ContribPokemon"], text="Delete", command=self.delete_pokemon)
        self.pokemon_delete["Delete"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update = dict()
        self.pokemon_update["SelectPokemon"] = tk.StringVar()
        self.pokemon_update["ChooseLabel"] = tk.Label(self.frame_dict["ContribPokemon"], text="Pokemon")
        self.pokemon_update["ChooseLabel"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"], command=lambda x: self.pokemon_update["ChooseLabel"].config(text=x))
        self.pokemon_update["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        
        self.pokemon_update["NID"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["NID"].place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_update["NID"].insert(0, "Enter the national id")
        self.pokemon_update["NID"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["NID"],"Enter the national id", self.pokemon_update["Choose"], "SELECT nid FROM Pokemons WHERE name=%s"))
        self.pokemon_update["NID"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["NID"],"Enter the national id", self.pokemon_update["Choose"], "SELECT nid FROM Pokemons WHERE name=%s"))
        
        self.pokemon_update["Name"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["Name"].place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Name"].insert(0, "Enter the name")
        self.pokemon_update["Name"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["Name"],"Enter the name", self.pokemon_update["Choose"], "SELECT name FROM Pokemons WHERE name=%s"))
        self.pokemon_update["Name"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["Name"],"Enter the name", self.pokemon_update["Choose"], "SELECT name FROM Pokemons WHERE name=%s"))
        
        
        self.pokemon_update["ImageLabel"] = tk.Label(self.frame_dict["ContribPokemon"], text="Type 1")
        self.pokemon_update["ImageLabel"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Image"] = tk.Button(self.frame_dict["ContribPokemon"], text="Image selection", compound="top", command=lambda: self.get_image_path(self.pokemon_update["ImageLabel"], self.pokemon_update["Image"]))
        self.pokemon_update["Image"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["SelectType1"] =  tk.StringVar()
        self.pokemon_update["SelectType2"] =  tk.StringVar()
        self.pokemon_update["SelectTier"] =  tk.StringVar()
        
        
        
        self.pokemon_update["Type1Label"] = tk.Label(self.frame_dict["ContribPokemon"], text="Type 1")
        self.pokemon_update["Type1Label"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType1"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_update["Type1Label"].config(text=x))
        self.pokemon_update["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Type2Label"] = tk.Label(self.frame_dict["ContribPokemon"], text="Type 2")
        self.pokemon_update["Type2Label"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType2"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_update["Type2Label"].config(text=x))
        self.pokemon_update["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        

        self.pokemon_update["TierLabel"] = tk.Label(self.frame_dict["ContribPokemon"], text="Tier")
        self.pokemon_update["TierLabel"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectTier"], *self.tier_contribute_dict["Select"], command=lambda x: self.pokemon_update["TierLabel"].config(text=x))
        self.pokemon_update["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["HP"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["HP"].place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_update["HP"].insert(0, "Enter the HP")
        self.pokemon_update["HP"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["HP"],"Enter the HP", self.pokemon_update["Choose"], "SELECT hp FROM Pokemons WHERE name=%s"))
        self.pokemon_update["HP"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["HP"],"Enter the HP", self.pokemon_update["Choose"], "SELECT hp FROM Pokemons WHERE name=%s"))
        
        self.pokemon_update["Attack"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["Attack"].place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Attack"].insert(0, "Enter the attack")
        self.pokemon_update["Attack"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["Attack"],"Enter the attack", self.pokemon_update["Choose"], "SELECT attack FROM Pokemons WHERE name=%s"))
        self.pokemon_update["Attack"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["Attack"],"Enter the attack", self.pokemon_update["Choose"], "SELECT attack FROM Pokemons WHERE name=%s"))
        
        self.pokemon_update["Defense"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["Defense"].place(relx=0.6, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Defense"].insert(0, "Enter the defense")
        self.pokemon_update["Defense"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["Defense"],"Enter the defense", self.pokemon_update["Choose"], "SELECT defense FROM Pokemons WHERE name=%s"))
        self.pokemon_update["Defense"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["Defense"],"Enter the defense", self.pokemon_update["Choose"], "SELECT defense FROM Pokemons WHERE name=%s"))
        
        self.pokemon_update["Speed"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["Speed"].place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Speed"].insert(0, "Enter the speed")
        self.pokemon_update["Speed"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["Speed"],"Enter the speed", self.pokemon_update["Choose"], "SELECT speed FROM Pokemons WHERE name=%s"))
        self.pokemon_update["Speed"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["Speed"],"Enter the speed", self.pokemon_update["Choose"], "SELECT speed FROM Pokemons WHERE name=%s"))
        
        self.pokemon_update["SpAt"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["SpAt"].place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_update["SpAt"].insert(0, "Enter the special attack")
        self.pokemon_update["SpAt"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["SpAt"],"Enter the special attack", self.pokemon_update["Choose"], "SELECT sp_def FROM Pokemons WHERE name=%s"))
        self.pokemon_update["SpAt"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["SpAt"],"Enter the special attack", self.pokemon_update["Choose"], "SELECT sp_def FROM Pokemons WHERE name=%s"))
        
        self.pokemon_update["SpDef"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["SpDef"].place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_update["SpDef"].insert(0, "Enter the special defense")
        self.pokemon_update["SpDef"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["SpDef"],"Enter the special defense", self.pokemon_update["Choose"], "SELECT sp_def FROM Pokemons WHERE name=%s"))
        self.pokemon_update["SpDef"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["SpDef"],"Enter the special defense", self.pokemon_update["Choose"], "SELECT sp_def FROM Pokemons WHERE name=%s"))
        
        
        self.pokemon_update["Update"] = tk.Button(self.frame_dict["ContribPokemon"], text="Update", command=self.update_pokemon)
        self.pokemon_update["Update"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        #%%% [2.1.4.2] Move change

        self.move_contribute_dict = dict()

        self.move_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribMove"], text=self.title_contribute("Move"), font=("Arial, 16"))
        self.move_contribute_dict["Title"].pack(pady=20)
        
        
        self.move_add = dict()
        self.move_contribute_dict["Add"] = self.move_add
        self.move_delete = dict()
        self.move_contribute_dict["Delete"] = self.move_delete
        self.move_update = dict()
        self.move_contribute_dict["Update"] = self.move_update
        self.move_contribute_dict["Select"] = self.get_binary("Moves", True)
        self.move_contribute_dict["Select"].insert(0, "None")
        self.move_contribute_dict["SelectUse"] = self.get_binary("Moves", False)
        self.move_contribute_dict["SelectUse"].insert(0, "None")
        
        self.move_add["Name"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_add["Name"].place(relx=0.2, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_add["Name"].insert(0, "Enter a name")
        self.move_add["Name"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.move_add["Name"],"Enter a name", False))
        self.move_add["Name"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.move_add["Name"],"Enter a name"))

        self.move_add["SelectType"] =  tk.StringVar()
        self.move_add["TypeLabel"] = tk.Label(self.frame_dict["ContribMove"], text="Type")
        self.move_add["TypeLabel"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_add["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectType"], *self.type_contribute_dict["Select"], command=lambda x: self.move_add["TypeLabel"].config(text=x))
        self.move_add["Type"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_add["SelectCategory"] =  tk.StringVar()
        self.move_add["CategoryLabel"] = tk.Label(self.frame_dict["ContribMove"], text="Category")
        self.move_add["CategoryLabel"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_add["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectCategory"], *self.category_contribute_dict["Select"], command=lambda x: self.move_add["CategoryLabel"].config(text=x))
        self.move_add["Category"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_add["Power"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_add["Power"].place(relx=0.8, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_add["Power"].insert(0, "Enter the power")
        self.move_add["Power"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.move_add["Power"],"Enter the power", False))
        self.move_add["Power"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.move_add["Power"],"Enter the power"))
        
        self.move_add["PP"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_add["PP"].place(relx=0.25, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_add["PP"].insert(0, "Enter the PP")
        self.move_add["PP"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.move_add["PP"],"Enter the PP", False))
        self.move_add["PP"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.move_add["PP"],"Enter the PP"))
        
        self.move_add["Priority"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_add["Priority"].place(relx=0.5, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_add["Priority"].insert(0, "Enter the priority")
        self.move_add["Priority"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.move_add["Priority"],"Enter the priority", False))
        self.move_add["Priority"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.move_add["Priority"],"Enter the priority"))
        
        self.move_add["Description"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_add["Description"].place(relx=0.75, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_add["Description"].insert(0, "Enter a description")
        self.move_add["Description"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.move_add["Description"],"Enter a description", False))
        self.move_add["Description"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.move_add["Description"],"Enter a description"))
        
        self.move_add["Create"] = tk.Button(self.frame_dict["ContribMove"], text="Create", command=self.create_move)
        self.move_add["Create"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        self.move_delete["SelectMove"] =  tk.StringVar()
        self.move_delete["MoveLabel"] = tk.Label(self.frame_dict["ContribMove"], text="Move")
        self.move_delete["MoveLabel"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        self.move_delete["Move"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_delete["SelectMove"], *self.move_contribute_dict["SelectUse"], command=lambda x: self.move_delete["MoveLabel"].config(text=x))
        self.move_delete["Move"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.move_delete["Delete"] = tk.Button(self.frame_dict["ContribMove"], text="Delete", command=self.delete_move)
        self.move_delete["Delete"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        self.move_update["Name"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["Name"].place(relx=0.2, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_update["Name"].insert(0, "Enter a name")
        self.move_update["Name"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["Name"], "Enter a name", self.move_delete["Move"], "SELECT name FROM Moves WHERE name=%s"))
        self.move_update["Name"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["Name"],"Enter a name", self.move_delete["Move"], "SELECT name FROM Moves WHERE name=%s"))

        self.move_update["SelectType"] =  tk.StringVar()
        self.move_update["TypeLabel"] = tk.Label(self.frame_dict["ContribMove"], text="Type")
        self.move_update["TypeLabel"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_update["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectType"], *self.type_contribute_dict["Select"], command=lambda x: self.move_delete["TypeLabel"].config(text=x))
        self.move_update["Type"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_update["SelectCategory"] =  tk.StringVar()
        self.move_update["CategoryLabel"] = tk.Label(self.frame_dict["ContribMove"], text="Category")
        self.move_update["CategoryLabel"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_update["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectCategory"], *self.category_contribute_dict["Select"], command=lambda x: self.move_delete["CategoryLabel"].config(text=x))
        self.move_update["Category"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_update["Power"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["Power"].place(relx=0.8, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_update["Power"].insert(0, "Enter the power")
        self.move_update["Power"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["Power"],"Enter the power", self.move_delete["Move"], "SELECT power FROM Moves WHERE name=%s"))
        self.move_update["Power"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["Power"],"Enter the power", self.move_delete["Move"], "SELECT power FROM Moves WHERE name=%s"))
        
        self.move_update["PP"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["PP"].place(relx=0.25, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_update["PP"].insert(0, "Enter the PP")
        self.move_update["PP"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["PP"],"Enter the PP", self.move_delete["Move"], "SELECT pp FROM Moves WHERE name=%s"))
        self.move_update["PP"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["PP"],"Enter the PP", self.move_delete["Move"], "SELECT pp FROM Moves WHERE name=%s"))
        
        self.move_update["Priority"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["Priority"].place(relx=0.5, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_update["Priority"].insert(0, "Enter the priority")
        self.move_update["Priority"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["Priority"],"Enter the priority", self.move_delete["Move"], "SELECT priority FROM Moves WHERE name=%s"))
        self.move_update["Priority"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["Priority"],"Enter the priority", self.move_delete["Move"], "SELECT priority FROM Moves WHERE name=%s"))
        
        self.move_update["Description"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["Description"].place(relx=0.75, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_update["Description"].insert(0, "Enter a description")
        self.move_update["Description"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["Description"],"Enter a description", self.move_delete["Move"], "SELECT description FROM Moves WHERE name=%s"))
        self.move_update["Description"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["Description"],"Enter a description", self.move_delete["Move"], "SELECT description FROM Moves WHERE name=%s"))
        
        self.move_update["Update"] = tk.Button(self.frame_dict["ContribMove"], text="Update", command=lambda: self.update_move(self.move_delete["Move"]))
        self.move_update["Update"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        self.move_update["Deconnection"] = tk.Button(self.frame_dict["ContribMove"], text="Return", compound="top", command=self.return_back)
        self.move_update["Deconnection"].place(relx=0.9, rely=0.9, anchor="center")
        
        
    def get_image_path(self, label, button):
        path = filedialog.askopenfilename(
            title="Select the design of your pokemon",
            filetypes=[("Images Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            label.config(text=path)
            button.config(text=path)
        else:
            label.config(text="")
            
    def clear_entry(self, event, entry, text):
        if entry.get() == "":
            entry.delete(0, tk.END)
            entry.insert(0, text)
            entry.config(fg="gray", show="")
    
    def fill_entry(self, event, entry, text, hide):
        if entry.get() == text:
            entry.delete(0, tk.END)
            if hide:
                entry.config(fg="black", show="*")
            else:
                entry.config(fg="black")
                
    def clear_entry_value_by_name(self, event, entry, text, origin, sql):
        param = (origin.cget("text"),)
    
        self.mycursor.execute(sql, param)
        val = self.mycursor.fetchall()
        if len(val) > 0 and entry.get() == "":
            entry.delete(0, tk.END)
            entry.insert(0, str(val[0][0]))
            entry.config(fg="gray", show="")
    
    def fill_entry_value_by_name(self, event, entry, text, origin, sql):
        param = (origin.cget("text"),)
        
        self.mycursor.execute(sql, param)
        val = self.mycursor.fetchall()
        if entry.get() == text and len(val) > 0:
            entry.delete(0, tk.END)
            entry.insert(0, str(val[0][0]))
            entry.config(fg="black")
                
                
    #%% [2.3] General Method
    
    def change_frame(self, origin, frame):
        self.last_frame.append(origin)
        frame.tkraise()
    
    def return_back(self):
        if len(self.last_frame) > 0 and (frame := self.last_frame.pop()) != None:
            frame.tkraise()
        
    def background(self, event, frame, frame_dict, filename):
        im = Image.open(filename).convert("RGB")
        im = im.resize((event.width, event.height), Image.Resampling.LANCZOS)
        
        im = ImageTk.PhotoImage(im)
        
        frame_dict["Background"] = tk.Label(frame, image=im)
        frame_dict["Background"].image = im
        frame_dict["Background"].place(relwidth=1, relheight=1)
    
    def creation_account(self):
        sql = "SELECT id FROM Connections WHERE login=%s"
        param1 = self.login_dict["LoginNew"].get()
        param2 = self.login_dict["PasswordNew"].get()
        param3 = self.login_dict["PasswordNew2"].get()
        if param1 and param2 and param2 == param3:
            params = (param1,)
            self.mycursor.execute(sql, params)
            result = self.mycursor.fetchall()
            if len(result) == 0:
                params = (param1,param2)
                sql = "INSERT INTO Connections (login,password) VALUES (%s,%s)"
                self.mycursor.execute(sql, params)
                self.mydb.commit()
                self.login_dict["Creation"].config(text="Successfully created")
            else:
                self.login_dict["Creation"].config(text="Login already used")
        else:
            self.login_dict["Creation"].config(text="Information issue")
        self.login_dict["LoginNew"].delete(0, tk.END)
        self.login_dict["LoginNew"].insert(0, "Enter your login")
        self.login_dict["LoginNew"].config(fg="gray")
        
        self.login_dict["PasswordNew"].delete(0, tk.END)
        self.login_dict["PasswordNew"].insert(0, "Enter your password")
        self.login_dict["PasswordNew"].config(fg="gray",show="")
        
        self.login_dict["PasswordNew2"].delete(0, tk.END)
        self.login_dict["PasswordNew2"].insert(0, "Confirm your password")
        self.login_dict["PasswordNew2"].config(fg="gray", show="")
    
    def connection(self):
        sql = "SELECT id FROM Connections WHERE login=%s AND password=%s"
        param1 = self.login_dict["Login"].get()
        param2 = self.login_dict["Password"].get()
        if param1 and param2:
            params = (param1,param2)
            self.mycursor.execute(sql, params)
            result = self.mycursor.fetchall()
            if len(result) > 0:
                self.id = result[0][0]
                self.change_frame(self.frame_dict["Login"], self.frame_dict["Choose"])
            else:
                self.login_dict["Connection"].config(text="Information issue")
        else:
            self.login_dict["Connection"].config(text="Missing information")
        self.login_dict["Login"].delete(0, tk.END)
        self.login_dict["Login"].insert(0, "Enter your login")
        self.login_dict["Login"].config(fg="gray")
        
        self.login_dict["Password"].delete(0, tk.END)
        self.login_dict["Password"].insert(0, "Enter your password")
        self.login_dict["Password"].config(fg="gray", show="")
        
        self.update_button()    
        
    def selection_mode(self, mod):
        self.mode = mod
        self.pokemon_contribute_dict["Title"].config(text=self.title_contribute("Pokemon"))
        self.ability_contribute_dict["Title"].config(text=self.title_contribute("Ability"))
        self.move_contribute_dict["Title"].config(text=self.title_contribute("Move"))
        self.category_contribute_dict["Title"].config(text=self.title_contribute("Category"))
        self.type_contribute_dict["Title"].config(text=self.title_contribute("Type"))
        self.tier_contribute_dict["Title"].config(text=self.title_contribute("Tier"))
        self.change_frame(self.frame_dict["Contribution"], self.frame_dict["SelectContribution"])
        
    def title_contribute(self, category):
        if self.mode == Mode.UPDATE:
            return category + ": update"
        elif self.mode == Mode.ADD:
            return category + ": creation"
        elif self.mode == Mode.DELETE:
            return category + ": delete" 
        else:
            return category + ": unknown mode"
        
    def update_button(self, desc=False):
        
        i = 0
        name = [("Tier", "Tiers", self.frame_dict["ContribTiers"], False), 
                ("Type", "Types", self.frame_dict["ContribType"], False), 
                ("Category", "Categories", self.frame_dict["ContribCategory"], False),
                ("Ability", "Abilities", self.frame_dict["ContribAbility"], True)
        ]
        dictionaries = [self.tier_contribute_dict,
                        self.type_contribute_dict,
                        self.category_contribute_dict,
                        self.ability_contribute_dict,
        ]
        
        self.move_contribute_dict["Select"] = self.get_binary("Moves", True)
        self.move_contribute_dict["Select"].insert(0, "None")
        self.move_contribute_dict["SelectUse"] = self.get_binary("Moves", False)
        self.move_contribute_dict["SelectUse"].insert(0, "None")
        
        self.pokemon_contribute_dict["Select"] = self.get_binary("Pokemons", True)
        self.pokemon_contribute_dict["Select"].insert(0, "None")
        
        self.pokemon_contribute_dict["SelectUse"] = self.get_binary("Pokemons", False)
        self.pokemon_contribute_dict["SelectUse"].insert(0, "None")
        for env in dictionaries:
            
            env["SelectUse"] = self.get_binary(name[i][1], False)
            env["SelectUse"].insert(0, "None")
            env["Select"] = self.get_binary(name[i][1], True)
            env["Select"].insert(0, "None")
            
            
            env["Delete"].destroy()
            env["Delete"] = tk.OptionMenu(name[i][2], env["Select2"], *env["SelectUse"], command=lambda x: env["DeleteLabel"].config(text=x))
            env["Delete"].place(relx=0.5, rely=0.45, relwidth=0.1, relheight=0.04)
            env["Update1"].destroy()
            env["Update1"] = tk.OptionMenu(name[i][2], env["Select1"], *env["SelectUse"], command=lambda x: env["UpdateLabel1"].config(text=x))
            if desc:
                env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
            else:
                env["Update1"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
            self.change_frame_binary(name[i][2], env, name[i][0], change=False, desc=name[i][3])
            i += 1        
        
    def get_binary(self, name, admin):
        sql = "SELECT name FROM " + name +" WHERE id_login=%s"
        if admin:
            sql += " OR id_login=1"
        sql += " ORDER BY name"
        params = (self.id,)
        self.mycursor.execute(sql, params)
        tiers = self.mycursor.fetchall()
       
        return list(tiers)
    
    def create_binary(self, env, frame, name, table_name, description=False):
        sentence = "Enter the " + name.lower() + " name"
        
        env["Title"] = tk.Label(frame, text=self.title_contribute(name), font=("Arial, 16"))
        env["Title"].pack(pady=20)
        env["Deconnection"] = tk.Button(frame, text="Return", compound="top", command=self.return_back)
        env["Deconnection"].place(relx=0.5, rely=0.9, anchor="center")
        env["Add"] =  tk.Entry(frame, width=35, fg="gray")
        if description:
            env["Add"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        else:
            env["Add"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        env["Add"].insert(0, sentence)
        env["Add"].bind("<FocusIn>", lambda event: self.fill_entry(event, env["Add"],sentence, False))
        env["Add"].bind("<FocusOut>",  lambda event: self.clear_entry(event, env["Add"],sentence))
        
        env["Select1"] = tk.StringVar()
        
        env["Select2"] = tk.StringVar()
        env["Select"] = self.get_binary(table_name, True)
        env["Select"].insert(0, "None")
        env["SelectUse"] = self.get_binary(table_name, False)
        env["SelectUse"].insert(0, "None")
       
        env["Select1"].set("None")
        
        env["Select2"].set("None")
        env["UpdateLabel1"] = tk.Label(frame, text="Old " + name.lower())
        if description:
            env["UpdateLabel1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
        else:
            env["UpdateLabel1"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        env["Update1"] = tk.OptionMenu(frame, env["Select1"], *env["SelectUse"], command=lambda x: env["UpdateLabel1"].config(text=x))
        if description:
            env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
        else:
            env["Update1"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        env["Update2"] =  tk.Entry(frame, width=35, fg="gray")
        if description:
            env["Update1"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
        else:
            env["Update2"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        env["Update2"].insert(0, sentence)
        env["Update2"].bind("<FocusIn>", lambda event: self.fill_entry(event, env["Update2"],sentence, False))
        env["Update2"].bind("<FocusOut>",  lambda event: self.clear_entry(event, env["Update2"],sentence))
        
        env["DeleteLabel"] = tk.Label(frame, text=name)
        env["DeleteLabel"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        env["Delete"] = tk.OptionMenu(frame, env["Select2"], *env["SelectUse"], command=lambda x: env["DeleteLabel"].config(text=x))
        env["Delete"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        if description:
            desc = "Enter a description"
            env["Description"] =  tk.Entry(frame, width=35, fg="gray")
            if self.mode == Mode.ADD:
                env["Description"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
            else:
                env["Description"].place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.04)
            env["Description"].insert(0, desc)
            env["Description"].bind("<FocusIn>", lambda event: self.fill_entry(event, env["Description"],desc, False))
            env["Description"].bind("<FocusOut>",  lambda event: self.clear_entry(event, env["Description"],desc))
            
        env["Confirm"] = tk.Button(frame, text="Confirm", command=lambda: self.contribute_binary(name, table_name, env, desc=description))
        env["Confirm"].place(relx=0.45, rely=0.7, relwidth=0.1, relheight=0.04)
        
    def change_frame_binary(self, frame, env, name, change=True, desc=False):
        if self.mode == Mode.ADD:
            if desc:
                env["Description"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Add"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
            else:                
                env["Add"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            env["DeleteLabel"].place_forget()
            env["Delete"].place_forget()
            env["UpdateLabel1"].place_forget()
            env["Update1"].place_forget()
            env["Update2"].place_forget()
        elif self.mode == Mode.DELETE:
            env["DeleteLabel"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            env["Delete"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            env["Add"].place_forget()
            if desc:
                env["Description"].place_forget()
            env["UpdateLabel1"].place_forget()
            env["Update1"].place_forget()
            env["Update2"].place_forget()
        elif self.mode == Mode.UPDATE:
            env["DeleteLabel"].place_forget()
            env["Delete"].place_forget()
            env["Add"].place_forget()
            if desc:
                env["UpdateLabel1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Update2"].place(relx=0.5, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Description"].place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.04)
            else:
                env["UpdateLabel1"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Update1"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Update2"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
        env["Confirm"].config(text="Confirm")
        sentence = "Enter the " + name.lower() + " name"
        env["Add"].delete(0, tk.END)
        env["Add"].insert(0, sentence)
        env["Add"].config(fg="gray")
        
        env["Update2"].delete(0, tk.END)
        env["Update2"].insert(0, sentence)
        env["Update2"].config(fg="gray")
        if desc:
            env["Description"].delete(0, tk.END)
            env["Description"].insert(0, "Enter a description")
            env["Description"].config(fg="gray")
        if change:
            self.change_frame(self.frame_dict["SelectContribution"], frame)
    
    
    
    def contribute_binary(self, name, table_name, env, desc=False):
        sentence = "Enter the " + name.lower() + " name"
        if self.mode == Mode.ADD:
            if desc:
                sql = "INSERT INTO " + table_name + " (name,description,id_login) VALUES (%s,%s,%s)"
                d = env["Description"].get()
                
            else:
                sql = "INSERT INTO " + table_name + " (name,id_login) VALUES (%s,%s)"
            name = env["Add"].get()
            
            if name != "":
                if desc:
                    if d == "Enter a description":
                        d = ""
                    
                    params = (name, d, self.id)
                else:
                    params = (name, self.id)
                self.mycursor.execute(sql, params)
                self.mydb.commit()
                env["Confirm"].config(text="Creation success")
            else:
                env["Confirm"].config(text="Please enter a name")
            env["Add"].delete(0, tk.END)
            env["Add"].insert(0, sentence)
            env["Add"].config(fg="gray")
        elif self.mode == Mode.UPDATE:
            if desc:
                sql = "UPDATE " + table_name + " SET name=%s, description=%s WHERE id=%s"
                d = env["Description"].get()
            else:
                sql = "UPDATE " + table_name + " SET name=%s WHERE id=%s"
            nami = env["Update1"].cget("text")
            nami2 = env["Update2"].get()

            if nami != "None" and ((nami2 != "" and not nami2.startswith("Enter the")) or desc):
                
                sql_type = "SELECT id FROM " + table_name + " WHERE name=%s LIMIT 1"
                self.mycursor.execute(sql_type, (nami,))
                tier = self.mycursor.fetchall()
               
                if len(tier) > 0:
                    if desc:
                        if d == "" or d == "Enter a description":
                            s = "SELECT description FROM " + table_name + " WHERE id=%s"
      
                            self.mycursor.execute(s, (tier[0][0],))
                            d = self.mycursor.fetchall()
                            d = d[0][0]
                           
                        if nami2 == "" or nami2.startswith("Enter the"):
                            nami2 = nami
                        params = (nami2,d, tier[0][0])
                    else:
                        params = (nami2, tier[0][0])

                    self.mycursor.execute(sql, params)
                    self.mydb.commit()
                    env["Confirm"].config(text="Update success")
                else:
                    env["Confirm"].config(text="Please select a good " + name.lower())
            else:
                env["Confirm"].config(text="Please select a good " + name.lower())
            env["Update2"].delete(0, tk.END)
            env["Update2"].insert(0, sentence)
            env["Update2"].config(fg="gray")
        elif self.mode == Mode.DELETE:
            sql = "DELETE FROM Types WHERE id=%s"
            nami = env["Delete"].cget("text")
            if nami != "None":
                sql_type = "SELECT id FROM " +table_name + " WHERE name=%s LIMIT 1"
                self.mycursor.execute(sql_type, (nami,))
                tier = self.mycursor.fetchall()
               
                if len(tier) > 0:
                    
                    self.mycursor.execute(sql, (tier[0][0],))
                    self.mydb.commit()
                    env["Confirm"].config(text="Delete success")
                else:
                    env["Confirm"].config(text="Please select a good " + name.lower())
            else:
                env["Confirm"].config(text="Please select a good " + name.lower())
            
        else:
            pass
        env["Select1"].set("None")
        env["Select2"].set("None")
        env["Select"] = self.get_binary(table_name, True)
        env["SelectUse"] = self.get_binary(table_name, False)
        env["Select"].insert(0,"None")
        env["SelectUse"].insert(0, "None")
        #sleep(1)
        self.update_button()
        
    def create_move(self):
        sql = "INSERT INTO Moves (name,type,category,power,pp,priority,description,id_login) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        name = self.move_add["Name"].get()
        type1 = self.move_add["Type"].cget("text")
        category =  self.move_add["Category"].cget("text")
      
        power = self.move_add["Power"].get()
        pp = self.move_add["PP"].get()
        priority = self.move_add["Priority"].get()
        description = self.move_add["Description"].get()
        if type1 == "None" or category == "None":
            self.move_add["Create"].config(text="Missing values")
        else:
            try:
                power = int(power)
                pp = int(pp)
                priority = int(priority)
                
                if description == "" or description == 'Enter a description':
                    description = ""
                if power < 0 or pp <= 0:
                    self.move_add["Create"].config(text="Power or PP issue")
                else:
                    
                    sql_type = "SELECT id FROM Types WHERE name=%s LIMIT 1"
                    self.mycursor.execute(sql_type, (type1,))
                    type1 = self.mycursor.fetchall()
                    sql_cat = "SELECT id FROM Categories WHERE name=%s LIMIT 1"
                    self.mycursor.execute(sql_cat, (category,))
                    category = self.mycursor.fetchall()
                    if len(type1) > 0 and len(category) > 0:
                        type1 = int(type1[0][0])
                        category = int(category[0][0])
                        params = (name,type1,category,power,pp,priority,description, self.id)    
                        self.mycursor.execute(sql, params)
                        self.mydb.commit()
                        
                        self.move_add["Create"].config(text="Creation success")
            except:
                self.move_add["Create"].config(text="Value issue")
                
        self.move_add["Name"].delete(0, tk.END)
        self.move_add["Name"].insert(0, "Enter a name")
        self.move_add["Name"].config(fg="gray") 
        
        self.move_add["Power"].delete(0, tk.END)
        self.move_add["Power"].insert(0, "Enter the power")
        self.move_add["Power"].config(fg="gray")
        
        self.move_add["PP"].delete(0, tk.END)
        self.move_add["PP"].insert(0, "Enter the PP")
        self.move_add["PP"].config(fg="gray")
        
        self.move_add["Priority"].delete(0, tk.END)
        self.move_add["Priority"].insert(0, "Enter the priority")
        self.move_add["Priority"].config(fg="gray")
        
        self.move_add["Description"].delete(0, tk.END)
        self.move_add["Description"].insert(0, "Enter a description")
        self.move_add["Description"].config(fg="gray")
        
        self.move_add["Type"].destroy()
        self.move_add["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectType"], *self.type_contribute_dict["Select"], command=lambda x: self.move_add["TypeLabel"].config(text=x))
        self.move_add["Type"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_add["Category"].destroy()
        self.move_add["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectCategory"], *self.category_contribute_dict["Select"], command=lambda x: self.move_add["CategoryLabel"].config(text=x))
        self.move_add["Category"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.update_button()
    
    def delete_move(self):
        sql = "DELETE FROM Moves WHERE id=%s"
        
        name = self.move_delete["Move"].cget("text")
        if name == "None":
            self.move_delete["Delete"].config(text="Wrong move")
        else:
            sql_id = "SELECT id FROM Moves WHERE name=%s LIMIT 1"
            self.mycursor.execute(sql_id, (name,))
            id1 = self.mycursor.fetchall()
            if len(id1) > 0:
                self.mycursor.execute(sql, (id1[0][0],))
                self.mydb.commit()
                self.move_delete["Delete"].config(text="Delete success")
            else:
                self.move_delete["Delete"].config(text="Wrong move")
        self.move_delete["Move"].destroy()
        self.move_delete["Move"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_delete["SelectMove"], *self.move_contribute_dict["SelectUse"], command=lambda x: self.move_delete["MoveLabel"].config(text=x))
        self.move_delete["Move"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        self.update_button()
        
    def update_move(self, origin):
        sql = "UPDATE Moves SET name=%s,type=%s,category=%s,power=%s,pp=%s,priority=%s,description=%s  WHERE name=%s"
        name = self.move_update["Name"].get()
        type1 = self.move_update["Type"].cget("text")
        
        category = self.move_update["Category"].cget("text")
        
        power = self.move_update["Power"].get()
        pp = self.move_update["PP"].get()
        priority = self.move_update["Priority"].get()
        description = self.move_update["Description"].get()
        
        if type1 == "None" or category == "None":
            self.move_update["Update"].config(text="Missing values")
        else:
            try:
                power = int(power)
                pp = int(pp)
                priority = int(priority)
                if description == "" or description == 'Enter a description':
                    description = ""
                if power < 0 or pp <= 0:
                    self.move_update["Update"].config(text="Power or PP issue")
                else:
                    sql_type = "SELECT id FROM Types WHERE name=%s LIMIT 1"
                    self.mycursor.execute(sql_type, (type1,))
                    type1 = self.mycursor.fetchall()
                    sql_cat = "SELECT id FROM Categories WHERE name=%s LIMIT 1"
                    self.mycursor.execute(sql_cat, (category,))
                    category = self.mycursor.fetchall()
                    
                    if len(type1) > 0 and len(category) > 0:
                        type1 = int(type1[0][0])
                        category = int(category[0][0])
                        
                        params = (name,type1,category,power,pp,priority,description, origin.cget("text"))
                        
                        self.mycursor.execute(sql, params)
                        self.mydb.commit()
                        self.move_update["Update"].config(text="Update success")
                    else:
                        self.move_update["Update"].config(text="Value issue")
            except:
                self.move_update["Update"].config(text="Value issue")
                
        self.move_update["Name"].delete(0, tk.END)
        self.move_update["Name"].insert(0, "Enter a name")
        self.move_update["Name"].config(fg="gray") 
        
        self.move_update["Power"].delete(0, tk.END)
        self.move_update["Power"].insert(0, "Enter the power")
        self.move_update["Power"].config(fg="gray")
        
        self.move_update["PP"].delete(0, tk.END)
        self.move_update["PP"].insert(0, "Enter the PP")
        self.move_update["PP"].config(fg="gray")
        
        self.move_update["Priority"].delete(0, tk.END)
        self.move_update["Priority"].insert(0, "Enter the priority")
        self.move_update["Priority"].config(fg="gray")
        
        self.move_update["Description"].delete(0, tk.END)
        self.move_update["Description"].insert(0, "Enter a description")
        self.move_update["Description"].config(fg="gray")
        
        self.move_update["Category"].destroy()
        self.move_update["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectCategory"], *self.category_contribute_dict["Select"], command=lambda x: self.move_update["CategoryLabel"].config(text=x))
        self.move_update["Category"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_update["Type"].destroy()
        self.move_update["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectType"], *self.type_contribute_dict["Select"], command=lambda x: self.move_update["TypeLabel"].config(text=x))
        self.move_update["Type"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)
        self.update_button()   
        
    def change_frame_move(self):
        if self.mode == Mode.ADD:
        
            self.move_add["Name"].place(relx=0.2, rely=0.33, relwidth=0.1, relheight=0.04)        
            self.move_add["TypeLabel"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)   
            self.move_add["Type"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)  
            self.move_add["CategoryLabel"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)     
            self.move_add["Category"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)     
            self.move_add["Power"].place(relx=0.8, rely=0.33, relwidth=0.1, relheight=0.04)         
            self.move_add["PP"].place(relx=0.25, rely=0.66, relwidth=0.1, relheight=0.04) 
            self.move_add["Priority"].place(relx=0.5, rely=0.66, relwidth=0.1, relheight=0.04)
            self.move_add["Description"].place(relx=0.75, rely=0.66, relwidth=0.1, relheight=0.04)
            self.move_add["Create"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
            for key in self.move_delete.keys():
                if not isinstance(self.move_delete[key], tk.StringVar):
                    self.move_delete[key].place_forget()
            for key in self.move_update.keys():
                if not isinstance(self.move_update[key], tk.StringVar):
                    self.move_update[key].place_forget()
        elif self.mode == Mode.DELETE:
            self.move_delete["Move"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            self.move_delete["Delete"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)

            for key in self.move_add.keys():
                if not isinstance(self.move_add[key], tk.StringVar):
                    self.move_add[key].place_forget()
            for key in self.move_update.keys():
                if not isinstance(self.move_update[key], tk.StringVar):
                    self.move_update[key].place_forget()
        elif self.mode == Mode.UPDATE:
            self.move_update["Name"].place(relx=0.2, rely=0.33, relwidth=0.1, relheight=0.04)        
            self.move_update["TypeLabel"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)   
            self.move_update["Type"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)  
            self.move_update["CategoryLabel"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)     
            self.move_update["Category"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)     
            self.move_update["Power"].place(relx=0.8, rely=0.33, relwidth=0.1, relheight=0.04)         
            self.move_update["PP"].place(relx=0.25, rely=0.66, relwidth=0.1, relheight=0.04) 
            self.move_update["Priority"].place(relx=0.5, rely=0.66, relwidth=0.1, relheight=0.04)
            self.move_update["Description"].place(relx=0.75, rely=0.66, relwidth=0.1, relheight=0.04)
            self.move_update["Update"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
            self.move_delete["Move"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            self.move_delete["Delete"].place_forget()
            for key in self.move_add.keys():
                if not isinstance(self.move_add[key], tk.StringVar):
                    self.move_add[key].place_forget()
        else:
            pass
        self.change_frame(self.frame_dict["SelectContribution"], self.frame_dict["ContribMove"])
    
    def change_frame_pokemon_pokemon(self):
        
        self.pokemon_update["Speed"].delete(0, tk.END)
        self.pokemon_update["Speed"].insert(0, "Enter the speed")
        self.pokemon_update["Speed"].config(fg="gray")
        
        self.pokemon_update["Type1"].destroy()
        self.pokemon_update["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType1"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_update["Type1Label"].config(text=x))
        self.pokemon_update["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Type2"].destroy()
        self.pokemon_update["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType2"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_update["Type2Label"].config(text=x))
        self.pokemon_update["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Tier"].destroy()
        self.pokemon_update["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectTier"], *self.tier_contribute_dict["Select"], command=lambda x: self.pokemon_update["TierLabel"].config(text=x))
        self.pokemon_update["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Choose"].destroy()
        self.pokemon_update["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"], command=lambda x: self.pokemon_update["ChooseLabel"].config(text=x))
        self.pokemon_update["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_delete["Choose"].destroy()
        self.pokemon_delete["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_delete["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"], command=lambda x: self.pokemon_delete["ChooseLabel"].config(text=x))
        self.pokemon_delete["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Type1"].destroy()
        self.pokemon_add["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType1"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_add["Type1Label"].config(text=x))
        self.pokemon_add["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Type2"].destroy()
        self.pokemon_add["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType2"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_add["Type2Label"].config(text=x))
        self.pokemon_add["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Tier"].destroy()
        self.pokemon_add["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectTier"], *self.tier_contribute_dict["Select"], command=lambda x: self.pokemon_add["TierLabel"].config(text=x))
        self.pokemon_add["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        if self.mode == Mode.ADD:
            
            
            self.pokemon_add["NID"].place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.04)
           
            self.pokemon_add["Name"].place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.04)
            
            self.pokemon_add["ImageLabel"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
            
            self.pokemon_add["Image"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)

            self.pokemon_add["Type1Label"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
           
            self.pokemon_add["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
         
            self.pokemon_add["Type2Label"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
            self.pokemon_add["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)

            self.pokemon_add["TierLabel"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
            
            self.pokemon_add["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
            
            
            self.pokemon_add["HP"].place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.04)
           
            self.pokemon_add["Attack"].place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.04)
            
            self.pokemon_add["Defense"].place(relx=0.6, rely=0.8, relwidth=0.1, relheight=0.04)
            
            self.pokemon_add["Speed"].place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.04)
            
            self.pokemon_add["SpAt"].place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.04)
            
            self.pokemon_add["SpDef"].place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.04)
            
            self.pokemon_add["Create"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
            for key in self.pokemon_update.keys():
                if not isinstance(self.pokemon_update[key], tk.StringVar):
                    self.pokemon_update[key].place_forget()
            for key in self.pokemon_delete.keys():
                if not isinstance(self.pokemon_delete[key], tk.StringVar):
                    self.pokemon_delete[key].place_forget()
        elif self.mode == Mode.DELETE:
            
            self.pokemon_delete["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            self.pokemon_delete["Delete"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
            for key in self.pokemon_add.keys():
                if not isinstance(self.pokemon_add[key], tk.StringVar):
                    self.pokemon_add[key].place_forget()
            for key in self.pokemon_update.keys():
                if not isinstance(self.pokemon_update[key], tk.StringVar):
                    self.pokemon_update[key].place_forget()
        elif self.mode == Mode.UPDATE:
            
            
            self.pokemon_update["ChooseLabel"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
           
            self.pokemon_update["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            
            
            
            self.pokemon_update["NID"].place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["Name"].place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.04)
           
            
            self.pokemon_update["ImageLabel"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
          
            self.pokemon_update["Image"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
            
            
            
            
            
            
            self.pokemon_update["Type1Label"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
            
          
            self.pokemon_update["Type2Label"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
           
            self.pokemon_update["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
            

           
            self.pokemon_update["TierLabel"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
            
            
            self.pokemon_update["HP"].place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["Attack"].place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["Defense"].place(relx=0.6, rely=0.8, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["Speed"].place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["SpAt"].place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["SpDef"].place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["Update"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
            for key in self.pokemon_add.keys():
                if not isinstance(self.pokemon_add[key], tk.StringVar):
                    self.pokemon_add[key].place_forget()
            for key in self.pokemon_delete.keys():
                if not isinstance(self.pokemon_delete[key], tk.StringVar):
                    self.pokemon_delete[key].place_forget()
        else:
            pass
        self.change_frame(self.frame_dict["ContribPokemonChoose"], self.frame_dict["ContribPokemon"])
            
    def create_pokemon(self):
        sql = "INSERT INTO Pokemons (nid, name, type_1, type_2, hp, attack, defense, sp_atk, sp_def, speed, tier, image, id_login) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        nid = self.pokemon_add["NID"].get()
        name = self.pokemon_add["Name"].get()
        type_1 = self.pokemon_add["Type1"].cget("text")
        type_2 = self.pokemon_add["Type2"].cget("text")
        hp = self.pokemon_add["HP"].get()
        attack = self.pokemon_add["Attack"].get()
        defense = self.pokemon_add["Defense"].get()
        sp_at = self.pokemon_add["SpAt"].get()
        sp_def = self.pokemon_add["SpDef"].get()
        speed = self.pokemon_add["Speed"].get()
        tier = self.pokemon_add["Tier"].cget("text")
        try:
            image = self.pokemon_add["Image"].cget("text")
        except:
            image = ""
        if type_1 != "None" and type_1 != type_2:
            try:
                nid = int(nid)
                hp = int(hp)
                attack = int(attack)
                defense = int(defense)
                sp_at = int(sp_at)
                sp_def = int(sp_def)
                speed = int(speed)
                if nid > 0 and hp > 0 and attack > 0 and defense > 0 and sp_def > 0 and sp_at > 0 and speed > 0:
                    sql_tier = "SELECT id FROM Tiers WHERE name=%s LIMIT 1"
                    self.mycursor.execute(sql_tier, (tier,))
                    tier = self.mycursor.fetchall()
                    sql_type = "SELECT id FROM Types WHERE name=%s LIMIT 1"
                    self.mycursor.execute(sql_type, (type_1,))
                    type_1 = self.mycursor.fetchall()
                    self.mycursor.execute(sql_type, (type_2,))
                    type_2 = self.mycursor.fetchall()
                    if len(tier) > 0 and len(type_1) > 0:
                        tier = int(tier[0][0])
                        type_1 = int(type_1[0][0])
                        type_2 = int(type_2[0][0]) if len(type_2) > 0 else 0 
                        params = (nid,name,type_1,type_2,hp, attack, defense, sp_at, sp_def, speed, tier, image, self.id)  
                       
                        self.mycursor.execute(sql, params)
                        self.mydb.commit()
                        self.pokemon_add["Create"].config(text="Creation success")
                    else:
                        self.pokemon_add["Create"].config(text="Type or tier error")
                else:
                    self.pokemon_add["Create"].config(text="Value error")
            except:
                self.pokemon_add["Create"].config(text="Wrong format value")
        else:    
            self.pokemon_add["Create"].config(text="Type problem")
            
        self.pokemon_add["NID"].delete(0, tk.END)
        self.pokemon_add["NID"].insert(0, "Enter the national id")
        self.pokemon_add["NID"].config(fg="gray")
        
        self.pokemon_add["Name"].delete(0, tk.END)
        self.pokemon_add["Name"].insert(0, "Enter the name")
        self.pokemon_add["Name"].config(fg="gray")
        
        self.pokemon_add["Attack"].delete(0, tk.END)
        self.pokemon_add["Attack"].insert(0, "Enter the attack")
        self.pokemon_add["Attack"].config(fg="gray")
        
        self.pokemon_add["Defense"].delete(0, tk.END)
        self.pokemon_add["Defense"].insert(0, "Enter the defense")
        self.pokemon_add["Defense"].config(fg="gray")
        
        self.pokemon_add["HP"].delete(0, tk.END)
        self.pokemon_add["HP"].insert(0, "Enter the HP")
        self.pokemon_add["HP"].config(fg="gray")
        
        self.pokemon_add["SpAt"].delete(0, tk.END)
        self.pokemon_add["SpAt"].insert(0, "Enter the special attack")
        self.pokemon_add["SpAt"].config(fg="gray")
        
        self.pokemon_add["SpDef"].delete(0, tk.END)
        self.pokemon_add["SpDef"].insert(0, "Enter the special defense")
        self.pokemon_add["SpDef"].config(fg="gray")
        
        self.pokemon_add["Speed"].delete(0, tk.END)
        self.pokemon_add["Speed"].insert(0, "Enter the speed")
        self.pokemon_add["Speed"].config(fg="gray")
        
        
        self.update_button()
                
        self.pokemon_add["Type1"].destroy()
        self.pokemon_add["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType1"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_add["Type1Label"].config(text=x))
        self.pokemon_add["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Type2"].destroy()
        self.pokemon_add["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType2"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_add["Type2Label"].config(text=x))
        self.pokemon_add["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Tier"].destroy()
        self.pokemon_add["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectTier"], *self.tier_contribute_dict["Select"], command=lambda x: self.pokemon_add["TierLabel"].config(text=x))
        self.pokemon_add["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        
                
    def delete_pokemon(self):
        sql = "DELETE FROM Pokemons WHERE name=%s"
        name = self.pokemon_delete["Choose"].cget("text")
        try:
            self.mycursor.execute(sql, (name,))
            self.mydb.commit()
            self.pokemon_delete["Delete"].config(text="Delete success")
        except:
            self.pokemon_delete["Delete"].config(text="Name error")
            
        self.update_button()
        
        self.pokemon_delete["Choose"].destroy()
        self.pokemon_delete["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_delete["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"], command=lambda x: self.pokemon_delete["ChooseLabel"].config(text=x))
        self.pokemon_delete["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
         
    def update_pokemon(self):
        sql = "UPDATE Pokemons SET nid=%s, name=%s, type_1=%s, type_2=%s, hp=%s, attack=%s, defense=%s, sp_atk=%s, sp_def=%s, speed=%s, tier=%s, image=%s, id_login=%s WHERE name=%s"
        nid = self.pokemon_update["NID"].get()
        name = self.pokemon_update["Name"].get()
        type_1 = self.pokemon_update["Type1"].cget("text")
        type_2 = self.pokemon_update["Type2"].cget("text")
        hp = self.pokemon_update["HP"].get()
        attack = self.pokemon_update["Attack"].get()
        defense = self.pokemon_update["Defense"].get()
        sp_at = self.pokemon_update["SpAt"].get()
        sp_def = self.pokemon_update["SpDef"].get()
        speed = self.pokemon_update["Speed"].get()
        tier = self.pokemon_update["Tier"].cget("text")
        final = self.pokemon_update["Choose"].cget("text")
        try:
            image = self.pokemon_update["Image"].cget("text")
        except:
            image = ""
        if type_1 != "None" and type_1 != type_2:
            try:
                nid = int(nid)
                hp = int(hp)
                attack = int(attack)
                defense = int(defense)
                sp_at = int(sp_at)
                sp_def = int(sp_def)
                speed = int(speed)
                if nid > 0 and hp > 0 and attack > 0 and defense > 0 and sp_def > 0 and sp_at > 0 and speed > 0:
                    sql_tier = "SELECT id FROM Tiers WHERE name=%s LIMIT 1"
                    self.mycursor.execute(sql_tier, (tier,))
                    tier = self.mycursor.fetchall()
                    sql_type = "SELECT id FROM Types WHERE name=%s LIMIT 1"
                    self.mycursor.execute(sql_type, (type_1,))
                    type_1 = self.mycursor.fetchall()
                    self.mycursor.execute(sql_type, (type_2,))
                    type_2 = self.mycursor.fetchall()
                    if len(tier) > 0 and len(type_1) > 0:
                        tier = int(tier[0][0])
                        type_1 = int(type_1[0][0])
                        type_2 = int(type_2[0][0]) if len(type_2) > 0 else 0 
                        params = (nid,name,type_1,type_2,hp, attack, defense, sp_at, sp_def, speed, tier, image, self.id, final)  
                        
                        self.mycursor.execute(sql, params)
                        self.mydb.commit()
                        self.pokemon_update["Update"].config(text="Creation success")
                    else:
                        self.pokemon_update["Update"].config(text="Type or tier error")
                else:
                    self.pokemon_update["Update"].config(text="Value error")
            except:
                self.pokemon_update["Update"].config(text="Wrong format value")
        else:    
            self.pokemon_update["Update"].config(text="Type problem")
            
        self.pokemon_update["NID"].delete(0, tk.END)
        self.pokemon_update["NID"].insert(0, "Enter the national id")
        self.pokemon_update["NID"].config(fg="gray")
        
        self.pokemon_update["Name"].delete(0, tk.END)
        self.pokemon_update["Name"].insert(0, "Enter the name")
        self.pokemon_update["Name"].config(fg="gray")
        
        self.pokemon_update["Attack"].delete(0, tk.END)
        self.pokemon_update["Attack"].insert(0, "Enter the attack")
        self.pokemon_update["Attack"].config(fg="gray")
        
        self.pokemon_update["Defense"].delete(0, tk.END)
        self.pokemon_update["Defense"].insert(0, "Enter the defense")
        self.pokemon_update["Defense"].config(fg="gray")
        
        self.pokemon_update["HP"].delete(0, tk.END)
        self.pokemon_update["HP"].insert(0, "Enter the HP")
        self.pokemon_update["HP"].config(fg="gray")
        
        self.pokemon_update["SpAt"].delete(0, tk.END)
        self.pokemon_update["SpAt"].insert(0, "Enter the special attack")
        self.pokemon_update["SpAt"].config(fg="gray")
        
        self.pokemon_update["SpDef"].delete(0, tk.END)
        self.pokemon_update["SpDef"].insert(0, "Enter the special defense")
        self.pokemon_update["SpDef"].config(fg="gray")
        
        self.pokemon_update["Speed"].delete(0, tk.END)
        self.pokemon_update["Speed"].insert(0, "Enter the speed")
        self.pokemon_update["Speed"].config(fg="gray")
        
        self.update_button()
        
        self.pokemon_update["Type1"].destroy()
        self.pokemon_update["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType1"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_update["Type1Label"].config(text=x))
        self.pokemon_update["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Type2"].destroy()
        self.pokemon_update["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType2"], *self.type_contribute_dict["Select"], command=lambda x: self.pokemon_update["Type2Label"].config(text=x))
        self.pokemon_update["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Tier"].destroy()
        self.pokemon_update["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectTier"], *self.tier_contribute_dict["Select"], command=lambda x: self.pokemon_update["TierLabel"].config(text=x))
        self.pokemon_update["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Choose"].destroy()
        self.pokemon_update["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"], command=lambda x: self.pokemon_update["ChooseLabel"].config(text=x))
        self.pokemon_update["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
     
        
    def mainloop(self):
        self.change_frame(None, self.frame_dict["Login"])
        self.root.mainloop()
        
#%% [3] Main program

if __name__ == '__main__':
    app = App()
    app.mainloop()