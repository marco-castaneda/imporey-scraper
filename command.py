import argparse

def run_report():
    print("Making report")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str)

    args = parser.parse_args()

    if args.command == "run_report":
        run_report()

