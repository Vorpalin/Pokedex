# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 12:00:02 2025

@author: MIALON alexis
"""

#%% [1] Import
import mysql.connector
from dbcredentials import db
import tkinter as tk
import pygame
import json
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from enum import Enum
from PIL import Image, ImageTk
from tkinter import filedialog
from collections import deque

#%% [2] OOP

class Mode(Enum):
    UPDATE = 1
    ADD = 2
    DELETE = 3
class PokemonCaracteristic(Enum):
    MOVE = 1
    EVOLUTION = 2
    ABILITY = 3
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
        pygame.mixer.init()
        pygame.mixer.music.load("Sound/music.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(1)
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
        self.frame_dict["Results"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["SearchImage"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["SearchSelection"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["TypeEfficacity"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["TypeSelect"] = tk.Frame(self.container, bg="lightblue")
        self.frame_dict["SearchFilter"] = tk.Frame(self.container, bg="lightblue")
        for frame in self.frame_dict.values():
            frame.place(relwidth=1, relheight=1)
            
        #%%% [2.1.1] Login page
        self.login_dict = dict()
        
        try:
            im = Image.open("Pictures/background_login.jpg").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.login_dict["Background"] = tk.Label(self.frame_dict["Login"], image=im)
            self.login_dict["Background"].image = im
            self.login_dict["Background"].place(relwidth=1, relheight=1)
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
        self.login_dict["Password"].bind("<Return>", lambda event: self.connection())

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

        self.login_dict["Sound"] = tk.Button(self.frame_dict["Login"], text="Switch the music", bg="#FF6347",
                                                  command=self.switch_sound)
        self.login_dict["Sound"].place(relx=0.86, rely=0.93, relwidth=0.1, relheight=0.04)

        self.login_dict["Quit"] = tk.Button(self.frame_dict["Login"], text="Quit", command=self.root.quit)
        self.login_dict["Quit"].place(relx=0.86, rely=0.05, relwidth=0.1, relheight=0.04)

        #%%% [2.1.2] Choose page
        self.choose_dict = dict()
        
        
        try:
            im = Image.open("Pictures/choose.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.choose_dict["Background"] = tk.Label(self.frame_dict["Choose"], image=im)
            self.choose_dict["Background"].image = im
            self.choose_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        
        self.choose_dict["Title"] = tk.Label(self.frame_dict["Choose"], text="Choose your mode", font=("Arial",36, "bold"), fg="black", bg="lightgreen", borderwidth=2, relief="solid")
        self.choose_dict["Title"].pack(pady=20)

        self.choose_dict["Research"] = tk.Button(self.frame_dict["Choose"], text="Research", compound="top", width=20, height=1, bg="lightblue", command= lambda: self.change_frame(self.frame_dict["Choose"], self.frame_dict["SearchSelection"]))
        self.choose_dict["Research"].place(relx=0.75, rely=0.9, anchor="center")
        self.choose_dict["Contribute"] = tk.Button(self.frame_dict["Choose"], text="Contribution", compound="top", width=20, height=1, bg="#ffa500", command= lambda: self.change_frame(self.frame_dict["Choose"], self.frame_dict["Contribution"]))
        self.choose_dict["Contribute"].place(relx=0.25, rely=0.9, anchor="center")
        self.choose_dict["Deconnection"] = tk.Button(self.frame_dict["Choose"], text="Deconnection", compound="top", bg="#FF6347", command=self.return_back)
        self.choose_dict["Deconnection"].place(relx=0.95, rely=0.03, anchor="center")
        
        
        #%%% [2.1.3] Contribute page
        self.contribute_dict = dict()
        
        try:
            im = Image.open("Pictures/selection_contribute.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.contribute_dict["Background"] = tk.Label(self.frame_dict["Contribution"], image=im)
            self.contribute_dict["Background"].image = im
            self.contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        
        self.contribute_dict["Title"] = tk.Label(self.frame_dict["Contribution"], text="Choose your type of contribution", font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        self.contribute_dict["Title"].pack(pady=20)
        
        self.contribute_dict["Update"] = tk.Button(self.frame_dict["Contribution"], text="Update", compound="top", width=20, height=1, bg="lightblue", command= lambda: self.selection_mode(Mode.UPDATE))
        self.contribute_dict["Update"].place(relx=0.79, rely=0.62, anchor="center")
        
        self.contribute_dict["Add"] = tk.Button(self.frame_dict["Contribution"], text="Create", compound="top", width=20, height=1, bg="lightgreen", command= lambda: self.selection_mode(Mode.ADD))
        self.contribute_dict["Add"].place(relx=0.21, rely=0.62, anchor="center")
        
        self.contribute_dict["Delete"] = tk.Button(self.frame_dict["Contribution"], text="Delete", compound="top", width=20, height=1, bg="#ffa500", command= lambda: self.selection_mode(Mode.DELETE))
        self.contribute_dict["Delete"].place(relx=0.5, rely=0.95, anchor="center")
        
        self.mode = 0
        self.contribute_dict["Deconnection"] = tk.Button(self.frame_dict["Contribution"], text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        self.contribute_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
        
        #%%% [2.1.4] Select Contribution
        
        self.select_contribute_dict = dict()
        
        try:
            im = Image.open("Pictures/contribute_2.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.select_contribute_dict["Background"] = tk.Label(self.frame_dict["SelectContribution"], image=im)
            self.select_contribute_dict["Background"].image = im
            self.select_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        
        self.category_contribute_dict = dict()
        self.type_contribute_dict = dict()
        self.tier_contribute_dict = dict()
        self.ability_contribute_dict = dict()
        
        self.select_contribute_dict["Title"] = tk.Label(self.frame_dict["SelectContribution"], text="Choose your field of contribution", font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        self.select_contribute_dict["Title"].pack(pady=20)
        
        self.select_contribute_dict["Pokemon"] = tk.Button(self.frame_dict["SelectContribution"], text="Pokemon", compound="top", width=20, height=1, command= lambda: self.change_frame(self.frame_dict["SelectContribution"], self.frame_dict["ContribPokemonChoose"]))
        self.select_contribute_dict["Pokemon"].place(relx=0.163, rely=0.45, anchor="center")
        
        self.select_contribute_dict["Abilities"] = tk.Button(self.frame_dict["SelectContribution"], text="Abilities", compound="top", width=20, height=1, bg="#cc9add", command= lambda: self.change_frame_binary(self.frame_dict["ContribAbility"], self.ability_contribute_dict, "Ability", desc=True))
        self.select_contribute_dict["Abilities"].place(relx=0.5, rely=0.45, anchor="center")
        
        self.select_contribute_dict["Categories"] = tk.Button(self.frame_dict["SelectContribution"], text="Attack categories", compound="top", width=20, height=1, bg="#ffa500", command= lambda: self.change_frame_binary(self.frame_dict["ContribCategory"], self.category_contribute_dict, "Category"))
        self.select_contribute_dict["Categories"].place(relx=0.84, rely=0.45, anchor="center")
        
        self.select_contribute_dict["Moves"] = tk.Button(self.frame_dict["SelectContribution"], text="Moves", compound="top", width=20, height=1, bg="#bf8013", command= lambda: self.change_frame_move())
        self.select_contribute_dict["Moves"].place(relx=0.163, rely=0.92, anchor="center")
        
        self.select_contribute_dict["Types"] = tk.Button(self.frame_dict["SelectContribution"], text="Types", compound="top", width=20, height=1, bg="lightgreen", command= lambda:self.change_frame(self.frame_dict["SelectContribution"], self.frame_dict["TypeSelect"]))
        self.select_contribute_dict["Types"].place(relx=0.5, rely=0.92, anchor="center")
        
        self.select_contribute_dict["Tiers"] = tk.Button(self.frame_dict["SelectContribution"], text="Tiers", compound="top", width=20, height=1, bg="lightblue", command= lambda: self.change_frame_binary(self.frame_dict["ContribTiers"], self.tier_contribute_dict, "Tier"))
        self.select_contribute_dict["Tiers"].place(relx=0.84, rely=0.92, anchor="center")
        
        self.select_contribute_dict["Deconnection"] = tk.Button(self.frame_dict["SelectContribution"], text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        self.select_contribute_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
        
        try:
            im = Image.open("Pictures/category.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.category_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribCategory"], image=im)
            self.category_contribute_dict["Background"].image = im
            self.category_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.create_binary(self.category_contribute_dict, self.frame_dict["ContribCategory"], "Category", "Categories")
        try:
            im = Image.open("Pictures/type.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.type_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribType"], image=im)
            self.type_contribute_dict["Background"].image = im
            self.type_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.create_binary(self.type_contribute_dict, self.frame_dict["ContribType"], "Type", "Types")
        try:
            im = Image.open("Pictures/tier.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.tier_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribTiers"], image=im)
            self.tier_contribute_dict["Background"].image = im
            self.tier_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.create_binary(self.tier_contribute_dict, self.frame_dict["ContribTiers"], "Tier", "Tiers")
        try:
            im = Image.open("Pictures/ability.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.ability_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribAbility"], image=im)
            self.ability_contribute_dict["Background"].image = im
            self.ability_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.create_binary(self.ability_contribute_dict, self.frame_dict["ContribAbility"], "Ability", "Abilities", description=True)
        
        
        #%%% [2.1.4]
        self.pokemon_select_contribute_dict = dict()
        try:
            im = Image.open("Pictures/choose_pokemon.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.pokemon_select_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribPokemonChoose"], image=im)
            self.pokemon_select_contribute_dict["Background"].image = im
            self.pokemon_select_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.pokemon_select_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribPokemonChoose"], text="Choose the type of modification", font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        self.pokemon_select_contribute_dict["Title"].pack(pady=20)
        
        self.pokemon_select_contribute_dict["Pokemon"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Pokemon", compound="top", width=20, height=1, bg="#cc9add", command=self.change_frame_pokemon_pokemon)
        self.pokemon_select_contribute_dict["Pokemon"].place(relx=0.25, rely=0.47, anchor="center")
        
        self.pokemon_select_contribute_dict["Moves"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Pokemon moves", compound="top", width=20, height=1, bg="#ffa500", command= lambda: self.change_frame(self.frame_dict["ContribPokemonChoose"], self.frame_dict["ContribPokemonMove"]))
        self.pokemon_select_contribute_dict["Moves"].place(relx=0.75, rely=0.47, anchor="center")
        
        self.pokemon_select_contribute_dict["Evolutions"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Pokemon evolution", compound="top", width=20, height=1, bg="lightgrey", command= lambda: self.change_frame(self.frame_dict["ContribPokemonChoose"], self.frame_dict["ContribPokemonEvolution"]))
        self.pokemon_select_contribute_dict["Evolutions"].place(relx=0.25, rely=0.88, anchor="center")
        
        self.pokemon_select_contribute_dict["Abilities"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Pokemon abilities", compound="top", width=20, height=1, bg="lightblue", command= lambda: self.change_frame(self.frame_dict["ContribPokemonChoose"], self.frame_dict["ContribPokemonAbility"]))
        self.pokemon_select_contribute_dict["Abilities"].place(relx=0.75, rely=0.88, anchor="center")
        
        self.pokemon_select_contribute_dict["Deconnection"] = tk.Button(self.frame_dict["ContribPokemonChoose"], text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        self.pokemon_select_contribute_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
        #%%% [2.1.4.1] Pokemon change
        
        self.pokemon_contribute_dict = dict()
        try:
            im = Image.open("Pictures/new_pokemon.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.pokemon_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribPokemon"], image=im)
            self.pokemon_contribute_dict["Background"].image = im
            self.pokemon_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.pokemon_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribPokemon"], text=self.title_contribute("Pokemon"), font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
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
        
        self.pokemon_add["SelectType1"] =  tk.StringVar(value="Type 1")
        self.pokemon_add["SelectType2"] =  tk.StringVar(value="Type 2")
        self.pokemon_add["SelectTier"] =  tk.StringVar(value="Tier")
        
        
        
        
        self.pokemon_add["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType1"], *self.type_contribute_dict["Select"])
        self.pokemon_add["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        
        self.pokemon_add["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType2"], *self.type_contribute_dict["Select"])
        self.pokemon_add["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        

        
        self.pokemon_add["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectTier"], *self.tier_contribute_dict["Select"])
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
        
        
        self.pokemon_add["Create"] = tk.Button(self.frame_dict["ContribPokemon"], text="Create", width=20, height=1, bg="lightgreen", command=self.create_pokemon)
        self.pokemon_add["Create"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        self.pokemon_contribute_dict["Deconnection"] = tk.Button(self.frame_dict["ContribPokemon"], text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        self.pokemon_contribute_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")

        
        self.pokemon_delete = dict()
        self.pokemon_delete["SelectPokemon"] = tk.StringVar(value="Pokemon")
        
        self.pokemon_delete["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_delete["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"])
        self.pokemon_delete["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_delete["Delete"] = tk.Button(self.frame_dict["ContribPokemon"], text="Delete", width=20, height=1, bg="#ffa500", command=self.delete_pokemon)
        self.pokemon_delete["Delete"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update = dict()
        self.pokemon_update["SelectPokemon"] = tk.StringVar(value="Pokemon")
        
        self.pokemon_update["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"])
        self.pokemon_update["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        
        self.pokemon_update["NID"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["NID"].place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_update["NID"].insert(0, "Enter the national id")
        self.pokemon_update["NID"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["NID"],"Enter the national id", self.pokemon_update["Choose"], "SELECT nid FROM Pokemons WHERE name=%s LIMIT 1"))
        self.pokemon_update["NID"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["NID"],"Enter the national id", self.pokemon_update["Choose"], "SELECT nid FROM Pokemons WHERE name=%s LIMIT 1"))
        
        self.pokemon_update["Name"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["Name"].place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Name"].insert(0, "Enter the name")
        self.pokemon_update["Name"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["Name"],"Enter the name", self.pokemon_update["Choose"], "SELECT name FROM Pokemons WHERE name=%s LIMIT 1"))
        self.pokemon_update["Name"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["Name"],"Enter the name", self.pokemon_update["Choose"], "SELECT name FROM Pokemons WHERE name=%s LIMIT 1"))
        
        
        self.pokemon_update["ImageLabel"] = tk.Label(self.frame_dict["ContribPokemon"], text="Type 1")
        self.pokemon_update["ImageLabel"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Image"] = tk.Button(self.frame_dict["ContribPokemon"], text="Image selection", compound="top", command=lambda: self.get_image_path(self.pokemon_update["ImageLabel"], self.pokemon_update["Image"]))
        self.pokemon_update["Image"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["SelectType1"] =  tk.StringVar(value="Type 1")
        self.pokemon_update["SelectType2"] =  tk.StringVar(value= "Type 2")
        self.pokemon_update["SelectTier"] =  tk.StringVar(value="Tier")
        
        
        
        
        self.pokemon_update["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType1"], *self.type_contribute_dict["Select"])
        self.pokemon_update["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        
        self.pokemon_update["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType2"], *self.type_contribute_dict["Select"])
        self.pokemon_update["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        

      
        self.pokemon_update["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectTier"], *self.tier_contribute_dict["Select"])
        self.pokemon_update["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["HP"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["HP"].place(relx=0.6, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_update["HP"].insert(0, "Enter the HP")
        self.pokemon_update["HP"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["HP"],"Enter the HP", self.pokemon_update["Choose"], "SELECT hp FROM Pokemons WHERE name=%s LIMIT 1"))
        self.pokemon_update["HP"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["HP"],"Enter the HP", self.pokemon_update["Choose"], "SELECT hp FROM Pokemons WHERE name=%s LIMIT 1"))
        
        self.pokemon_update["Attack"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["Attack"].place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Attack"].insert(0, "Enter the attack")
        self.pokemon_update["Attack"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["Attack"],"Enter the attack", self.pokemon_update["Choose"], "SELECT attack FROM Pokemons WHERE name=%s LIMIT 1"))
        self.pokemon_update["Attack"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["Attack"],"Enter the attack", self.pokemon_update["Choose"], "SELECT attack FROM Pokemons WHERE name=%s LIMIT 1"))
        
        self.pokemon_update["Defense"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["Defense"].place(relx=0.6, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Defense"].insert(0, "Enter the defense")
        self.pokemon_update["Defense"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["Defense"],"Enter the defense", self.pokemon_update["Choose"], "SELECT defense FROM Pokemons WHERE name=%s LIMIT 1"))
        self.pokemon_update["Defense"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["Defense"],"Enter the defense", self.pokemon_update["Choose"], "SELECT defense FROM Pokemons WHERE name=%s LIMIT 1"))
        
        self.pokemon_update["Speed"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["Speed"].place(relx=0.8, rely=0.2, relwidth=0.1, relheight=0.04)
        self.pokemon_update["Speed"].insert(0, "Enter the speed")
        self.pokemon_update["Speed"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["Speed"],"Enter the speed", self.pokemon_update["Choose"], "SELECT speed FROM Pokemons WHERE name=%s LIMIT 1"))
        self.pokemon_update["Speed"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["Speed"],"Enter the speed", self.pokemon_update["Choose"], "SELECT speed FROM Pokemons WHERE name=%s LIMIT 1"))
        
        self.pokemon_update["SpAt"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["SpAt"].place(relx=0.8, rely=0.5, relwidth=0.1, relheight=0.04)
        self.pokemon_update["SpAt"].insert(0, "Enter the special attack")
        self.pokemon_update["SpAt"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["SpAt"],"Enter the special attack", self.pokemon_update["Choose"], "SELECT sp_def FROM Pokemons WHERE name=%s LIMIT 1"))
        self.pokemon_update["SpAt"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["SpAt"],"Enter the special attack", self.pokemon_update["Choose"], "SELECT sp_def FROM Pokemons WHERE name=%s LIMIT 1"))
        
        self.pokemon_update["SpDef"] = tk.Entry(self.frame_dict["ContribPokemon"], width=35, fg="gray")
        self.pokemon_update["SpDef"].place(relx=0.8, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_update["SpDef"].insert(0, "Enter the special defense")
        self.pokemon_update["SpDef"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.pokemon_update["SpDef"],"Enter the special defense", self.pokemon_update["Choose"], "SELECT sp_def FROM Pokemons WHERE name=%s LIMIT 1"))
        self.pokemon_update["SpDef"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.pokemon_update["SpDef"],"Enter the special defense", self.pokemon_update["Choose"], "SELECT sp_def FROM Pokemons WHERE name=%s LIMIT 1"))
        
        
        self.pokemon_update["Update"] = tk.Button(self.frame_dict["ContribPokemon"], text="Update", width=20, height=1, bg="lightblue", command=self.update_pokemon)
        self.pokemon_update["Update"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        #%%% [2.1.4.2] Move change

        self.move_contribute_dict = dict()
        try:
            im = Image.open("Pictures/move.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.move_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribMove"], image=im)
            self.move_contribute_dict["Background"].image = im
            self.move_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass

        self.move_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribMove"], text=self.title_contribute("Move"), font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
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
        self.move_add["Name"].place(relx=0.15, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_add["Name"].insert(0, "Enter a name")
        self.move_add["Name"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.move_add["Name"],"Enter a name", False))
        self.move_add["Name"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.move_add["Name"],"Enter a name"))

        self.move_add["SelectType"] =  tk.StringVar(value="Type")
       
        self.move_add["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectType"], *self.type_contribute_dict["Select"])
        self.move_add["Type"].place(relx=0.34, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_add["SelectCategory"] =  tk.StringVar(value="Category")

        self.move_add["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectCategory"], *self.category_contribute_dict["Select"])
        self.move_add["Category"].place(relx=0.65, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_add["Power"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_add["Power"].place(relx=0.85, rely=0.33, relwidth=0.1, relheight=0.04)
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
        self.move_add["Priority"].insert(0, "Enter the accuracy")
        self.move_add["Priority"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.move_add["Priority"],"Enter the accuracy", False))
        self.move_add["Priority"].bind("<FocusOut>", lambda event: self.clear_entry(event, self.move_add["Priority"],"Enter the accuracy"))
        
        self.move_add["Description"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_add["Description"].place(relx=0.75, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_add["Description"].insert(0, "Enter a description")
        self.move_add["Description"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.move_add["Description"],"Enter a description", False))
        self.move_add["Description"].bind("<FocusOut>", lambda event: self.clear_entry(event, self.move_add["Description"],"Enter a description"))
        
        self.move_add["Create"] = tk.Button(self.frame_dict["ContribMove"], text="Create", width=20, height=1, bg="lightgreen", command=self.create_move)
        self.move_add["Create"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        self.move_delete["SelectMove"] =  tk.StringVar(value="Move")
        
        self.move_delete["Move"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_delete["SelectMove"], *self.move_contribute_dict["SelectUse"])
        self.move_delete["Move"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.move_delete["Delete"] = tk.Button(self.frame_dict["ContribMove"], text="Delete", width=20, height=1, bg="#ffa500", command=self.delete_move)
        self.move_delete["Delete"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        self.move_update["Name"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["Name"].place(relx=0.2, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_update["Name"].insert(0, "Enter a name")
        self.move_update["Name"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["Name"], "Enter a name", self.move_delete["Move"], "SELECT name FROM Moves WHERE name=%s LIMIT 1"))
        self.move_update["Name"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["Name"],"Enter a name", self.move_delete["Move"], "SELECT name FROM Moves WHERE name=%s LIMIT 1"))

        self.move_update["SelectType"] =  tk.StringVar(value="Type")
        
        self.move_update["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectType"], *self.type_contribute_dict["Select"])
        self.move_update["Type"].place(relx=0.4, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_update["SelectCategory"] =  tk.StringVar(value="Category")
        
        self.move_update["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectCategory"], *self.category_contribute_dict["Select"])
        self.move_update["Category"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_update["Power"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["Power"].place(relx=0.8, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_update["Power"].insert(0, "Enter the power")
        self.move_update["Power"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["Power"],"Enter the power", self.move_delete["Move"], "SELECT power FROM Moves WHERE name=%s LIMIT 1"))
        self.move_update["Power"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["Power"],"Enter the power", self.move_delete["Move"], "SELECT power FROM Moves WHERE name=%s LIMIT 1"))
        
        self.move_update["PP"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["PP"].place(relx=0.25, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_update["PP"].insert(0, "Enter the PP")
        self.move_update["PP"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["PP"],"Enter the PP", self.move_delete["Move"], "SELECT pp FROM Moves WHERE name=%s LIMIT 1"))
        self.move_update["PP"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["PP"],"Enter the PP", self.move_delete["Move"], "SELECT pp FROM Moves WHERE name=%s LIMIT 1"))
        
        self.move_update["Priority"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["Priority"].place(relx=0.5, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_update["Priority"].insert(0, "Enter the accuracy")
        self.move_update["Priority"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["Priority"],"Enter the accuracy", self.move_delete["Move"], "SELECT accuracy FROM Moves WHERE name=%s LIMIT 1"))
        self.move_update["Priority"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["Priority"],"Enter the accuracy", self.move_delete["Move"], "SELECT accuracy FROM Moves WHERE name=%s LIMIT 1"))
        
        self.move_update["Description"] = tk.Entry(self.frame_dict["ContribMove"], width=35, fg="gray")
        self.move_update["Description"].place(relx=0.75, rely=0.66, relwidth=0.1, relheight=0.04)
        self.move_update["Description"].insert(0, "Enter a description")
        self.move_update["Description"].bind("<FocusIn>", lambda event: self.fill_entry_value_by_name(event, self.move_update["Description"],"Enter a description", self.move_delete["Move"], "SELECT description FROM Moves WHERE name=%s LIMIT 1"))
        self.move_update["Description"].bind("<FocusOut>",  lambda event: self.clear_entry_value_by_name(event, self.move_update["Description"],"Enter a description", self.move_delete["Move"], "SELECT description FROM Moves WHERE name=%s LIMIT 1"))
        
        self.move_update["Update"] = tk.Button(self.frame_dict["ContribMove"], text="Update", width=20, height=1, bg="lightgreen", command=lambda: self.update_move(self.move_delete["Move"]))
        self.move_update["Update"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        self.move_contribute_dict["Deconnection"] = tk.Button(self.frame_dict["ContribMove"], text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        self.move_contribute_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
        
        self.pokemon_move_contribute_dict = dict()
        self.pokemon_evolution_contribute_dict = dict()
        self.pokemon_ability_contribute_dict = dict()
        
        try:
            im = Image.open("Pictures/evolution.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.pokemon_evolution_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribPokemonEvolution"], image=im)
            self.pokemon_evolution_contribute_dict["Background"].image = im
            self.pokemon_evolution_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        
        try:
            im = Image.open("Pictures/ability.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.pokemon_ability_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribPokemonAbility"], image=im)
            self.pokemon_ability_contribute_dict["Background"].image = im
            self.pokemon_ability_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        
        try:
            im = Image.open("Pictures/move.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.move_contribute_dict["Background"] = tk.Label(self.frame_dict["ContribPokemonMove"], image=im)
            self.move_contribute_dict["Background"].image = im
            self.move_contribute_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.pokemon_move_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribPokemonMove"], text=self.title_contribute("Pokemon move"), font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        self.pokemon_move_contribute_dict["Title"].pack(pady=20)
        
        self.pokemon_evolution_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribPokemonEvolution"], text=self.title_contribute("Pokemon evolution"), font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        self.pokemon_evolution_contribute_dict["Title"].pack(pady=20)
        
        self.pokemon_ability_contribute_dict["Title"] = tk.Label(self.frame_dict["ContribPokemonAbility"], text=self.title_contribute("Pokemon ability"), font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        self.pokemon_ability_contribute_dict["Title"].pack(pady=20)
        
        self.create_pokemon_carateristic(self.pokemon_move_contribute_dict, self.frame_dict["ContribPokemonMove"], PokemonCaracteristic.MOVE)
        self.create_pokemon_carateristic(self.pokemon_evolution_contribute_dict, self.frame_dict["ContribPokemonEvolution"], PokemonCaracteristic.EVOLUTION)
        self.create_pokemon_carateristic(self.pokemon_ability_contribute_dict, self.frame_dict["ContribPokemonAbility"], PokemonCaracteristic.ABILITY)
        
        #%% Research Part
        
        self.research_sql_dict = dict()
        try:
            im = Image.open("Pictures/research_name.jpg").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.research_sql_dict["Background"] = tk.Label(self.frame_dict["Research"], image=im)
            self.research_sql_dict["Background"].image = im
            self.research_sql_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.research_sql_dict["Title"] = tk.Label(self.frame_dict["Research"], text="Research your pokemon", font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        self.research_sql_dict["Title"].pack(pady=20)
        
        self.research_sql_dict["Deconnection"] = tk.Button(self.frame_dict["Research"], text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        self.research_sql_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
        
        
        self.research_sql_dict["ListName"] = tk.Listbox(self.frame_dict["Research"], width=80, height=15)
        self.research_sql_dict["ListName"].place(relx=0.5, rely=0.3)
        
        self.research_sql_dict["Name"] = tk.Entry(self.frame_dict["Research"], width=45, fg="gray")
        self.research_sql_dict["Name"].place(relx=0.3, rely=0.48, relwidth=0.1, relheight=0.04)
        self.research_sql_dict["Name"].insert(0, "Enter the name")
        self.research_sql_dict["Name"].bind("<FocusIn>", lambda event: self.fill_entry(event, self.research_sql_dict["Name"],"Enter the name", False))
        self.research_sql_dict["Name"].bind("<FocusOut>",  lambda event: self.clear_entry(event, self.research_sql_dict["Name"],"Enter the name"))
        self.research_sql_dict["Name"].bind("<KeyRelease>", lambda event: self.on_key_release(event, self.research_sql_dict["Name"],self.research_sql_dict["ListName"]))
        
        self.research_sql_dict["Select"] = deque([])
        self.research_sql_dict["ListName"].bind("<Double-1>", lambda event: self.on_select_list(event,self.research_sql_dict["Name"], self.research_sql_dict["ListName"]))
        
        self.research_sql_dict["Search"] = tk.Button(self.frame_dict["Research"], text="Search", width=20, height=1, bg="lightgreen", command=lambda: self.search_by_name(self.research_sql_dict["Name"], strict=False))
        self.research_sql_dict["Search"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        self.result_sql_dict = dict()
        
        try:
            im = Image.open("Pictures/result_pokemon.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.result_sql_dict["Background"] = tk.Label(self.frame_dict["Results"], image=im)
            self.result_sql_dict["Background"].image = im
            self.result_sql_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        
        try:
            im = Image.open("Pictures/question_mark.jpg").convert("RGB")
            im = im.resize((300, 300), Image.Resampling.LANCZOS)
            
            im = ImageTk.PhotoImage(im)
            
            self.result_sql_dict["PokemonImage"] = tk.Label(self.frame_dict["Results"], image=im)
            self.result_sql_dict["PokemonImage"].image = im
            self.result_sql_dict["PokemonImage"].place(relx=0.5, rely=0.5, anchor="center")
        except:
            pass
        
        self.result_sql_dict["Title"] = tk.Label(self.frame_dict["Results"], text="Your selected pokemon", font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        self.result_sql_dict["Title"].pack(pady=20)
        
        
        self.poke_ability = ["None"]
        self.poke_id = 0
        self.poke_move = ["None"]
        self.research_sql_dict["PreEvolution"] = ["None"]
        self.research_sql_dict["Evolution"] = ["None"]
        
        
        self.result_sql_dict["Deconnection"] = tk.Button(self.frame_dict["Results"], text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        self.result_sql_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
        self.result_sql_dict["Tier"] = tk.Label(self.frame_dict["Results"], text="Type :")
        self.result_sql_dict["Tier"].place(relx=0.32, rely=0.8)
        self.result_sql_dict["Type1"] = tk.Label(self.frame_dict["Results"], text="Type 1 :")
        self.result_sql_dict["Type1"].place(relx=0.32, rely=0.85)
        self.result_sql_dict["Type2"] = tk.Label(self.frame_dict["Results"], text="Type 2 :")
        self.result_sql_dict["Type2"].place(relx=0.32, rely=0.9)
        self.result_sql_dict["HP"] = tk.Label(self.frame_dict["Results"], text="HP :")
        self.result_sql_dict["HP"].place(relx=0.48, rely=0.8)
        self.result_sql_dict["Attack"] = tk.Label(self.frame_dict["Results"], text="Attack :")
        self.result_sql_dict["Attack"].place(relx=0.48, rely=0.85)
        self.result_sql_dict["Defense"] = tk.Label(self.frame_dict["Results"], text="Defense :")
        self.result_sql_dict["Defense"].place(relx=0.48, rely=0.9)
        self.result_sql_dict["Speed"] = tk.Label(self.frame_dict["Results"], text="Type :")
        self.result_sql_dict["Speed"].place(relx=0.63, rely=0.8)
        self.result_sql_dict["AttackSpe"] = tk.Label(self.frame_dict["Results"], text="Attack special :")
        self.result_sql_dict["AttackSpe"].place(relx=0.63, rely=0.85)
        self.result_sql_dict["DefenseSpe"] = tk.Label(self.frame_dict["Results"], text="Defense Special :")
        self.result_sql_dict["DefenseSpe"].place(relx=0.63, rely=0.9)
        
        self.result_sql_dict["SelectAbility"] = tk.StringVar(value="Ability")
        self.result_sql_dict["AbilityDescription"] = tk.Text(self.frame_dict["Results"], font=("Arial", 14), wrap="word", height=10, width=20)
        self.result_sql_dict["AbilityDescription"].place(relx=0.13, rely=0.33)
        self.result_sql_dict["Ability"] = tk.OptionMenu(self.frame_dict["Results"], self.result_sql_dict["SelectAbility"], *self.poke_ability, command=lambda event: self.display_ability_description(event, self.result_sql_dict["Ability"], self.result_sql_dict["AbilityDescription"]))
        self.result_sql_dict["Ability"].place(relx=0.13, rely=0.85, relwidth=0.1, relheight=0.04)
        self.result_sql_dict["AbilityDescription"].config(state="disabled")
        
        self.result_sql_dict["SelectMove"] = tk.StringVar(value="Move")
        self.result_sql_dict["MoveDescription"] = tk.Text(self.frame_dict["Results"], font=("Arial", 14), wrap="word", height=10, width=20)
        self.result_sql_dict["MoveDescription"].place(relx=0.70, rely=0.33)
        self.result_sql_dict["Move"] = tk.OptionMenu(self.frame_dict["Results"], self.result_sql_dict["SelectMove"], *self.poke_move, command=lambda event: self.display_move_description(event, self.result_sql_dict["Move"], self.result_sql_dict["MoveDescription"]))
        self.result_sql_dict["Move"].place(relx=0.78, rely=0.85, relwidth=0.1, relheight=0.04)
        self.result_sql_dict["MoveDescription"].config(state="disabled")
        
        self.result_sql_dict["NextImage"] = ImageTk.PhotoImage(Image.open("Pictures/right_arrow.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.result_sql_dict["Next"] = tk.Button(self.frame_dict["Results"], text="Next pokemon", width=20, height=5, image=self.result_sql_dict["NextImage"], compound="bottom", command=lambda: self.change_pokemon(True))
        self.result_sql_dict["Next"].place(relx=0.95, rely=0.33)
        
        self.result_sql_dict["PreviousImage"] = ImageTk.PhotoImage(Image.open("Pictures/left_arrow.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.result_sql_dict["Previous"] = tk.Button(self.frame_dict["Results"], text="Previous pokemon", width=20, height=5, image=self.result_sql_dict["PreviousImage"], compound="bottom", command=lambda: self.change_pokemon(False))
        self.result_sql_dict["Previous"].place(relx=0.05, rely=0.33)
        
        self.result_sql_dict["SelectEvolution"] = tk.StringVar(value="Evolution")
        self.result_sql_dict["ButtonEvolution"] = tk.OptionMenu(self.frame_dict["Results"], self.result_sql_dict["SelectEvolution"], *self.research_sql_dict["Evolution"], command=lambda event: self.go_to_evolution(self.result_sql_dict["ButtonEvolution"]))
        self.result_sql_dict["ButtonEvolution"].place(relx=0.85, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.result_sql_dict["SelectPreEvolution"] = tk.StringVar(value="Pre-evolution")
        self.result_sql_dict["ButtonPreEvolution"] = tk.OptionMenu(self.frame_dict["Results"], self.result_sql_dict["SelectPreEvolution"], *self.research_sql_dict["PreEvolution"], command=lambda event: self.go_to_evolution(self.result_sql_dict["ButtonPreEvolution"]))
        self.result_sql_dict["ButtonPreEvolution"].place(relx=0.85, rely=0.08, relwidth=0.1, relheight=0.04)

        self.filter_search_dict = dict()

        try:
            im = Image.open("Pictures/filter.jpg").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)

            im = ImageTk.PhotoImage(im)

            self.filter_search_dict["Background"] = tk.Label(self.frame_dict["SearchFilter"], image=im)
            self.filter_search_dict["Background"].image = im
            self.filter_search_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.filter_search_dict["Title"] = tk.Label(self.frame_dict["SearchFilter"], text="Search by filter",
                                                   font=("Arial", 36, "bold"), fg="black", bg="lightgrey",
                                                   borderwidth=2,
                                                   relief="solid")
        self.filter_search_dict["Title"].pack(pady=20)
        self.filter_search_dict["Button"] = []
        for i in range(12):
            self.filter_search_dict["Button"].append([self.create_filter_button(None, i, self.frame_dict["SearchFilter"], init=True)])

        self.filter_search_dict["Search"] = tk.Button(self.frame_dict["SearchFilter"], text="Search", width=20, height=1,
                                                     bg="lightgreen", command=self.search_by_filter
                                                     )
        self.filter_search_dict["Search"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)

        self.filter_search_dict["Deconnection"] = tk.Button(self.frame_dict["SearchFilter"], text="Return",
                                                           compound="top",
                                                           width=15, height=1, bg="#FF6347",
                                                           command=self.return_back)
        self.filter_search_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")

        self.image_select_dict = dict()
        try:
            im = Image.open("Pictures/ai_image.jpg").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)

            im = ImageTk.PhotoImage(im)

            self.image_select_dict["Background"] = tk.Label(self.frame_dict["SearchImage"], image=im)
            self.image_select_dict["Background"].image = im
            self.image_select_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.image_select_dict["Title"] = tk.Label(self.frame_dict["SearchImage"], text="Search by image",
                                                 font=("Arial", 36, "bold"), fg="black", bg="lightgrey", borderwidth=2,
                                                 relief="solid")
        self.image_select_dict["Title"].pack(pady=20)
        self.image_select_dict["ImageLabel"] = tk.Label(self.frame_dict["SearchImage"], text="Image selection")
        self.image_select_dict["ImageLabel"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        self.image_select_dict["Image"] = tk.Button(self.frame_dict["SearchImage"], text="Image selection", compound="top",
                                              command=lambda: self.get_image_path(self.image_select_dict["ImageLabel"],
                                                                                  self.image_select_dict["Image"]))
        self.image_select_dict["Image"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)

        self.image_select_dict["Search"] = tk.Button(self.frame_dict["SearchImage"], text="Search", width=20, height=1,
                                                     bg="lightgreen",
                                                     command=lambda: self.recognition_by_image(self.image_select_dict["Image"].cget("text")))
        self.image_select_dict["Search"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)

        self.image_select_dict["Deconnection"] = tk.Button(self.frame_dict["SearchImage"], text="Return",
                                                               compound="top",
                                                               width=15, height=1, bg="#FF6347",
                                                               command=self.return_back)
        self.image_select_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")

        self.search_selection_dict = dict()
        try:
            im = Image.open("Pictures/selection_choose.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)

            im = ImageTk.PhotoImage(im)

            self.search_selection_dict["Background"] = tk.Label(self.frame_dict["SearchSelection"], image=im)
            self.search_selection_dict["Background"].image = im
            self.search_selection_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.search_selection_dict["Title"] = tk.Label(self.frame_dict["SearchSelection"], text="Search your mode of selection",
                                                   font=("Arial", 36, "bold"), fg="black", bg="lightgrey",
                                                   borderwidth=2,
                                                   relief="solid")
        self.search_selection_dict["Title"].pack(pady=20)

        self.search_selection_dict["Name"] = tk.Button(self.frame_dict["SearchSelection"], text="Name", compound="top",
                                                   width=20, height=1, bg="#ffa500",
                                                   command=lambda: self.change_frame(self.frame_dict["SearchSelection"],
                                                                                     self.frame_dict["Research"]))
        self.search_selection_dict["Name"].place(relx=0.21, rely=0.46, anchor="center")
        self.search_selection_dict["Filter"] = tk.Button(self.frame_dict["SearchSelection"], text="Filter", compound="top",
                                                       width=20, height=1, bg="lightblue",
                                                       command=lambda: self.change_frame(
                                                           self.frame_dict["SearchSelection"],
                                                           self.frame_dict["SearchFilter"]))
        self.search_selection_dict["Filter"].place(relx=0.5, rely=0.72, anchor="center")

        self.search_selection_dict["Image"] = tk.Button(self.frame_dict["SearchSelection"], text="Image", compound="top",
                                                width=20, height=1, bg="#FFFF00",
                                                command=lambda: self.change_frame(self.frame_dict["SearchSelection"],
                                                                          self.frame_dict["SearchImage"])
                                                        )
        self.search_selection_dict["Image"].place(relx=0.79, rely=0.46, anchor="center")

        self.search_selection_dict["Deconnection"] = tk.Button(self.frame_dict["SearchSelection"], text="Return", compound="top",
                                                         width=15, height=1, bg="#FF6347", command=self.return_back)
        self.search_selection_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")

        self.type_efficaty_dict = dict()
        try:
            im = Image.open("Pictures/type.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)

            im = ImageTk.PhotoImage(im)

            self.type_efficaty_dict["Background"] = tk.Label(self.frame_dict["TypeEfficacity"], image=im)
            self.type_efficaty_dict["Background"].image = im
            self.type_efficaty_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.type_efficaty_dict["Title"] = tk.Label(self.frame_dict["TypeEfficacity"],
                                                       text=self.title_contribute("Type efficacity"),
                                                       font=("Arial", 36, "bold"), fg="black", bg="lightgrey",
                                                       borderwidth=2,
                                                       relief="solid")
        self.type_efficaty_dict["Title"].pack(pady=20)

        self.type_efficaty_dict["SelectType1"] = tk.StringVar(value="Attacker")

        self.type_efficaty_dict["Type1"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"], self.type_efficaty_dict["SelectType1"],
                                              *self.type_contribute_dict["Select"])
        self.type_efficaty_dict["Type1"].place(relx=0.3, rely=0.33, relwidth=0.1, relheight=0.04)

        self.type_efficaty_dict["SelectType2"] = tk.StringVar(value="Defender")

        self.type_efficaty_dict["Type2"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                         self.type_efficaty_dict["SelectType2"],
                                                         *self.type_contribute_dict["Select"])
        self.type_efficaty_dict["Type2"].place(relx=0.6, rely=0.33, relwidth=0.1, relheight=0.04)
        self.type_efficaty_dict["SelectType3"] = tk.StringVar(value="New attacker")

        self.type_efficaty_dict["Type3"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                         self.type_efficaty_dict["SelectType3"],
                                                         *self.type_contribute_dict["Select"])
        self.type_efficaty_dict["Type3"].place(relx=0.3, rely=0.66, relwidth=0.1, relheight=0.04)

        self.type_efficaty_dict["SelectType4"] = tk.StringVar(value="New defender")

        self.type_efficaty_dict["Type4"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                         self.type_efficaty_dict["SelectType4"],
                                                         *self.type_contribute_dict["Select"])
        self.type_efficaty_dict["Type4"].place(relx=0.6, rely=0.66, relwidth=0.1, relheight=0.04)

        self.type_efficaty_dict["SelectCoef1"] = tk.StringVar(value="Efficacity")

        self.type_efficaty_dict["Coef1"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                         self.type_efficaty_dict["SelectCoef1"],
                                                         *["Immune", "Resistant", "Efficient", "Very Efficient"])
        self.type_efficaty_dict["Coef1"].place(relx=0.4, rely=0.7, relwidth=0.1, relheight=0.04)



        self.type_efficaty_dict["Confirm"] = tk.Button(self.frame_dict["TypeEfficacity"], text="Confirm", width=20, height=1,
                                                     bg="lightgreen",
                                                     command=self.type_efficacity_change)
        self.type_efficaty_dict["Confirm"].place(relx=0.45, rely=0.92, relwidth=0.1, relheight=0.04)
        self.type_efficaty_dict["Deconnection"] = tk.Button(self.frame_dict["TypeEfficacity"], text="Return",
                                                               compound="top",
                                                               width=15, height=1, bg="#FF6347",
                                                               command=self.return_back)
        self.type_efficaty_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")

        self.type_select_dict = dict()
        try:
            im = Image.open("Pictures/type.png").convert("RGB")
            im = im.resize((1280, 680), Image.Resampling.LANCZOS)

            im = ImageTk.PhotoImage(im)

            self.type_select_dict["Background"] = tk.Label(self.frame_dict["TypeSelect"], image=im)
            self.type_select_dict["Background"].image = im
            self.type_select_dict["Background"].place(relwidth=1, relheight=1)
        except:
            pass
        self.type_select_dict["Title"] = tk.Label(self.frame_dict["TypeSelect"],
                                                    text="Type contribution",
                                                    font=("Arial", 36, "bold"), fg="black", bg="lightgrey",
                                                    borderwidth=2,
                                                    relief="solid")
        self.type_select_dict["Title"].pack(pady=20)

        self.type_select_dict["New type"] = tk.Button(self.frame_dict["TypeSelect"], text="Type management", compound="top",
                                                   width=20, height=1, bg="lightgreen",
                                                   command= lambda: self.change_frame_binary(self.frame_dict["ContribType"], self.type_contribute_dict, "Type"))
        self.type_select_dict["New type"].place(relx=0.35, rely=0.9, anchor="center")

        self.type_select_dict["Efficacity"] = tk.Button(self.frame_dict["TypeSelect"], text="Type efficacity",
                                                      compound="top",
                                                      width=20, height=1, bg="lightgreen",
                                                      command=lambda: self.change_frame(self.frame_dict["TypeSelect"],
                                                                                        self.frame_dict["TypeEfficacity"]))
        self.type_select_dict["Efficacity"].place(relx=0.65, rely=0.9, anchor="center")

        self.type_select_dict["Deconnection"] = tk.Button(self.frame_dict["TypeSelect"], text="Return",
                                                            compound="top",
                                                            width=15, height=1, bg="#FF6347",
                                                            command=self.return_back)
        self.type_select_dict["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
    #%% Methods
    def get_image_path(self, label, button):
        path = filedialog.askopenfilename(
            title="Select the design of your pokemon",
            filetypes=[("Images Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            label.config(text=path)
            button.config(text=path)
        else:
            label.config(text="")
            button.config(text="Select an image")
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
        self.update_button()
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
        sql = "SELECT id FROM Connections WHERE login=%s LIMIT 1"
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
        sql = "SELECT id, login, password FROM Connections WHERE login=%s AND password=%s LIMIT 1"
        param1 = self.login_dict["Login"].get()
        param2 = self.login_dict["Password"].get()
        if param1 and param2:
            params = (param1,param2)
            self.mycursor.execute(sql, params)
            result = list(self.mycursor.fetchall())
            if any(map(lambda v: v[1]==param1 and v[2]==param2, result)):
                for p,x,y in result:
                    if (x,y) == params:
                        self.id = p
                        break
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
        self.pokemon_move_contribute_dict["Title"].config(text=self.title_contribute("Pokemon move"))
        self.pokemon_evolution_contribute_dict["Title"].config(text=self.title_contribute("Pokemon evolution"))
        self.pokemon_ability_contribute_dict["Title"].config(text=self.title_contribute("Pokemon ability"))
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
            env["Delete"] = tk.OptionMenu(name[i][2], env["Select2"], *env["SelectUse"])
            env["Delete"].place(relx=0.5, rely=0.45, relwidth=0.1, relheight=0.04)
            env["Update1"].destroy()
            env["Update1"] = tk.OptionMenu(name[i][2], env["Select1"], *env["SelectUse"])
            if desc:
                env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
            else:
                env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
            self.change_frame_binary(name[i][2], env, name[i][0], change=False, desc=name[i][3])
            i += 1        
        dictionaries = [self.pokemon_move_contribute_dict,
                        self.pokemon_evolution_contribute_dict,
                        self.pokemon_ability_contribute_dict,
        ]
        frame = [self.frame_dict["ContribPokemonMove"],
                 self.frame_dict["ContribPokemonEvolution"],
                 self.frame_dict["ContribPokemonAbility"]
        ]
        i = 0
        for env in dictionaries:
            if i == 2:
                n = "Select an ability"
                n2 = "Select a new ability"
            elif i == 1:
                n = "Select an evolution"
                n2 = "Select a new evolution"
            elif i == 0:
                n = "Select a move"
                n2 = "Select a new move"
            else:
                n = "An error occured"
                n2 = "An error occured"
            #"""
            env["ChooseStr"].set("Select a pokemon")
            env["Choose"].destroy()
            env["Choose"] = tk.OptionMenu(frame[i], env["ChooseStr"], *self.pokemon_contribute_dict["Select"])
            env["Choose"].place(relx=0.26, rely=0.5, relwidth=0.1, relheight=0.04)
            env["ChooseStr2"].set(n)
            env["Choose2"].destroy()
            env["Choose2"] = tk.OptionMenu(frame[i], env["ChooseStr2"], "")
            env["Choose2"].place(relx=0.64, rely=0.5, relwidth=0.1, relheight=0.04)
            #"""

            if self.mode == Mode.UPDATE:
                env["Choose3"].destroy()
                env["ChooseStr3"].set(n2)
                env["Choose3"] = tk.OptionMenu(frame[i], env["ChooseStr3"], "")
                env["Choose3"].place(relx=0.45, rely=0.58, relwidth=0.1, relheight=0.04)
                env["Apply"].config(bg="lightblue")
            else:
                env["Choose3"].place_forget()
                if self.mode == Mode.ADD:
                    env["Apply"].config(bg="lightgreen")
                else:
                    env["Apply"].config(bg="#ffa500")
            i += 1
        self.pokemon_add["SelectType1"].set(value="Type 1")
        self.pokemon_add["SelectType2"].set(value="Type 2")
        self.pokemon_add["SelectTier"].set(value="Tier")
        
        self.pokemon_update["SelectPokemon"].set(value="Pokemon")
        
        self.pokemon_update["SelectType1"].set(value="Type 1")
        self.pokemon_update["SelectType2"].set(value="Type 2")
        self.pokemon_update["SelectTier"].set(value="Tier")
        self.pokemon_delete["SelectPokemon"].set(value="Pokemon")

        self.type_efficaty_dict["SelectType1"].set(value="Attacker")
        self.type_efficaty_dict["Type1"].destroy()
        self.type_efficaty_dict["Type1"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                         self.type_efficaty_dict["SelectType1"],
                                                         *self.type_contribute_dict["Select"])
        self.type_efficaty_dict["Type1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)

        self.type_efficaty_dict["SelectType2"].set(value="Defender")
        self.type_efficaty_dict["Type2"].destroy()
        self.type_efficaty_dict["Type2"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                         self.type_efficaty_dict["SelectType2"],
                                                         *self.type_contribute_dict["Select"])
        self.type_efficaty_dict["Type2"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
        self.type_efficaty_dict["SelectType3"].set(value="New attacker")
        self.type_efficaty_dict["SelectType4"].set(value="New defender")
        self.type_efficaty_dict["Type3"].place_forget()
        self.type_efficaty_dict["Type4"].place_forget()
        if self.mode == Mode.UPDATE:
            self.type_efficaty_dict["Confirm"].config(bg="lightblue")
            self.type_efficaty_dict["Type3"].destroy()
            self.type_efficaty_dict["Type4"].destroy()
            self.type_efficaty_dict["Type3"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                             self.type_efficaty_dict["SelectType3"],
                                                             *self.type_contribute_dict["Select"])
            self.type_efficaty_dict["Type3"].place(relx=0.2, rely=0.66, relwidth=0.1, relheight=0.04)

            self.type_efficaty_dict["Type4"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                             self.type_efficaty_dict["SelectType4"],
                                                             *self.type_contribute_dict["Select"])
            self.type_efficaty_dict["Type4"].place(relx=0.7, rely=0.66, relwidth=0.1, relheight=0.04)
        elif self.mode == Mode.ADD:
            self.type_efficaty_dict["Confirm"].config(bg="lightgreen")
        else:
            self.type_efficaty_dict["Confirm"].config(bg="#ffa500")
        self.type_efficaty_dict["SelectCoef1"].set(value="Efficacity")
        self.type_efficaty_dict["Coef1"].place_forget()
        self.type_efficaty_dict["Title"].config(text=self.title_contribute("Type efficacity"))
        if self.mode != Mode.DELETE:
            self.type_efficaty_dict["Coef1"].destroy()
            self.type_efficaty_dict["Coef1"] = tk.OptionMenu(self.frame_dict["TypeEfficacity"],
                                                             self.type_efficaty_dict["SelectCoef1"],
                                                             *["Immune", "Resist", "Efficient", "Very efficient"])
            self.type_efficaty_dict["Coef1"].place(relx=0.45, rely=0.7, relwidth=0.1, relheight=0.04)

        for i in range(12):
            while len(self.filter_search_dict["Button"][i]) > 0:
                b = self.filter_search_dict["Button"][i].pop()
                b.destroy()
        for i in range(12):
            self.filter_search_dict["Button"][i].append(self.create_filter_button(None, i, self.frame_dict["SearchFilter"], init=True))
    def get_binary(self, name, admin):
        sql = "SELECT name FROM " + name +" WHERE id_login=%s"
        if admin:
            sql += " OR id_login=1"
        sql += " ORDER BY name"
        params = (self.id,)
        self.mycursor.execute(sql, params)
        tiers = self.mycursor.fetchall()
        tiers = list(tiers)
        return [t[0] for t in tiers]
    
    def create_binary(self, env, frame, name, table_name, description=False):
        sentence = "Enter the " + name.lower() + " name"
        
        env["Title"] = tk.Label(frame, text=self.title_contribute(name), font=("Arial",36, "bold"), fg="black", bg="lightgrey", borderwidth=2, relief="solid")
        env["Title"].pack(pady=20)
        env["Deconnection"] = tk.Button(frame, text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        env["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
        env["Add"] =  tk.Entry(frame, width=35, fg="gray")
        if description:
            env["Add"].place(relx=0.25, rely=0.5, relwidth=0.1, relheight=0.04)
        else:
            env["Add"].place(relx=0.45, rely=0.4, relwidth=0.1, relheight=0.04)
        env["Add"].insert(0, sentence)
        env["Add"].bind("<FocusIn>", lambda event: self.fill_entry(event, env["Add"],sentence, False))
        env["Add"].bind("<FocusOut>",  lambda event: self.clear_entry(event, env["Add"],sentence))
        
        env["Select1"] = tk.StringVar(value="Old " + name.lower())
        
        env["Select2"] = tk.StringVar(value="New " + name.lower())
        env["Select"] = self.get_binary(table_name, True)
        env["Select"].insert(0, "None")
        env["SelectUse"] = self.get_binary(table_name, False)
        env["SelectUse"].insert(0, "None")
       
        #env["Select1"].set("None")
        
        #env["Select2"].set("None")
        
        env["Update1"] = tk.OptionMenu(frame, env["Select1"], *env["SelectUse"])
        if description:
            env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
        else:
            env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
        
        env["Update2"] =  tk.Entry(frame, width=35, fg="gray")
        if description:
            env["Update2"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
        else:
            env["Update2"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        env["Update2"].insert(0, sentence)
        env["Update2"].bind("<FocusIn>", lambda event: self.fill_entry(event, env["Update2"],sentence, False))
        env["Update2"].bind("<FocusOut>",  lambda event: self.clear_entry(event, env["Update2"],sentence))
        
        
        env["Delete"] = tk.OptionMenu(frame, env["Select2"], *env["SelectUse"])
        env["Delete"].place(relx=0.45, rely=0.4, relwidth=0.1, relheight=0.04)
        if description:
            desc = "Enter a description"
            env["Description"] =  tk.Entry(frame, width=35, fg="gray")
            if self.mode == Mode.ADD:
                env["Description"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
            else:
                env["Description"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
            env["Description"].insert(0, desc)
            env["Description"].bind("<FocusIn>", lambda event: self.fill_entry(event, env["Description"],desc, False))
            env["Description"].bind("<FocusOut>",  lambda event: self.clear_entry(event, env["Description"],desc))
            
        env["Confirm"] = tk.Button(frame, text="Confirm", width=20, height=1, bg="lightgreen", command=lambda: self.contribute_binary(name, table_name, env, desc=description))
        env["Confirm"].place(relx=0.45, rely=0.92, relwidth=0.1, relheight=0.04)
        
    def change_frame_binary(self, frame, env, name, change=True, desc=False):
        if self.mode == Mode.ADD:
            env["Confirm"].config(bg="lightgreen")
            if desc:
                env["Description"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Add"].place(relx=0.25, rely=0.5, relwidth=0.1, relheight=0.04)
            else:
                env["Add"].place(relx=0.45, rely=0.4, relwidth=0.1, relheight=0.04)
                
            
            env["Delete"].place_forget()
            
            env["Update1"].place_forget()
            env["Update2"].place_forget()
        elif self.mode == Mode.DELETE:
            env["Confirm"].config(bg="#ffa500")
           
            env["Delete"].place(relx=0.45, rely=0.4, relwidth=0.1, relheight=0.04)
            env["Add"].place_forget()
            if desc:
                env["Description"].place_forget()
            
            env["Update1"].place_forget()
            env["Update2"].place_forget()
        elif self.mode == Mode.UPDATE:
            env["Confirm"].config(bg="lightblue")
            
            env["Delete"].place_forget()
            env["Add"].place_forget()
            if desc:
  
                env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Update2"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
                env["Description"].place(relx=0.7, rely=0.5, relwidth=0.1, relheight=0.04)
            else:
                
                env["Update1"].place(relx=0.2, rely=0.5, relwidth=0.1, relheight=0.04)
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
            if frame != self.frame_dict["ContribType"]:
                self.change_frame(self.frame_dict["SelectContribution"], frame)
            else:
                self.change_frame(self.frame_dict["TypeSelect"], frame)
    
    
    
    def contribute_binary(self, name, table_name, env, desc=False):
        sentence = "Enter the " + name.lower() + " name"
        if self.mode == Mode.ADD:
            if desc:
                sql = "INSERT INTO " + table_name + " (name,description,id_login) VALUES (%s,%s,%s)"
                d = env["Description"].get()
                
            else:
                sql = "INSERT INTO " + table_name + " (name,id_login) VALUES (%s,%s)"
            name = env["Add"].get()
            
            if name != "" and name != sentence:
                if desc:
                    if d == "Enter a description":
                        d = ""
                    
                    params = (name, d, self.id)
                else:
                    params = (name, self.id)
                self.mycursor.execute(sql, params)
                self.mydb.commit()
                #env["Confirm"].config(text="Creation success")
                self.play_sound("Sound/good.mp3")
            else:
                #env["Confirm"].config(text="Please enter a name")
                self.play_sound("Sound/not_good.mp3")
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

            if nami != "None" and ((nami2 != "" and nami2 != sentence) or desc):
                
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
                    #env["Confirm"].config(text="Update success")
                    self.play_sound("Sound/good.mp3")
                else:
                    #env["Confirm"].config(text="Please select a good " + name.lower())
                    self.play_sound("Sound/not_good.mp3")
            else:
                #env["Confirm"].config(text="Please select a good " + name.lower())
                self.play_sound("Sound/not_good.mp3")
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
                    #env["Confirm"].config(text="Delete success")
                    self.play_sound("Sound/good.mp3")
                else:
                    #env["Confirm"].config(text="Please select a good " + name.lower())
                    self.play_sound("Sound/not_good.mp3")
            else:
                #env["Confirm"].config(text="Please select a good " + name.lower())
                self.play_sound("Sound/not_good.mp3")
            
        else:
            pass
        env["Select1"].set("None")
        env["Select2"].set("None")
        env["Select"] = self.get_binary(table_name, True)
        env["SelectUse"] = self.get_binary(table_name, False)
        env["Select"].insert(0,"None")
        env["SelectUse"].insert(0, "None")
        env["Select1"] = tk.StringVar(value="Old " + name.lower())
        
        env["Select2"] = tk.StringVar(value="New " + name.lower())
        self.update_button()
        
    def create_move(self):
        sql = "INSERT INTO Moves (name,type,category,power,pp,accuracy,description,id_login) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
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
                    #self.move_add["Create"].config(text="Power or PP issue")
                    self.play_sound("Sound/not_good.mp3")
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
                        
                        #self.move_add["Create"].config(text="Creation success")
                        self.play_sound("Sound/good.mp3")
            except:
                #self.move_add["Create"].config(text="Value issue")
                self.play_sound("Sound/not_good.mp3")
                
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
        self.move_add["Priority"].insert(0, "Enter the accuracy")
        self.move_add["Priority"].config(fg="gray")
        
        self.move_add["Description"].delete(0, tk.END)
        self.move_add["Description"].insert(0, "Enter a description")
        self.move_add["Description"].config(fg="gray")
        
        self.move_add["SelectType"].set(value="Type")
        self.move_add["Type"].destroy()
        self.move_add["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectType"], *self.type_contribute_dict["Select"])
        self.move_add["Type"].place(relx=0.35, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_add["SelectCategory"].set(value="Category")
        self.move_add["Category"].destroy()
        self.move_add["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectCategory"], *self.category_contribute_dict["Select"])
        self.move_add["Category"].place(relx=0.55, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.update_button()
    
    def delete_move(self):
        sql = "DELETE FROM Moves WHERE id=%s"
        
        name = self.move_delete["Move"].cget("text")
        if name == "None":
            #self.move_delete["Delete"].config(text="Wrong move")
            self.play_sound("Sound/not_good.mp3")
        else:
            sql_id = "SELECT id FROM Moves WHERE name=%s LIMIT 1"
            self.mycursor.execute(sql_id, (name,))
            id1 = self.mycursor.fetchall()
            if len(id1) > 0:
                self.mycursor.execute(sql, (id1[0][0],))
                self.mydb.commit()
                #self.move_delete["Delete"].config(text="Delete success")
                self.play_sound("Sound/good.mp3")
            else:
                #self.move_delete["Delete"].config(text="Wrong move")
                self.play_sound("Sound/not_good.mp3")
        self.move_delete["Move"].destroy()
        self.move_delete["Move"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_delete["SelectMove"], *self.move_contribute_dict["SelectUse"])
        self.move_delete["Move"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        self.update_button()
        
    def update_move(self, origin):
        sql = "UPDATE Moves SET name=%s,type=%s,category=%s,power=%s,pp=%s,accuracy=%s,description=%s  WHERE name=%s"
        name = self.move_update["Name"].get()
        type1 = self.move_update["Type"].cget("text")
        
        category = self.move_update["Category"].cget("text")
        
        power = self.move_update["Power"].get()
        pp = self.move_update["PP"].get()
        priority = self.move_update["Priority"].get()
        description = self.move_update["Description"].get()
        
        if type1 == "None" or category == "None":
            #self.move_update["Update"].config(text="Missing values")
            self.play_sound("Sound/not_good.mp3")
        else:
            try:
                power = int(power)
                pp = int(pp)
                priority = int(priority)
                if description == "" or description == 'Enter a description':
                    description = ""
                if power < 0 or pp <= 0:
                    #self.move_update["Update"].config(text="Power or PP issue")
                    self.play_sound("Sound/not_good.mp3")
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
                        #self.move_update["Update"].config(text="Update success")
                        self.play_sound("Sound/good.mp3")
                    else:
                        #self.move_update["Update"].config(text="Value issue")
                        self.play_sound("Sound/not_good.mp3")
            except:
                #self.move_update["Update"].config(text="Value issue")
                self.play_sound("Sound/not_good.mp3")
                
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
        self.move_update["Priority"].insert(0, "Enter the accuracy")
        self.move_update["Priority"].config(fg="gray")
        
        self.move_update["Description"].delete(0, tk.END)
        self.move_update["Description"].insert(0, "Enter a description")
        self.move_update["Description"].config(fg="gray")
        
        self.move_update["SelectType"].set(value="Type")
        self.move_update["SelectCategory"].set(value="Category")
        self.move_update["Category"].destroy()
        self.move_update["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectCategory"], *self.category_contribute_dict["Select"])
        self.move_update["Category"].place(relx=0.55, rely=0.33, relwidth=0.1, relheight=0.04)
        
        self.move_update["Type"].destroy()
        self.move_update["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectType"], *self.type_contribute_dict["Select"])
        self.move_update["Type"].place(relx=0.35, rely=0.33, relwidth=0.1, relheight=0.04)
        self.move_delete["Move"].destroy()
        self.move_delete["Move"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_delete["SelectMove"],
                                                 *self.move_contribute_dict["SelectUse"])
        self.move_delete["Move"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        self.update_button()   
        
    def change_frame_move(self):
        self.move_contribute_dict["SelectUse"] = self.get_binary("Moves", False)
        self.move_contribute_dict["Select"] = self.get_binary("Moves", True)
        self.move_contribute_dict["Select"].insert(0, "None")
        self.move_contribute_dict["SelectUse"].insert(0, "None")
        if self.mode == Mode.ADD:
        
            self.move_add["Name"].place(relx=0.15, rely=0.33, relwidth=0.1, relheight=0.04)        
            
            self.move_add["Type"].destroy()
            self.move_add["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectType"], *self.type_contribute_dict["Select"])
            self.move_add["Type"].place(relx=0.35, rely=0.33, relwidth=0.1, relheight=0.04)  
            
            self.move_add["Category"].destroy()
            self.move_add["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_add["SelectCategory"], *self.category_contribute_dict["Select"])
            self.move_add["Category"].place(relx=0.55, rely=0.33, relwidth=0.1, relheight=0.04)     
            self.move_add["Power"].place(relx=0.75, rely=0.33, relwidth=0.1, relheight=0.04)         
            self.move_add["PP"].place(relx=0.2, rely=0.66, relwidth=0.1, relheight=0.04) 
            self.move_add["Priority"].place(relx=0.45, rely=0.66, relwidth=0.1, relheight=0.04)
            self.move_add["Description"].place(relx=0.7, rely=0.66, relwidth=0.1, relheight=0.04)
            self.move_add["Create"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
            for key in self.move_delete.keys():
                if not isinstance(self.move_delete[key], tk.StringVar):
                    self.move_delete[key].place_forget()
            for key in self.move_update.keys():
                if not isinstance(self.move_update[key], tk.StringVar):
                    self.move_update[key].place_forget()
        elif self.mode == Mode.DELETE:
            self.move_delete["Move"].destroy()
            self.move_delete["Move"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_delete["SelectMove"], *self.move_contribute_dict["SelectUse"])
            self.move_delete["Move"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            self.move_delete["Delete"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)

            for key in self.move_add.keys():
                if not isinstance(self.move_add[key], tk.StringVar):
                    self.move_add[key].place_forget()
            for key in self.move_update.keys():
                if not isinstance(self.move_update[key], tk.StringVar):
                    self.move_update[key].place_forget()
        elif self.mode == Mode.UPDATE:
            self.move_update["Name"].place(relx=0.15, rely=0.33, relwidth=0.1, relheight=0.04)        
            
            self.move_update["Type"].destroy()
            self.move_update["Type"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectType"], *self.type_contribute_dict["Select"])
            self.move_update["Type"].place(relx=0.35, rely=0.33, relwidth=0.1, relheight=0.04)  
            
            self.move_update["Category"].destroy()
            self.move_update["Category"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_update["SelectCategory"], *self.category_contribute_dict["Select"])
            self.move_update["Category"].place(relx=0.55, rely=0.33, relwidth=0.1, relheight=0.04)     
            self.move_update["Power"].place(relx=0.75, rely=0.33, relwidth=0.1, relheight=0.04)         
            self.move_update["PP"].place(relx=0.2, rely=0.66, relwidth=0.1, relheight=0.04) 
            self.move_update["Priority"].place(relx=0.45, rely=0.66, relwidth=0.1, relheight=0.04)
            self.move_update["Description"].place(relx=0.7, rely=0.66, relwidth=0.1, relheight=0.04)
            self.move_update["Update"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
            self.move_delete["Move"].destroy()
            self.move_delete["Move"] = tk.OptionMenu(self.frame_dict["ContribMove"], self.move_delete["SelectMove"], *self.move_contribute_dict["SelectUse"])
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
        self.pokemon_update["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType1"], *self.type_contribute_dict["Select"])
        self.pokemon_update["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Type2"].destroy()
        self.pokemon_update["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType2"], *self.type_contribute_dict["Select"])
        self.pokemon_update["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Tier"].destroy()
        self.pokemon_update["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectTier"], *self.tier_contribute_dict["Select"])
        self.pokemon_update["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Choose"].destroy()
        self.pokemon_update["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"])
        self.pokemon_update["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_delete["Choose"].destroy()
        self.pokemon_delete["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_delete["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"])
        self.pokemon_delete["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Type1"].destroy()
        self.pokemon_add["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType1"], *self.type_contribute_dict["Select"])
        self.pokemon_add["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Type2"].destroy()
        self.pokemon_add["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType2"], *self.type_contribute_dict["Select"])
        self.pokemon_add["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Tier"].destroy()
        self.pokemon_add["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectTier"], *self.tier_contribute_dict["Select"])
        self.pokemon_add["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        if self.mode == Mode.ADD:
            
            
            self.pokemon_add["NID"].place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.04)
           
            self.pokemon_add["Name"].place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.04)
            
            
            
            self.pokemon_add["Image"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)

           
           
            self.pokemon_add["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
         
          
        
            self.pokemon_add["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)

            
            
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
            
            
            
           
            self.pokemon_update["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)
            
            
            
            self.pokemon_update["NID"].place(relx=0.1, rely=0.2, relwidth=0.1, relheight=0.04)
            
            self.pokemon_update["Name"].place(relx=0.1, rely=0.5, relwidth=0.1, relheight=0.04)
           
            
          
          
            self.pokemon_update["Image"].place(relx=0.1, rely=0.8, relwidth=0.1, relheight=0.04)
            
            
            
            
            
            
            
            
            self.pokemon_update["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
            
          
            
            self.pokemon_update["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
            

           
            
            
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
                        #self.pokemon_add["Create"].config(text="Creation success")
                        self.play_sound("Sound/good.mp3")
                    else:
                        #self.pokemon_add["Create"].config(text="Type or tier error")
                        self.play_sound("Sound/not_good.mp3")
                else:
                    #self.pokemon_add["Create"].config(text="Value error")
                    self.play_sound("Sound/not_good.mp3")
            except:
                #self.pokemon_add["Create"].config(text="Wrong format value")
                self.play_sound("Sound/not_good.mp3")
        else:    
            #self.pokemon_add["Create"].config(text="Type problem")
            self.play_sound("Sound/not_good.mp3")
            
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
        self.pokemon_add["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType1"], *self.type_contribute_dict["Select"])
        self.pokemon_add["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Type2"].destroy()
        self.pokemon_add["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectType2"], *self.type_contribute_dict["Select"])
        self.pokemon_add["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_add["Tier"].destroy()
        self.pokemon_add["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_add["SelectTier"], *self.tier_contribute_dict["Select"])
        self.pokemon_add["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        self.pokemon_add["Image"].config(text="Image selection")
        
                
    def delete_pokemon(self):
        sql = "DELETE FROM Pokemons WHERE name=%s AND id_login=%s"
        name = self.pokemon_delete["Choose"].cget("text")
        try:
            self.mycursor.execute(sql, (name,self.id))
            self.mydb.commit()
            #self.pokemon_delete["Delete"].config(text="Delete success")
            self.play_sound("Sound/good.mp3")
        except:
            #self.pokemon_delete["Delete"].config(text="Name error")
            self.play_sound("Sound/not_good.mp3")
            
        self.update_button()
        
        self.pokemon_delete["Choose"].destroy()
        self.pokemon_delete["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_delete["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"])
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
                        #self.pokemon_update["Update"].config(text="Creation success")
                        self.play_sound("Sound/good.mp3")
                    else:
                         #self.pokemon_update["Update"].config(text="Type or tier error")
                         self.play_sound("Sound/not_good.mp3")
                else:
                    #self.pokemon_update["Update"].config(text="Value error")
                    self.play_sound("Sound/not_good.mp3")
            except:
                #self.pokemon_update["Update"].config(text="Wrong format value")
                self.play_sound("Sound/not_good.mp3")
        else:    
            #self.pokemon_update["Update"].config(text="Type problem")
            self.play_sound("Sound/not_good.mp3")
            
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
        self.pokemon_update["Type1"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType1"], *self.type_contribute_dict["Select"])
        self.pokemon_update["Type1"].place(relx=0.3, rely=0.2, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Type2"].destroy()
        self.pokemon_update["Type2"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectType2"], *self.type_contribute_dict["Select"])
        self.pokemon_update["Type2"].place(relx=0.3, rely=0.5, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Tier"].destroy()
        self.pokemon_update["Tier"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectTier"], *self.tier_contribute_dict["Select"])
        self.pokemon_update["Tier"].place(relx=0.3, rely=0.8, relwidth=0.1, relheight=0.04)
        
        self.pokemon_update["Choose"].destroy()
        self.pokemon_update["Choose"] = tk.OptionMenu(self.frame_dict["ContribPokemon"], self.pokemon_update["SelectPokemon"], *self.pokemon_contribute_dict["SelectUse"])
        self.pokemon_update["Choose"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)

        self.pokemon_update["Image"].config(text="Image selection")
    def update_selection_box(self, env, caracteristic, op=False):
        
        val = env["Choose"].cget("text")
        if caracteristic == PokemonCaracteristic.ABILITY:
            if self.mode == Mode.ADD:
                s = "(id_login= 1 OR id_login=%s)"
            elif not op:
                s = "PA.id_login=%s"
            else:
                s = "id_login=%s"
            if self.mode == Mode.ADD or op:
                sql = "SELECT name FROM Abilities WHERE id not in (SELECT A.id FROM PokemonAbilities AS PA JOIN Pokemons AS P ON PA.id_pokemon = P.id JOIN Abilities AS A ON A.id = PA.id_ability WHERE P.name=%s) AND " + s
            else:
                sql = "SELECT A.name FROM PokemonAbilities AS PA JOIN Pokemons AS P ON PA.id_pokemon = P.id JOIN Abilities AS A ON A.id = PA.id_ability WHERE P.name=%s AND " + s
                
            if op:
   
                sql += " AND name!=%s"
  
                param = (val, self.id,env["Choose2"].cget("text"))
            else:
                param = (val,self.id)
            if self.mode == Mode.ADD or op:
                sql += " ORDER BY name"
            else:
                sql += " ORDER BY A.name"
            self.mycursor.execute(sql, param)
            l = self.mycursor.fetchall()
            l = list(l)
            l = [v[0] for v in l]
        elif caracteristic == PokemonCaracteristic.EVOLUTION:
            if self.mode == Mode.ADD:
                s = "(id_login= 1 OR id_login=%s)"
            elif not op:
                s = "E.id_login=%s"
            else:
                s = "id_login=%s"
            if self.mode == Mode.ADD or op:
                sql = "SELECT name FROM Pokemons WHERE id not in (SELECT P2.id FROM Evolutions AS E JOIN Pokemons AS P1 ON E.id_base = P1.id JOIN Pokemons AS P2 ON P2.id = E.id_evolution WHERE P1.name=%s) AND name!=%s AND " + s
            else:
                sql = "SELECT P2.name FROM Evolutions AS E JOIN Pokemons AS P1 ON E.id_base = P1.id JOIN Pokemons AS P2 ON P2.id = E.id_evolution WHERE P1.name=%s  AND " + s
            if op:
               
                    sql += " AND name!=%s"
                    param = (val, val, self.id, env["Choose2"].cget("text"))
      
            else:
                if self.mode == Mode.ADD:
                    param = (val, val, self.id)
                else:
                    param = (val, self.id)
            if self.mode == Mode.ADD or op:
                sql += " ORDER BY name"
            else:
                sql += " ORDER BY P2.name"
            self.mycursor.execute(sql, param)
            l = self.mycursor.fetchall()
            l = list(l)
            l = [v[0] for v in l]
        elif caracteristic == PokemonCaracteristic.MOVE:
            if self.mode == Mode.ADD:
                s = "(id_login= 1 OR id_login=%s)"
            
            elif not op:
                s = "PM.id_login=%s"
            else:
                s = "id_login=%s"
                
            if self.mode == Mode.ADD or op:  
                sql = "SELECT name FROM Moves WHERE id not in (SELECT M.id FROM PokemonMoves AS PM JOIN Pokemons AS P ON PM.id_pokemon = P.id JOIN Moves AS M ON M.id = PM.id_move WHERE P.name=%s) AND " + s
            else:
                sql = "SELECT M.name FROM PokemonMoves AS PM JOIN Pokemons AS P ON PM.id_pokemon = P.id JOIN Moves AS M ON M.id = PM.id_move WHERE P.name=%s AND " + s
            if op:
              
                    sql += " AND name!=%s"
                    param = (val, self.id, env["Choose2"].cget("text"))
            else:
                param = (val, self.id)
            if self.mode == Mode.ADD or op:
                sql += " ORDER BY name"
            else:
                sql += " ORDER BY M.name"
            self.mycursor.execute(sql, param)
            l = self.mycursor.fetchall()
            l = list(l)
            l = [v[0] for v in l]
        else:
            l = []
        
        if op:
            env["Choose3"]['menu'].delete(0, 'end')
            for option in l:
                env["Choose3"]['menu'].add_command(label=option, command=tk._setit(env["ChooseStr3"], option))
            env["ChooseStr3"].set(l[0] if l else "No options")
        else:
            env["Choose2"]['menu'].delete(0, 'end')
            for option in l:
                env["Choose2"]['menu'].add_command(label=option, command=tk._setit(env["ChooseStr2"], option))
            env["ChooseStr2"].set(l[0] if l else "No options")
           
    def create_pokemon_carateristic(self, env, frame, caracteristic):
        env["ChooseStr"] =  tk.StringVar(value="Select a pokemon")
        
        env["ChooseStr"].trace_add("write", lambda *args: self.update_selection_box(env, caracteristic))
        
        
        env["Choose"] = tk.OptionMenu(frame, env["ChooseStr"], *self.pokemon_contribute_dict["Select"])
        env["Choose"].place(relx=0.26, rely=0.5, relwidth=0.1, relheight=0.04)
        
        if caracteristic == PokemonCaracteristic.ABILITY:
            n = "Select an ability"
            n2 = "Select a new ability"
        elif caracteristic == PokemonCaracteristic.EVOLUTION:
            n = "Select a pokemon"
            n2 = "Select a new pokemon"
        elif caracteristic == PokemonCaracteristic.MOVE:
            n = "Select a move"
            n2 = "Select a new move"
        else:
            n = "An error occured"
            n2 = "An error occured"
            
        env["ChooseStr2"] =  tk.StringVar(value=n)
        
        env["ChooseStr2"].trace_add("write", lambda *args: self.update_selection_box(env, caracteristic, True))
        
        env["Choose2"] = tk.OptionMenu(frame, env["ChooseStr2"], "")
        env["Choose2"].place(relx=0.64, rely=0.5, relwidth=0.1, relheight=0.04)
        
        
        env["ChooseStr3"] =  tk.StringVar(value=n2)
        
        env["Choose3"] = tk.OptionMenu(frame, env["ChooseStr3"], "")
        env["Choose3"].place(relx=0.45, rely=0.7, relwidth=0.1, relheight=0.04)
        
        
        env["Apply"] = tk.Button(frame, text="Apply change", command=lambda: self.apply_pokemon_carateristic(env, frame, caracteristic))
        env["Apply"].place(relx=0.45, rely=0.9, relwidth=0.1, relheight=0.04)
        
        
        env["Deconnection"] = tk.Button(frame, text="Return", compound="top", width=15, height=1, bg="#FF6347", command=self.return_back)
        env["Deconnection"].place(relx=0.95, rely=0.97, anchor="center")
    
    def apply_pokemon_carateristic(self, env, frame, caracteristic):
        match self.mode:
            case Mode.ADD:
                match caracteristic:
                    case PokemonCaracteristic.ABILITY:
                        t = "PokemonAbilities"
                        t2 = "Abilities"
                        v1 = "id_pokemon"
                        v2 = "id_ability"
                    case PokemonCaracteristic.EVOLUTION:
                        t = "Evolutions"
                        t2 = "Pokemons"
                        v1 = "id_base"
                        v2 = "id_evolution"
                    case PokemonCaracteristic.MOVE:
                        t = "PokemonMoves"
                        t2 = "Moves"
                        v1 = "id_pokemon"
                        v2 = "id_move"
                    case _:
                        t = ""
                        v1 = ""
                        v2 = ""
                sql = "INSERT INTO " + t + " (" + v1 + "," + v2 + ",id_login) VALUES (%s,%s,%s)"
                p1 = env["Choose"].cget("text")
                p2 = env["Choose2"].cget("text")
                sql1 = "SELECT id FROM Pokemons WHERE name=%s LIMIT 1"
                self.mycursor.execute(sql1, (p1,))
                p1 = self.mycursor.fetchall()
                sql2 = "SELECT id FROM " + t2 +" WHERE name=%s LIMIT 1"
                self.mycursor.execute(sql2, (p2,))
                p2 = self.mycursor.fetchall()
                if len(p1) > 0 and len(p2) > 0:
                    p1 = p1[0][0]
                    p2 = p2[0][0]
                    params = (p1, p2, self.id)
                    
                    self.mycursor.execute(sql, params)
                    self.mydb.commit()
                    #env["Apply"].config(text="Creation success")
                    self.play_sound("Sound/good.mp3")
                else:
                    #env["Apply"].config(text="Select all the field")
                    self.play_sound("Sound/not_good.mp3")
                env["Choose3"].destroy()
                env["Choose3"] = tk.OptionMenu(frame, env["ChooseStr3"], "")
                env["Choose3"].place(relx=0.45, rely=0.7, relwidth=0.1, relheight=0.04)
            case Mode.UPDATE:
                match caracteristic:
                    case PokemonCaracteristic.ABILITY:
                        t = "PokemonAbilities"
                        t2 = "Abilities"
                        v1 = "id_pokemon"
                        v2 = "id_ability"
                    case PokemonCaracteristic.EVOLUTION:
                        t = "Evolutions"
                        t2 = "Pokemons"
                        v1 = "id_base"
                        v2 = "id_evolution"
                    case PokemonCaracteristic.MOVE:
                        t = "PokemonMoves"
                        t2 = "Moves"
                        v1 = "id_pokemon"
                        v2 = "id_move"
                    case _:
                        t = ""
                        v1 = ""
                        v2 = ""
                sql = "UPDATE " + t + " SET " + v2 + "=%s WHERE " + v1 + "=%s AND " + v2 +"=%s AND id_login=%s"
                p1 = env["Choose"].cget("text")
                p2 = env["Choose2"].cget("text")
                p3 = env["Choose3"].cget("text")
                sql1 = "SELECT id FROM Pokemons WHERE name=%s LIMIT 1"
                self.mycursor.execute(sql1, (p1,))
                p1 = self.mycursor.fetchall()
                sql2 = "SELECT id FROM " + t2 + " WHERE name=%s LIMIT 1"
                self.mycursor.execute(sql2, (p2,))
                p2 = self.mycursor.fetchall()
                self.mycursor.execute(sql2, (p3,))
                p3 = self.mycursor.fetchall()
                if len(p1) > 0 and len(p2) > 0 and len(p3) > 0:
                    p1 = p1[0][0]
                    p2 = p2[0][0]
                    p3 = p3[0][0]
                    params = (p3, p1, p2, self.id)
                    self.mycursor.execute(sql, params)
                    self.mydb.commit()
                    #env["Apply"].config(text="Update success")
                    self.play_sound("Sound/good.mp3")
                else:
                    #env["Apply"].config(text="Select all the field")
                    self.play_sound("Sound/not_good.mp3")
            case Mode.DELETE:
                match caracteristic:
                    case PokemonCaracteristic.ABILITY:
                        t = "PokemonAbilities"
                        t2 = "Abilities"
                        v1 = "id_pokemon"
                        v2 = "id_ability"
                    case PokemonCaracteristic.EVOLUTION:
                        t = "Evolutions"
                        t2 = "Pokemons"
                        v1 = "id_base"
                        v2 = "id_evolution"
                    case PokemonCaracteristic.MOVE:
                        t = "PokemonMoves"
                        t2 = "Moves"
                        v1 = "id_pokemon"
                        v2 = "id_move"
                    case _:
                        t = ""
                        t2 = ""
                        v1 = ""
                        v2 = ""
                sql = "DELETE FROM " + t + " WHERE " + v1 + "=%s AND " + v2 + "=%s AND id_login=%s"
                p1 = env["Choose"].cget("text")
                p2 = env["Choose2"].cget("text")
                sql1 = "SELECT id FROM Pokemons WHERE name=%s LIMIT 1"
                self.mycursor.execute(sql1, (p1,))
                p1 = self.mycursor.fetchall()
                sql2 = "SELECT id FROM " + t2 + " WHERE name=%s LIMIT 1"
                self.mycursor.execute(sql2, (p2,))
                p2 = self.mycursor.fetchall()
                if len(p1) > 0 and len(p2) > 0:
                    p1 = p1[0][0]
                    p2 = p2[0][0]
                    params = (p1, p2, self.id)
                    
                    self.mycursor.execute(sql, params)
                    self.mydb.commit()
                    #env["Apply"].config(text="Delete success")
                    self.play_sound("Sound/good.mp3")
                else:
                    #env["Apply"].config(text="Select all the field")
                    self.play_sound("Sound/not_good.mp3")
            case _:
                pass
        self.update_button()
        
        
    def on_key_release(self, event, entry, list_entry):
        self.search_database(entry.get(), list_entry)
        
    def search_database(self, text, list_entry):
        list_entry.delete(0, tk.END)
        if text != "Enter the name":
            sql = "SELECT name FROM Pokemons WHERE LOWER(name) LIKE %s ORDER BY LOWER(name)"
            self.mycursor.execute(sql, (text.lower() +"%",))
            l = self.mycursor.fetchall()
            for val in l:
                list_entry.insert(tk.END, val[0])
    
            
    def on_select_list(self, event, entry, l):
        entry.delete(0, tk.END)
        text = l.get(l.curselection())
        entry.insert(0, text)
        self.search_by_name(entry)
        
    def change_evolution(self, next_pokemon):
        if next_pokemon:
            name = ("id_evolution", "id_base")
        else:
            name = ("id_base", "id_evolution")
        sql = "SELECT " + name[0] + " FROM Evolutions WHERE " + name[1] + "=%s AND (id_login=%s OR id_login=1)"
        params = (self.poke_id,self.id)
        self.mycursor.execute(sql, params)
        l = list(self.mycursor.fetchall())
        if next_pokemon:
            self.research_sql_dict["Evolution"] = [val[0] for val in l]
            if len(l) == 0:
                self.research_sql_dict["Evolution"] = ["None"]
            else:
                l = []
                sql_val = "SELECT name FROM Pokemons WHERE id=%s"
                for val in self.research_sql_dict["Evolution"]:
                    self.mycursor.execute(sql_val, (val,))
                    l.extend([value[0] for value in list(self.mycursor.fetchall())])
                if len(l) == 0:
                    self.research_sql_dict["Evolution"] = ["None"]
                else:
                    self.research_sql_dict["Evolution"] = deque(l)
        else:
            self.research_sql_dict["PreEvolution"] = [val[0] for val in l]
            if len(l) == 0:
                self.research_sql_dict["PreEvolution"] = ["None"]
            else:
                l = []
                sql_val = "SELECT name FROM Pokemons WHERE id=%s"
                for val in self.research_sql_dict["PreEvolution"]:
                    self.mycursor.execute(sql_val, (val,))
                    l.extend([value[0] for value in list(self.mycursor.fetchall())])
                if len(l) == 0:
                    self.research_sql_dict["PreEvolution"] = ["None"]
                else:
                    self.research_sql_dict["PreEvolution"] = deque(l)
                    
    def go_to_evolution(self, button):
        name = button.cget("text")
        sql = "SELECT id FROM Pokemons WHERE name=%s AND (id_login=1 OR id_login=%s)"
        params = (name, self.id)
        self.mycursor.execute(sql, params)
        l = list(self.mycursor.fetchall())
        if len(l) >0:
            id_poke = l[0][0]
            
        
            self.update_research(id_poke)
    
    def change_pokemon(self, next_pokemon):
        if next_pokemon:
            self.research_sql_dict["Select"].rotate(-1)
        else:
            self.research_sql_dict["Select"].rotate(1)
        self.update_research()
        
        
    def search_by_name(self, entry, strict=True):
        text = entry.get()
        if strict:
            sql = "SELECT id FROM Pokemons WHERE name=%s AND (id_login=1 OR id_login=%s) ORDER BY nid"
        else:
            sql = "SELECT id FROM Pokemons WHERE name LIKE %s AND (id_login=1 OR id_login=%s) ORDER BY nid"
            text += "%"
        params = (text, self.id)
        self.mycursor.execute(sql, params)
        l = list(self.mycursor.fetchall())
        self.research_sql_dict["Select"] = deque([val[0] for val in l])
        self.update_research()
        
        self.change_frame(self.frame_dict["Research"], self.frame_dict["Results"])
    
    def update_research(self, id_poke=None):
        if len(self.research_sql_dict["Select"]) == 0 and id_poke == None:
            try:
                im = Image.open("Pictures/question_mark.jpg").convert("RGB")
                im = im.resize((300, 300), Image.Resampling.LANCZOS)
                im = ImageTk.PhotoImage(im)
                self.result_sql_dict["PokemonImage"].config(image=im)
                self.result_sql_dict["PokemonImage"].image = im
            except:
                pass
            self.result_sql_dict["Title"].config(text="Unknown pokemon")
            self.result_sql_dict["Type1"].config(text="Type : " + "unknown")
            self.result_sql_dict["Type2"].place_forget()
            self.result_sql_dict["Tier"].config(text="Tier : unknown")
            self.result_sql_dict["HP"].config(text="HP : unknown")
            self.result_sql_dict["Speed"].config(text="Speed : unknown")
            self.result_sql_dict["Attack"].config(text="Attack : unknown")
            self.result_sql_dict["AttackSpe"].config(text="Attack special : unknown")
            self.result_sql_dict["Defense"].config(text="Defense : unknown")
            self.result_sql_dict["DefenseSpe"].config(text="Defense special : unknown")
            self.poke_id = 0
            self.poke_ability = ["None"]
            self.poke_move = ["None"]
            
        else:

            if id_poke==None:
                id_poke = self.research_sql_dict["Select"][0]

            sql = "SELECT * FROM Pokemons WHERE id=%s"
            self.mycursor.execute(sql, (id_poke,))
            poke = self.mycursor.fetchall()
            (id1, nid, name, type1, type2, hp, atk, defense, sp_atk, sp_def, speed, tier, image, id_login) = poke[0]
            self.poke_id = id1
            try:
                im = Image.open(image).convert("RGB")
                im = im.resize((300, 300), Image.Resampling.LANCZOS)
                im = ImageTk.PhotoImage(im)
                self.result_sql_dict["PokemonImage"].config(image=im)
                self.result_sql_dict["PokemonImage"].image = im
            except:
                try:
                    im = Image.open("Pictures/question_mark.jpg").convert("RGB")
                    im = im.resize((300, 300), Image.Resampling.LANCZOS)
                    im = ImageTk.PhotoImage(im)
                    self.result_sql_dict["PokemonImage"].config(image=im)
                    self.result_sql_dict["PokemonImage"].image = im
                except:
                    pass
            self.result_sql_dict["Title"].config(text=str(nid) +". "+name)
            sql_type = "SELECT name FROM Types WHERE id=%s"
            self.mycursor.execute(sql_type, (type1,))
            type1 = self.mycursor.fetchall()
            if len(type1) > 0:
                self.mycursor.execute(sql_type, (type2,))
                type2 = self.mycursor.fetchall()
                if len(type2) > 0:
                    self.result_sql_dict["Type1"].config(text="Type 1 : " + type1[0][0])
                    self.result_sql_dict["Type2"].config(text="Type 2 : " + type2[0][0])
                    self.result_sql_dict["Type2"].place(relx=0.32, rely=0.9)
                else:
                    self.result_sql_dict["Type1"].config(text="Type : " + type1[0][0])
                    self.result_sql_dict["Type2"].place_forget()
            else:
                self.result_sql_dict["Type1"].config(text="Type : " + "unknown")
                self.result_sql_dict["Type2"].place_forget()
            sql_tier = "SELECT name FROM Tiers WHERE id=%s"
            self.mycursor.execute(sql_tier, (tier,))
            tier = self.mycursor.fetchall()
            if len(tier) > 0:
                self.result_sql_dict["Tier"].config(text="Tier : " + tier[0][0])
            else:
                self.result_sql_dict["Tier"].config(text="Tier : unknown")
            self.result_sql_dict["HP"].config(text="HP : " + str(hp))
            self.result_sql_dict["Speed"].config(text="Speed : " + str(speed))
            self.result_sql_dict["Attack"].config(text="Attack : " + str(atk))
            self.result_sql_dict["AttackSpe"].config(text="Attack special : " + str(sp_atk))
            self.result_sql_dict["Defense"].config(text="Defense : " + str(defense))
            self.result_sql_dict["DefenseSpe"].config(text="Defense special : " + str(sp_def))
            sql_ab = "SELECT A.name FROM PokemonAbilities AS PA JOIN Pokemons AS P ON P.id=PA.id_pokemon JOIN Abilities AS A ON A.id=PA.id_ability WHERE P.id=%s AND (PA.id_login=1 OR PA.id_login=%s) ORDER BY A.name"
            self.mycursor.execute(sql_ab, (self.poke_id, self.id))
            ab = self.mycursor.fetchall()
            self.poke_ability = [val[0] for val in ab]
            if len(self.poke_ability) == 0:
                self.poke_ability.append("None")
            sql_move = "SELECT M.name FROM PokemonMoves AS MP JOIN Pokemons AS P ON P.id=MP.id_pokemon JOIN Moves AS M ON M.id=MP.id_move WHERE P.id=%s AND (MP.id_login=1 OR MP.id_login=%s) ORDER BY M.name"
            self.mycursor.execute(sql_move, (self.poke_id, self.id))
            move = self.mycursor.fetchall()
            self.poke_move = [val[0] for val in move]
            if len(self.poke_move) == 0:   
                self.poke_move.append(["None"])
        self.result_sql_dict["AbilityDescription"].config(state="normal")
        self.result_sql_dict["AbilityDescription"].delete("1.0", tk.END)
        self.result_sql_dict["AbilityDescription"].config(state="disable")
        self.result_sql_dict["SelectAbility"].set(value="Ability")
        self.result_sql_dict["Ability"].destroy()
        self.result_sql_dict["Ability"] = tk.OptionMenu(self.frame_dict["Results"], self.result_sql_dict["SelectAbility"], *self.poke_ability, command=lambda event: self.display_ability_description(event, self.result_sql_dict["Ability"], self.result_sql_dict["AbilityDescription"]))
        self.result_sql_dict["Ability"].place(relx=0.13, rely=0.85, relwidth=0.1, relheight=0.04)
        self.result_sql_dict["MoveDescription"].config(state="normal")
        self.result_sql_dict["MoveDescription"].delete("1.0", tk.END)
        self.result_sql_dict["SelectMove"].set(value="Move")
        self.result_sql_dict["Move"].destroy()
        self.result_sql_dict["Move"] = tk.OptionMenu(self.frame_dict["Results"], self.result_sql_dict["SelectMove"], *self.poke_move, command=lambda event: self.display_move_description(event, self.result_sql_dict["Move"], self.result_sql_dict["MoveDescription"]))
        self.result_sql_dict["Move"].place(relx=0.78, rely=0.85, relwidth=0.1, relheight=0.04)
        self.result_sql_dict["MoveDescription"].config(state="disabled")
        
        
        self.result_sql_dict["SelectEvolution"].set(value="Evolution")
        self.result_sql_dict["ButtonEvolution"].destroy()
        
        
        self.result_sql_dict["SelectPreEvolution"].set(value="Pre-evolution")
        self.result_sql_dict["ButtonPreEvolution"].destroy()
        
        self.result_sql_dict["Next"].destroy()
        self.change_evolution(True)
        self.change_evolution(False)
        self.result_sql_dict["Previous"].destroy()
        
        if len(self.research_sql_dict["Select"]) > 1 and id_poke == self.research_sql_dict["Select"][0]:
            self.result_sql_dict["Next"] = tk.Button(self.frame_dict["Results"], text="Next pokemon", width=100, height=100, image=self.result_sql_dict["NextImage"], compound="top", command=lambda: self.change_pokemon(True))
            self.result_sql_dict["Next"].place(relx=0.9, rely=0.43)
            
            self.result_sql_dict["Previous"] = tk.Button(self.frame_dict["Results"], text="Previous pokemon", width=100, height=100, image=self.result_sql_dict["PreviousImage"], compound="top", command=lambda: self.change_pokemon(False))
            self.result_sql_dict["Previous"].place(relx=0.02, rely=0.43)
        if self.research_sql_dict["Evolution"] != ['None']:
            
            self.result_sql_dict["ButtonEvolution"] = tk.OptionMenu(self.frame_dict["Results"], self.result_sql_dict["SelectEvolution"], *self.research_sql_dict["Evolution"], command=lambda event: self.go_to_evolution(self.result_sql_dict["ButtonEvolution"]))
            self.result_sql_dict["ButtonEvolution"].place(relx=0.85, rely=0.76, relwidth=0.1, relheight=0.04)
        if self.research_sql_dict["PreEvolution"] != ['None']:
            
            self.result_sql_dict["ButtonPreEvolution"] = tk.OptionMenu(self.frame_dict["Results"], self.result_sql_dict["SelectPreEvolution"], *self.research_sql_dict["PreEvolution"], command=lambda event: self.go_to_evolution(self.result_sql_dict["ButtonPreEvolution"]))
            self.result_sql_dict["ButtonPreEvolution"].place(relx=0.07, rely=0.76, relwidth=0.1, relheight=0.04)
            
    def display_ability_description(self, event, button, display):
        display.config(state="normal")
        entry = button.cget("text")
        sql = "SELECT description FROM Abilities WHERE name=%s"
        self.mycursor.execute(sql, (entry,))
        l = self.mycursor.fetchall()
        display.delete("1.0", tk.END)
       
        if len(l) > 0:
            display.insert(tk.END, l[0][0])
        else:
            display.insert(tk.END, "No description")
        display.config(state="disabled")
    
    def display_move_description(self, event, button, display):
        display.config(state="normal")
        entry = button.cget("text")
        sql = "SELECT * FROM Moves WHERE name=%s"
        self.mycursor.execute(sql, (entry,))
        l = self.mycursor.fetchall()
        display.delete("1.0", tk.END)
       
        if len(l) > 0:
            (id1, name, type1, category, power, pp, accuracy, description, id_login) = l[0]
            sql_type = "SELECT name FROM Types WHERE id=%s"
            sql_cat = "SELECT name FROM Categories WHERE id=%s"
            text = ""
            self.mycursor.execute(sql_type, (type1,))
            type1 = self.mycursor.fetchall()
            if len(type1) > 0:
                text += "Type : " + type1[0][0] + "\n"
            else:
                text += "Type : unknown\n"
            self.mycursor.execute(sql_cat, (category,))
            category = self.mycursor.fetchall()
            if len(category) > 0:
                text += "Category : " + category[0][0] + "\n"
            else:
                text += "Category : unknown\n"
            if power != 0:
                text += "Power : " + str(power) + "\n"
            else:
                text += "Power : _\n"
            text += "PP : " + str(pp) + "\n"
            if accuracy == 0:
                text += "Accuracy : _ \n"
            else:
                text += "Accuracy : " + str(accuracy)+"%\n\n"
            if description == "":
                text += "No description"
            else:
                text += description
            display.insert(tk.END, text)
        else:
            display.insert(tk.END, "No description")
        display.config(state="disabled")

    def play_sound(self, title):
        pygame.mixer.init()
        pygame.mixer.Sound(title).play()

    def recognition_by_image(self, filename):
        try:

            model = tf.keras.models.load_model("pokemon_AI.h5")

            im = image.load_img(filename, target_size=(128,128))
            im = image.img_to_array(im) / 255.
            im = np.expand_dims(im, axis=0)

            with open("pokemon_AI.json", "r") as f:
                pokemon = json.load(f)
            res = np.argmax(model.predict(im))
            sql = "SELECT id FROM Pokemons WHERE LOWER(name)=%s AND (id_login=1 OR id_login=%s) LIMIT 1"
            params = (pokemon[str(int(res))].lower(), self.id)
            self.mycursor.execute(sql, params)
            l = self.mycursor.fetchall()
            if len(l) > 0:
                self.update_research(id_poke=l[0][0])
                self.change_frame(self.frame_dict["SearchImage"], self.frame_dict["Results"])
            else:
                self.play_sound("Sound/not_good.mp3")
        except:
            self.play_sound("Sound/not_good.mp3")

        self.image_select_dict["Image"].destroy()
        self.image_select_dict["Image"] = tk.Button(self.frame_dict["SearchImage"], text="Image selection",
                                                    compound="top",
                                                    command=lambda: self.get_image_path(
                                                        self.image_select_dict["ImageLabel"],
                                                        self.image_select_dict["Image"]))
        self.image_select_dict["Image"].place(relx=0.45, rely=0.5, relwidth=0.1, relheight=0.04)


    def type_efficacity_change(self):
        match self.mode:
            case Mode.ADD:
                try:

                    sql = "INSERT INTO TypeEfficacities (id_type1, id_type2, coeff, id_login) VALUES (%s,%s,%s,%s)"
                    type1 = self.type_efficaty_dict["Type1"].cget("text")
                    type2 = self.type_efficaty_dict["Type2"].cget("text")
                    coef = self.type_efficaty_dict["Coef1"].cget("text")
                    if coef == "Immune":
                        coef = 0
                    elif "Resist" == coef:
                        coef = 1
                    elif coef == "Efficient":
                        coef = 2
                    elif coef == "Very efficient":
                        coef = 4

                    sql_type = "SELECT id FROM Types WHERE name=%s"
                    self.mycursor.execute(sql_type, (type1,))
                    type1 = self.mycursor.fetchall()
                    self.mycursor.execute(sql_type, (type2,))
                    type2 = self.mycursor.fetchall()

                    if len(type1) > 0 and len(type2) > 0:
                        type1 = type1[0][0]
                        type2 = type2[0][0]
                        sql_verif = "SELECT * FROM TypeEfficacities WHERE id_type1=%s AND id_type2=%s AND (id_login=1 OR id_login=%s)"
                        params = (type1,type2, self.id)
                        self.mycursor.execute(sql_verif, params)

                        if len(list(self.mycursor.fetchall())) == 0:
                            params = (type1, type2, coef, self.id)
                            self.mycursor.execute(sql, params)
                            self.mydb.commit()
                            self.play_sound("Sound/good.mp3")
                        else:
                            self.play_sound("Sound/not_good.mp3")
                    else:
                        self.play_sound("Sound/not_good.mp3")
                except:
                    self.play_sound("Sound/not_good.mp3")
            case Mode.UPDATE:
                try:
                    sql = "UPDATE TypeEfficacities SET id_type1=%s, id_type2=%s, coeff=%s WHERE id_type1=%s AND id_type2=%s AND id_login=%s"
                    type1 = self.type_efficaty_dict["Type1"].cget("text")
                    type2 = self.type_efficaty_dict["Type2"].cget("text")
                    type1_new = self.type_efficaty_dict["Type3"].cget("text")
                    type2_new = self.type_efficaty_dict["Type4"].cget("text")
                    coef = self.type_efficaty_dict["Coef1"].cget("text")
                    if coef == "Immune":
                        coef = 0
                    elif "Resist" == coef:
                        coef = 1
                    elif coef == "Efficient":
                        coef = 2
                    elif coef == "Very efficient":
                        coef = 4
                    params =(type1, type2, coef, type1_new, type2_new, self.id)
                    self.mycursor.execute(sql, params)
                    self.mydb.commit()
                    self.play_sound("Sound/good.mp3")
                except:
                    self.play_sound("Sound/not_good.mp3")
            case Mode.DELETE:
                try:
                    sql = "DELETE FROM TypeEfficacities WHERE id_type1=%s AND id_type2=%s AND id_login=%s"
                    type1 = self.type_efficaty_dict["Type1"].cget("text")
                    type2 = self.type_efficaty_dict["Type2"].cget("text")
                    params = (type1, type2, self.id)
                    self.mycursor.execute(sql, params)
                    self.mydb.commit()
                    self.play_sound("Sound/good.mp3")
                except:
                    self.play_sound("Sound/not_good.mp3")
            case _:
                pass
        self.update_button()

    def create_filter_button(self, button, index, frame, init=False):
        list_field = ["Type", "Tier", "Resistant", "Immune", "Efficient", "Very efficient", "Attack", "Defense", "Special Attack", "Special Defense", "Speed", "HP"]
        list_agregate = ["between", "superior", "inferior", "equal"]
        list_add = [self.type_contribute_dict["Select"],
                    self.tier_contribute_dict["Select"],
                    self.type_contribute_dict["Select"],
                    self.type_contribute_dict["Select"],
                    self.type_contribute_dict["Select"],
                    self.type_contribute_dict["Select"],
                    list_agregate,
                    list_agregate,
                    list_agregate,
                    list_agregate,
                    list_agregate,
                    list_agregate,
                    ]
        if init and frame != None:
            string = tk.StringVar(value="Select your field")
            b = tk.OptionMenu(frame, string,
                                                     *list_field, command=lambda value: self.create_filter_button(b, index, frame, init=False))
            b.place(relx=0.2, rely=0.2+0.05*index, relwidth=0.1, relheight=0.04)

            return b
        else:
            if init==False:
                val = self.filter_search_dict["Button"][index][0].cget("text")
                ind = list_field.index(val)
                if ind <= 5:
                    string = tk.StringVar(value="Select your value")
                    b = tk.OptionMenu(frame, string,
                                      *list_add[ind])
                    b.place(relx=0.4, rely=0.2 + 0.05 * index, relwidth=0.1, relheight=0.04)
                else:
                    string = tk.StringVar(value="Select your filter")
                    b = tk.OptionMenu(frame, string,*list_add[ind],
                                      command=lambda event: self.create_filter_button(b, index, frame, init=None))
                    b.place(relx=0.4, rely=0.2 + 0.05 * index, relwidth=0.1, relheight=0.04)

                self.filter_search_dict["Button"][index].append(b)
            else:
                val = self.filter_search_dict["Button"][index][1].cget("text")
                while len(self.filter_search_dict["Button"][index]) > 2:
                    button = self.filter_search_dict["Button"][index].pop()
                    button.destroy()
                l_b = []
                b = tk.Entry(frame, width=35, fg="gray")
                b.place(relx=0.6, rely=0.2 + 0.05 * index, relwidth=0.1, relheight=0.04)
                b.insert(0, "Enter a value")
                b.bind("<FocusIn>",
                                               lambda event: self.fill_entry(event, b,
                                                                             "Enter a value", False))
                b.bind("<FocusOut>",
                                               lambda event: self.clear_entry(event, b,
                                                                              "Enter a value"))
                l_b.append(b)

                if val == list_agregate[0]:
                    b2 = tk.Entry(frame, width=35, fg="gray")
                    b2.place(relx=0.8, rely=0.2 + 0.05 * index, relwidth=0.1, relheight=0.04)
                    b2.insert(0, "Enter a value")
                    b2.bind("<FocusIn>",
                           lambda event: self.fill_entry(event, b2,
                                                         "Enter a value", False))
                    b2.bind("<FocusOut>",
                           lambda event: self.clear_entry(event, b2,
                                                          "Enter a value"))
                    l_b.append(b2)
                self.filter_search_dict["Button"][index].extend(l_b)

    def search_by_filter(self):
        list_field = ["Type", "Tier", "Attack", "Defense",
                      "Special Attack", "Special Defense", "Speed", "HP", "Resistant", "Immune", "Efficient", "Very efficient"]
        list_agregate = ["between", "superior", "inferior", "equal"]
        list_equiv = [' (type_1=%s OR type_2=%s) ', " tier=%s ", " attack ", " defense ",
                      " sp_atk ", " sp_def ", " speed ", " hp "]
        sql = "SELECT id FROM Pokemons WHERE (id_login=1 OR id_login=%s)"
        l_params = [self.id]
        verif = True
        try:
            for i in range(12):
                val = self.filter_search_dict["Button"][i][0].cget("text")

                if val in list_field:

                    ind = list_field.index(val)
                    if ind <= 1:
                        name = self.filter_search_dict["Button"][i][1].cget("text")

                        sql += "AND" + list_equiv[ind]

                        if ind==0:
                            sql_type ="SELECT id FROM Types WHERE name=%s"
                            self.mycursor.execute(sql_type, (name,))
                            name = self.mycursor.fetchall()

                            if len(name) > 0:
                                for j in range(2):
                                    l_params.append(name[0][0])
                            else:
                                raise Exception()
                        else:
                            sql_type = "SELECT id FROM Tiers WHERE name=%s"
                            self.mycursor.execute(sql_type, (name,))
                            name = self.mycursor.fetchall()
                            if len(name) > 0:
                                    l_params.append(name[0][0])
                            else:
                                raise Exception()
                    elif ind <= 7:
                        name = self.filter_search_dict["Button"][i][1].cget("text")

                        sql += " AND" + list_equiv[ind]
                        if name == list_agregate[0]:
                            sql += "BETWEEN %s AND %s"
                            val1 = int(self.filter_search_dict["Button"][i][2].get())
                            val2 = int(self.filter_search_dict["Button"][i][3].get())
                            l_params.append(val1)
                            l_params.append(val2)
                        else:
                            val1 = int(self.filter_search_dict["Button"][i][2].get())
                            l_params.append(val1)
                            if name == list_agregate[1]:
                                sql += ">%s"
                            elif name == list_agregate[2]:
                                sql += "<%s"
                            elif name == list_agregate[3]:
                                sql += "=%s"
                            else:
                                raise Exception()
                    else:
                        value = self.filter_search_dict["Button"][i][1].cget("text")
                        sql_type = "SELECT id FROM Types WHERE name=%s"
                        self.mycursor.execute(sql_type, (value,))
                        value = self.mycursor.fetchall()
                        if len(value) > 0:
                            value = value[0][0]
                        else:
                            raise Exception()
                        sql += " AND "
                        if ind==8:
                            sql_im = "SELECT TE.id_type2 FROM TypeEfficacities AS TE JOIN Types AS T2 ON TE.id_type1=T2.id WHERE TE.coeff=1 AND (TE.id_login=1 OR TE.id_login=%s) AND TE.id_type1=%s"
                            sql_im2 = "SELECT TE.id_type2 FROM TypeEfficacities AS TE JOIN Types AS T2 ON TE.id_type1=T2.id WHERE TE.coeff IN (1,2) AND (TE.id_login=1 OR TE.id_login=%s) AND TE.id_type1=%s"
                            self.mycursor.execute(sql_im, (self.id, value))
                            l_1 = self.mycursor.fetchall()
                            self.mycursor.execute(sql_im2, (self.id,value))
                            l_2 = self.mycursor.fetchall()
                            if len(l_1) > 0:
                                l_1 = [val[0] for val in list(l_1)]
                                l_2 = [val[0] for val in list(l_2)]
                                s1 = " (%s"
                                for i in range(1, len(l_1)):
                                    s1 += ",%s"
                                s1 += ") "
                                if len(l_2)==0:
                                    s2 = " (0) "
                                else:
                                    s2 = " (%s"
                                    for i in range(1, len(l_2)):
                                        s2 += ",%s"
                                    s2 += ") "
                                sql += " ((type_2=0 AND type_1 IN" + s1 + ") OR (type_2 IN" + s1 + "AND type_1 IN" + s2 + ") OR (type_2 IN" + s2 + "AND type_1 IN" + s1 + "))"
                                l_params.extend(l_1)
                                l_params.extend(l_1)
                                l_params.extend(l_2)
                                l_params.extend(l_2)
                                l_params.extend(l_1)
                            else:
                                raise Exception()
                        elif ind==9:
                            sql_im = "SELECT TE.id_type2 FROM TypeEfficacities AS TE JOIN Types AS T2 ON TE.id_type1=T2.id WHERE TE.coeff=0 AND (TE.id_login=1 OR TE.id_login=%s) AND TE.id_type1=%s"
                            self.mycursor.execute(sql_im, (self.id,value))
                            name = self.mycursor.fetchall()

                            if len(name) > 0:
                                name = [val[0] for val in list(name)]

                                s=" (%s"
                                for i in range(1, len(name)):
                                    s += ",%s"
                                s +=") "
                                sql += "(type_1 IN" +s +" OR type_2 IN" + s + ')'
                                l_params.extend(name)
                                l_params.extend(name)
                            else:
                                raise Exception()
                        elif ind==10:
                            sql_im = "SELECT TE.id_type1 FROM TypeEfficacities AS TE JOIN Types AS T2 ON TE.id_type2=T2.id WHERE TE.coeff=2 AND (TE.id_login=1 OR TE.id_login=%s) AND TE.id_type2=%s"
                            sql_im2 = "SELECT TE.id_type1 FROM TypeEfficacities AS TE JOIN Types AS T2 ON TE.id_type2=T2.id WHERE TE.coeff=1 AND (TE.id_login=1 OR TE.id_login=%s) AND TE.id_type2=%s"
                            sql_im3 = "SELECT TE.id_type1 FROM TypeEfficacities AS TE JOIN Types AS T2 ON TE.id_type2=T2.id WHERE TE.coeff=4 AND (TE.id_login=1 OR TE.id_login=%s) AND TE.id_type2=%s"
                            self.mycursor.execute(sql_im, (self.id,value))
                            l_1 = self.mycursor.fetchall()
                            self.mycursor.execute(sql_im2, (self.id,value))
                            l_2 = self.mycursor.fetchall()
                            self.mycursor.execute(sql_im3, (self.id,value))
                            l_3 = self.mycursor.fetchall()
                            if len(l_1) > 0:
                                l_1 = [val[0] for val in list(l_1)]
                                l_2 = [val[0] for val in list(l_2)]
                                l_3 = [val[0] for val in list(l_3)]
                                s1 = " (%s"
                                for i in range(1, len(l_1)):
                                    s1 += ",%s"
                                s1 += ") "
                                if len(l_2) == 0:
                                    s2 = " (0) "
                                else:
                                    s2 = " (%s"
                                    for i in range(1, len(l_2)):
                                        s2 += ",%s"
                                    s2 += ") "
                                if len(l_3) == 0:
                                    s3 = " (0) "
                                else:
                                    s3 = " (%s"
                                    for i in range(1, len(l_3)):
                                        s3 += ",%s"
                                    s3 += ") "
                                sql += " ((type_2=0 AND type_1 IN" + s1 + ") OR (type_2 IN" + s1 + "AND type_1 IN" + s1 + ") OR (type_2 IN" + s2 + "AND type_1 IN" + s3 + ") OR (type_2 IN" + s3 + "AND type_1 IN" + s2 + "))"
                                l_params.extend(l_1)
                                l_params.extend(l_1)
                                l_params.extend(l_1)
                                l_params.extend(l_2)
                                l_params.extend(l_3)
                                l_params.extend(l_3)
                                l_params.extend(l_2)
                            else:
                                raise Exception()
                        else:
                            sql_im = "SELECT TE.id_type1 FROM TypeEfficacities AS TE JOIN Types AS T2 ON TE.id_type2=T2.id WHERE TE.coeff=4 AND (TE.id_login=1 OR TE.id_login=%s) AND TE.id_type2=%s"
                            sql_im2 = "SELECT TE.id_type1 FROM TypeEfficacities AS TE JOIN Types AS T2 ON TE.id_type2=T2.id WHERE TE.coeff>1 AND (TE.id_login=1 OR TE.id_login=%s) AND TE.id_type2=%s"

                            self.mycursor.execute(sql_im, (self.id,value))

                            l_1 = self.mycursor.fetchall()

                            self.mycursor.execute(sql_im2, (self.id,value))
                            l_2 = self.mycursor.fetchall()
                            if len(l_1) > 0:
                                l_1 = [val[0] for val in list(l_1)]
                                l_2 = [val[0] for val in list(l_2)]
                                s1 = " (%s"
                                for i in range(1, len(l_1)):
                                    s1 += ",%s"
                                s1 += ") "
                                if len(l_2) == 0:
                                    s2 = " (0) "
                                else:
                                    s2 = " (%s"
                                    for i in range(1, len(l_2)):
                                        s2 += ",%s"
                                    s2 += ") "
                                sql += " ((type_2=0 AND type_1 IN" + s1 + ") OR (type_2 IN" + s1 + "AND type_1 IN" + s2 + ") OR (type_2 IN" + s2 + "AND type_1 IN" + s1 + "))"
                                l_params.extend(l_1)
                                l_params.extend(l_1)
                                l_params.extend(l_2)
                                l_params.extend(l_2)
                                l_params.extend(l_1)
                            else:
                                raise Exception()
        except:
            self.play_sound("Sound/not_good.mp3")
            verif = False

        self.update_button()
        if verif:
            self.mycursor.execute(sql, tuple(l_params))
            l = self.mycursor.fetchall()
            self.research_sql_dict["Select"] = deque([val[0] for val in l])
            self.update_research()
            self.change_frame(self.frame_dict["SearchFilter"], self.frame_dict["Results"])

    def switch_sound(self):
        if pygame.mixer.music.get_volume() == 1:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1)

    def mainloop(self):
        self.change_frame(None, self.frame_dict["Login"])
        self.root.mainloop()
        
#%% [3] Main program

if __name__ == '__main__':
    app = App()
    app.mainloop()