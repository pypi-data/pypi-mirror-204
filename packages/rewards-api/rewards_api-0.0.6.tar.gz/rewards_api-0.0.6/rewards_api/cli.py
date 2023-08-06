import argparse  
from .main import app 
from .cli_args import args


debug = True 
def main():
    app.run(
        host = args.url, 
        port = args.port, 
        debug = debug
    )
    
    

if __name__ == "__main__":
    main() 