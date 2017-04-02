apps = [

]

urls = [
    (r"/register", "user.RegisterHandler"),
    (r"/login", "user.LoginHandler"),
    (r"/user/projects", "project.UserProjectsHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})", "project.UserProjectHandler"),
    (r"/user/(?P<uuid>[0-9a-fA-F]{32})/count", "project.ProjectsCountHandler"),
    (r"/user/sensor/(?P<uuid>[0-9a-fA-F]{32})/function", "function.FunctionSensorHandler"),

]
