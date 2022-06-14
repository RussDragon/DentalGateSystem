import sys
from DataAdapter import main as da_main
from DataProcessor import main as dp_main
from colored import fore, style

def main(argv):
    print("Dental Implants Generator started\n")
    config = da_main.main(argv)
    dp_main.simple_generation_mode(config)
    dp_main.complex_generation_mode(config)

if __name__ == "__main__":
    main(sys.argv[1:])
