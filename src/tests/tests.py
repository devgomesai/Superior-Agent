import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(base_dir)
output_dir = os.path.join(base_dir, "output")



path = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(path)