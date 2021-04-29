# main.py
# -------------
from bayesianNetwork import BayesianNetwork
import optparse
import os
import sys


# register arguments and set default values
def readCommand(argv):
    parser = optparse.OptionParser(
        description='Run public tests on student code')
    parser.add_option('--model-directory',
                      dest='modelRoot',
                      default='models',
                      help='Root model directory which contains models')
    parser.add_option('--test-directory',
                      dest='testRoot',
                      default='testcases',
                      help='Root test directory which contains testcases')
    parser.add_option('--model',
                      dest='modelFilename',
                      default='model01.txt',
                      help='File name which contains the model')                  
    parser.add_option('--testcase',
                      dest='testFilename',
                      default="testcase01.txt",
                      help='File name which contains the testcase')
    (options, _) = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    options = readCommand(sys.argv)
    model = BayesianNetwork(options.modelRoot + '/' + options.modelFilename)
    result = model.exact_inference(options.testRoot + '/' + options.testFilename)
    print('%0.5f' % result)
    result = model.approx_inference(options.testRoot + '/' + options.testFilename)
    print('%0.5f' % result)
   