export default {
  login: '/api/login', // 登陆
  register: '/api/register', // 注册
  getUserProjects: '/api/user/projects', // 得到全部projects
  createProject: '/api/user/project', // 新建
  editProject: '/api/user/project', // 修改
  deleteProject: '/api/user/project', // 删除 delete
  deploy: uid => {
    return `/api/user/project/${uid}/deploy`
  },
  undeploy: uid => {
    return `/api/user/project/${uid}/undeploy`
  }
}

// auth ---> user
// createProject post ---> project ---> 替换
// editProject patch ---> project
// server post
