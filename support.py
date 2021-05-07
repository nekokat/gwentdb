def modifyrows(html_data ,rows):
  modified_rows = []
  for row in rows:
    opp_fraction = html_data[row[3].i['class'][1]]
    result_score = row[4].text.split(" ")
    row = (row[0].text, row[2].text, row[3].text, opp_fraction, *result_score)
    modified_rows.append(row)
  return modified_rows

def сondition(cond, jumper= ", "):
  return jumper.join([f"{column} = '{value}'" for column, value in cond])

def log(countrows):
  print(f'\nAdded: {countrows} rows.')
  print('Done')