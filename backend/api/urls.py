apps = [

]

urls = [
    (r"/register", "user.RegisterHandler"),
    (r"/login", "user.LoginHandler"),
    (r"/user/projects", "project.UserProjectsHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})", "project.UserProjectHandler"),
    (r"/user/(?P<uuid>[0-9a-fA-F]{32})/count", "project.ProjectsCountHandler"),
    (r"/user/sensor/(?P<uuid>[0-9a-fA-F]{32})/function", "function.FunctionSensorHandler"),
    (r"/user/sensors", "sensor.UserSensorHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})/sensors", "sensor.ProjectSensorHandler"),
    (r"/user/project/(?P<project_uuid>[0-9a-fA-F]{32})/sensor/(?P<sensor_uuid>[0-9a-fA-F]{32})",
     "sensor.SensorHandler"),
    (r"/user/effector/(?P<uuid>[0-9a-fA-F]{32})/function", "function.FunctionEffectorHandler"),
    (r"/user/effectors", "effector.UserEffectorHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})/effectors", "effector.ProjectEffectorHandler"),
    (r"/user/project/(?P<project_uuid>[0-9a-fA-F]{32})/effector/(?P<sensor_uuid>[0-9a-fA-F]{32})",
     "effector.EffectorHandler"),
]
