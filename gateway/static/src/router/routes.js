import Loading from '@view/Loading'
import Main from '@view/Main'
import TargetMng from '@view/TargetMng'
import PositionMng from '@view/PositionMng'

export default [
  {
    path: '/',
    name: 'main',
    component: Main,
    children: [
      {
        path: '/target/:panel',
        name: 'TargetMng',
        component: TargetMng
      }, {
        path: '/position',
        name: 'PositionMng',
        component: PositionMng
      }
    ]
  }, {
    path: '/loading',
    component: Loading
  }
]
