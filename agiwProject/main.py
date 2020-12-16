import pipeline
import time


def main():
    start_time = time.time()
    print("Starting pipeline...\n")
    pipeline.Pipeline()
    print("Pipeline finished in %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()
