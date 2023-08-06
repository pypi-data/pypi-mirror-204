import argparse 
from .main import app 

def main():
    parser = argparse.ArgumentParser(
        description="rewards-api v0.0.1 package to launch the rewards backend server"
    )
    
    parser.add_argument(
        "--url", "-u", type=str, default="127.0.0.1", 
        help = "The host connection url."
    )
    
    parser.add_argument(
        "--port", "-p", type=int, default=8000, 
        help = "The port to connect to"
    )
    
    args = parser.parse_args() 
    debug = True 
    app.run(
        host = args.url, 
        port = args.port, 
        debug = debug
    )
    

if __name__ == "__main__":
    main() 