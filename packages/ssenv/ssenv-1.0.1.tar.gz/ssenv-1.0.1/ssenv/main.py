import os

class Environment:
    def __init__(self):
        self._dotenv_path = os.path.join(os.getcwd(), '.env')
        self._dotenv_dict = {}
        self.load_dotenv()
    
    def load_dotenv(self):
        with open(self._dotenv_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                k, v = line.split('=', 1)
                self._dotenv_dict[k] = v

    def get(self, key: str):
        return self._dotenv_dict[key] if key in self._dotenv_dict else None