apps = [

]

urls = [
    (r"/register", "user.RegisterHandler"),
    (r"/login", "user.LoginHandler"),
    (r"/user/projects", "project.UserProjectsHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})", "project.UserProjectHandler"),
    (r"/user/(?P<uuid>[0-9a-fA-F]{32})/count", "project.ProjectsCountHandler"),
    (r"/user/sensors", "sensor.UserSensorHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})/sensors", "sensor.ProjectSensorHandler"),
    (r"/user/project/(?P<project_uuid>[0-9a-fA-F]{32})/sensor/(?P<sensor_uuid>[0-9a-fA-F]{32})",
     "sensor.SensorHandler"),
    (r"/user/effector/(?P<uuid>[0-9a-fA-F]{32})/function", "function.FunctionEffectorHandler"),
    (r"/user/effectors", "effector.UserEffectorHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})/effectors", "effector.ProjectEffectorHandler"),
    (r"/user/project/(?P<project_uuid>[0-9a-fA-F]{32})/effector/(?P<sensor_uuid>[0-9a-fA-F]{32})",
     "effector.EffectorHandler"),
    (r"/user/project/(?P<project_uuid>[0-9a-fA-F]{32})/sensor/(?P<sensor_uuid>[0-9a-fA-F]{32})/function",
     "function.FunctionSensorHandler"),
    (r"/user/project/(?P<project_uuid>[0-9a-fA-F]{32})/sensor/(?P<sensor_uuid>[0-9a-fA-F]{32})" +
     "/function/(?P<function_uuid>[0-9a-fA-F]{32})",
     "function.SensorFunctionHandler"),
    (r"/user/project/(?P<project_uuid>[0-9a-fA-F]{32})/effector/(?P<effector_uuid>[0-9a-fA-F]{32})/function",
     "function.FunctionEffectorHandler"),
    (r"/user/project/(?P<project_uuid>[0-9a-fA-F]{32})/effector/(?P<effector_uuid>[0-9a-fA-F]{32})" +
     "/function/(?P<function_uuid>[0-9a-fA-F]{32})",
     "function.EffectorFunctionHandler"),
    (r"/user/project/(?P<uuid>[0-9a-fA-F]{32})/deploy", "deploy.DeployHandler"),
]
