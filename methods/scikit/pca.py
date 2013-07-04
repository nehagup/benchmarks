'''
  @file pca.py
  @author Marcus Edel

  Principal Components Analysis with scikit.
'''

import os
import sys
import inspect

# Import the util path, this method even works if the path contains symlinks to
# modules.
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(
  os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../util")))
if cmd_subfolder not in sys.path:
  sys.path.insert(0, cmd_subfolder)

from log import *
from timer import *

import numpy as np
from sklearn import decomposition

'''
This class implements the Principal Components Analysis benchmark.
'''
class PCA(object):

  ''' 
  Create the Principal Components Analysis benchmark instance.
  
  @param dataset - Input dataset to perform PCA on.
  @param verbose - Display informational messages.
  '''
  def __init__(self, dataset, verbose=True): 
    self.verbose = verbose
    self.dataset = dataset

  '''
  Destructor to clean up at the end.
  '''
  def __del__(self):
    pass

  '''
  Use the scikit libary to implement Principal Components Analysis.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or -1 if the method was not successful.
  '''
  def PCAScikit(self, options):
    totalTimer = Timer()

    # Load input dataset.
    Log.Info("Loading dataset", self.verbose)
    data = np.genfromtxt(self.dataset, delimiter=',')

    with totalTimer:
      # Find out what dimension we want.
      match = re.search('-d (\d+)', options)

      if not match:
        k = data.shape[1]
      else:
        k = int(match.group(1))      
        if (k > data.shape[1]):
          Log.Fatal("New dimensionality (" + str(k) + ") cannot be greater "
              + "than existing dimensionality (" + str(data.shape[1]) + ")!")
          return -1

      # Get the options for running PCA.
      s = True if options.find("-s") > -1 else False

      # Perform PCA.
      pca = decomposition.PCA(n_components = k, whiten = s)
      pca.fit(data)
      score = pca.transform(data)

    return totalTimer.ElapsedTime()

  '''
  Perform Principal Components Analysis. If the method has been successfully 
  completed return the elapsed time in seconds.

  @param options - Extra options for the method.
  @return - Elapsed time in seconds or -1 if the method was not successful.
  '''
  def RunMethod(self, options):
    Log.Info("Perform PCA.", self.verbose)

    return self.PCAScikit(options)
