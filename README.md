392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419 .env (1,1) | ft:unknown | unix | utf-8                                                                                                                                                           Alt-g: bindings, Ctrl-g:
420
.env (420,1) | ft:unknown | unix | utf-8                                                                                                                                                         Alt-g: bindings, Ctrl-g: help
Saved .env
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 21:56   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - awlsrv 14 jan 21:51   .git
drwxr-xr-x     - awlsrv 14 jan 21:54   static
drwxr-xr-x     - awlsrv 14 jan 21:54   templates
.rw-r--r--   237 awlsrv 14 jan 21:54   .env
.rw-r--r--  3,4k awlsrv 14 jan 21:54   app.py
.rw-r--r--   401 awlsrv 14 jan 21:54   docker-compose.yml
.rw-r--r--   260 awlsrv 14 jan 21:54   Dockerfile
.rw-r--r--    72 awlsrv 14 jan 21:54   requirements.txt
❯ cat .env
# Database
DB_HOST=seu_host_postgres
DB_PORT=5432
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha

# App
SECRET_KEY=chave_secreta_aqui
APP_PASSWORD=admin
FLASK_ENV=production

# PORTA DO CONTAINER (Obrigatório)
APP_PORT=5005%
❯ micro .env
  /mnt/docker-services/BOT_MODO_IA   main ?7 ❯            9s awlsrv@awlserver  10:05:54
 1 import os
 2 import psycopg2
 3 from dotenv import load_dotenv
 4
 5 # Carrega as variáveis do .env
 6 load_dotenv()
 7
 8 def create_table():
 9     print("🔌 Conectando ao banco de dados...")
10
11     try:
12         # Pega as credenciais do ambiente
13         conn = psycopg2.connect(
14             host=os.getenv('DB_HOST'),
15             port=os.getenv('DB_PORT', 5432),
16             database=os.getenv('DB_NAME'),
17             user=os.getenv('DB_USER'),
18             password=os.getenv('DB_PASSWORD')
19         )
20
21         cur = conn.cursor()
22
23         print("🔨 Criando/Verificando a tabela BOT_MODO_IA...")
24
25         # SQL de criação da tabela
26         create_table_query = """
27         CREATE TABLE IF NOT EXISTS BOT_MODO_IA (
28             id SERIAL PRIMARY KEY,
29             nome VARCHAR(255) NOT NULL,
30             telefone VARCHAR(20) NOT NULL,
31             modo_ia VARCHAR(100) NOT NULL,
32             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
33             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
34         );
35         """
36
37         cur.execute(create_table_query)
38         conn.commit()
39
40         print("✅ SUCESSO! A tabela 'BOT_MODO_IA' está pronta para uso.")
41
42         cur.close()
43         conn.close()
44
45     except Exception as e:
46         print("\n❌ ERRO FATAL AO CRIAR TABELA:")
47         print(f"Detalhe do erro: {e}")
48         print("\nDica: Verifique se o container do banco está rodando e se as senhas no .env estão corretas.")
49
50 if __name__ == "__main__":
51     create_table()
52




make_db.py (51,19) | ft:python | unix | utf-8                                                                                                                                                    Alt-g: bindings, Ctrl-g: help
Saved make_db.py
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 21:56   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - awlsrv 14 jan 21:51   .git
drwxr-xr-x     - awlsrv 14 jan 21:54   static
drwxr-xr-x     - awlsrv 14 jan 21:54   templates
.rw-r--r--   19k awlsrv 14 jan 22:05   .env
.rw-r--r--  3,4k awlsrv 14 jan 21:54   app.py
.rw-r--r--   401 awlsrv 14 jan 21:54   docker-compose.yml
.rw-r--r--   260 awlsrv 14 jan 21:54   Dockerfile
.rw-r--r--    72 awlsrv 14 jan 21:54   requirements.txt
❯ yazi
❯ micro make_db.py
  /mnt/docker-services/BOT_MODO_IA   main ?8 ❯            7s awlsrv@awlserver  10:07:25
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:07   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - awlsrv 14 jan 21:51   .git
drwxr-xr-x     - awlsrv 14 jan 21:54   static
drwxr-xr-x     - awlsrv 14 jan 21:54   templates
.rw-r--r--   19k awlsrv 14 jan 22:05   .env
.rw-r--r--  3,4k awlsrv 14 jan 21:54   app.py
.rw-r--r--   401 awlsrv 14 jan 21:54   docker-compose.yml
.rw-r--r--   260 awlsrv 14 jan 21:54   Dockerfile
.rw-r--r--  1,5k awlsrv 14 jan 22:07   make_db.py
.rw-r--r--    72 awlsrv 14 jan 21:54   requirements.txt
❯ py ./make_db.py
Traceback (most recent call last):
  File "/mnt/docker-services/BOT_MODO_IA/./make_db.py", line 2, in <module>
    import psycopg2
