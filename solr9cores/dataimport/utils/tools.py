
def normalize_list_santanderProfile(cl):
  search_terms = ['NAME', 'Name']
  index = next((cl.index(term) for term in search_terms if term in cl), -1)
  if index==-1: return cl
  cl[index]=cl[index].lower()
  return cl