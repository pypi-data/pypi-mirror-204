"""
Test
"""
import mindoptpy
from mindoptpy import MdoError
import logging
import argparse


def setup_logging(level):
    logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=level)


if __name__ == "__main__":

    # Register arguments.
    parser = argparse.ArgumentParser(description='Run MindOpt.')
    parser.add_argument('--filename', type=str, default='../data/afiro.mps', help='Input LP/MPS filename.')
    args = parser.parse_args()
    filename = args.filename
   
    logging.info("Started MindOpt.")
    logging.info(" - Filename  : {0}".format(filename))

    model = mindoptpy.MdoModel()

    try:
        model.read_prob(filename)
        model.solve_prob()
        model.display_results()

    except MdoError as e:
        logging.error("Received MindOpt exception.")
        logging.error(" - Code          : {}".format(e.code))
        logging.error(" - Reason        : {}".format(e.message))
    except Exception as e:
        logging.error("Received exception.")
        logging.error(" - Reason        : {}".format(e))
    finally:
        model.free_mdl()


