import Main from '@view/Main'
import TargetMng from '@view/TargetMng'
import PositionMng from '@view/PositionMng'

export default [
  {
    path: '/',
    name: 'main',
    component: Main,
    redirect: '/target/mng',
    children: [
      {
        path: '/target/mng',
        name: 'TargetMng',
        component: TargetMng
      }, {
        path: '/position/mng',
        name: 'PositionMng',
        component: PositionMng
      }
    ]
  }, {
    path: '*',
    redirect: '/target/mng'
  }
]
