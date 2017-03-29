apps = [

]

urls = [
    (r"/register", "user.RegisterHandler"),
    (r"/login", "user.LoginHandler"),
    (r"/user/projects", "project.UserProjectsHandler")
]
