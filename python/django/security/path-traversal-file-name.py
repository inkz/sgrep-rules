
def post1(request, format=None):
  try:
      # ruleid: path-traversal
      app_log_path = request.data['app_log_path']
      host = request.data['host']
      connect = connect_init(host)
      commands = "find %s -name '*.log'" % (app_log_path)
      result = connect.run(commands).stdout
      res = []
      for i in result.split():
          res.append(i)
      res = filter(None, res)
      connect.close()
      http_status = OK
  except:
      print("foo")

def post2(request, format=None):
  try:
      # ruleid: path-traversal
      app_log_path = request.data['app_log_path']
      host = request.data['host']
      connect = connect_init(host)
      commands = 'hours_{0}.csv'.format(app_log_path)
      result = connect.run(commands).stdout
      res = []
      for i in result.split():
          res.append(i)
      res = filter(None, res)
      connect.close()
      http_status = OK
  except:
      print("foo")

def post3(request, format=None):
  try:
      # should be ok given that we call abspath
      app_log_path = request.data['app_log_path']
      app_log_path = os.path.abspath(app_log_path)
      host = request.data['host']
      connect = connect_init(host)
      commands = "find %s -name '*.log'" % (app_log_path)
      result = connect.run(commands).stdout
      res = []
      for i in result.split():
          res.append(i)
      res = filter(None, res)
      connect.close()
      http_status = OK
  except:
      print("foo")