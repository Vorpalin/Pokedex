# Pokedex
Pokedex system using python and SQL

To use this project, you have to create a file named dbcredentials.py where you have to create a dictionary db with the fields host, user and password. This dictionnary will be used in order to connect to your MySQL databases.

In addition, to use the project, you also have to create your different SQL tables. Here are the specifications:

Table: abilities  
Columns:  
  id int AI PK   
  name varchar(45)   
  description varchar(1000)   
  id_login int UN  

Table: categories  
Columns:  
  id int AI PK   
  name varchar(45)   
  id_login int UN    

Table: connections  
Columns:  
  id int AI PK   
  login varchar(45)   
  password varchar(45)  

Table: evolutions  
Columns:  
  id int AI PK   
  id_base int UN   
  id_evolution int UN   
  id_login int UN  

Table: moves  
Columns:  
  id int AI PK   
  name varchar(45)   
  type int UN   
  category int UN   
  power int UN   
  pp int UN   
  accuracy int   
  description varchar(1000)   
  id_login int UN  

Table: pokemonabilities  
Columns:  
  id int AI PK   
  id_pokemon int UN   
  id_ability int UN   
  id_login int UN  

Table: pokemonmoves  
Columns:  
  id int AI PK   
  id_pokemon int UN   
  id_move int UN   
  id_login int UN  

Table: pokemons  
Columns:  
  id int AI PK   
  nid int UN   
  name varchar(45)   
  type_1 int UN   
  type_2 int UN   
  hp int UN   
  attack int UN   
  defense int UN   
  sp_atk int UN   
  sp_def int UN   
  speed int UN   
  tier int UN   
  image varchar(255)   
  id_login int UN  

Table: tiers  
Columns:  
  id int AI PK   
  name varchar(45)   
  id_login int UN  

Table: typeefficacities  
Columns:  
  id int AI PK   
  id_type1 int UN   
  id_type2 int UN   
  coeff int UN   
  id_login int UN  

Table: types  
Columns:  
  id int AI PK   
  name varchar(45)   
  id_login int UN  

