"""Main module."""
from numpy import dot, max, abs, arccos, arcsin, sqrt, Inf
from functools import reduce
from warnings import warn

from .utils import hav, spherToCart, isSpherical, \
  isGeographical, throw, hasKey, geoToSpher

'''
  @abstract n-norm of a number
 
  @param {Array} arr
  @param {Number} p
  @return {Number}
'''
def pNorm(arr, p):
  pNormFun=lambda dist, elem: dist + abs(elem) ** p
  return reduce(pNormFun, arr, 0) ** (1 / p)

'''
  @abstract returns the n-norm of a vector
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {Number} p
  @return {Number}
'''
def pNormDistance(coordinate_1, coordinate_2, p):
  if (p < 1):
    throw("The exponent n must be a number greater or equal to 1!")

  diffAbsFun=lambda coords: abs(coords[0] - coords[1])
  coordiff=list(map(diffAbsFun, zip(coordinate_1, coordinate_2)))

  return max(coordiff) if p == Inf else pNorm(coordiff, p)

'''
  @abstract returns the central angle between two coordinate points on a sphere
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {Number} p
  @return {Number}
'''
def sphereCentralAngle(coordinate_1, coordinate_2):
  longitude_1=coordinate_1[0]
  longitude_2=coordinate_2[0]
  
  latitude_1=coordinate_1[1]
  latitude_2=coordinate_2[1]
  
  aux_1=1 - hav(latitude_1 - latitude_2) - hav(latitude_1 + latitude_2)
  aux_2=hav(longitude_2 - longitude_1)
  aux_3=hav(latitude_2 - latitude_1)
  
  hav_theta=aux_3 + aux_2 * aux_1

  return 2 * arcsin(sqrt(hav_theta))

'''
  @abstract vector argument based on n-norm
 
  @param {Array} u
  @param {Array} v
  @param {Number} n
  @return {Number}
'''
def cosnuv(u, v, n):
  if(pNorm(u, n)==0 or pNorm(v, n)==0):
    msg='Method \'cosine\' does not support a null vector.'
    throw(msg, ZeroDivisionError)
  
  else:
    return dot(u, v) / (pNorm(u, n) * pNorm(v, n))

'''
  @abstract vector argument based on n-norm
 
  @param {Array} u
  @param {Array} v
  @param {Number} n
  @return {Number}
'''
def arguv(u, v, n):
  return arccos(cosnuv(u, v, n))

'''
  @abstract returns the central angle between two coordinate points on a sphere
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {Number} p
  @return {Number}
'''
def centralAngle(vector_1, vector_2, R):
  return arguv(spherToCart(vector_1, R), spherToCart(vector_2, R), 2)

'''
  @abstract returns the distance of two points on a sphere
 
  @param {Array} coord_1
  @param {Array} coord_2
  @param {Number} p
  @return {Number}
'''
def greatCircleDistance(coord_1, coord_2, R): 
  return R * sphereCentralAngle(coord_1, coord_2)

'''
  @abstract returns the distance of two points on a sphere
 
  @param {Array} coord_1
  @param {Array} coord_2
  @param {Number} n
  @return {Number}
'''
def nSphereDistance(coord_1, coord_2, R):
  return R * centralAngle(coord_1, coord_2, R)   

