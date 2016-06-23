"""Initalizer for test package"""
import os

script_dir = os.path.dirname(__file__)
rel_path = 'files/'
abs_file_path = os.path.join(script_dir, rel_path)

file_paths = [os.path.join(abs_file_path, x) for x in os.listdir(abs_file_path)]
