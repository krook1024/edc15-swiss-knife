def to_edcsuite(rows):
  result = ""
  for y, line in enumerate(rows):
    for x, val in enumerate(line):
        if val == '':
            result = result + '~'
            continue

        result = result + "{}{}:{}:{}:".format('~' if (x > 0 or y > 0) else '2', x, y, val)
  return result

def to_rows(inputStr: str):
  inputStr = inputStr.replace(",", ".")
  result = []

  tmp = inputStr.replace('2', '~', 1).split(':')
  line = []
  newl = ""
  skip = False
  for val in tmp:
    if (skip):
      skip = False
      continue

    if ('~' in val):
      skip = True

      if ("" == newl):
        newl = val # first number after ~ is our marker to start a new line

    if (not skip):
      line.append(val)

    if (val == newl and len(line) > 0):
      result.append(line)
      line = []

  if (len(line) > 0):
    result.append(line) # add any leftovers

  return result


if __name__=='__main__':
  for x in to_rows():
    print(x)