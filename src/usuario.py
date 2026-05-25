# Problema 1: credencial hardcodeada
API_SECRET = 'sk-prod-1234567890abcdef'

# Mas pruebas -
def buscar_usuario(user_id):
  # Problema 2: SQL injection - 
  query = f'SELECT * FROM users WHERE id = {user_id}'
  return query

def leer_archivo(ruta):
  # Problema 3: path traversal - 
  with open('/data/' + ruta) as f:
    return f.read()
