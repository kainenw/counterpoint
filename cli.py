import argparse
from counterpoint.primatives import CounterpointEngine, NoCounterpointFoundError
import cProfile

def main():
    parser = argparse.ArgumentParser(description="Generate counterpoint for a given melody.")
    parser.add_argument(
        "melody",
        metavar="N",
        type=int,
        nargs="+",
        help="A melody as a sequence of integers (notes)."
    )

    args = parser.parse_args()
    melody = args.melody

    # Profile the counterpoint generation process
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        engine = CounterpointEngine()
        counterpoint = engine.findCounterpoint(melody)
        print("Generated Counterpoint:")
        print(counterpoint)
    except NoCounterpointFoundError:
        print("Could not find a valid counterpoint for the provided melody.")
    except Exception as e:
        print(f"An error occurred: {e}")

    profiler.disable()
    profiler.print_stats(sort='cumulative')

if __name__ == "__main__":
    main()