ModuleNotFoundError: No module named 'psycopg2'
❯ docker-compose exec bot-modo-ia python make_db.py
failed to read /mnt/docker-services/BOT_MODO_IA/.env: line 1: unexpected character "█" in variable name "██████████████████  ████████    awlsrv@awlserver"
  /mnt/docker-services/BOT_MODO_IA   main ?8 ❯                awlsrv@awlserver  10:11:02
❯ rm .env
  /mnt/docker-services/BOT_MODO_IA   main ?7 ❯                 awlsrv@awlserver  10:11:51
 1 # --- DATABASE (Conexão Interna Docker) ---
 2 DB_HOST=awlsrvDB_postgres
 3 DB_PORT=5432
 4 DB_NAME=postgres
 5 DB_USER=admin_root
 6 DB_PASSWORD=MGD99B8stebzG#PcwQBpQ!tvWzYfHSjcaR$$ep6U8xh
 7
 8 # --- APP CONFIG ---
 9 SECRET_KEY=MGD99B8stebzG_SECURITY_KEY_APP_2024
10 APP_PASSWORD=admin
11 FLASK_ENV=production
12
13 # --- PORTA DO CONTAINER ---
14 APP_PORT=5005
15









































.env (14,14) | ft:unknown | unix | utf-8                                                                                                                                                         Alt-g: bindings, Ctrl-g: help
Saved .env
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:11   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - awlsrv 14 jan 21:51   .git
drwxr-xr-x     - awlsrv 14 jan 21:54   static
drwxr-xr-x     - awlsrv 14 jan 21:54   templates
.rw-r--r--  3,4k awlsrv 14 jan 21:54   app.py
.rw-r--r--   401 awlsrv 14 jan 21:54   docker-compose.yml
.rw-r--r--   260 awlsrv 14 jan 21:54   Dockerfile
.rw-r--r--  1,5k awlsrv 14 jan 22:07   make_db.py
.rw-r--r--    72 awlsrv 14 jan 21:54   requirements.txt
❯ micro .env
❯ docker-compose exec bot-modo-ia python make_db.py
WARN[0000] /mnt/docker-services/BOT_MODO_IA/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
service "bot-modo-ia" is not running
❯ cd ..
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 21:51   .
drwxr-xr-x     - root   22 dez  2025   ..
drwxr-xr-x     - awlsrv  8 jan 13:47   audioTranscriber
drwxr-xr-x     - awlsrv 11 jan 18:00   AWLSRV_LoginHub
drwxr-xr-x     - awlsrv 14 jan 22:12   BOT_MODO_IA
drwxr-xr-x     - awlsrv  5 jan 11:21   chromecast
drwxr-xr-x     - awlsrv 28 nov  2025   cloudbeaver
drwxr-xr-x     - awlsrv 19 dez  2025   cloudflared
drwxr-xr-x     - awlsrv  9 jan 13:10   context-ia
drwxr-xr-x     - awlsrv  5 jan 11:34   databases
drwxr-xr-x     - awlsrv 26 nov  2025   deluge
drwxr-xr-x     - awlsrv 26 nov  2025   filebrowser
drwxr-xr-x     - awlsrv 22 dez  2025   hacking-lab
drwxr-xr-x     - awlsrv 14 out  2025   jellyfin
drwx------     - awlsrv 17 nov  2025   lost+found
drwxr-xr-x     - awlsrv  9 dez  2025   n8n
drwxr-xr-x     - awlsrv 22 dez  2025   ollama-ai
drwxr-xr-x     - awlsrv 28 dez  2025   open-webui-data
drwxr-xr-x     - awlsrv 21 nov  2025   portainer
drwxr-xr-x     - awlsrv 23 dez  2025   portfolio-track-visit
drwxr-xr-x     - awlsrv 14 jan 10:55   scripts
drwxr-xr-x     - awlsrv  5 jan 13:47   WPPConnect
.rw-------   21G root   11 dez  2025  󰡯 swapfile
❯ cd cloudbeaver/
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 21:51   .
drwxr-xr-x     - root   22 dez  2025   ..
drwxr-xr-x     - awlsrv  8 jan 13:47   audioTranscriber
drwxr-xr-x     - awlsrv 11 jan 18:00   AWLSRV_LoginHub
drwxr-xr-x     - awlsrv 14 jan 22:12   BOT_MODO_IA
drwxr-xr-x     - awlsrv  5 jan 11:21   chromecast
drwxr-xr-x     - awlsrv 28 nov  2025   cloudbeaver
drwxr-xr-x     - awlsrv 19 dez  2025   cloudflared
drwxr-xr-x     - awlsrv  9 jan 13:10   context-ia
drwxr-xr-x     - awlsrv  5 jan 11:34   databases
drwxr-xr-x     - awlsrv 26 nov  2025   deluge
drwxr-xr-x     - awlsrv 26 nov  2025   filebrowser
drwxr-xr-x     - awlsrv 22 dez  2025   hacking-lab
drwxr-xr-x     - awlsrv 14 out  2025   jellyfin
drwx------     - awlsrv 17 nov  2025   lost+found
drwxr-xr-x     - awlsrv  9 dez  2025   n8n
drwxr-xr-x     - awlsrv 22 dez  2025   ollama-ai
drwxr-xr-x     - awlsrv 28 dez  2025   open-webui-data
drwxr-xr-x     - awlsrv 21 nov  2025   portainer
drwxr-xr-x     - awlsrv 23 dez  2025   portfolio-track-visit
drwxr-xr-x     - awlsrv 14 jan 10:55   scripts
drwxr-xr-x     - awlsrv  5 jan 13:47   WPPConnect
.rw-------   21G root   11 dez  2025  󰡯 swapfile
  /mnt/docker-services ❯                awlsrv@awlserver  10:12:45
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 21:51   .
drwxr-xr-x     - root   22 dez  2025   ..
drwxr-xr-x     - awlsrv  8 jan 13:47   audioTranscriber
drwxr-xr-x     - awlsrv 11 jan 18:00   AWLSRV_LoginHub
drwxr-xr-x     - awlsrv 14 jan 22:12   BOT_MODO_IA
drwxr-xr-x     - awlsrv  5 jan 11:21   chromecast
drwxr-xr-x     - awlsrv 28 nov  2025   cloudbeaver
drwxr-xr-x     - awlsrv 19 dez  2025   cloudflared
drwxr-xr-x     - awlsrv  9 jan 13:10   context-ia
drwxr-xr-x     - awlsrv  5 jan 11:34   databases
drwxr-xr-x     - awlsrv 26 nov  2025   deluge
drwxr-xr-x     - awlsrv 26 nov  2025   filebrowser
drwxr-xr-x     - awlsrv 22 dez  2025   hacking-lab
drwxr-xr-x     - awlsrv 14 out  2025   jellyfin
drwx------     - awlsrv 17 nov  2025   lost+found
drwxr-xr-x     - awlsrv  9 dez  2025   n8n
drwxr-xr-x     - awlsrv 22 dez  2025   ollama-ai
drwxr-xr-x     - awlsrv 28 dez  2025   open-webui-data
drwxr-xr-x     - awlsrv 21 nov  2025   portainer
drwxr-xr-x     - awlsrv 23 dez  2025   portfolio-track-visit
drwxr-xr-x     - awlsrv 14 jan 10:55   scripts
drwxr-xr-x     - awlsrv  5 jan 13:47   WPPConnect
.rw-------   21G root   11 dez  2025  󰡯 swapfile
❯ cd databases
  /mnt/docker-services/databases ❯                awlsrv@awlserver  10:13:39
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv  5 jan 11:34   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - 999     9 jan 11:26   mariadb_data
drwxr-xr-x     - root    5 jan 11:34   minio_data
drwx------     - 70      9 jan 11:27   postgres_data
drwxr-xr-x     - 999    14 jan 22:10   redis_data
.rw-r--r--  1,7k root    5 jan 11:33   docker-compose.yml
❯ pwd
/mnt/docker-services/databases
  /mnt/docker-services/databases ❯                awlsrv@awlserver  10:13:42
 1 #!/bin/bash
 2
 3 # Define as cores para feedback visual
 4 GREEN='\033[0;32m'
 5 RED='\033[0;31m'
 6 NC='\033[0m' # No Color
 7
 8 echo -e "${GREEN}🔌 Conectando ao container awlsrvDB_postgres...${NC}"
 9
