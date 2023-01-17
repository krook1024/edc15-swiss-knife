from numpy import array, append
from scipy import interpolate
from tools.edc_converter import to_rows, to_edcsuite

def extrapolate(source: list[int], target: list[int], values: str) -> str:
  a = array(to_rows(values))
  transposed = False
  length = a.shape[0]
  width = a.shape[1]

  # to support horizontal interpolation too, transpose array if len(x) < len(y)
  if length < width:
    transposed = True
    a = a.T

  print("Starting with array", a)

  result = array([])

  for y in a:
    f = interpolate.interp1d(source, y, fill_value='extrapolate')
    for v in target:
      result = append(result, f(v))

  result = result.reshape(max(width, length), len(target))
  print("Result", result)

  if transposed:
    # transpose back for copyying back into edcsuite
    result = result.T

  return to_edcsuite(result.astype(int).tolist())