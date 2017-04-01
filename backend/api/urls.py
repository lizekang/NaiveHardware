apps = [

]

urls = [
    (r"/register", "user.RegisterHandler"),
    (r"/login", "user.LoginHandler"),
    (r"/user/projects", "project.UserProjectsHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})", "project.UserProjectHandler")
]
