import ssenv

# Create env instance
env = ssenv.Environment()

# Load .env file
env.load_dotenv()

# Get value from .env file
print(env.get('MY_PASSWORD'))
