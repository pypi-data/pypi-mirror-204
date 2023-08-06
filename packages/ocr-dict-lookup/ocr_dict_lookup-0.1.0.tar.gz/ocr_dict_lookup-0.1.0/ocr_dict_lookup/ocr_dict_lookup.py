import cv2 
import numpy as np
import pytesseract
import re
import requests

# Extract Highlighted Words
def extract_highlighted_words(image_path):
  # Load the image
  img = cv2.imread(image_path)

  # Convert the image to HSV color space
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  # Define a range of yellow color in HSV
  lower_yellow = (20, 100, 100)
  upper_yellow = (30, 255, 255)

  # Threshold the image to get the yellow regions
  mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

  # Find contours in the mask
  contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  # Extract the text from each contour
  highlighted_words = []
  for contour in contours:
      x, y, w, h = cv2.boundingRect(contour)
      roi = img[y:y+h, x:x+w]
      text = pytesseract.image_to_string(roi)
      highlighted_words.extend(text.split())

  # Return the highlighted words
  return highlighted_words

# Get Word Meanings => Just for searching up!
def get_word_meanings(word):
  url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
  response = requests.get(url)
  if response.status_code == 200:
      meaning = response.json()[0]['meanings'][0]['definitions'][0]['definition']
      return meaning
  else:
      return 'Error - Word not found in dictionary'

# Deals with the entire process of looking up the meanings of the words and writing them to a file
def write_word_meanings(words, filename):
  # Create or open the output file for writing
  with open(filename, 'a') as file:
      # Loop over each word and look up its meaning using the API
      for word in words:
          url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
          response = requests.get(url)
          if response.status_code == 200:
              # Extract the meaning from the API response and write to the file
              meaning = response.json()[0]['meanings'][0]['definitions'][0]['definition']
              file.write(f'{word}: {meaning}\n')
          else:
              file.write(f'{word}: Error - Word not found in dictionary\n')