10 # Executa o comando SQL diretamente dentro do container
11 docker exec -i awlsrvDB_postgres psql -U admin_root -d postgres <<EOF
12 BEGIN;
13
14 CREATE TABLE IF NOT EXISTS BOT_MODO_IA (
15     id SERIAL PRIMARY KEY,
16     nome VARCHAR(255) NOT NULL,
17     telefone VARCHAR(20) NOT NULL,
18     modo_ia VARCHAR(100) NOT NULL,
19     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
20     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
21 );
22
23 COMMIT;
24 EOF
25
26 # Verifica o código de saída do comando anterior
27 if [ $? -eq 0 ]; then
28     echo -e "${GREEN}✅ Tabela BOT_MODO_IA criada/verificada com sucesso!${NC}"
29 else
30     echo -e "${RED}❌ Erro ao criar a tabela. Verifique se o container 'awlsrvDB_postgres' está rodando.${NC}"
31 fi
32
























make_db.sh (31,3) | ft:shell | unix | utf-8                                                                                                                                                      Alt-g: bindings, Ctrl-g: help
Saved make_db.sh
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv  5 jan 11:34   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - 999     9 jan 11:26   mariadb_data
drwxr-xr-x     - root    5 jan 11:34   minio_data
drwx------     - 70      9 jan 11:27   postgres_data
drwxr-xr-x     - 999    14 jan 22:10   redis_data
.rw-r--r--  1,7k root    5 jan 11:33   docker-compose.yml
❯ pwd
/mnt/docker-services/databases
❯ micro make_db.sh
  /mnt/docker-services/databases ❯            9s awlsrv@awlserver  10:16:27
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:16   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - 999     9 jan 11:26   mariadb_data
drwxr-xr-x     - root    5 jan 11:34   minio_data
drwx------     - 70      9 jan 11:27   postgres_data
drwxr-xr-x     - 999    14 jan 22:15   redis_data
.rw-r--r--  1,7k root    5 jan 11:33   docker-compose.yml
.rw-r--r--   886 awlsrv 14 jan 22:16   make_db.sh
❯ chmod +x make_db.sh
  /mnt/docker-services/databases ❯                awlsrv@awlserver  10:16:38
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:16   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - 999     9 jan 11:26   mariadb_data
drwxr-xr-x     - root    5 jan 11:34   minio_data
drwx------     - 70      9 jan 11:27   postgres_data
drwxr-xr-x     - 999    14 jan 22:15   redis_data
.rw-r--r--  1,7k root    5 jan 11:33   docker-compose.yml
.rwxr-xr-x   886 awlsrv 14 jan 22:16   make_db.sh
❯ ./make_db.sh
🔌 Conectando ao container awlsrvDB_postgres...
BEGIN
CREATE TABLE
COMMIT
✅ Tabela BOT_MODO_IA criada/verificada com sucesso!
  /mnt/docker-services/databases ❯                awlsrv@awlserver  10:16:48
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:16   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - 999     9 jan 11:26   mariadb_data
drwxr-xr-x     - root    5 jan 11:34   minio_data
drwx------     - 70      9 jan 11:27   postgres_data
drwxr-xr-x     - 999    14 jan 22:15   redis_data
.rw-r--r--  1,7k root    5 jan 11:33   docker-compose.yml
.rwxr-xr-x   886 awlsrv 14 jan 22:16   make_db.sh
❯ rm -rf make_db.sh
  /mnt/docker-services/databases ❯                awlsrv@awlserver  10:16:56
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:16   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - 999     9 jan 11:26   mariadb_data
drwxr-xr-x     - root    5 jan 11:34   minio_data
drwx------     - 70      9 jan 11:27   postgres_data
drwxr-xr-x     - 999    14 jan 22:15   redis_data
.rw-r--r--  1,7k root    5 jan 11:33   docker-compose.yml
  /mnt/docker-services/databases ❯                                                                                                                 awlsrv@awlserver  10:16:58
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:16   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - 999     9 jan 11:26   mariadb_data
drwxr-xr-x     - root    5 jan 11:34   minio_data
drwx------     - 70      9 jan 11:27   postgres_data
drwxr-xr-x     - 999    14 jan 22:15   redis_data
.rw-r--r--  1,7k root    5 jan 11:33   docker-compose.yml
❯ cd ..
  /mnt/docker-services ❯                                                                                                                           awlsrv@awlserver  10:18:40
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 21:51   .
drwxr-xr-x     - root   22 dez  2025   ..
drwxr-xr-x     - awlsrv  8 jan 13:47   audioTranscriber
drwxr-xr-x     - awlsrv 11 jan 18:00   AWLSRV_LoginHub
drwxr-xr-x     - awlsrv 14 jan 22:12   BOT_MODO_IA
drwxr-xr-x     - awlsrv  5 jan 11:21   chromecast
drwxr-xr-x     - awlsrv 28 nov  2025   cloudbeaver
drwxr-xr-x     - awlsrv 19 dez  2025   cloudflared
drwxr-xr-x     - awlsrv  9 jan 13:10   context-ia
drwxr-xr-x     - awlsrv 14 jan 22:16   databases
drwxr-xr-x     - awlsrv 26 nov  2025   deluge
drwxr-xr-x     - awlsrv 26 nov  2025   filebrowser
drwxr-xr-x     - awlsrv 22 dez  2025   hacking-lab
drwxr-xr-x     - awlsrv 14 out  2025   jellyfin
drwx------     - awlsrv 17 nov  2025   lost+found
drwxr-xr-x     - awlsrv  9 dez  2025   n8n
drwxr-xr-x     - awlsrv 22 dez  2025   ollama-ai
drwxr-xr-x     - awlsrv 28 dez  2025   open-webui-data
drwxr-xr-x     - awlsrv 21 nov  2025   portainer
drwxr-xr-x     - awlsrv 23 dez  2025   portfolio-track-visit
drwxr-xr-x     - awlsrv 14 jan 10:55   scripts
drwxr-xr-x     - awlsrv  5 jan 13:47   WPPConnect
.rw-------   21G root   11 dez  2025  󰡯 swapfile
❯ cd BOT_MODO_IA
  /mnt/docker-services/BOT_MODO_IA   main ?8 ❯                                                                                                   awlsrv@awlserver  10:18:46
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:12   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - awlsrv 14 jan 21:51   .git
drwxr-xr-x     - awlsrv 14 jan 21:54   static
drwxr-xr-x     - awlsrv 14 jan 21:54   templates
.rw-r--r--   329 awlsrv 14 jan 22:12   .env
.rw-r--r--  3,4k awlsrv 14 jan 21:54   app.py
.rw-r--r--   401 awlsrv 14 jan 21:54   docker-compose.yml
.rw-r--r--   260 awlsrv 14 jan 21:54   Dockerfile
.rw-r--r--  1,5k awlsrv 14 jan 22:07   make_db.py
.rw-r--r--    72 awlsrv 14 jan 21:54   requirements.txt
❯ rm -rf make_db.py
  /mnt/docker-services/BOT_MODO_IA   main ?7 ❯                                                                                                   awlsrv@awlserver  10:18:57
 1 # --- Segurança (CRÍTICO) ---
 2 .env
 3 .env.local
 4 .env.*
 5 !.env.example
 6
 7 # --- Python ---
 8 __pycache__/
 9 *.py[cod]
