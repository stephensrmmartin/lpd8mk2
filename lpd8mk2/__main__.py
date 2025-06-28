import argparse
from .config import Program
from .midi import LPD8Mk2IO

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=int, help="Program Number: int [1-4]")
    parser.add_argument("json_file", type=str, help="Path to JSON file: str")
    args = parser.parse_args()

    set_program(program = args.program, json_path = args.json_file)

def set_program(program: int, json_path: str):
    io = LPD8Mk2IO()
    prog = Program.from_json(json_path)
    sysex_message = prog.to_sysex(program)
    io.send(sysex_message)

if __name__ == "__main__":
    main()