'''
  @abstract returns the distance of two points based on
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {String} method
  @param {Object} methodConfig
  @return {Number}
'''
def distance(coordinate_1, coordinate_2, method="euclidean", methodConfig={}):
  notification_message="There must exist property '_placeholder_' on config argument 'methodConfig'!"
  
  # pNorm-based distance
  if(method=="pnorm"):
    exponent=-1

    if (hasKey(methodConfig, "exponent")):
      exponent=methodConfig['exponent']
    else:
      emsg=notification_message.replace("_placeholder_", "radius")
      warn(emsg, UserWarning)
      
      exponent=2

    return pNormDistance(coordinate_1, coordinate_2, exponent)

  # 1-Norm-based distance
  elif(method=="manhattan" or method=="cityblock"):
    return pNormDistance(coordinate_1, coordinate_2, 1)

  # Cosine distance
  elif(method=="cosine"):
    return 1-cosnuv(coordinate_1, coordinate_2, 2)
  
  # Canberra distance
  elif(method=="canberra"):
    add_lambda=lambda acc, x: acc+x
    canberra_lambda=lambda x_i: (abs(x_i[0]-x_i[1]))/(abs(x_i[0])+abs(x_i[1]))
    
    return reduce(add_lambda, map(canberra_lambda, zip(coordinate_1, coordinate_2)))
  
  # Braycurtis distance
  elif(method=="braycurtis"):
    braycurtis_numerator_lambda=lambda acc, x_i: acc+abs(x_i[0]-x_i[1])
    braycurtis_denominator_lambda=lambda acc, x_i: acc+abs(x_i[0]+x_i[1])
    
    coords_zip=zip(coordinate_1, coordinate_2)
    numerator=reduce(braycurtis_numerator_lambda, coords_zip, 0)

    coords_zip=zip(coordinate_1, coordinate_2)
    denominator=reduce(braycurtis_denominator_lambda, coords_zip, 0)

    return numerator/denominator

  # 2-Norm-based distance
  elif(method=="euclidean"):
    return pNormDistance(coordinate_1, coordinate_2, 2)
  
  # Squared 2-Norm-based distance
  elif(method=="sqeuclidean"):
    return pNormDistance(coordinate_1, coordinate_2, 2) ** 2

  # Inf-Norm-based distance
  elif(method=="max" or method=="chebyshev"):
    return pNormDistance(coordinate_1, coordinate_2, Inf)

  # Sphere-based distance
  elif(method=="sphere"):
    are_spherical=isSpherical(coordinate_1) and isSpherical(coordinate_2)
    has_radius_key=hasKey(methodConfig, "radius")

    emsg1=notification_message.replace("_placeholder_", "radius")
    emsg2="Provided coordinates are not spherical!"
    
    return throw(emsg1, TypeError) if not has_radius_key \
      else ( \
        throw(emsg2, TypeError) if not are_spherical \
        else nSphereDistance(coordinate_1, coordinate_2, methodConfig['radius']) \
      )
  
  # Sphere-based distance
  elif(method=="geographical"):
    coordinate_1_is_geographical=isGeographical(coordinate_1)
    coordinate_2_is_geographical=isGeographical(coordinate_2)
    are_geographical=coordinate_1_is_geographical and coordinate_2_is_geographical
    both_are_not_geographical=not coordinate_1_is_geographical and not coordinate_2_is_geographical
    
    has_radius_key=hasKey(methodConfig, "radius")

    emsg1=notification_message.replace("_placeholder_", "radius")
    
    subject='Both provided coordinates' if both_are_not_geographical \
      else (\
        'Provided coordinate 1' if not coordinate_1_is_geographical \
        else ( \
          'Provided coordinate 2' if not coordinate_2_is_geographical \
          else 'None'
        ) 
      )
    verb= 'are' if both_are_not_geographical else 'is'

    emsg2="{subject} {verb} not geographical!".format(subject=subject, verb=verb)
    
    return throw(emsg1, TypeError) if not has_radius_key \
      else ( \
        throw(emsg2, TypeError) if not are_geographical \
        else nSphereDistance(
        geoToSpher(coordinate_1[0], coordinate_1[1]), \
        geoToSpher(coordinate_2[0], coordinate_2[1]), \
        methodConfig['radius']
      ) 
      )

  # Complains on unknown method
  else:
    methods=['pnorm', 'cosine', 'sqeuclidean', 'euclidean', 'manhattan', 
             'cityblock', 'max', 'chebyshev', 'sphere', 'geographical']
    emsg="Method \"{method}\" not found among available methods: {methods}".format(\
      method=method, methods=str(methods)
    )
    throw(emsg, TypeError)

'''
  @abstract returns the distance of two points based on
 
  @param {Array} coordinate_1
  @param {Array} coordinate_2
  @param {String} method
  @param {Object} methodConfig
  @return {Number}
'''
def travelTime( average_speed, coordinate_1, coordinate_2, method="euclidean", methodConfig={}):
    return distance(coordinate_1, coordinate_2, method, methodConfig) / average_speed
