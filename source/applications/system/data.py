"""Data representation for system.py"""
# TODO: fake data for use in testing -- move or delete later
data = [
    ("Documents", [
        ("Projects"),
        ("Games"),
        ("History 101"),
    ]),
    ("Music", []),
    ("Pictures", [
        ("Family Pictures", [
            "Photo_1.png",
            "Photo_2.png"
        ]),
        "Random_Photo.png"
    ]),
    "Out_Of_Place_File.txt",
    "VeryLongFileName" + "_" * 60 + ".txt"
]

# this involves having models. system.py should be able to produce this
# data = [
#     Folder("Documents", [
#         File("Projects"),
#         File("Games"),
#         File("History 101"),
#     ]),
#     Folder("Music"),
#     Folder("Pictures", [
#         Folder("Family Pictures", [
#             File("Photo_1.png"),
#             File("Photo_2.png")
#         ]),
#         File("Random_Photo.png")
#     ]),
#     File("Out_Of_Place_File.txt"),
#     File("VeryLongFileName" + "_" * 60 + ".txt")
# ]

sysdat = None

if __name__ == "__main__":
    pass