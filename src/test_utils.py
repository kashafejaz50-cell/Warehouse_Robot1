from utils import set_seed, load_config

# 1️⃣ Set the random seed
set_seed(42)

# 2️⃣ Load configuration from your YAML file
config = load_config("config/config.yaml")  # Make sure the path is correct

# 3️⃣ Print some values to check
print("Grid Template:")
for row in config["grid_template"]:
    print(row)

print("\nAlgorithm:", config["algorithm"])