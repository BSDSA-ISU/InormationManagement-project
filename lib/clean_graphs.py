import os


def clean():
    """
    Simple cleaner for junk graphs
    """
    graph_path = "static/graphs"

    for i in os.listdir(graph_path):
        if i.endswith(".png") and not i == "logo.png":
            os.remove(f"static/graphs/{i}")