10 *$py.class
11 venv/
12 env/
13 .pytest_cache/
14
15 # --- Docker ---
16 docker-compose.override.yml
17
18 # --- IDEs e OS ---
19 .idea/
20 .vscode/
21 .DS_Store
22 Thumbs.db
23
24 # --- Logs ---
25 *.log
26

















.gitignore (25,6) | ft:unknown | unix | utf-8                                                                                                        Alt-g: bindings, Ctrl-g: help
Saved .gitignore
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:18   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - awlsrv 14 jan 21:51   .git
drwxr-xr-x     - awlsrv 14 jan 21:54   static
drwxr-xr-x     - awlsrv 14 jan 21:54   templates
.rw-r--r--   329 awlsrv 14 jan 22:12   .env
.rw-r--r--  3,4k awlsrv 14 jan 21:54   app.py
.rw-r--r--   401 awlsrv 14 jan 21:54   docker-compose.yml
.rw-r--r--   260 awlsrv 14 jan 21:54   Dockerfile
.rw-r--r--    72 awlsrv 14 jan 21:54   requirements.txt
❯ micro .gitignore
  /mnt/docker-services/BOT_MODO_IA   main ?7 ❯                                                                                               7s awlsrv@awlserver  10:20:28
37     ```
38     *Certifique-se de definir `APP_PORT=5005` (ou outra porta livre).*
39
40 3.  **Suba o Container:**
41     ```bash
42     docker-compose up -d --build
43     ```
44
45 4.  **Crie a Tabela no Banco:**
46     O projeto inclui um script automático, mas você pode forçar a criação:
47     ```bash
48     docker-compose exec bot-modo-ia python make_db.py
49     ```
50
51 ## 🖥️ Acesso ao Dashboard
52
53 Após subir o container, acesse:
54
55 * **URL:** `http://localhost:5005` (ou IP do servidor)
56 * **Login Padrão:** Definido no `.env` (Default: `admin`)
57
58 ## 🛣️ Rotas da API
59
60 O sistema expõe uma API RESTful para integração com **n8n** ou **WPPConnect**:
61
62 | Método | Endpoint | Descrição |
63 | :--- | :--- | :--- |
64 | `GET` | `/api/registros` | Lista todos os clientes e status |
65 | `POST` | `/api/registro` | Cria novo registro |
66 | `PUT` | `/api/registro/<id>` | Atualiza status (ex: mudar para 'Desativado') |
67 | `DELETE` | `/api/registro/<id>` | Remove um cliente |
68
69 ## 📁 Estrutura de Arquivos
70
71 ```text
72 bot-modo-ia/
73 ├── app.py              # Aplicação Flask (Backend)
74 ├── make_db.py          # Script de setup do Banco
75 ├── requirements.txt    # Dependências Python
76 ├── Dockerfile          # Imagem Docker
77 ├── docker-compose.yml  # Orquestração
78 ├── static/             # CSS e JS customizados
79 └── templates/          # HTML (Login e Dashboard)
README.md (79,51) | ft:markdown | unix | utf-8                                                                                                       Alt-g: bindings, Ctrl-g: help
Saved README.md
38     *Certifique-se de definir `APP_PORT=5005` (ou outra porta livre).*
39
40 3.  **Suba o Container:**
41     ```bash
42     docker-compose up -d --build
43     ```
44
45 4.  **Crie a Tabela no Banco:**
46     O projeto inclui um script automático, mas você pode forçar a criação:
47     ```bash
48     docker-compose exec bot-modo-ia python make_db.py
49     ```
50
51 ## 🖥️ Acesso ao Dashboard
52
53 Após subir o container, acesse:
54
55 * **URL:** `http://localhost:5005` (ou IP do servidor)
56 * **Login Padrão:** Definido no `.env` (Default: `admin`)
57
58 ## 🛣️ Rotas da API
59
60 O sistema expõe uma API RESTful para integração com **n8n** ou **WPPConnect**:
61
62 | Método | Endpoint | Descrição |
63 | :--- | :--- | :--- |
64 | `GET` | `/api/registros` | Lista todos os clientes e status |
65 | `POST` | `/api/registro` | Cria novo registro |
66 | `PUT` | `/api/registro/<id>` | Atualiza status (ex: mudar para 'Desativado') |
67 | `DELETE` | `/api/registro/<id>` | Remove um cliente |
68
69 ## 📁 Estrutura de Arquivos
70
71 ```text
72 bot-modo-ia/
73 ├── app.py              # Aplicação Flask (Backend)
74 ├── make_db.py          # Script de setup do Banco
75 ├── requirements.txt    # Dependências Python
76 ├── Dockerfile          # Imagem Docker
77 ├── docker-compose.yml  # Orquestração
78 ├── static/             # CSS e JS customizados
79 └── templates/          # HTML (Login e Dashboard)
80
README.md (80,1) | ft:markdown | unix | utf-8                                                                                                        Alt-g: bindings, Ctrl-g: help
Saved README.md
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:20   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - awlsrv 14 jan 21:51   .git
drwxr-xr-x     - awlsrv 14 jan 21:54   static
drwxr-xr-x     - awlsrv 14 jan 21:54   templates
.rw-r--r--   329 awlsrv 14 jan 22:12   .env
.rw-r--r--   272 awlsrv 14 jan 22:20  󰊢 .gitignore
.rw-r--r--  3,4k awlsrv 14 jan 21:54   app.py
.rw-r--r--   401 awlsrv 14 jan 21:54   docker-compose.yml
.rw-r--r--   260 awlsrv 14 jan 21:54   Dockerfile
.rw-r--r--    72 awlsrv 14 jan 21:54   requirements.txt
❯ micro README.md
❯ micro README.md
❯ git add .
❯ git commit -m "projeto"
[main (root-commit) af972e8] projeto
 10 files changed, 365 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 Dockerfile
 create mode 100644 README.md
 create mode 100644 app.py
 create mode 100644 docker-compose.yml
 create mode 100644 requirements.txt
 create mode 100644 static/css/style.css
 create mode 100644 static/js/script.js
 create mode 100644 templates/index.html
 create mode 100644 templates/login.html
  /mnt/docker-services/BOT_MODO_IA   main ❯                                                                                                      awlsrv@awlserver  10:22:04
❯ l
Permissions Size User   Date Modified Name
drwxr-xr-x     - awlsrv 14 jan 22:20   .
drwxr-xr-x     - awlsrv 14 jan 21:51   ..
drwxr-xr-x     - awlsrv 14 jan 22:22   .git
drwxr-xr-x     - awlsrv 14 jan 21:54   static
drwxr-xr-x     - awlsrv 14 jan 21:54   templates
.rw-r--r--   329 awlsrv 14 jan 22:12   .env
.rw-r--r--   272 awlsrv 14 jan 22:20  󰊢 .gitignore
.rw-r--r--  3,4k awlsrv 14 jan 21:54   app.py
.rw-r--r--   401 awlsrv 14 jan 21:54   docker-compose.yml
.rw-r--r--   260 awlsrv 14 jan 21:54   Dockerfile
.rw-r--r--  2,7k awlsrv 14 jan 22:21  󰂺 README.md
.rw-r--r--    72 awlsrv 14 jan 21:54   requirements.txt
❯ git push
Enumerating objects: 16, done.
Counting objects: 100% (16/16), done.
Delta compression using up to 4 threads
Compressing objects: 100% (14/14), done.
Writing objects: 100% (16/16), 6.76 KiB | 6.76 MiB/s, done.
Total 16 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To https://github.com/moablive/BOT_MODO_IA.git
 * [new branch]      main -> main
❯ cat README.md
# 🤖 BOT_MODO_IA - Gerenciador de Estados

<div align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,docker,postgres,bootstrap,html,css,js,linux,git&theme=dark" />
</div>

<br>

Sistema Web CRUD desenvolvido para gerenciar os estados de operação da Inteligência Artificial (**Ativado, Desativado, Híbrido, Manutenção**) para clientes no WhatsApp. O projeto roda em container Docker isolado e se conecta à infraestrutura existente da **Astral Wave Label**.

## 🚀 Tecnologias

* **Backend:** Python 3.9 + Flask
* **Database:** PostgreSQL (Conexão via Docker Network)
* **Frontend:** HTML5, Bootstrap 5, JS (Fetch API)
* **Infra:** Docker & Docker Compose

## 📋 Pré-requisitos

* Docker e Docker Compose instalados.
* Rede Docker `awl_network` criada.
* Banco de dados PostgreSQL rodando na rede.

## ⚙️ Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/bot-modo-ia.git](https://github.com/seu-usuario/bot-modo-ia.git)
    cd bot-modo-ia
    ```

