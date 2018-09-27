"""Fake data generator"""
__author__ = "Samuel Whang"

from source import Table

# This can either go two ways. Building data directly from sql queries with a
# join on the tables being used. Very similar to a view table. Or load all
# tables being used into python and have the dataprocessing done within a
# python program.

# Let's try both ways
# Option 1: Sql Join Query to generate data

# Option 2: Generate data using python