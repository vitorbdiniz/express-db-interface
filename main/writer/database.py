def define_matrix_env(env):
    if env == "prod" or env == "producao" or env == "produção":
        host = "10.55.192.42"
        user = "vitor.diniz"
        password = "-uV3Fg*yA^xh?2VR&tAu6LH"
        dbname = "tc_matrix"
    elif env == "hml" or env == "homolog" or env == "homologação":
        host = "10.249.240.10"
        user = "mmuser"
        password = "TradersPetr4"
        dbname = "tc_matrix"
    else:
        raise AttributeError("Definição incorreta do ambiente")
    return (host, user, password, dbname)


class env():
    def __init__(self):
        self.host = "10.249.240.8"
        self.user = "vitor.diniz"
        self.password = "P@ssw0rd9090"
        self.dbname = "tcschool"
    
    def defined_db_env(self):
        return (self.host, self.user, self.password, self.dbname)
    def get_host(self):
        return self.host
    def get_user(self):
        return self.user
    def get_password(self):
        return self.password
    def get_dbname(self):
        return self.dbname


import urllib3, json

class tc_user():
    def __init__(self, env='hml'):
        self.id = "vitorbdiniz"
        self.password = self.make_password(env)
        self.login_resp = self.login_tc(env)
        self.token = self.generate_token()

    def make_password(self, env='hml'):
        return 'vbd10072020' if env=='prod' else "vbd3141592"

    def login_tc(self, env='hml'):
        http = urllib3.PoolManager()

        login = self.get_login()
        login = json.dumps(login, indent = 4).encode('utf-8')
        
        if env=='hml':
            resp = http.request('POST', 'https://tchml.tradersclub.com.br/api/v4/users/login', body=login)
        else:
            resp = http.request('POST', 'https://tc.tradersclub.com.br/api/v4/users/login', body=login)

        return resp

    def get_login(self):
        login = {
            "device_id":"",
            "login_id":self.id,
            "password":self.password,
            "token":None
            }
        return login

    def generate_token(self):
        if self.logged_in():
            cookie = str(self.login_resp.headers['set-cookie'])
            pos0 = cookie.find('MMAUTHTOKEN=')+12
            pos1 = cookie.find(';')
            token = cookie[pos0:pos1]
        else:
            token = None
        return token

    def logged_in(self):
        return self.login_resp.status < 300

    def get_token(self):
        return self.token

    def get_id(self):
        return self.id

    def __dict__(self) -> dict:
        return {
            'id':self.id,
            'password':self.password,
            'logged_in':self.logged_in(),
            'token':self.token
        }

    def __str__(self) -> str:
        return str(self.__dict__())
    
    