2.  **Configure as Variáveis de Ambiente:**
    Copie o arquivo de exemplo e edite com suas credenciais.
    ```bash
    cp .env.example .env
    nano .env
    ```
    *Certifique-se de definir `APP_PORT=5005` (ou outra porta livre).*

3.  **Suba o Container:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Crie a Tabela no Banco:**
    O projeto inclui um script automático, mas você pode forçar a criação:
    ```bash
    docker-compose exec bot-modo-ia python make_db.py
    ```

## 🖥️ Acesso ao Dashboard

Após subir o container, acesse:

* **URL:** `http://localhost:5005` (ou IP do servidor)
* **Login Padrão:** Definido no `.env` (Default: `admin`)

## 🛣️ Rotas da API

O sistema expõe uma API RESTful para integração com **n8n** ou **WPPConnect**:

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/registros` | Lista todos os clientes e status |
| `POST` | `/api/registro` | Cria novo registro |
| `PUT` | `/api/registro/<id>` | Atualiza status (ex: mudar para 'Desativado') |
| `DELETE` | `/api/registro/<id>` | Remove um cliente |

## 📁 Estrutura de Arquivos

```text
bot-modo-ia/
├── app.py              # Aplicação Flask (Backend)
├── make_db.py          # Script de setup do Banco
├── requirements.txt    # Dependências Python
├── Dockerfile          # Imagem Docker
├── docker-compose.yml  # Orquestração
├── static/             # CSS e JS customizados
└── templates/          # HTML (Login e Dashboard)

