import pygame, sys
from pygame.locals import *
import tkinter as tk
from tkinter import filedialog
import json

class Controls:
    def __init__(self):
        self.is_charging_throw = False

        self.is_moving_left = False
        self.is_moving_right = False

        self.is_jumping = False

        self.is_respawning = False

    
    def handle_controls_events(self, events):
        for event in events:
            if (event.type == KEYDOWN):
                if (event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if (event.key == K_a):
                    self.is_moving_left = True
                if (event.key == K_d):
                    self.is_moving_right = True
                if (event.key == K_w):
                    self.is_jumping = True
                    
            if (event.type == KEYUP):
                if (event.key == K_a):
                    self.is_moving_left = False
                if (event.key == K_d):
                    self.is_moving_right = False
                if (event.key == K_r):
                    self.is_respawning = True

            if (event.type == QUIT):
                pygame.quit()
                sys.exit()
            
            if (event.type == MOUSEBUTTONDOWN):
                if (event.button) == 1:
                    self.is_charging_throw = True
            if (event.type == MOUSEBUTTONUP):
                if (event.button) == 1:
                    self.is_charging_throw = False
    
    
    def import_image(self):
        # Create a file explorer dialog to select an image file
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        return file_path
    
    def export_map(self, map_json):
        # Create a Tk root widget
        root = tk.Tk()
        # Hide the main window
        root.withdraw()

        # Open a save file dialog
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Json Files", "*.json")])

        # If a file location is selected
        if file_path:
            # You can write the JSON object to the selected file
            with open(file_path, 'w') as json_file:
                json.dump(map_json, json_file, indent=4)