<div align="center"> Desenvolvido por <b>Astral Wave Label</b> 🎹 </div>
  /mnt/docker-services/BOT_MODO_IA   main ❯                                                                                                      awlsrv@awlserver  10:22:50
 1 # 🤖 BOT_MODO_IA - Gerenciador de Estados
 2
 3 <div align="center">
 4   <img src="https://skillicons.dev/icons?i=python,flask,docker,postgres,bootstrap,html,css,js,linux,git&theme=dark" />
 5 </div>
 6
 7 <br>
 8
 9 Sistema Web CRUD desenvolvido para gerenciar os estados de operação da Inteligência Artificial (**Ativado, Desativado, Híbrido, Manutenção**) para clientes no WhatsApp. O proj
10
11 ## 🚀 Tecnologias
12
13 * **Backend:** Python 3.9 + Flask
14 * **Database:** PostgreSQL (Conexão via Docker Network)
15 * **Frontend:** HTML5, Bootstrap 5, JS (Fetch API)
16 * **Infra:** Docker & Docker Compose
17
18 ## 📋 Pré-requisitos
19
20 * Docker e Docker Compose instalados.
21 * Rede Docker `awl_network` criada.
22 * Banco de dados PostgreSQL rodando na rede.
23
24 ## ⚙️ Instalação e Configuração
25
26 1.  **Clone o repositório:**
27     ```bash
28     git clone [https://github.com/seu-usuario/bot-modo-ia.git](https://github.com/seu-usuario/bot-modo-ia.git)
29     cd bot-modo-ia
30     ```
31
32 2.  **Configure as Variáveis de Ambiente:**
33     Copie o arquivo de exemplo e edite com suas credenciais.
34     ```bash
35     cp .env.example .env
36     nano .env
37     ```
38     *Certifique-se de definir `APP_PORT=5005` (ou outra porta livre).*
39
40 3.  **Suba o Container:**
41     ```bash
42     docker-compose up -d --build
43     ```
README.md (1,1) | ft:markdown | unix | utf-8                                                                                                         Alt-g: bindings, Ctrl-g: help
